import requests

def weather(city):
    if city.isalpha():
        url = f"https://wttr.in/{city}?format=j1"
    
        # Наш собственный статический словарь. Тексты ниже никогда не изменятся, 
        # так как они прописаны прямо в вашем коде.
        WEATHER_STATUSES = {
            # Ясно и облачно
            "113": "Clear/Sunny",
            "116": "Partly cloudy",
            "119": "Cloudy",
            "122": "Overcast",
            # Видимость
            "143": "Mist",
            "248": "Fog",
            "260": "Freezing fog",
            # Осадки / Дожди
            "176": "Patchy rain possible",
            "263": "Patchy light drizzle",
            "266": "Light drizzle",
            "281": "Freezing drizzle",
            "284": "Heavy freezing drizzle",
            "293": "Patchy light rain",
            "296": "Light rain",
            "299": "Moderate rain at times",
            "302": "Moderate rain",
            "305": "Heavy rain at times",
            "308": "Heavy rain",
            "311": "Light freezing rain",
            "314": "Moderate or heavy freezing rain",
            # Ливни
            "353": "Light rain shower",
            "356": "Moderate or heavy rain shower",
            "359": "Torrential rain shower",
            # Зима / Снег
            "179": "Patchy snow possible",
            "182": "Patchy sleet possible",
            "185": "Patchy freezing drizzle possible",
            "227": "Blowing snow",
            "230": "Blizzard",
            "317": "Light sleet",
            "320": "Moderate or heavy sleet",
            "323": "Patchy light snow",
            "326": "Light snow",
            "329": "Patchy moderate snow",
            "332": "Moderate snow",
            "335": "Patchy heavy snow",
            "338": "Heavy snow",
            "350": "Ice pellets",
            "362": "Light sleet showers",
            "365": "Moderate or heavy sleet showers",
            "368": "Light snow showers",
            "371": "Moderate or heavy snow showers",
            "374": "Light showers of ice pellets",
            "377": "Moderate or heavy showers of ice pellets",
            # Грозы
            "200": "Thundery outbreaks possible",
            "386": "Light rain with thunderstorm",
            "389": "Heavy rain with thunderstorm",
            "392": "Light snow with thunderstorm",
            "395": "Heavy snow with thunderstorm"
        }

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                # 1. Берем код погоды (он всегда возвращается в виде строки из 3 цифр)
                code = current['weatherCode']
                temp = current['temp_C']
                humidity = current['humidity']
                
                # 2. Ищем код в нашем статическом словаре. 
                # Если API вернет неизвестный код, вернется дефолтное "Unknown"
                static_desc = WEATHER_STATUSES.get(code, "Unknown weather condition")
                
                return static_desc
        except Exception as e:
            return {"error": f"Failed to get data: {e}"}
    else:
        return {"error": "Invalid city name. Please enter a valid city."}
