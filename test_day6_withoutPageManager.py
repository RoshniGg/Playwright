import time

from playwright.sync_api import Playwright, expect

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.page_manager import PageManager


def test_checkout(playwright:Playwright,):
    # opening browser
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # navigation to the site
    page.goto("https://www.saucedemo.com/")

    #loginpage
    login_page = LoginPage(page)
    login_page.login("standard_user","secret_sauce")

    # inventory page: adding product to cart
    inventory_page = InventoryPage(page)
    inventory_page.product_addition('Sauce Labs Backpack')
    inventory_page.product_addition('Sauce Labs Bike Light')

    # click on the shopping cart
    inventory_page.shopping_cart_click()

    # cart page
    cart= CartPage(page)
    cart.shopping_checkout_click()

    # checkoutStep1 page: filling checkout details
    checkout_one = CheckoutStepOnePage(page)
    checkout_one.fill_checkout_step_one("John","Lisa","695502")
    checkout_one.click_continue()

    # checkout step 2
    checkout_two = CheckoutStepTwoPage(page)
    checkout_two.click_finish()

    #checkoutComplete
    checkout_complete = CheckoutCompletePage(page)
    expect(checkout_complete.get_title()).to_contain_text("Checkout: Complete!")







