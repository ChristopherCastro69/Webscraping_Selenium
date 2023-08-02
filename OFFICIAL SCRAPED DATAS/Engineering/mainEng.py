import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

def scrape_job_details(driver,job):
    title_element = job.find_element(By.XPATH, './/p[@class="href-button css-qkcbob"]')
    job_title = title_element.text if title_element else "N/A"

    salary_elements = job.find_elements(By.XPATH, './/p[@class="css-1yqpud"]')
    salary = salary_elements[0].text if salary_elements else "N/A"

    experience_element = job.find_elements(By.XPATH, './/h6[@class="badge-name-text"]')
    experience = experience_element[0].text if experience_element else "N\A"

    company_elem = job.find_element(By.XPATH, './/h5[@class="company-name-text"]')
    company = company_elem.text if company_elem else "N/A"

    emp_elem = job.find_elements(By.XPATH, './/p[@class="css-1ht1cys"]')
    employees = emp_elem[2].text if len(emp_elem) >= 3 else "N/A"

    link_elem = job.get_attribute('href')

    driver.execute_script("arguments[0].click();", job)
    try:
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//div[@role="alert"]')))
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1lz7cfx"]')))
    except StaleElementReferenceException:
        print("Element became stale. Skipping to next job...")
        driver.back()
        return None

    job_details = driver.find_elements(By.XPATH, './/div[@class="tw-flex tw-flex-col"]')
    for jobsD in job_details:
        address_elem = driver.find_element(By.XPATH, './/h6[@class="css-17y5fzp"]')
        address = address_elem.text if address_elem else 'N/A'

        date_elem = driver.find_element(By.XPATH, './/h5[@class="tw-text-gray-600 tw-text-sm"]')
        date = date_elem.text if date_elem else "N/A"

        id_elem = driver.find_elements(By.XPATH, './/h5[@class="tw-text-gray-600 tw-text-sm"]')
        job_id = id_elem[1].text if id_elem else 'N/A'

        job_details_element = driver.find_element(By.XPATH, '//div[@class="html-box"]')
        job_details_items = job_details_element.find_elements(By.XPATH, './/ul/li')
        details_list = [item.text.strip() for item in job_details_items]
        details = "\n".join(details_list)

        return job_id, job_title, salary, experience, company, details, address, employees, date, link_elem

def write_to_csv(data):
    with open('Job_data_cebu.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Job Title', 'Salary', 'Experience', 'Company', 'Details', 'Address', 'Employees', 'Date', 'Link'])
        for row in data:
            writer.writerow(row)

def scrape_mynimo_jobs(url, total_pages):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))
        data = []

        for page_number in range(1, total_pages + 1):
            if page_number > total_pages:
                break

            print(f"Scraping page {page_number}...")
            jobs = driver.find_elements(By.XPATH, '//a[@class="href-button css-h9szfi"]')

            for job in jobs:
                scraped_data = scrape_job_details(driver, job)
                if scraped_data:
                    data.append(scraped_data)
                    time.sleep(1)
                    driver.back()
                    time.sleep(3)

            if page_number < total_pages:
                page_buttons = driver.find_elements(By.XPATH, '//a[@class="href-button css-1ok8g35"]')
                for button in page_buttons:
                    if int(button.text) == page_number + 1:
                        button.click()
                        break
                WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))
                time.sleep(3)

        return data

    except StaleElementReferenceException:
        print("Element became stale. Skipping to next job...")
        driver.back()

    finally:
        driver.quit()

def main():
    url = 'https://www.mynimo.com/cebu/engineering-architecture-jobs'
    total_pages = 8  # You may need to update this value based on the actual total number of pages

    data = scrape_mynimo_jobs(url, total_pages)
    write_to_csv(data)

if __name__ == "__main__":
    main()