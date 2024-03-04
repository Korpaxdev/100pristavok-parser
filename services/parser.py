from urllib.parse import urlparse, urlunparse

from rich.console import Console

from services.chrome_driver import ChromeDriver
from utils.constants import Dirs, Urls, Selectors, PAGE_PARAM, LogMessages, RESULT_FILE
from utils.other import create_dir_if_not_exists, str_to_int, remove_dir_if_exists, write_to_json


class Parser:
    def __init__(self, max_page=None):
        remove_dir_if_exists(Dirs.RESULT)
        self._console = Console()
        self._driver = ChromeDriver()
        self._current_category_name = None
        self._current_dir_category = None
        self._result_file_path = None
        self.max_page = max_page
        create_dir_if_not_exists(Dirs.CATEGORIES)

    def parse(self):
        for page_url in Urls.CATEGORIES:
            self._driver.get(page_url)
            self._current_category_name = self._driver.find_element(Selectors.CATEGORY_TITLE).text.strip()
            self._current_dir_category = create_dir_if_not_exists(Dirs.CATEGORIES / self._current_category_name)
            self._result_file_path = self._current_dir_category / RESULT_FILE
            elements_info = self._find_elements()
            write_to_json(elements_info, self._result_file_path)

            self._console.log(LogMessages.RESULT_FILE_LOG % self._result_file_path)

    def _find_elements(self) -> list[dict]:
        elements_count_page = int(self._driver.find_elements(Selectors.PAGE_NUM_LINK).pop().text)

        if self.max_page and elements_count_page > self.max_page:
            elements_count_page = self.max_page

        elements_info = []
        for page in range(1, elements_count_page + 1):
            current_url = str(urlunparse(urlparse(self._driver.current_url)._replace(query="")))
            page_url = current_url + f"?{PAGE_PARAM}={page}"
            self._driver.get(page_url)

            self._console.log(
                LogMessages.PAGE_LOG.format(page=page, total=elements_count_page, category=self._current_category_name)
            )

            with self._console.status(LogMessages.BASE_INFO_LOG) as status:
                elements = self._driver.find_elements(Selectors.ELEMENT)
                for index, element in enumerate(elements):
                    title = self._driver.find_element_in_parent(element, Selectors.ELEMENT_TITLE).text
                    price = self._driver.find_element_in_parent(element, Selectors.ELEMENT_PRICE, raise_exception=False)
                    url = self._driver.find_element_in_parent(element, Selectors.ELEMENT_URL).get_attribute("href")
                    base_element_info = {"title": title, "price": str_to_int(price.text) if price else None, "url": url}
                    elements_info.append(base_element_info)

                    status.console.log(
                        LogMessages.BASE_INFO_ELEMENT_DONE.format(
                            element=index + 1, total=len(elements), category=self._current_category_name
                        )
                    )

        self._console.log(LogMessages.BASE_INFO_IS_DONE)

        with self._console.status(LogMessages.DETAIL_INFO_LOG) as status:
            for index, base_element in enumerate(elements_info):
                self._driver.get(base_element["url"])
                detail = self._driver.find_element(Selectors.ELEMENT_DETAIL_TEXT, raise_exception=False)
                image = None
                image_element = self._driver.find_element(Selectors.ELEMENT_IMAGE, raise_exception=False)
                if image_element:
                    image = str(
                        self._driver.download_file_by_url(
                            image_element.get_attribute("src"), self._current_dir_category / "images"
                        )
                    )
                detail_info = {"detail": detail.text if detail else None, "image": image}
                del base_element["url"]
                base_element.update(detail_info)

                status.console.log(
                    LogMessages.DETAIL_INFO_ELEMENT_DONE.format(
                        element=index + 1, total=len(elements_info), category=self._current_category_name
                    )
                )

        self._console.log(LogMessages.DETAIL_INFO_IS_DONE)

        return elements_info
