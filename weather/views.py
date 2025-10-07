import requests
import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

def debug_env(request):
    """Debug route to check environment variables"""
    api_key_env = os.getenv('WEATHER_API_KEY')
    api_key_settings = getattr(settings, 'WEATHER_API_KEY', 'Not found in settings')
    
    debug_info = f"""
    <h1>Environment Debug Info</h1>
    <p><strong>WEATHER_API_KEY from environment:</strong> {api_key_env}</p>
    <p><strong>WEATHER_API_KEY from settings:</strong> {api_key_settings}</p>
    <p><strong>API Key exists:</strong> {bool(api_key_env)}</p>
    <p><strong>API Key length:</strong> {len(api_key_env) if api_key_env else 0}</p>
    <br>
    <a href="/test-api/">Test API Key</a> | 
    <a href="/">Back to Weather App</a>
    """
    return HttpResponse(debug_info)

def test_api_key(request):
    """Test if the API key is valid"""
    api_key = os.getenv('WEATHER_API_KEY')
    
    if not api_key:
        return HttpResponse("❌ ERROR: API key not found in environment variables")
    
    # Test the API key
    test_url = f'http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}'
    
    try:
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            return HttpResponse("✅ SUCCESS: API key is valid and working!")
        elif response.status_code == 401:
            return HttpResponse("❌ ERROR: Invalid API key - please check your OpenWeatherMap API key")
        else:
            error_msg = response.json().get('message', 'Unknown error')
            return HttpResponse(f"❌ ERROR: API returned {response.status_code} - {error_msg}")
    except Exception as e:
        return HttpResponse(f"❌ ERROR: API test failed - {str(e)}")

def weather_view(request):
    city = request.GET.get('city', 'London')
    
    # Get API key from environment
    api_key = os.getenv('WEATHER_API_KEY')
    
    # Check if API key is configured
    if not api_key:
        context = {
            'error': """
            🔧 API Key Configuration Required
            
            The API key is not configured on the server.
            
            Steps to fix:
            1. Go to your Render dashboard
            2. Click on your weather-app service  
            3. Go to "Environment" tab
            4. Add: WEATHER_API_KEY = your_actual_api_key
            5. Click "Save Changes"
            6. Go to "Manual Deploy" → "Clear Cache and Deploy"
            
            Current status: API key not found in environment variables
            """,
            'searched_city': city,
            'weather_data': None
        }
        return render(request, 'weather/weather.html', context)
    
    # Main weather API call
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
        elif response.status_code == 401:
            error = "Invalid API key. The key exists but OpenWeatherMap rejected it. Please check your API key in OpenWeatherMap dashboard."
        elif response.status_code == 404:
            error = f"City '{city}' not found. Please try another city."
        else:
            error_msg = response.json().get('message', 'Unknown error')
            error = f"API Error {response.status_code}: {error_msg}"
            
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