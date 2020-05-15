from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models.sites import Sites
from services.general import scraper
from services.seek import seek_sign_in, format_seek_data, process_seek_application
# TODO: Better way to set site url
# TODO: Add readme


if __name__ == '__main__':
    load_dotenv()

    print(os.getenv('SEEK_USERNAME'))
    print(os.getenv('DATABASE_USERNAME'))
    engine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(
        os.getenv('DATABASE_USERNAME'),
        os.getenv('DATABASE_PASSWORD'),
        os.getenv('DATABASE_HOST'),
        os.getenv('DATABASE_NAME')))

    Session = sessionmaker(bind=engine)
    session = Session()

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--auto-open-devtools-for-tabs")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome('/Users/joseph/Code/Job_Applier/chromedriver', options=options)

    seek_sign_in(driver)
    sites = session.query(Sites).all()
    for site in sites:
        soup = scraper(driver, site.url)
        if site.name == 'seek':
            jobs_to_apply = format_seek_data(soup)
            for job_data in jobs_to_apply:
                process_seek_application(driver, session, job_data)

    driver.quit()
    exit()
