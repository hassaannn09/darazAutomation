from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time

class SearchPage(BasePage):
    # Known product card selectors (Daraz changes classes often)
    PRODUCT_XPATHS = [
        "//div[contains(@class,'c3KeDq')]",
        "//div[contains(@class,'gridItem')]",
        "//div[contains(@class,'product-card')]",
        "//div[contains(@class,'card-jfy')]",
        "//div[contains(@class,'Bm3ON')]",
        "//li[contains(@class,'product')]",
        "//div[@data-qa-locator='product-item']",
        "//div[contains(@class,'item--')]",
    ]

    MIN_PRICE = (By.XPATH, "//input[@placeholder='Min']")
    MAX_PRICE = (By.XPATH, "//input[@placeholder='Max']")
    BRAND_SECTION = (By.XPATH, "//div[contains(text(),'Brand')]")

    def _find_products(self):
        """Try each known product card XPath and return the first non-empty result."""
        for xpath in self.PRODUCT_XPATHS:
            elements = self.driver.find_elements(By.XPATH, xpath)
            if elements:
                print(f"[DEBUG] Products found using XPath: {xpath} ({len(elements)} items)")
                return elements
        return []

    def apply_brand_filter(self, brand_name):
        """Scrolls and clicks the brand checkbox (Remington or any brand)."""
        self.wait.until(EC.presence_of_element_located(self.BRAND_SECTION))

        labels = self.driver.find_elements(By.XPATH, "//label[contains(@class,'ant-checkbox-wrapper')]")
        for label in labels:
            if brand_name.lower() in label.text.lower():
                self.driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -150);", label)
                time.sleep(0.5)
                try:
                    label.click()
                except Exception:
                    # Fallback to JS click
                    self.driver.execute_script("arguments[0].click();", label)
                # Wait for products to reload after applying brand filter
                self.wait.until(lambda d: len(self._find_products()) > 0)
                return
        raise Exception(f"Brand checkbox '{brand_name}' not found")

    def apply_price_filter(self, min_price, max_price):
        """Sets min/max prices and applies filter."""
        self.wait_and_send_keys(self.MIN_PRICE, min_price)
        self.wait_and_send_keys(self.MAX_PRICE, max_price)

        apply_xpaths = [
            "//input[@placeholder='Max']/following-sibling::button",
            "//input[@placeholder='Max']/..//button",
            "//input[@placeholder='Max']/../..//button",
            "//div[contains(@class,'price') or contains(@class,'Price')]//button",
            "//button[contains(@class,'ant-btn')]",
        ]

        for xpath in apply_xpaths:
            try:
                buttons = self.driver.find_elements(By.XPATH, xpath)
                if buttons:
                    btn = buttons[-1]
                    self.driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -150);", btn)
                    time.sleep(0.3)
                    try:
                        btn.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", btn)
                    # Wait for filtered products to appear
                    self.wait.until(lambda d: len(self._find_products()) > 0)
                    return
            except NoSuchElementException:
                continue

        # Last resort: press Enter in Max field
        max_el = self.driver.find_element(*self.MAX_PRICE)
        max_el.send_keys(Keys.RETURN)
        self.wait.until(lambda d: len(self._find_products()) > 0)

    def get_product_count(self):
        """Return the number of visible products after filters."""
        self.wait.until(lambda d: len(self._find_products()) > 0)
        products = self._find_products()
        if not products:
            raise Exception(
                "No products found. The product card CSS class may have changed. "
                "Update PRODUCT_XPATHS accordingly."
            )
        return len(products)

    def open_first_product(self):
        """Opens the first product safely, retries if stale."""
        attempts = 3
        while attempts > 0:
            try:
                products = self._find_products()
                if not products:
                    raise Exception("No products found to click")
                first = products[0]
                self.driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -150);", first)
                time.sleep(0.5)
                try:
                    first.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", first)
                return
            except (StaleElementReferenceException, TimeoutException) as e:
                print(f"[DEBUG] Retry clicking first product due to: {e}")
                time.sleep(0.5)
                attempts -= 1
        raise Exception("Failed to click the first product after 3 attempts")
