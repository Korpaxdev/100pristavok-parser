from urllib.parse import urlparse, urlunparse

from services.chrome_driver import ChromeDriver
from utils.constants import Dirs, Urls, Selectors
from utils.other import create_dir_if_not_exists, str_to_int


class Parser:
    def __init__(self):
        self._driver = ChromeDriver()
        self._current_category = None
        create_dir_if_not_exists(Dirs.CATEGORIES)

    def parse(self):
        for page_url in Urls.CATEGORIES:
            self._driver.get(page_url)
            title = self._driver.find_element(Selectors.CATEGORY_TITLE).text.strip()
            self._current_category = create_dir_if_not_exists(Dirs.CATEGORIES / title)
            self._find_elements()

    def _find_elements(self):
        max_page = int(self._driver.find_elements(Selectors.PAGE_NUM_LINK).pop().text)
        elements_info = []
        for page in range(1, max_page + 1):
            current_url = str(urlunparse(urlparse(self._driver.current_url)._replace(query="")))
            page_url = current_url + f"?PAGEN_1={page}"
            self._driver.get(page_url)

            for element in self._driver.find_elements(Selectors.ELEMENT):
                title = self._driver.find_element_in_parent(element, Selectors.ELEMENT_TITLE).text
                price = self._driver.find_element_in_parent(element, Selectors.ELEMENT_PRICE, raise_exception=False)
                url = self._driver.find_element_in_parent(element, Selectors.ELEMENT_URL).get_attribute("href")
                base_element_info = {"title": title, "price": str_to_int(price.text) if price else None, "url": url}
                elements_info.append(base_element_info)
                print(f"{base_element_info=}")

        for base_element in elements_info:
            self._driver.get(base_element["url"])
            detail = self._driver.find_element(Selectors.ELEMENT_DETAIL_TEXT, raise_exception=False)
            detail_info = {"detail": detail.text if detail else None}
            del base_element["url"]
            base_element.update(detail_info)
            print(f"{base_element=}")
