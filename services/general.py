from bs4 import BeautifulSoup


def scraper(driver, url=''):
    """
    :param driver:
    :param url:
    :return:
    """
    driver.get(url)
    result = BeautifulSoup(driver.page_source, "html.parser")
    return result
