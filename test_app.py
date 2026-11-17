# description: tests for the Search/Filter microservice acceptance criteria
#
# Run with python -m unittest -v
#
# Created by: Landon Trent
# Created on: 11/16/2026

import time
import unittest

from app import app

FOOD = [
    {"name": "Chicken Quesadillas", "category": "Dinner"},
    {"name": "Vegetable Fried Rice", "category": "Dinner"},
    {"name": "Chocolate Cake", "category": "Dessert"},
]

BUILDS = ["Athletic", "Slim", "Curvy", "Average"]


def twenty_records():
    """20 records. Ids 0, 4, 8, 12, and 16 are the Athletic ones."""
    return [{"id": i, "name": f"Item {i}", "build": BUILDS[i % 4], "height": 150 + i}
            for i in range(20)]


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def call(self, **body):
        response = self.client.post("/search", json=body)
        return response.status_code, response.get_json()


class SearchData(ServiceTestCase):
    """Story 1: Search Data"""

    def test_returns_items_matching_the_search_term(self):
        code, out = self.call(data=FOOD, search_term="Chicken")
        self.assertEqual(code, 200)
        self.assertEqual([r["name"] for r in out["results"]], ["Chicken Quesadillas"])
        self.assertEqual(out["total"], 1)

    def test_no_match_returns_an_empty_result(self):
        code, out = self.call(data=FOOD, search_term="pizza")
        self.assertEqual(code, 200)
        self.assertEqual(out["results"], [])
        self.assertEqual(out["total"], 0)

    def test_search_ignores_case(self):
        _, out = self.call(data=FOOD, search_term="chocolate")
        self.assertEqual(out["total"], 1)

    def test_search_and_filter_together(self):
        _, out = self.call(data=FOOD, search_term="Chicken", filters={"category": "Dinner"})
        self.assertEqual(out["total"], 1)
        _, out = self.call(data=FOOD, search_term="Chicken", filters={"category": "Dessert"})
        self.assertEqual(out["total"], 0)

    def test_performance_1000_items_within_2_seconds(self):
        data = [{"name": f"Item {i}", "category": "A" if i % 2 else "B"} for i in range(1000)]
        start = time.perf_counter()
        code, out = self.call(data=data, search_term="Item 99")
        self.assertLess(time.perf_counter() - start, 2.0)
        self.assertEqual(code, 200)
        self.assertEqual(out["total"], 11)  # Item 99 and Items 990 to 999


class FilterByCategory(ServiceTestCase):
    """Story 2: Filter by category"""

    def test_only_athletic_records_are_returned(self):
        code, out = self.call(data=twenty_records(), filters={"build": "Athletic"})
        self.assertEqual(code, 200)
        self.assertEqual([r["id"] for r in out["results"]], [0, 4, 8, 12, 16])

    def test_filter_without_a_search_term(self):
        _, out = self.call(data=FOOD, filters={"category": "Dessert"})
        self.assertEqual(out["total"], 1)

    def test_filter_with_no_matches_returns_empty(self):
        _, out = self.call(data=FOOD, filters={"category": "Breakfast"})
        self.assertEqual(out["results"], [])


class SortResults(ServiceTestCase):
    """Story 3: Sort Search Results"""

    def test_ascending(self):
        _, out = self.call(data=twenty_records(), sort_by="height", order="ascending")
        heights = [r["height"] for r in out["results"]]
        self.assertEqual(heights, sorted(heights))

    def test_descending(self):
        _, out = self.call(data=twenty_records(), sort_by="height", order="descending")
        heights = [r["height"] for r in out["results"]]
        self.assertEqual(heights, sorted(heights, reverse=True))

    def test_order_defaults_to_ascending(self):
        _, out = self.call(data=list(reversed(twenty_records())), sort_by="height")
        self.assertEqual(out["results"][0]["height"], 150)

    def test_sorting_an_empty_result_has_no_error(self):
        code, out = self.call(data=FOOD, search_term="pizza", sort_by="name", order="descending")
        self.assertEqual(code, 200)
        self.assertEqual(out["results"], [])

    def test_same_request_gives_the_same_order_every_time(self):
        data = [{"id": i, "build": BUILDS[i % 2]} for i in range(50)]  # lots of ties
        runs = [self.call(data=data, sort_by="build")[1]["results"] for _ in range(5)]
        self.assertTrue(all(run == runs[0] for run in runs))

    def test_performance_1000_records_within_2_seconds(self):
        data = [{"id": i, "score": (i * 7919) % 1000} for i in range(1000)]
        start = time.perf_counter()
        code, out = self.call(data=data, sort_by="score", order="descending")
        self.assertLess(time.perf_counter() - start, 2.0)
        self.assertEqual(code, 200)
        self.assertEqual(out["total"], 1000)


class BadRequests(ServiceTestCase):
    def test_bad_requests_get_a_400_and_an_error_message(self):
        cases = [
            {"search_term": "x"},                    # no data
            {"data": "not a list"},
            {"data": FOOD, "search_term": 5},
            {"data": FOOD, "filters": "x"},
            {"data": FOOD, "sort_by": 7},
            {"data": FOOD, "sort_by": "name", "order": "sideways"},
            {"data": FOOD, "sort_by": "nope"},       # field does not exist
        ]
        for body in cases:
            with self.subTest(body=body):
                code, out = self.call(**body)
                self.assertEqual(code, 400)
                self.assertTrue(out["error"])

    def test_service_keeps_working_after_an_error(self):
        self.call(data="bad")
        code, out = self.call(data=FOOD, search_term="Cake")
        self.assertEqual((code, out["total"]), (200, 1))


if __name__ == "__main__":
    unittest.main()