import requests
import json

from playwright.sync_api import Playwright

from utils.data_loaded import read_json

# Load the test configuration from test_data.json
testdata= read_json("data/api_details.json")
BASE_URL = testdata["base_url"]

class APIUtils:
    def create_cart(self, playwright: Playwright):
        api_request_context = playwright.request.new_context(base_url=BASE_URL)
        # Create a new cart using the endpoint from the test data.
        cart_create_data = testdata["cart"]["create"]
        end_point = cart_create_data["endpoint"]
        expected_status = int(cart_create_data["status"])
        print(end_point)
        response = api_request_context.post( end_point, headers={"Context-Type": "application/json"})
        assert response.status == expected_status
        return response.json()

    def get_product(self, playwright: Playwright):
        api_request_context = playwright.request.new_context(base_url=BASE_URL)
        # Retrieve the first product id and name
        product_get_details = testdata["product"]["get"]
        end_point = product_get_details["endpoint"]
        print(end_point)
        response = api_request_context.get(end_point)
        print(response.status )
        assert response.status == int(product_get_details["status"])
        product_data = response.json()
        return product_data


    def add_item_to_cart(self,playwright: Playwright,cart_id, payload):
        # Add an item to the given cart using
        api_request_context = playwright.request.new_context(base_url=BASE_URL)
        # Create a new cart using the endpoint from the test data.
        add_item_data = testdata["add_item"]
        endpoint_template = add_item_data["endpoint_template"]
        # Replace {cart_id} in the endpoint
        endpoint = endpoint_template.replace("{cart_id}", cart_id)
        print(endpoint)
        expected_status = int(add_item_data["status"])
        response = api_request_context.post(endpoint, headers={"Context-Type": "application/json"},data=payload )
        assert response.status == expected_status
        return response.json()

    def get_cart(self,playwright: Playwright,cart_id):
        # Add an item to the given cart using
        api_request_context = playwright.request.new_context(base_url=BASE_URL)
        # Create a new cart using the endpoint from the test data.
        get_cart_details= testdata["cart"]["get"]
        endpoint_template = get_cart_details["endpoint_template"]
        # Replace {cart_id} in the endpoint
        endpoint = endpoint_template.replace("{cart_id}", cart_id)
        print(endpoint)
        response = api_request_context.get(endpoint, headers={"Context-Type": "application/json"} )
        expected_status = int(get_cart_details["status"])
        assert response.status == expected_status

        response_data = response.json()
        cart_items = response_data["cart_items"]
        first_item = cart_items[0]
        product = first_item["product"]
        product_name = product["name"]

        return product_name
