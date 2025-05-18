import requests

URL = 'https://opentdb.com/api.php'
url_categories = "https://opentdb.com/api_category.php"
def request_questions(num_questions, category, difficulty,q_type):
    params = {
        'amount': num_questions,
        'category': category,
        'difficulty': difficulty,
        'type': q_type,

    }
    response = requests.get(URL,params=params)
    response.raise_for_status()
    data = response.json()
    return data['results']

def get_categories():
    response = requests.get(url_categories)
    data = response.json()
    return data['trivia_categories']