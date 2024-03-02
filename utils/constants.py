from pathlib import Path
from typing import NamedTuple


class Urls(NamedTuple):
    CATEGORIES = ["https://100pristavok.ru/catalog/sony_play_station/igry_dlya_playstation/igry_dlya_playstation_5_1/"]


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
