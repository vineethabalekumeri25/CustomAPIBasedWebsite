import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# API setup (OpenWeatherMap)
API_KEY = '9de243494c0b295cca9337e1e96b00e2'  # Replace with your OpenWeatherMap API Key
CITY = 'London'  # Replace with the city you want to check
LAT = 51.5085  # Latitude of the city
LON = -0.1257  # Longitude of the city
URL = f'https://c.sat.owm.io/maps/2.0/radar/7/34/46?appid=9de243494c0b295cca9337e1e96b00e2&day=2024-11-30T05:00'  # Corrected URL

# Email setup
SMTP_SERVER = 'smtp.gmail.com'  # For Gmail
SMTP_PORT = 587
FROM_EMAIL = 'vineethab322@gmail.com'  # Your email address
FROM_PASSWORD = 'Neethas2504$'  # Your email password (for Gmail, consider using App Passwords)
TO_EMAIL = 'vineethab322@gmail.com'  # Recipient's email address

def send_email(subject, body):
    """Send an email alert"""
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(FROM_EMAIL, FROM_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()  # Attempt to parse the response as JSON
        except requests.exceptions.JSONDecodeError:
            print("Error: The response is not valid JSON.")
            return None
    else:
        print(f"Error: Unable to fetch data for {city}. Status Code: {response.status_code}")
        return None


def check_weather():
    """Check the weather for rain and send an alert if needed and download radar image."""
    # Fetch weather forecast data
    data = get_forecast_data()
    if not data:
        return

    # Check for rain in the daily forecast (next 7 days)
    for day in data.get('daily', []):
        if 'rain' in day:
            weather_condition = day['weather'][0]['main'].lower()  # 'clear', 'rain', etc.
            icon = day['weather'][0]['icon']  # e.g., '01d', '10d'
            icon_url = f'http://openweathermap.org/img/wn/{icon}@2x.png'  # Image URL

            date = time.strftime('%Y-%m-%d', time.localtime(day['dt']))
            temp = day['temp']['day']
            humidity = day['humidity']
            rain = day.get('rain', 0)  # Default to 0 if no rain data is available
            rain_amount = day['rain']
            print(f"Date: {date}")
            print(f"Temperature: {temp}°C")
            print(f"Humidity: {humidity}%")
            print(f"Rain: {rain}mm")
            print(f"Weather: {weather_condition}")
            print(f"Weather Icon: {icon_url}")
            if rain_amount > 0:  # If rain is expected
                date = time.strftime('%Y-%m-%d', time.localtime(day['dt']))
                subject = f"Rain Alert for {CITY} on {date}"
                body = f"Rain is expected in {CITY} on {date}. The forecasted rainfall is {rain_amount} mm."
                print(f"Weather Icon URL: {icon_url}")  # Display the URL for the weather icon
                send_email(subject, body)
                break  # Send only the first alert for the upcoming rain
        else:
            print(f"No rain expected on {time.strftime('%Y-%m-%d', time.localtime(day['dt']))}")

    # Download and save radar image
    radar_url = f'https://c.sat.owm.io/maps/2.0/radar/7/{LAT}/{LON}?appid={API_KEY}&day={time.strftime("%Y-%m-%dT%H:%M")}'
    radar_response = requests.get(radar_url)

    if radar_response.status_code == 200:
        with open("radar_image.png", "wb") as file:
            file.write(radar_response.content)
        print("Radar image saved as 'radar_image.png'")
    else:
        print(f"Failed to fetch the radar image. Status code: {radar_response.status_code}")



def get_forecast_data():
    """Fetch weather forecast data from OpenWeatherMap API."""
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()  # Return forecast data as JSON
        except requests.exceptions.JSONDecodeError:
            print("Error: The response is not valid JSON.")
            return None
    else:
        print(f"Error: Unable to fetch forecast data. Status Code: {response.status_code}")
        return None


def validate_api_key():
    """Validate the OpenWeatherMap API key by making a simple test request."""
    test_url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    response = requests.get(test_url)
    if response.status_code == 200:
        print("API key is valid!")
    else:
        print(f"Invalid API key or error: {response.status_code}")
        print(response.json())

if __name__ == '__main__':
    validate_api_key()
    while True:
        check_weather()
        time.sleep(86400)  # Wait for 24 hours before checking again
