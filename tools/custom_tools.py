"""
Custom tools for the smolagents Agent.

Rules for a tool:
1. Use the @tool decorator from smolagents.
2. Add type hints to ALL arguments and the return value.
3. Write a clear docstring with an `Args:` section describing each argument.
   smolagents parses this docstring to tell the LLM how to use the tool.

Security note:
- The calculator tool walks a Python AST against an operator whitelist.
  No `eval()` call exists anywhere.
"""

import ast
import datetime
import operator

import pytz
import requests
from smolagents import tool


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.

    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A tool that does nothing yet. Amaze us with your creativity!

    Args:
        arg1: the first argument (a string)
        arg2: the second argument (an integer)
    """
    return f"What magic will you build? You passed arg1={arg1} and arg2={arg2}."


_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _safe_eval_node(node):
    if isinstance(node, ast.Expression):
        return _safe_eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return _BIN_OPS[type(node.op)](
            _safe_eval_node(node.left), _safe_eval_node(node.right)
        )
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_safe_eval_node(node.operand))
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


@tool
def calculator(expression: str) -> str:
    """Evaluates a basic arithmetic expression and returns the result.

    Args:
        expression: A string containing an arithmetic expression,
                    e.g. '2 + 3 * 4' or '(10 / 2) ** 2'.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval_node(tree)
        return f"The result of '{expression}' is: {result}"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


_WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snowfall", 73: "Moderate snowfall", 75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


@tool
def get_weather(city: str) -> str:
    """Fetches the current weather for a city using the free Open-Meteo API.

    Args:
        city: The city name (e.g. 'New York', 'Tokyo', 'Cape Town').
    """
    try:
        geo_resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        geo_resp.raise_for_status()
        geo = geo_resp.json()

        results = geo.get("results") or []
        if not results:
            return f"Could not find a location matching '{city}'."

        place = results[0]
        lat = place["latitude"]
        lon = place["longitude"]
        display_name = (
            f"{place.get('name', city)}, "
            f"{place.get('admin1', '')}, "
            f"{place.get('country', '')}"
        ).strip(", ")

        wx_resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "wind_speed_10m,wind_direction_10m,weather_code"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )
        wx_resp.raise_for_status()
        current = wx_resp.json().get("current", {})

        code = current.get("weather_code")
        condition = _WMO_CODES.get(code, f"Weather code {code}")

        return (
            f"Current weather in {display_name}:\n"
            f"  Condition: {condition}\n"
            f"  Temperature: {current.get('temperature_2m')} °C\n"
            f"  Relative humidity: {current.get('relative_humidity_2m')} %\n"
            f"  Wind: {current.get('wind_speed_10m')} km/h "
            f"from {current.get('wind_direction_10m')}°\n"
            f"  Local time: {current.get('time')}"
        )
    except Exception as e:
        return f"Error fetching weather for '{city}': {e}"