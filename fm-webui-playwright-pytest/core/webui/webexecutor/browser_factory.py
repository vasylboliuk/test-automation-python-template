from playwright.sync_api import Page
from playwright.sync_api import sync_playwright

from core.utils.web_ui_config_loader import WebUiConfigLoader


class BrowserFactorySingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BrowserFactory(metaclass=BrowserFactorySingleton):

    _init_error = "The Playwright browser instance was not initialized. You should first call the method init_web_browser."

    def __init__(self):
        self.web_ui_config = WebUiConfigLoader().get_config()
        self.browser_config = self.web_ui_config.web_driver_config
        self.sync_playwright = sync_playwright().start()
        self.__browser = None
        self.__browser_context = None
        self.__browser_page = None

    def init_web_browser(self, browser_type: str):
        if browser_type == "Chrome":
            self.__browser = self.sync_playwright.chromium.launch(headless=self.browser_config.headless_mode)
            self.__browser_context = self.__browser.new_context()
            self.__browser_page = self.__browser.new_page()
        return self

    def get_browser(self):
        if self.__browser is None:
            raise ValueError(self._init_error)
        return self.__browser

    def get_browser_contex(self):
        if self.__browser_context is None:
            raise ValueError(self._init_error)
        return self.__browser_context

    def get_browser_page(self) -> Page:
        if self.__browser_page is None:
            raise ValueError(self._init_error)
        return self.__browser_page

    def close_browser(self):
        self.__browser_context.close()
        self.__browser.close()
