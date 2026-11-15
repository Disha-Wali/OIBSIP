
import tkinter as tk
import requests
from datetime import datetime
from collections import defaultdict, Counter

# COLOUR PALETTE
BG = "#FFF1E6"
CARD = "#FAD2C0"
ACCENT = "#F4A582"
BUTTON = "#C76D50"
TEXT = "#783F2D"
WHITE = "#FFFFFF"

# OPENWEATHER API KEY
API_KEY = "59760948cfe27c70bea82f5c4c8a4dc8"

# TEMPERATURE UNIT
weather_unit = "metric"


# WEATHER ICONS
weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️"
}


# MAIN WINDOW
root = tk.Tk()
root.title("Weather App")
root.geometry("750x780")
root.state("normal")
root.resizable(False, False)
root.configure(bg=BG)
root.resizable(False, False)


# HEADING
title = tk.Label(
    root,
    text="WEATHER APP",
    font=("Arial", 28, "bold"),
    fg=TEXT,
    bg=BG
)
title.pack(pady=(25, 5))


# SUBTITLE
subtitle = tk.Label(
    root,
    text="Discover the weather around you",
    font=("Arial", 12),
    fg=BUTTON,
    bg=BG
)
subtitle.pack()


# DATE AND TIME
datetime_label = tk.Label(
    root,
    text="",
    font=("Arial", 11),
    fg=BUTTON,
    bg=BG
)
datetime_label.pack(pady=5)


def update_datetime():
    current_time = datetime.now().strftime(
        "%A, %d %B %Y | %I:%M:%S %p"
    )

    datetime_label.config(text=current_time)
    root.after(1000, update_datetime)


update_datetime()


# CITY INPUT
city_entry = tk.Entry(
    root,
    font=("Arial", 16),
    width=25,
    justify="center",
    bg=WHITE,
    fg=TEXT,
    relief="flat"
)
city_entry.pack(pady=18, ipady=8)


# SEARCH BAR PLACEHOLDER
placeholder = "Enter city name..."

city_entry.insert(0, placeholder)
city_entry.config(fg="#999999")


def on_entry_click(event):
    if city_entry.get() == placeholder:
        city_entry.delete(0, tk.END)
        city_entry.config(fg=TEXT)


def on_focusout(event):
    if not city_entry.get().strip():
        city_entry.delete(0, tk.END)
        city_entry.insert(0, placeholder)
        city_entry.config(fg="#999999")


city_entry.bind("<FocusIn>", on_entry_click)
city_entry.bind("<FocusOut>", on_focusout)


# CURRENT WEATHER CARD
weather_frame = tk.Frame(
    root,
    bg=CARD,
    padx=20,
    pady=12
)
weather_frame.pack(padx=35, pady=8, fill="x")


# CITY NAME
city_label = tk.Label(
    weather_frame,
    text="Your City",
    font=("Arial", 18, "bold"),
    fg=TEXT,
    bg=CARD
)
city_label.pack()


# WEATHER ICON
icon_label = tk.Label(
    weather_frame,
    text="🌤️",
    font=("Arial", 30),
    bg=CARD
)
icon_label.pack(pady=3)


# TEMPERATURE
temperature_label = tk.Label(
    weather_frame,
    text="-- °C",
    font=("Arial", 38, "bold"),
    fg=BUTTON,
    bg=CARD
)
temperature_label.pack()


# WEATHER CONDITION
condition_label = tk.Label(
    weather_frame,
    text="Weather condition",
    font=("Arial", 13),
    fg=TEXT,
    bg=CARD
)
condition_label.pack(pady=3)


# DETAILS FRAME
details_frame = tk.Frame(
    weather_frame,
    bg=CARD
)
details_frame.pack(pady=10)


# HUMIDITY CARD
humidity_card = tk.Label(
    details_frame,
    text="HUMIDITY\n-- %",
    font=("Arial", 11, "bold"),
    bg=BG,
    fg=TEXT,
    padx=18,
    pady=12
)
humidity_card.pack(side="left", padx=5)


# WIND CARD
wind_card = tk.Label(
    details_frame,
    text="WIND SPEED\n-- m/s",
    font=("Arial", 11, "bold"),
    bg=BG,
    fg=TEXT,
    padx=12,
    pady=12
)
wind_card.pack(side="left", padx=5)


