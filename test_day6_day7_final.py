import time

import pytest
from playwright.sync_api import Playwright, expect

from pages.page_manager import PageManager
from utils.data_loaded import read_csv, read_excel, read_json
from utils.logger import logger

user_details = read_json("data/login.json")
user_credentials = user_details["user_details"]


@pytest.mark.parametrize("user",user_credentials)
def test_checkout(browse_open_url,user):
    logger.info( "Starting Playwright test")
    pm = PageManager(browse_open_url)
    #login page
    pm.login_page.login(user["username"],user["password"])
    logger.info(f"User '{user['username']}' logged in successfully.")

    # inventory page: adding product to cart
    product_details= read_csv("data/ProductDetails.csv")
    print(product_details)
    for product in product_details:
        logger.info(f"Adding product: {product['ProductName']}")
        pm.inventory_page.product_addition(product["ProductName"])
    time.sleep(2)

    # click on the shopping cart
    pm.inventory_page.shopping_cart_click()

    # cart page
    pm.cart.shopping_checkout_click()

    # checkoutStep1 page: filling checkout details
    data= read_excel("data/userDetailsExcel.xlsx")
    for items in data:
        pm.checkout_one.fill_checkout_step_one(items["FirstName"],items["LastName"],str(items["postal code"]))
    time.sleep(2)
    pm.checkout_one.click_continue()

    # checkout step 2
    pm.checkout_two.click_finish()

    #checkoutComplete
    expect(pm.checkout_complete.get_title()).to_contain_text("Checkout: Complete!")
    logger.info("Checkout success full")
