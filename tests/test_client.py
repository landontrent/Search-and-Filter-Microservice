# description: small test program that calls the Search/Filter microservice
#
# Created by: Landon Trent
# Created on: 11/16/2026
import json
import urllib.error
import urllib.request

URL = "http://localhost:5001/search"


def call(body):
    request = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, json.load(error)


FOOD = [
    {"name": "Chicken Quesadillas", "category": "Dinner"},
    {"name": "Vegetable Fried Rice", "category": "Dinner"},
    {"name": "Chocolate Cake", "category": "Dessert"},
]

REVIEWS = [
    {"brand": "Levi's", "height": 168, "build": "Athletic"},
    {"brand": "Zara", "height": 162, "build": "Curvy"},
    {"brand": "Adidas", "height": 165, "build": "Athletic"},
    {"brand": "Nike", "height": 175, "build": "Slim"},
]

DEMOS = [
    ("Story 1: search for 'Chicken'", {"data": FOOD, "search_term": "Chicken"}),
    ("Story 1: search with no match", {"data": FOOD, "search_term": "pizza"}),
    ("Story 2: filter build = Athletic", {"data": REVIEWS, "filters": {"build": "Athletic"}}),
    ("Story 3: sort by height ascending", {"data": REVIEWS, "sort_by": "height", "order": "ascending"}),
    ("Story 3: sort by height descending", {"data": REVIEWS, "sort_by": "height", "order": "descending"}),
    ("Story 3: sort an empty result", {"data": FOOD, "search_term": "pizza", "sort_by": "name"}),
    ("Error: data is not a list", {"data": "oops"}),
]

if __name__ == "__main__":
    for title, body in DEMOS:
        status, out = call(body)
        print(f"--- {title}  (HTTP {status})")
        print(json.dumps(out, indent=2))