# FEELS LIKE CARD
feels_card = tk.Label(
    details_frame,
    text="FEELS LIKE\n-- °C",
    font=("Arial", 11, "bold"),
    bg=BG,
    fg=TEXT,
    padx=12,
    pady=12
)
feels_card.pack(side="left", padx=5)


# MINIMUM AND MAXIMUM TEMPERATURE
temp_range_label = tk.Label(
    weather_frame,
    text="MIN: -- °C          MAX: -- °C",
    font=("Arial", 12, "bold"),
    fg=TEXT,
    bg=CARD
)
temp_range_label.pack(pady=(2, 8))


# WEATHER SUGGESTION
tip_label = tk.Label(
    weather_frame,
    text="Weather tip will appear here!",
    font=("Arial", 11, "italic"),
    fg=TEXT,
    bg=BG,
    wraplength=350,
    padx=12,
    pady=10
)
tip_label.pack(pady=5)


# FORECAST HEADING
forecast_title = tk.Label(
    root,
    text="5-DAY FORECAST",
    font=("Arial", 17, "bold"),
    fg=TEXT,
    bg=BG
)
forecast_title.pack(pady=(15, 10))


# FORECAST CONTAINER
forecast_frame = tk.Frame(
    root,
    bg=BG
)
forecast_frame.pack(padx=10, pady=5)


# FORECAST STATUS
forecast_status = tk.Label(
    root,
    text="Search a city to see its forecast",
    font=("Arial", 10),
    fg=BUTTON,
    bg=BG
)
forecast_status.pack(pady=8)


