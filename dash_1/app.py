from dash import Dash, html, dcc, callback, Output, Input
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("whether-81e2c-firebase-adminsdk-fbsvc-902ded42d3.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
])

# Free weather API details
API_KEY = "fdf5aa0e4fbac495833ff7e7b793c6f3"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# List of cities for dropdown
CITIES = [
    "Delhi",
    "Mumbai",
    "Kolkata",
    "Chennai",
    "Bengaluru",
    "Hyderabad",
    "Pune",
    "Ahmedabad",
    "Jaipur",
    "Lucknow"
          ]

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Weather Dashboard", className="text-center text-light my-4"),
        dcc.Dropdown(
            CITIES,
            id='city-dropdown',
            placeholder="🌍 Select a city",
            className="mb-3",
        ),
        
        html.Div(id='weather-output', className="weather-output")
    ], className="container p-4 rounded shadow-lg bg-dark")
], className="vh-100 d-flex justify-content-center align-items-center bg-secondary")

# Callback to fetch weather data
@callback(
    Output('weather-output', 'children'),
    Input('city-dropdown', 'value')
)
def update_weather(city):
    if not city:
        return html.Div("Select a city to view weather data.", className="alert alert-info ")

    # Fetch weather data
    response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
    if response.status_code != 200:
        return html.Div(f"Error fetching weather data: {response.status_code}", className="alert alert-danger")

    weather_data = response.json()
    weather_details = {
        "City": weather_data["name"],
        "Temperature (°C)": weather_data["main"]["temp"],
        "Weather": weather_data["weather"][0]["description"].capitalize(),
        "Humidity (%)": weather_data["main"]["humidity"],
        "Wind Speed (m/s)": weather_data["wind"]["speed"]
    }

    # Save to Firebase
    db.collection("weather_data").add(weather_details)

    # Display data in Dash
    return html.Div([
        html.Div([
            html.H2(weather_details['City'], className="card-title text-center text-primary"),
            html.Div([
                html.P(f"🌡️ Temperature: {weather_details['Temperature (°C)']}°C", className="card-text"),
                html.P(f"🌤️ Condition: {weather_details['Weather']}", className="card-text"),
                html.P(f"💧 Humidity: {weather_details['Humidity (%)']}%", className="card-text"),
                html.P(f"🌬️ Wind Speed: {weather_details['Wind Speed (m/s)']} m/s", className="card-text"),
            ], className="text-center")
        ], className="card-body")
    ], className="card border-primary shadow-lg my-3")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
