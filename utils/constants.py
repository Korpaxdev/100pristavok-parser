from pathlib import Path
from typing import NamedTuple


class Urls(NamedTuple):
    CATEGORIES = [
        "https://100pristavok.ru/catalog/sony_play_station/igry_dlya_playstation/igry_dlya_playstation_5_1/",
        "https://100pristavok.ru/catalog/sony_play_station/igry_dlya_playstation/igry_dlya_playstation_4/",
    ]


class Dirs(NamedTuple):
    RESULT = Path("./results")
    CATEGORIES = RESULT / "categories"


class Selectors(NamedTuple):
    CATEGORY_TITLE = "#pagetitle"
    PAGE_NUM_LINK = "a.dark_link"
    ELEMENT = ".catalog_item.main_item_wrapper.item_wrap"
    ELEMENT_URL = ".item-title > a.dark_link"
    ELEMENT_TITLE = ".item-title > a > span"
    ELEMENT_PRICE = ".price_value"
    ELEMENT_DETAIL_TEXT = ".detail_text"
    ELEMENT_IMAGE = "#photo-0 img"


class LogMessages(NamedTuple):
    PAGE_LOG = "Получаю информацию: {page} страница из {total} страниц в категории {category}"
    BASE_INFO_LOG = "Получаю базовую информацию по элементам"
    BASE_INFO_ELEMENT_DONE = (
        "Базовая информация заполнена: {element} элементов из {total} элементов в категории {category}"
    )
    BASE_INFO_IS_DONE = "[green bold]УСПЕШНО![/green bold] Базовая информация заполнена"
    DETAIL_INFO_LOG = "Получаю детальную информацию по элементам"
    DETAIL_INFO_ELEMENT_DONE = (
        "Детальная информация заполнена: {element} элементов из {total} элементов в категории {category}"
    )
    DETAIL_INFO_IS_DONE = "[green bold]УСПЕШНО![/green bold] Детальная информация заполнена"


PAGE_PARAM = "PAGEN_1"
