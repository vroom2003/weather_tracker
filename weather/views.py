import requests
from django.shortcuts import render
from django.conf import settings

def weather_view(request):
    city = request.GET.get('city', 'London')
    
    # Get API key from settings
    api_key = getattr(settings, 'WEATHER_API_KEY', None)
    
    # Check if API key is configured
    if not api_key:
        context = {
            'error': "API key not configured. Please set WEATHER_API_KEY in environment variables.",
            'searched_city': city,
            'weather_data': None
        }
        return render(request, 'weather/weather.html', context)
    
    # Build API URL
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    weather_data = None
    error = None
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data.get('name', 'Unknown'),
                'country': data.get('sys', {}).get('country', ''),
                'temperature': data.get('main', {}).get('temp', 0),
                'description': data.get('weather', [{}])[0].get('description', ''),
                'icon': data.get('weather', [{}])[0].get('icon', ''),
                'humidity': data.get('main', {}).get('humidity', 0),
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'feels_like': data.get('main', {}).get('feels_like', 0),
                'pressure': data.get('main', {}).get('pressure', 0),
            }
        else:
            error = f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}"
            
    except requests.exceptions.RequestException as e:
        error = f"Network error: {str(e)}"
    except Exception as e:
        error = f"Unexpected error: {str(e)}"
    
    context = {
        'weather_data': weather_data,
        'error': error,
        'searched_city': city
    }
    
    return render(request, 'weather/weather.html', context)