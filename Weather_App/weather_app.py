
import requests

API_KEY = "59760948cfe27c70bea82f5c4c8a4dc8"

url = "https://api.openweathermap.org/data/2.5/weather"

# Start the loop
while True:

    # Ask for city
    city = input("\nEnter city name (or Q to quit): ").strip()

    # Exit condition
    if city.lower() == "q":
        print("Thank you for using Weather App!")
        break

    # Empty input validation
    if not city:
        print("Error: City name cannot be empty!")
        continue

    # API parameters
    params = {
        "appid": API_KEY,
        "units": "metric"
    }

    if city.isdigit():
        params["zip"] = f"{city},IN"
    else:
        params["q"] = city

    # Send API request
    try:
        response = requests.get(
            url, params=params, timeout=10
        )

    except requests.exceptions.Timeout:
        print("Error: Request timed out!")
        continue

    except requests.exceptions.ConnectionError:
        print("Error: Check your internet connection!")
        continue

    except requests.exceptions.RequestException:
        print("Error: Something went wrong!")
        continue

    # Check API response
    if response.status_code == 404:
        print("Error: City not found!")
        continue

    elif response.status_code == 401:
        print("Error: Invalid API key!")
        print("API Response:", response.text)
        continue

    elif response.status_code != 200:
        print("Error: Something went wrong!")
        continue

    # Convert response into JSON
    data = response.json()

    # Extract weather information
    temperature = data["main"]["temp"]
    fahrenheit = (temperature * 9/5) + 32
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    # Display weather report
    print("\n===== WEATHER REPORT =====")
    print("City:", data["name"])
    print("Temperature:", temperature, "°C")
    print("Temperature:", round(fahrenheit, 2), "°F")
    print("Humidity:", humidity, "%")
    print("Weather:", description)
    print("Wind Speed:", wind_speed, "m/s")
    print("==========================")
