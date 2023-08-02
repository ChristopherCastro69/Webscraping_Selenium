import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException


import time

url = 'https://www.mynimo.com/cebu/engineering-architecture-jobs'

try:
    # Set up the web driver using Chrome
    driver = webdriver.Chrome()

    driver.get(url)
    # Wait for the job listings to be visible
    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))

    total_pages = 7  # You may need to update this value based on the actual total number of pages

    # Open the CSV file for writing
    with open('Job_data_cebu.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Job Title', 'Salary', 'Experience', 'Company', 'Details', 'Address', 'Employees', 'Date', 'Link'])

        for page_number in range(1, total_pages + 1):
            if page_number > 7:
                print("Scraping Complete. Good Job!")
                break  # Exit the loop if the page number is greater than 2
            
            try:
                print(f"Scraping page {page_number}...")
                # Find all job listings on the current page
                jobs = driver.find_elements(By.XPATH, '//a[@class="href-button css-h9szfi"]')

                for job in jobs:
                    # Find the job title element within each job listing
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
                    try:
                    # Click on the link to navigate to the job details page
                        driver.execute_script("arguments[0].click();", job)

                        # Wait for the overlay/popup to disappear
                        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//div[@role="alert"]')))
                        
                        # Wait for the job details page to load completely
                        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1lz7cfx"]')))

                        job_details = driver.find_elements(By.XPATH, './/div[@class="tw-flex tw-flex-col"]')
                        for jobsD in job_details:   

                            address_elem = driver.find_element(By.XPATH, './/h6[@class="css-17y5fzp"]')
                            address = address_elem.text if address_elem else 'N/A'     
        
                            date_elem = driver.find_element(By.XPATH, './/h5[@class="tw-text-gray-600 tw-text-sm"]')
                            date = date_elem.text if date_elem else "N/A"   

                            id_elem = driver.find_elements(By.XPATH, './/h5[@class="tw-text-gray-600 tw-text-sm"]')
                            job_id =  id_elem[1].text if id_elem else 'N/A'

                            # Find the job details element containing the unordered list (<ul>) with job details
                            job_details_element = driver.find_element(By.XPATH, '//div[@class="html-box"]')

                            # Extract all the <li> elements within the <ul>
                            job_details_items = job_details_element.find_elements(By.XPATH, './/ul/li')
                            details_list = [item.text.strip() for item in job_details_items]

                            # Combine the details into a single string (separated by newline)
                            details = "\n".join(details_list)
                    
                                
                        print("ID:", job_id, 
                            " || Job title:", job_title,
                            " || Salary:", salary,
                            " || Experience: ", experience,
                            " || Company:", company,
                            " || Details:", details,
                            " || Address:", address,
                            " || Employees:", employees,
                            " || Date:", date,
                            " || Link:", link_elem                   

                        )
                        
                        time.sleep(1)
                        # Write the data to the CSV file
                        writer.writerow([job_id, job_title, salary, experience, company, details, address, employees, date, link_elem ])
                        # Go back to the original page with the list of jobs

                        driver.back()
                            # Wait for the job listings to be visible on the new page
                    
                        time.sleep(3)
                    except StaleElementReferenceException:
                    # If the element becomes stale, catch the exception and continue to the next iteration
                        print("Element became stale. Skipping to next job...")
                        driver.back()
                        continue

            except (TimeoutException, NoSuchElementException, WebDriverException) as e:
                print(f"An error occurred while scraping {job_title}: {e}")
                print("Attempting to refresh the page and retry...")
                driver.refresh()  # Refresh the page
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))
                continue  # Retry scraping the same page                


            if page_number < total_pages:
                # Find all page buttons
                page_buttons = driver.find_elements(By.XPATH, '//a[@class="href-button css-1ok8g35"]')

                # Click on the next page button
                for button in page_buttons:
                    if int(button.text) == page_number + 1:
                        button.click()
                        break

                # Wait for the job listings to be visible on the new page
                WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))

            time.sleep(3)

except Exception as e:
    print("An error occurred:", e)


finally:
    # Quit the driver after finishing the task
    driver.quit()
