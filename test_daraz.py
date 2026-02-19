import pathlib
import sys
import os
import subprocess
import json
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import selenium.common.exceptions

# Fix module path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage


def open_dashboard():
    """Start a local server and open the dashboard in the browser."""
    dashboard_dir = str(pathlib.Path(__file__).parent)

    # Kill anything already on port 8000
    subprocess.call(
        'for /f "tokens=5" %a in (\'netstat -aon ^| find ":8000"\') do taskkill /F /PID %a',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(0.5)

    # Start the server
    subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000"],
        cwd=dashboard_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1.5)  # give server time to start

    webbrowser.open("http://localhost:8000/dashboard.html")
    print("Dashboard opened at http://localhost:8000/dashboard.html")


def test_daraz_automation():

    start_time = time.time()

    # ---------------------------
    # Chrome Configuration
    # ---------------------------
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(r"C:\Users\ASUS\Desktop\darazAutomation\drivers\chromedriver.exe"),
        options=chrome_options
    )

    print("Browser launched successfully.")

    # Default result values
    product_count = 0
    free_shipping = False
    status = "FAIL"

    try:
        # ---------------------------
        # 1. Open Website
        # ---------------------------
        driver.get("https://www.daraz.pk")
        print("Daraz.pk opened successfully.")

        # ---------------------------
        # 2. Search Product
        # ---------------------------
        home = HomePage(driver)
        home.search_product("electronics")
        print("Search performed for 'electronics'.")

        # ---------------------------
        # 3. Apply Brand Filter (Planet X)
        # ---------------------------
        search = SearchPage(driver)
        search.apply_brand_filter("Planet X")
        print("Brand filter applied: Planet X")

        # ---------------------------
        # 4. Apply Price Filter
        # ---------------------------
        search.apply_price_filter("500", "5000")
        print("Price filter applied: 500 - 5000")

        # ---------------------------
        # 5. Get Product Count
        # ---------------------------
        product_count = search.get_product_count()
        print(f"Total products found: {product_count}")

        if product_count > 0:
            # ---------------------------
            # 6. Open First Product
            # ---------------------------
            search.open_first_product()
            print("First product opened successfully.")

            # ---------------------------
            # 7. Check Free Shipping
            # ---------------------------
            product = ProductPage(driver)
            free_shipping = product.is_free_shipping_available()
            print("Free Shipping Available:", free_shipping)

            status = "PASS"
        else:
            print("No products found after filtering.")
            status = "FAIL"

    except selenium.common.exceptions.WebDriverException as e:
        print("Selenium error occurred:", e)
        status = "FAIL"

    except Exception as e:
        print("Unexpected error occurred:", e)
        status = "FAIL"

    finally:
        execution_time = round(time.time() - start_time, 2)

        # ---------------------------
        # Save report.json
        # ---------------------------
        results = {
            "test_name": "Daraz Automation Test",
            "search_term": "electronics",
            "brand": "Planet X",
            "price_range": "500-5000",
            "product_count": product_count,
            "free_shipping": free_shipping,
            "status": status,
            "execution_time_seconds": execution_time
        }

        report_path = pathlib.Path(__file__).parent / "report.json"
        with open(report_path, "w") as f:
            json.dump(results, f, indent=4)

        print("\nTest execution completed.")
        print("Final Status:", status)
        print("Execution Time:", execution_time, "seconds")
        print("Report saved to:", report_path)

        driver.quit()

        # ---------------------------
        # Open Dashboard (AFTER quit)
        # ---------------------------
        open_dashboard()


if __name__ == "__main__":
    test_daraz_automation()