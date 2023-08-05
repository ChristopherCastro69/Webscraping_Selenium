import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException

def get_job_details(job):
    try:
        title_element = job.find_element(By.XPATH, './/p[@class="href-button css-qkcbob"]')
        job_title = title_element.text if title_element else "N/A"

        salary_elements = job.find_elements(By.XPATH, './/p[@class="css-1yqpud"]')
        salary = salary_elements[0].text if salary_elements else "N/A"

        experience_element = job.find_element(By.XPATH, './/h6[@class="badge-name-text"]')
        experience = experience_element.text if experience_element else "N\A"

        company_elem = job.find_element(By.XPATH, './/h5[@class="company-name-text"]')
        company = company_elem.text if company_elem else "N/A"

        emp_elem = job.find_elements(By.XPATH, './/p[@class="css-1ht1cys"]')
        employees = emp_elem[2].text if len(emp_elem) >= 3 else "N/A"

        link_elem = job.get_attribute('href')

        return job_title, salary, experience, company, employees, link_elem
    except StaleElementReferenceException as e:
        print("Stale element reference occurred. Trying again...")
        return get_job_details(job)  # Retry fetching the element

def scrape_job_details(driver):
    address_elem = driver.find_element(By.XPATH, './/h6[@class="css-17y5fzp"]')
    address = address_elem.text if address_elem else 'N/A'

    date_elem = driver.find_element(By.XPATH, './/h5[@class="tw-text-gray-600 tw-text-sm"]')
    date = date_elem.text if date_elem else "N/A"

    id_elem = driver.find_elements(By.XPATH, './/h5[@class="tw-text-gray-600 tw-text-sm"]')
    job_id =  id_elem[1].text if id_elem else 'N/A'

    job_details_element = driver.find_element(By.XPATH, '//div[@class="html-box"]')
    job_details_items = job_details_element.find_elements(By.XPATH, './/ul/li')
    details_list = [item.text.strip() for item in job_details_items]
    details = "\n".join(details_list)

    return job_id, details, address, date


def scrape_jobs_on_page(driver, total_pages):
    with open('Job_data_cebu.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Job Title', 'Salary', 'Experience', 'Company', 'Details', 'Address', 'Employees', 'Date', 'Link'])
        
        for page_number in range(1, total_pages + 1):
            if page_number > 7:
                break

            print(f"Scraping page {page_number}...")
            # Find all job listings on the current page
            jobs = driver.find_elements(By.XPATH, '//a[@class="href-button css-h9szfi"]')

            for job in jobs:
                job_title, salary, experience, company, employees, link_elem = get_job_details(job)
                if job_title is not None:
                    # Click on the link to navigate to the job details page
                    driver.execute_script("arguments[0].click();", job)

                    # Wait for the overlay/popup to disappear
                    WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.XPATH, '//div[@role="alert"]')))
                    # Switch to the new tab/window
                    # driver.switch_to.window(driver.window_handles[1])

                    # Wait for the job details page to load completely
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1lz7cfx"]')))

                    job_id, details, address, date = scrape_job_details(driver)

                    print("ID:", job_id,
                          " || Job title:", job_title,
                          " || Salary:", salary,
                          " || Experience: ", experience,
                          " || Company:", company,
                          " || Details:", details,
                          " || Address:", address,
                          " || Employees:", employees,
                          " || Date:", date,
                          " || Link:", link_elem)

                    time.sleep(1)
                    # Write the data to the CSV file
                    writer.writerow([job_id, job_title, salary, experience, company, details, address, employees, date, link_elem])
                    # Go back to the original page with the list of jobs
                    driver.back()
                    # Wait for the job listings to be visible on the new page
                    time.sleep(3)

            if page_number < total_pages:
                # Find all page buttons
                page_buttons = driver.find_elements(By.XPATH, '//a[@class="href-button css-1ok8g35"]')

                # Click on the next page button
                for button in page_buttons:
                    if int(button.text) == page_number + 1:
                        button.click()
                        break

                # Wait for the job listings to be visible on the new page
                WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))

            time.sleep(3)
    
    for page_number in range(1, total_pages + 1):
        if page_number > 7:
            break

        print(f"Scraping page {page_number}...")
        # Find all job listings on the current page
        jobs = driver.find_elements(By.XPATH, '//a[@class="href-button css-h9szfi"]')

        for job in jobs:
            job_title, salary, experience, company, employees, link_elem = get_job_details(job)
            if job_title is not None:
                # Click on the link to navigate to the job details page
                driver.execute_script("arguments[0].click();", job)

                # Wait for the overlay/popup to disappear
                WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.XPATH, '//div[@role="alert"]')))
                # Switch to the new tab/window
                # driver.switch_to.window(driver.window_handles[1])

                # Wait for the job details page to load completely
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1lz7cfx"]')))

                job_id, details, address, date = scrape_job_details(driver)

                print("ID:", job_id,
                      " || Job title:", job_title,
                      " || Salary:", salary,
                      " || Experience: ", experience,
                      " || Company:", company,
                      " || Details:", details,
                      " || Address:", address,
                      " || Employees:", employees,
                      " || Date:", date,
                      " || Link:", link_elem)

                time.sleep(1)
                # Write the data to the CSV file
                writer.writerow([job_id, job_title, salary, experience, company, details, address, employees, date, link_elem])
                # Go back to the original page with the list of jobs
                driver.back()
                # Wait for the job listings to be visible on the new page
                time.sleep(3)

        if page_number < total_pages:
            # Find all page buttons
            page_buttons = driver.find_elements(By.XPATH, '//a[@class="href-button css-1ok8g35"]')

            # Click on the next page button
            for button in page_buttons:
                if int(button.text) == page_number + 1:
                    button.click()
                    break

            # Wait for the job listings to be visible on the new page
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))

        time.sleep(3)

def main():
    url = 'https://www.mynimo.com/cebu/admin-office-clerical-jobs'
    total_pages = 7

    try:
        # Set up the web driver using Chrome
        driver = webdriver.Chrome()

        driver.get(url)
        # Wait for the job listings to be visible
        WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))

        # Open the CSV file for writing
        with open('Job_data_cebu.csv', mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Job Title', 'Salary', 'Experience', 'Company', 'Details', 'Address', 'Employees', 'Date', 'Link'])
            
            try:
                scrape_jobs_on_page(driver, total_pages)
            except (WebDriverException, StaleElementReferenceException) as e:
                # Handle the disconnected exception
                print("An error occurred:", e)
                print("WebDriver lost connection. Trying to recover...")
                driver.refresh()
                time.sleep(5)
                scrape_jobs_on_page(driver, total_pages)
                    
    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Quit the driver after finishing the task
        driver.quit()

if __name__ == "__main__":
    main()