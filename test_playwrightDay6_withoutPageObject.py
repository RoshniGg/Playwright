import time

from playwright.sync_api import Playwright, expect


def test_checkout(playwright:Playwright):
    # opening browser
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # navigation to the site
    page.goto("https://www.saucedemo.com/")

    # login page
    page.locator('#user-name').fill("standard_user")
    page.locator('#password').fill("secret_sauce")
    page.locator('#login-button').click()

    # inventory page: adding product to cart
    item= page.locator(".inventory_item").filter(has_text='Sauce Labs Backpack')
    item.locator("button:has-text('Add to cart')").click()
    time.sleep(2)


    item = page.locator(".inventory_item").filter(has_text='Sauce Labs Bike Light')
    item.locator("button:has-text('Add to cart')").click()
    time.sleep(2)

    # click on the shopping cart
    page.locator(".shopping_cart_link").click()
    time.sleep(2)

    # cart page
    page.locator('#checkout').click()
    time.sleep(2)

    # checkoutStep1 page: filling checkout details
    page.fill("#first-name", "John")
    page.fill("#last-name", "Doe")
    page.fill("#postal-code", "12345")
    page.locator(".btn_primary.cart_button").click()

    # checkout step 2
    page.locator(".btn_action.cart_button").click()
    time.sleep(2)

    #checkoutComplete
    expect(page.locator('.title')).to_contain_text("Checkout: Complete!")







