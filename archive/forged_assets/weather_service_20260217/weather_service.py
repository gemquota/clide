# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "None",
#   "mcp[cli]",
# ]
# ///
import asyncio
from mcp.server.fastmcp import FastMCP
import json
import urllib.request
import urllib.parse

# Initialize FastMCP server synthesized by CLIDE
mcp = FastMCP("weather_service")

@mcp.tool()

def weather_service(args: str) -> str:
    """
    Fetches weather data for a given city.

    Args:
        args: City name (str).

    Returns:
        A string containing weather information or an error message.
    """
    try:
        city = args.strip()
        if not city:
            return "Error: City name cannot be empty."

        base_url = "http://api.openweathermap.org/data/2.5/weather"
        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        url = f"{base_url}?q={urllib.parse.quote(city)}&appid={api_key}&units=metric"

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        if data["cod"] != 200:
            return f"Error: {data['message']}"

        weather_desc = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        result = (
            f"Weather in {city}:\n"
            f"Description: {weather_desc}\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
        return result

    except urllib.error.URLError as e:
        return f"Error: Network issue - {e}"
    except Exception as e:
        return f"Error: An unexpected error occurred - {e}"

if __name__ == "__main__":
    mcp.run()
