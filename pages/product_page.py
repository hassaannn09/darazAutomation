from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):
    FREE_SHIPPING_LABEL = (By.XPATH, "//span[contains(text(),'Free Shipping')]")

    def is_free_shipping_available(self):
        try:
            self.wait_for_element(self.FREE_SHIPPING_LABEL)
            return True
        except:
            return False
