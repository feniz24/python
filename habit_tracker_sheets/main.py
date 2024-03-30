import requests
import datetime

APP_ID = "acae61cf"
API_KEY = "8186571f5008ae367ccfd1c0c1cfc971"
ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
BEARER_TOKEN = "Bearer eowajfaeiowj092340129u30123"
SHETTY_API = "https://api.sheety.co/1c0dbdefd0d8a9f44f84738a9ac8fb27/workoutTracking/workouts"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

shetty_header = {
    "Authorization": BEARER_TOKEN,
}

parameters = {
    "query": input("Tell me which exercises you did.")
}

response = requests.post(url=ENDPOINT, json=parameters, headers=headers)
data = response.json()
exercises = data["exercises"]

today = datetime.datetime.today()
date = today.strftime("%d-%m-%Y")
time = today.strftime("%X")
for exercise in exercises:
    workout_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    response = requests.post(url=SHETTY_API, json=workout_params, headers=shetty_header)
