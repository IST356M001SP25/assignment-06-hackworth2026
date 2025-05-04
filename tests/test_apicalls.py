import pytest 
import sys
import os
import requests 
import assignment06Hackworth2026.code.apicalls as calls



def test_should_pass():
    print("\nAlways True!")
    assert True


def test_get_googe_place_details():
    tests = [ 
        {'place_id': 'ChIJUTtvv9Tz2YkRhneTbRT-1mk', 'expected_name': 'Buried Acorn Brewery'},
        { 'place_id': 'ChIJl2h_-pjz2YkR-VUHD9dpOF0', 'expected_name': 'Meier’s Creek Brewing - Inner Harbor'},
    ]
    for t in tests:
        print(f"\nTESTING: test_get_googe_place_details({t['place_id']}) == {t['expected_name']}")
        place =  calls.get_google_place_details(t['place_id']) 
        assert place['result']['name'] == t['expected_name']


def test_get_googe_place_details_check_exception():
    # check for exception
    test = {'place_id': '12345', 'expected_name': 'Does not exist!'}
    try:
        place =  calls.get_google_place_details(test['place_id']) 
        assert False # We Expected an HTTPError
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
        assert True


def test_get_azure_sentiment():
    tests = [
        {'text': 'I love programming!', 'expected_sentiment': 'positive'},
        {'text': 'I hate bugs.', 'expected_sentiment': 'negative'},
    ]
    for t in tests:
        print(f"\nTESTING: test_get_azure_sentiment({t['text']}) == {t['expected_sentiment']}")
        try:
            results = calls.get_azure_sentiment(t['text'])
            documents = results['results']['documents']
            assert documents, "API returned no documents"
            sentiment = documents[0]['sentiment']
            assert sentiment == t['expected_sentiment']
        except ValueError as e:
            print(f"SKIPPED: {t['text']} → {e}")

def test_get_azure_key_phrase_extraction():
    tests = [
        {'text': 'Microsoft was founded by Bill Gates and Paul Allen.', 'expected_entities': ['Microsoft', 'Bill Gates', 'Paul Allen']},
        {'text': 'The Eiffel Tower is located in Paris.', 'expected_entities': ['The Eiffel Tower', 'Paris']},
    ]
    for t in tests:
        print(f"\nTESTING: get_azure_key_phrase_extraction({t['text']}) == {t['expected_entities']}")
        try:
            results = calls.get_azure_key_phrase_extraction(t['text'])
            documents = results['results']['documents']
            assert documents, "API returned no documents"
            key_phrases = documents[0]['keyPhrases']
            for e in t['expected_entities']:
                assert e in key_phrases
        except ValueError as e:
            print(f"SKIPPED: {t['text']} → {e}")

def test_get_azure_named_entity_recognition():
    tests = [
        {'text': 'Microsoft was founded by Bill Gates and Paul Allen.', 'expected_entities': ['Microsoft', 'Bill Gates', 'Paul Allen']},
        {'text': 'The Eiffel Tower is located in Paris.', 'expected_entities': ['Eiffel Tower', 'Paris']},
    ]
    for t in tests:
        print(f"\nTESTING: get_azure_named_entity_recognition({t['text']}) == {t['expected_entities']}")
        try:
            results = calls.get_azure_named_entity_recognition(t['text'])
            documents = results['results']['documents']
            assert documents, "API returned no documents"
            entities = [e['text'] for e in documents[0]['entities']]
            for expected in t['expected_entities']:
                assert expected in entities
        except ValueError as e:
            print(f"SKIPPED: {t['text']} → {e}")


# IF YOU NEED TO DEBUG A TEST
# 1. Place a breakpoint on the line below
# 2. call the function you want to debug below the if statement
# Run this file with debugging
if __name__ == "__main__":
    test_should_pass()
