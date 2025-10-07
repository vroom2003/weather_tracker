import requests
from django.shortcuts import render
from django.conf import settings

def weather_view(request):
    city = request.GET.get('city', 'London')  # Default to London
    
    # Get API key from settings (which comes from .env)
    api_key = settings.WEATHER_API_KEY
    
    # Check if API key is configured
    if not api_key or api_key == '70f7010d4422e80d4b71752c8ae8ded5a':
        return render(request, 'weather/weather.html', context)
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    weather_data = None
    error = None
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'feels_like': data['main']['feels_like'],
                'pressure': data['main']['pressure'],
            }
        elif response.status_code == 401:
            error = "Invalid API key. Please check your OpenWeatherMap API key in the .env file."
        elif response.status_code == 404:
            error = f"City '{city}' not found. Please try another city."
        else:
            error = f"Error fetching weather data. API returned status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        error = "Network error. Please check your internet connection."
    except requests.exceptions.Timeout:
        error = "Request timeout. Please try again."
    except Exception as e:
        error = f"Unexpected error: {str(e)}"
    
    context = {
        'weather_data': weather_data,
        'error': error,
        'searched_city': city
    }
    
    return render(request, 'weather/weather.html', context)