# GET WEATHER FUNCTION
def get_weather():

    city = city_entry.get().strip()

    if city == placeholder:
        city = ""

    if not city:
        condition_label.config(
            text="Please enter a city name."
        )
        return

    if API_KEY == "YOUR_OPENWEATHER_API_KEY":
        condition_label.config(
            text="Please add your API key."
        )
        return

    search_button.config(state="disabled")
    condition_label.config(text="Fetching weather...")
    forecast_status.config(text="Loading forecast...")
    root.update_idletasks()

    params = {
        "q": city,
        "appid": API_KEY,
        "units": weather_unit
    }

    try:

        # CURRENT WEATHER API
        current_url = (
            "https://api.openweathermap.org/data/2.5/weather"
        )

        response = requests.get(
            current_url,
            params=params,
            timeout=10
        )

        data = response.json()

        if response.status_code == 401:
            condition_label.config(
                text="Invalid API key. Check your key."
            )
            forecast_status.config(text="")
            return

        if response.status_code == 404:
            condition_label.config(
                text="City not found. Try again!"
            )
            forecast_status.config(text="")
            return

        if response.status_code != 200:
            condition_label.config(
                text="Weather service unavailable."
            )
            forecast_status.config(text="")
            return


        # CURRENT WEATHER DATA
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        feels_like = data["main"]["feels_like"]

        description = data["weather"][0]["description"]
        weather_main = data["weather"][0]["main"]

        min_temp = data["main"]["temp_min"]
        max_temp = data["main"]["temp_max"]

        unit_symbol = (
            "°C" if weather_unit == "metric" else "°F"
        )

        wind_unit = (
            "m/s" if weather_unit == "metric" else "mph"
        )


        # WEATHER-BASED SUGGESTIONS
        if weather_main == "Clear":
            tip = "Perfect day to explore! ☀️"

        elif weather_main == "Clouds":
            tip = "Keep a light jacket handy! ☁️"

        elif weather_main == "Rain":
            tip = "Don't forget your umbrella! ☔"

        elif weather_main == "Drizzle":
            tip = "Take an umbrella just in case! 🌦️"

        elif weather_main == "Thunderstorm":
            tip = "Stay indoors if possible! ⛈️"

        elif weather_main == "Snow":
            tip = "Stay warm and cozy! ❄️"

        else:
            tip = "Check the weather before heading out! 🌤️"

        tip_label.config(text=tip)


        # UPDATE CURRENT WEATHER
        city_label.config(text=city.title())

        icon_label.config(
            text=weather_icons.get(
                weather_main, "🌤️"
            )
        )

        temperature_label.config(
            text=f"{temperature:.1f}{unit_symbol}"
        )

        condition_label.config(
            text=description.title()
        )

        humidity_card.config(
            text=f"HUMIDITY\n{humidity}%"
        )

        wind_card.config(
            text=f"WIND SPEED\n{wind_speed} {wind_unit}"
        )

        feels_card.config(
            text=f"FEELS LIKE\n{feels_like:.1f} {unit_symbol}"
        )

        temp_range_label.config(
            text=(
                f"MIN: {min_temp:.1f} {unit_symbol}     "
                f"MAX: {max_temp:.1f} {unit_symbol}"
            )
        )


        # 5-DAY FORECAST API
        forecast_url = (
            "https://api.openweathermap.org/data/2.5/forecast"
        )

        forecast_response = requests.get(
            forecast_url,
            params=params,
            timeout=10
        )

        forecast_data = forecast_response.json()

        if forecast_response.status_code != 200:
            forecast_status.config(
                text="Forecast unavailable."
            )
            return


        # GROUP FORECAST DATA BY DATE
        daily_data = defaultdict(list)

        for item in forecast_data["list"]:
            date = item["dt_txt"].split(" ")[0]
            daily_data[date].append(item)


        # CLEAR OLD FORECAST CARDS
        for widget in forecast_frame.winfo_children():
            widget.destroy()


        # DISPLAY FIVE DAYS
        dates = sorted(daily_data.keys())[:5]

        for date in dates:

            entries = daily_data[date]

            # CALCULATE AVERAGE TEMPERATURE
            temperatures = [
                item["main"]["temp"]
                for item in entries
            ]

            average_temp = (
                sum(temperatures) / len(temperatures)
            )


            # FIND MOST COMMON WEATHER
            conditions = [
                item["weather"][0]["main"]
                for item in entries
            ]

            common_weather = Counter(
                conditions
            ).most_common(1)[0][0]


            # DAY NAME
            day_name = datetime.strptime(
                date, "%Y-%m-%d"
            ).strftime("%a")


            # WEATHER ICON
            day_icon = weather_icons.get(
                common_weather, "🌤️"
            )


            # CREATE FORECAST CARD
            day_card = tk.Frame(
                forecast_frame,
                bg=CARD,
                padx=5,
                pady=12,
                width=88,
                height=125
            )

            day_card.pack(
                side="left",
                padx=3
            )

            day_card.pack_propagate(False)


            # DAY
            tk.Label(
                day_card,
                text=day_name,
                font=("Arial", 11, "bold"),
                fg=TEXT,
                bg=CARD
            ).pack(pady=5)


            # ICON
            tk.Label(
                day_card,
                text=day_icon,
                font=("Arial", 21),
                bg=CARD
            ).pack(pady=3)


            # TEMPERATURE
            tk.Label(
                day_card,
                text=f"{average_temp:.0f}{unit_symbol}",
                font=("Arial", 12, "bold"),
                fg=BUTTON,
                bg=CARD
            ).pack(pady=5)

        forecast_status.config(
            text="Forecast updated successfully!"
        )


    except requests.exceptions.RequestException:
        condition_label.config(
            text="Network error. Check your internet."
        )

        forecast_status.config(
            text="Could not load forecast."
        )

    except (KeyError, IndexError, TypeError, ValueError):
        condition_label.config(
            text="Unexpected weather data. Try again."
        )

        forecast_status.config(
            text="Could not process weather data."
        )

    finally:
        search_button.config(state="normal")


# TEMPERATURE UNIT SWITCH
def toggle_unit():

    global weather_unit

    if weather_unit == "metric":
        weather_unit = "imperial"
    else:
        weather_unit = "metric"

    if city_entry.get().strip() not in ("", placeholder):
        get_weather()


# TEMPERATURE UNIT BUTTON

update_datetime()

# SEARCH BUTTON
search_button = tk.Button(
    root,
    text="GET WEATHER",
    font=("Arial", 14, "bold"),
    bg=BUTTON,
    fg=WHITE,
    activebackground="#A95139",
    activeforeground=WHITE,
    padx=25,
    pady=10,
    relief="flat",
    cursor="hand2",
    command=get_weather
)
search_button.pack(pady=12)


# ENTER KEY SUPPORT
city_entry.bind(
    "<Return>",
    lambda event: get_weather()
)


# RUN APPLICATION
root.mainloop()
