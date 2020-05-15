import time
from selenium.webdriver.support.ui import Select
import os
import datetime
from models.jobs import Jobs


def seek_sign_in(web_driver):
    """
    :param web_driver:
    :return:
    """

    web_driver.get('https://www.seek.com.au/sign-in')
    time.sleep(3)
    web_driver.find_element_by_id('email').send_keys(os.getenv('SEEK_USERNAME'))
    web_driver.find_element_by_id('password').send_keys(os.getenv('SEEK_PASSWORD'))
    web_driver.find_element_by_xpath('//button[@data-automation="signin-submit"]').click()
    time.sleep(5)
    return True


def format_seek_data(seek_data):
    """
    :param seek_data:
    :return:
    """
    jobs = list()
    sections = seek_data.find_all('article')

    for section in sections:
        data = section.find("h1").find('a')
        job = dict()
        job['title'] = data.get_text()

        # Strip get params
        data['href'] = data['href'].split("?")[0]
        job['url'] = data['href']
        jobs.append(job)

    return jobs


def process_seek_application(driver, session, seek_job_data):
    """
    :param driver:
    :param session:
    :param seek_job_data:
    :return:
    """
    # First double check if we have already applied for this job
    job = session.query(Jobs).filter_by(url=seek_job_data['url']).first()

    if job is not None:
        print('Already applied for job: ' + str(seek_job_data['url']))
        return True

    driver.get("https://www.seek.com.au" + str(seek_job_data['url']))
    url = None
    for anchors in driver.find_elements_by_tag_name('a'):
        if anchors.get_attribute('data-automation') == 'job-detail-apply':
            url = anchors.get_attribute('href')
            break

    if url is None:
        return False

    driver.get(str(url))
    time.sleep(3)

    job = Jobs()
    try:
        # Part 1 Resume
        driver.execute_script('document.getElementById("dontIncludecoverLetter").click()')
        select = Select(driver.find_element_by_id('selectedResume'))
        select.select_by_value('0')
        time.sleep(5)

        driver.find_element_by_xpath('//button[@data-testid="continue-button"]').click()
        time.sleep(20)

        # Part 2 Questions (optional)
        try:
            driver.find_element_by_xpath('//button[@data-testid="continue-button"]').click()
            time.sleep(3)
        except:
            pass

        # Part 3 Update seek
        try:
            driver.find_element_by_xpath('//button[@data-testid="continue-button"]').click()
            time.sleep(3)
        except:
            pass

        # Part 4 Review and Submit
        driver.find_element_by_xpath('//button[@data-testid="review-submit-application"]').click()
        time.sleep(7)

        job.submitted = True
    except Exception as e:
        print('Issue submitting application')
        job.submitted = False

    job.site_id = 1
    job.job_title = seek_job_data['title']
    job.url = seek_job_data['url']
    job.created_at = datetime.datetime.now()
    job.updated_at = datetime.datetime.now()
    session.add(job)
    session.commit()

    if job.submitted:
        print('Submitted application for job: ' + str(seek_job_data['url']))

    return True
