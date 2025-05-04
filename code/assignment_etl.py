import streamlit as st
import pandas as pd
import requests
import json 
if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from apicalls import get_google_place_details, get_azure_sentiment, get_azure_named_entity_recognition
else:
    from code.apicalls import get_google_place_details, get_azure_sentiment, get_azure_named_entity_recognition

PLACE_IDS_SOURCE_FILE = "cache/place_ids.csv"
CACHE_REVIEWS_FILE = "cache/reviews.csv"
CACHE_SENTIMENT_FILE = "cache/reviews_sentiment_by_sentence.csv"
CACHE_ENTITIES_FILE = "cache/reviews_sentiment_by_sentence_with_entities.csv"


def reviews_step(place_ids: str | pd.DataFrame) -> pd.DataFrame:
    '''
      1. place_ids --> reviews_step --> reviews: place_id, name (of place), author_name, rating, text 
    '''
    # TODO: implement this function
    if isinstance(place_ids, str):
        place_ids = pd.read_csv(place_ids)
    
    reviews_list = []
    for _, row in place_ids.iterrows():
        place_id = row['place_id']
        response = requests.get(f"https://cent.ischool-iot.net/api/google/place", 
                                headers={'X-API-KEY': APIKEY}, 
                                params={'place_id': place_id})
        response.raise_for_status()
        details = response.json()
        for review in details.get('reviews', []):
            reviews_list.append({
                'place_id': place_id,
                'name': details.get('name'),
                'author_name': review.get('author_name'),
                'rating': review.get('rating'),
                'text': review.get('text')
            })
    
    return pd.DataFrame(reviews_list)

def sentiment_step(reviews: str | pd.DataFrame) -> pd.DataFrame:
    '''
      2. reviews --> sentiment_step --> review_sentiment_by_sentence
    '''
    # TODO: implement this function
    if isinstance(reviews, str):
        reviews = pd.read_csv(reviews)
    
    sentiment_data = []
    for _, row in reviews.iterrows():
        payload = json.dumps({'text': row['text']})
        response = requests.post("https://cent.ischool-iot.net/api/azure/sentiment",
                                 headers={'X-API-KEY': APIKEY, 'Content-Type': 'application/json'},
                                 data=payload)
        response.raise_for_status()
        sentiment = response.json()
        for sentence in sentiment.get('sentences', []):
            sentiment_data.append({
                'place_id': row['place_id'],
                'name': row['name'],
                'author_name': row['author_name'],
                'rating': row['rating'],
                'sentence_text': sentence.get('text'),
                'sentence_sentiment': sentence.get('sentiment'),
                'confidenceScores.positive': sentence['confidenceScores']['positive'],
                'confidenceScores.neutral': sentence['confidenceScores']['neutral'],
                'confidenceScores.negative': sentence['confidenceScores']['negative']
            })
    
    return pd.DataFrame(sentiment_data)

def entity_extraction_step(sentiment: str | pd.DataFrame) -> pd.DataFrame:
    '''
      3. review_sentiment_by_sentence --> entity_extraction_step --> review_sentiment_entities_by_sentence
    '''
    # TODO: implement this function
    if isinstance(sentiment, str):
        sentiment = pd.read_csv(sentiment)
    
    entity_data = []
    for _, row in sentiment.iterrows():
        payload = json.dumps({'text': row['sentence_text']})
        response = requests.post("https://cent.ischool-iot.net/api/azure/entities",
                                 headers={'X-API-KEY': APIKEY, 'Content-Type': 'application/json'},
                                 data=payload)
        response.raise_for_status()
        entities_result = response.json()
        for entity in entities_result.get('entities', []):
            entity_data.append({
                'place_id': row['place_id'],
                'name': row['name'],
                'author_name': row['author_name'],
                'rating': row['rating'],
                'sentence_text': row['sentence_text'],
                'sentence_sentiment': row['sentence_sentiment'],
                'confidenceScores.positive': row['confidenceScores.positive'],
                'confidenceScores.neutral': row['confidenceScores.neutral'],
                'confidenceScores.negative': row['confidenceScores.negative'],
                'entity_text': entity.get('text'),
                'entity_category': entity.get('category'),
                'entity_subcategory': entity.get('subcategory'),
                'confidenceScores.entity': entity.get('confidenceScore')
            })
    
    return pd.DataFrame(entity_data)


if __name__ == '__main__':
    # helpful for debugging as you can view your dataframes and json outputs
    import streamlit as st 
    st.write("What do you want to debug?")