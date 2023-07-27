import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time

url = 'https://www.mynimo.com/cebu/it-jobs'

try:
    # Set up the web driver using Chrome
    driver = webdriver.Chrome()

    driver.get(url)
    # Wait for the job listings to be visible
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))

    total_pages = 6  # You may need to update this value based on the actual total number of pages

    # Open the CSV file for writing
    with open('Job_data_cebu.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Job Title', 'Salary', 'Experience', 'Company', 'City', 'Street', 'Employees', 'Date', 'Link', 'Details'])

        for page_number in range(1, total_pages + 1):
            if page_number > 2:
                break  # Exit the loop if the page number is greater than 2

            print(f"Scraping page {page_number}...")
            # Find all job listings on the current page
            jobs = driver.find_elements(By.XPATH, '//a[@class="href-button css-h9szfi"]')

            for job in jobs:
                # Find the job title element within each job listing
                title_element = job.find_element(By.XPATH, './/p[@class="href-button css-qkcbob"]')
                job_title = title_element.text if title_element else "N/A"

                salary_elements = job.find_elements(By.XPATH, './/p[@class="css-1yqpud"]')
                salary = salary_elements[0].text if salary_elements else "N/A"

                experience_element = job.find_element(By.XPATH, './/h6[@class="badge-name-text"]')
                experience = experience_element.text if experience_element else "N\A"

                company_elem = job.find_element(By.XPATH, './/h5[@class="company-name-text"]')
                company = company_elem.text if company_elem else "N/A"

                city_elem = job.find_element(By.XPATH, './/p[@class="css-6of238"]')
                city = city_elem.text if city_elem else "N/A"

                street_elem = job.find_element(By.XPATH, './/p[@class="css-1ht1cys"]')
                street = street_elem.text if street_elem else "N/A"

                emp_elem = job.find_elements(By.XPATH, './/p[@class="css-1ht1cys"]')
                employees = emp_elem[2].text if len(emp_elem) >= 3 else "N/A"

                date_elem = job.find_element(By.XPATH, './/p[@class="css-19bqwrc"]')
                date = date_elem.text if date_elem else "N/A"

                link_elem = job.get_attribute('href')

                # Click on the link to navigate to the job details page
                driver.execute_script("arguments[0].click();", job)

                # Wait for the overlay/popup to disappear
                WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, '//div[@role="alert"]')))
                # Switch to the new tab/window
                #driver.switch_to.window(driver.window_handles[1])
                
                # Wait for the job details page to load completely
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1lz7cfx"]')))

                job_details = driver.find_elements(By.XPATH, './/div[@class="tw-flex tw-flex-col"]')
                for jobsD in job_details:
                    # Extract job title
                    # job_title_element = driver.find_element(By.XPATH, '//div[@class="html-box"]/p/strong')
                    # job_title2 = job_title_element.text.strip() if job_title_element else "N/A"

                    # # Extract job highlights
                    # job_highlights = []
                    # highlight_elements = driver.find_elements(By.XPATH, '//p[contains(text(), "Job Highlights")]/following-sibling::ul/li')
                    # for highlight_element in highlight_elements:
                    #     job_highlights.append(highlight_element.text.strip())

                    # Find the job details element containing the unordered list (<ul>) with job details
                    job_details_element = driver.find_element(By.XPATH, '//div[@class="html-box"]')

                    # Extract all the <li> elements within the <ul>
                    job_details_items = job_details_element.find_elements(By.XPATH, './/ul/li')
                    details_list = [item.text.strip() for item in job_details_items]

                    # Combine the details into a single string (separated by newline)
                    details = "\n".join(details_list)

            
                print("Job Title:", job_title, 
                      " || Salary:", salary,
                      " || Experience: ", experience,
                      " || Company:", company,
                      " || City:", city,
                      " || Street:", street,
                      " || Employees:", employees,
                      " || Date:", date,
                      " || Link:", link_elem,
                      " || Details:", details

                )

                time.sleep(1)
                # Write the data to the CSV file
                writer.writerow([job_title, salary, experience, company, city, street, employees, date, link_elem, details])
                break #Bug test
            # if page_number < total_pages:
            #     # Find all page buttons
            #     page_buttons = driver.find_elements(By.XPATH, '//a[@class="href-button css-1ok8g35"]')

            #     # Click on the next page button
            #     for button in page_buttons:
            #         if int(button.text) == page_number + 1:
            #             button.click()
            #             break

            #     # Wait for the job listings to be visible on the new page
            #     WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-h9szfi"]')))

            # time.sleep(2)

except Exception as e:
    print("An error occurred:", e)

finally:
    # Quit the driver after finishing the task
    driver.quit()
