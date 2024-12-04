const API_KEY = 'aa9f26af8c69d71c794f056347a5fc44'; // Get an API key from https://openweathermap.org/
const API_URL = 'https://api.openweathermap.org/data/2.5';

document.getElementById('locationForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const location = document.getElementById('locationInput').value;
    if (!location) return;

    // Fetch current weather
    const currentWeather = await fetch(`${API_URL}/weather?q=${location}&units=metric&appid=${API_KEY}`)
        .then(response => response.json())
        .catch(err => console.error(err));

    if (currentWeather.cod === 200) {
        displayCurrentWeather(currentWeather);

        // Fetch 5-day forecast
        const forecast = await fetch(`${API_URL}/forecast?q=${location}&units=metric&appid=${API_KEY}`)
            .then(response => response.json())
            .catch(err => console.error(err));

        displayForecast(forecast);
    } else {
        alert('City not found!');
    }
});

function displayCurrentWeather(data) {
    const iconUrl = `http://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;

    document.getElementById('cityName').textContent = data.name;
    const weatherIcon = document.createElement('img');
    weatherIcon.src = iconUrl;
    weatherIcon.alt = data.weather[0].description;
    weatherIcon.classList.add('weatherIcon');

    // Append or replace icon
    const weatherDetails = document.getElementById('weatherDetails');
    const existingIcon = document.querySelector('#weatherDetails img');
    if (existingIcon) {
        weatherDetails.replaceChild(weatherIcon, existingIcon);
    } else {
        weatherDetails.appendChild(weatherIcon);
    }
    document.getElementById('temperature').textContent = `Temperature: ${data.main.temp}°C`;
    document.getElementById('humidity').textContent = `Humidity: ${data.main.humidity}%`;
    document.getElementById('rain').textContent = `Rain: ${data.rain ? data.rain['1h'] || 0 : 0}mm`;
    document.getElementById('weatherCondition').textContent = `Condition: ${data.weather[0].description}`;
}

function displayForecast(data) {
    const forecastContainer = document.getElementById('forecastContainer');
    forecastContainer.innerHTML = '';

    // Extract forecast for the next 5 days (3-hour interval data)
    const dailyData = data.list.filter(item => item.dt_txt.includes('12:00:00'));
    dailyData.forEach(day => {
        const iconUrl = `http://openweathermap.org/img/wn/${day.weather[0].icon}@2x.png`;

        const forecastItem = document.createElement('div');
        forecastItem.classList.add('forecastItem');
        forecastItem.innerHTML = `
            <p>${new Date(day.dt * 1000).toLocaleDateString()}</p>
            <img src="${iconUrl}" alt="${day.weather[0].description}" class="weatherIcon" />
            <p>${day.main.temp}°C</p>
            <p>${day.weather[0].description}</p>
        `;
        forecastContainer.appendChild(forecastItem);
    });
}