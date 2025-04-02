import flet as ft
import requests
from api_key import API_KEY

# API TO GET A RESPONSE 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
MAP_URL = "https://api.openstreetmap.org/api/0.6/map?bbox=-0.489,-0.123,0.236,51.569'"

def get_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:  # Check for a successful response
        data = response.json()  # Parse the JSON response
        return {
            "City": data["name"],
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Pressure": data["main"]["pressure"],
            "Weather": data["weather"][0]["description"],
            "Wind Speed": data["wind"]["speed"],
            "Visibility": data.get("visibility", "N/A"),  # Handle missing fields
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
            "timezone": data.get("timezone", "N/A")  # Handle missing fields
        }
    return None

def main(page: ft.Page):
    page.title = "Weather App"
    page.bgcolor = "#e0f7fa"  # Light teal background
    page.padding = 20
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 540
    page.window_height = 4

    # Define UI components
    city_input = ft.TextField(
        label="Enter city name",
        autofocus=True,
        width=300,
        bgcolor="#ffffff",  # White background for input
        border_radius=10,
        border_color="#00796b",  # Teal border
        color="#00796b"  # Teal text
    )
    result_text = ft.Text(
        size=16,
        color="#004d40",  # Dark teal text
        weight=ft.FontWeight.BOLD
    )
    # Initialize map_image with a placeholder image
    map_image = ft.Image(
        src="https://via.placeholder.com/600x400?text=Map+Not+Available",  # Placeholder image
        width=600,
        height=400,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10
    )

    def search_weather(e):
        city = city_input.value.strip()
        if not city:
            result_text.value = "Please enter a city name."
            map_image.src = "https://via.placeholder.com/600x400?text=Map+Not+Available"  # Reset to placeholder
        else:
            weather_data = get_weather_data(city)
            if weather_data:
                result_text.value = (
                    f"City: {weather_data['City']}\n"
                    f"Temperature: {weather_data['Temperature']}°C\n"
                    f"Humidity: {weather_data['Humidity']}%\n"
                    f"Pressure: {weather_data['Pressure']} hPa\n"
                    f"Weather: {weather_data['Weather']}\n"
                    f"Wind Speed: {weather_data['Wind Speed']} m/s\n"
                    f"Visibility: {weather_data['Visibility']} m\n"
                )
                # Generate a static map URL using MAP_URL
                lat, lon = weather_data["lat"], weather_data["lon"]
                map_image.src = MAP_URL.format(lat=lat, lon=lon)
            else:
                result_text.value = "Could not retrieve weather data. Please try again."
                map_image.src = "https://via.placeholder.com/600x400?text=Map+Not+Available"  # Reset to placeholder
        page.update()  # Ensure the page is updated after setting the result_text value

    # Define the search button
    search_button = ft.IconButton(
        icon=ft.icons.SEARCH,
        icon_color="#004d40",  # Dark teal icon
        bgcolor="#ffffff",  # White background
        tooltip="Search",
        on_click=search_weather  # Attach the event handler
    )

    # Add components to the page
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Weather App",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="#004d40",  # Dark teal text
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Row([city_input, search_button], alignment=ft.MainAxisAlignment.CENTER),
                    result_text,
                    map_image
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="#ffffff",  # White container background
            padding=20,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=15,
                color="#b2dfdb"  # Light teal shadow
            ),
            width=700
        )
    )

if __name__ == "__main__":
    ft.app(target=main)  # Run the app in a desktop window
