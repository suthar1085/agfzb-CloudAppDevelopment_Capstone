import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    try:
        api_key = None
        if 'api_key' in kwargs:
            params = {
                'text': kwargs['text'],
                'version': '2021-03-25',
                'features': 'sentiment',
                'return_analyzed_text': True
            }
            api_key = kwargs['api_key']
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=params, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            print('Response Status Code = ', status_code)
            return None
    except Exception as e:
        print('Error occurred', e)
        return None

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            print('Response Status Code = ', status_code)
            return None
    except Exception as e:
        print('Error occurred', e)
        return None

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_by_id_from_cf(url, dealerId):
    results=[]
    # call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        reviews = json_result["entries"]
        for review in reviews:
            review_obj = DealerReview(dealership=review["dealership"],name=review["name"],purchase=review["purchase"],
            review=review["review"],purchase_date=review["purchase_date"],car_make=review["car_make"],car_model=review["car_model"],
            car_year=review["car_year"], sentiment=analyze_review_sentiments(review["review"]))
            results.append(review_obj)

    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    kwargs = {
        'text': text,
        'api_key': os.getenv('API_KEY')
    }
    url = os.getenv('API_URL')
    result = get_request(url + '/v1/analyze', **kwargs)
    return result['sentiment']['document']['label']



