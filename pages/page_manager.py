from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class PageManager:
    def __init__(self,page):
        self.login_page= LoginPage(page)
        self.inventory_page= InventoryPage(page)
        self.cart= CartPage(page)
        self.checkout_one= CheckoutStepOnePage(page)
        self.checkout_two= CheckoutStepTwoPage(page)
        self.checkout_complete= CheckoutCompletePage(page)
