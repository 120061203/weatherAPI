
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# 掛載 static 目錄（假設你從 backend/ 執行）
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

CITY_MAP = {
    "台北": "Taipei,TW", "臺北": "Taipei,TW",
    "台中": "Taichung,TW", "臺中": "Taichung,TW",
    "高雄": "Kaohsiung,TW", "台南": "Tainan,TW",
    "桃園": "Taoyuan District,TW", "新北": "New Taipei,TW",
    "東京": "Tokyo,JP", "紐約": "New York,US"
}

@app.get("/weather")
def get_weather(city: str = "Taipei"):
    if not API_KEY:
        return {"錯誤": "API 金鑰未設定"}
    city_query = CITY_MAP.get(city, city)
    params = {
        "q": city_query,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_tw"
    }
    res = requests.get(BASE_URL, params=params)
    if res.status_code == 200:
        data = res.json()
        return {
            "城市": data["name"],
            "天氣": data["weather"][0]["description"],
            "氣溫": data["main"]["temp"],
            "體感溫度": data["main"]["feels_like"],
            "濕度": data["main"]["humidity"]
        }
    return {"錯誤": "無法取得天氣資訊", "API 回傳": res.text}

@app.get("/weather/geo")
def get_weather_by_geo(lat: float, lon: float):
    if not API_KEY:
        return {"錯誤": "API 金鑰未設定"}
    params = {
        "lat": lat, "lon": lon,
        "appid": API_KEY, "units": "metric", "lang": "zh_tw"
    }
    res = requests.get(BASE_URL, params=params)
    if res.status_code == 200:
        data = res.json()
        return {
            "城市": data["name"],
            "天氣": data["weather"][0]["description"],
            "氣溫": data["main"]["temp"],
            "體感溫度": data["main"]["feels_like"],
            "濕度": data["main"]["humidity"]
        }
    return {"錯誤": "無法取得天氣資訊", "API 回傳": res.text}

@app.get("/weather/forecast")
def get_forecast(lat: float, lon: float):
    if not API_KEY:
        return {"錯誤": "API 金鑰未設定"}
    url = "https://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat": lat, "lon": lon,
        "exclude": "current,minutely,hourly,alerts",
        "appid": API_KEY,
        "units": "metric", "lang": "zh_tw"
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        return {"錯誤": f"無法取得預報資料：{res.text}"}
    data = res.json()
    daily_data = []
    for day in data.get("daily", [])[:7]:
        daily_data.append({
            "date": datetime.fromtimestamp(day["dt"]).strftime("%m/%d"),
            "temp": day["temp"]["day"],
            "feels_like": day["feels_like"]["day"]
        })
    return {"forecast": daily_data}

@app.get("/weather/air")
def get_air_quality(lat: float, lon: float):
    if not API_KEY:
        return {"錯誤": "API 金鑰未設定"}
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = { "lat": lat, "lon": lon, "appid": API_KEY }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        return {"錯誤": f"無法取得空氣品質資料：{res.text}"}
    data = res.json()
    comp = data["list"][0]["components"]
    return {
        "aqi": data["list"][0]["main"]["aqi"],
        "pm2_5": comp["pm2_5"],
        "pm10": comp["pm10"],
        "o3": comp["o3"],
        "no2": comp["no2"]
    }
