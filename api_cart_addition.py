import json
import pytest
from playwright.sync_api import Playwright

from utils.api_utils import APIUtils
from utils.data_loaded import read_json

def test_cart_end_to_end(playwright:Playwright):
    data = read_json("data/api_details.json")
    api = APIUtils()

    # Step 1: Create Cart
    cart_result = api.create_cart(playwright)
    print(f"CREATE CART RESPONSE: {cart_result}")
    expected_response_keys = data["cart"].get("expected_response_keys", [])
    assert all(key in cart_result for key in expected_response_keys)

    cart_id = cart_result["id"]
    print(cart_id)

    #Step2: get details of the product and create the payload.
    response_data = api.get_product(playwright)
    print(response_data)
    # Take the first product
    product_list = response_data["data"]
    print(product_list)
    first_product = product_list[0]
    product_name = first_product["name"]

    # Create payload for cart
    payload = {
        "product_id": first_product["id"],
        "quantity": 1
    }
    #
    # Step 3: Add Item
    add_item_result = api.add_item_to_cart(playwright,cart_id, payload)
    print(add_item_result)
    assert add_item_result['result'] == data["add_item"]["expected_result"]

    # Step4: Retrieve the cart and check if we get the product added
    cart_response_product_name= api.get_cart(playwright,cart_id)
    print(cart_response_product_name)
    assert cart_response_product_name == product_name