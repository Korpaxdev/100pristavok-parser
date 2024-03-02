from typing import Optional, List

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils.other import run_callback_with_ignore_errors


class ChromeDriver(Chrome):
    def __init__(self, options: Options = None, service: Service = None, keep_alive: bool = True):
        if not options:
            options = ChromeOptions()
            options.page_load_strategy = "eager"
            options.add_argument("--headless")
        super().__init__(options, service, keep_alive)

    def find_element(self, css_selector: Optional[str] = None, raise_exception=True) -> WebElement | None:
        if raise_exception:
            return super().find_element(By.CSS_SELECTOR, css_selector)
        return run_callback_with_ignore_errors(super().find_element, by=By.CSS_SELECTOR, value=css_selector)

    def find_elements(self, css_selector: Optional[str] = None, raise_exception=True) -> List[WebElement]:
        if raise_exception:
            return super().find_elements(By.CSS_SELECTOR, css_selector)
        return run_callback_with_ignore_errors(super().find_elements, by=By.CSS_SELECTOR, value=css_selector)

    @staticmethod
    def find_element_in_parent(parent: WebElement, css_selector: Optional[str] = None, raise_exception=True):
        if raise_exception:
            return parent.find_element(By.CSS_SELECTOR, css_selector)
        return run_callback_with_ignore_errors(parent.find_element, by=By.CSS_SELECTOR, value=css_selector)
