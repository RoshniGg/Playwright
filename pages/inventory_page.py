class InventoryPage:

    def __init__(self,page):
        self.page = page
        self.inventory= page.locator(".inventory_item")
        self.shopping_cart_button=page.locator(".shopping_cart_link")

    def product_addition(self, product_name:str):
        item = self.inventory.filter(has_text=product_name)
        add_to_cart_button= item.locator("button:has-text('Add to cart')")
        add_to_cart_button.click()

    def shopping_cart_click(self):
        self.shopping_cart_button.click()