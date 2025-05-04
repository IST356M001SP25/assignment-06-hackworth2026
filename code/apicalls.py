import requests

APIKEY = "75810a48248cee2b50a513c0"

def get_google_place_details(google_place_id: str) -> dict:
    header = {'X-API-KEY': APIKEY}
    params = {'place_id': google_place_id}
    url = "https://cent.ischool-iot.net/api/google/places/details"
    response = requests.get(url, headers=header, params=params)
    response.raise_for_status()
    data = response.json()
    
    if 'result' not in data or 'name' not in data['result']:
        raise ValueError("Missing 'result' or 'name' in Google Place Details response.")
    
    return data

def get_azure_sentiment(text: str) -> dict:
    header = {'X-API-KEY': APIKEY}
    payload = {'text': text}
    url = "https://cent.ischool-iot.net/api/azure/sentiment"
    response = requests.post(url, headers=header, json=payload)
    response.raise_for_status()
    data = response.json()
    
    if not data.get('results', {}).get('documents'):
        raise ValueError("No documents returned in Azure Sentiment response.")
    
    return data

def get_azure_key_phrase_extraction(text: str) -> dict:
    header = {'X-API-KEY': APIKEY}
    payload = {'text': text}
    url = "https://cent.ischool-iot.net/api/azure/keyphrasextraction"
    response = requests.post(url, headers=header, json=payload)
    response.raise_for_status()
    data = response.json()
    
    if not data.get('results', {}).get('documents'):
        raise ValueError("No documents returned in Azure Key Phrase Extraction response.")
    
    return data

def get_azure_named_entity_recognition(text: str) -> dict:
    header = {'X-API-KEY': APIKEY}
    payload = {'text': text}
    url = "https://cent.ischool-iot.net/api/azure/entityrecognition"
    response = requests.post(url, headers=header, json=payload)
    response.raise_for_status()
    data = response.json()
    
    if not data.get('results', {}).get('documents'):
        raise ValueError("No documents returned in Azure Named Entity Recognition response.")
    
    return data

def geocode(place: str) -> dict:
    header = {'X-API-KEY': APIKEY}
    params = {'location': place}
    url = "https://cent.ischool-iot.net/api/google/geocode"
    response = requests.get(url, headers=header, params=params)
    response.raise_for_status()
    data = response.json()
    
    if 'results' not in data or not data['results']:
        raise ValueError("No geocode results returned.")
    
    return data

def get_weather(lat: float, lon: float) -> dict:
    header = {'X-API-KEY': APIKEY}
    params = {'lat': lat, 'lon': lon, 'units': 'imperial'}
    url = "https://cent.ischool-iot.net/api/weather/current"
    response = requests.get(url, headers=header, params=params)
    response.raise_for_status()
    data = response.json()
    
    if 'weather' not in data:
        raise ValueError("No weather data returned.")
    
    return data
