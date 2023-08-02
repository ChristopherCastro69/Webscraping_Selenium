import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = 'https://www.mynimo.com/cebu/accounting-finance-jobs'

try:
    # Set up the web driver using Chrome
    driver = webdriver.Chrome()

    driver.get(url)
    # Wait for the job listings to be visible
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-hvwiok"]')))

    total_pages = 9  # You may need to update this value based on the actual total number of pages

    # Open the CSV file for writing
    with open('Job_data_cebu.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Job Title', 'Salary', 'Experience', 'Company', 'City', 'Street', 'Employees', 'Date', 'Link'])

        for page_number in range(1, total_pages + 1):
            if page_number > 9:
                break  # Exit the loop if the page number is greater than 2

            print(f"Scraping page {page_number}...")
            # Find all job listings on the current page
            jobs = driver.find_elements(By.XPATH, '//a[@class="href-button css-hvwiok"]')

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

                city_elem = job.find_element(By.XPATH, './/p[@class="css-6of238"]')
                city = city_elem.text if city_elem else "N/A"

                street_elem = job.find_element(By.XPATH, './/p[@class="css-1ht1cys"]')
                street = street_elem.text if street_elem else "N/A"

                emp_elem = job.find_elements(By.XPATH, './/p[@class="css-1ht1cys"]')
                employees = emp_elem[2].text if len(emp_elem) >= 3 else "N/A"

                date_elem = job.find_element(By.XPATH, './/p[@class="css-19bqwrc"]')
                date = date_elem.text if date_elem else "N/A"

                link_elem = job.get_attribute('href')

            
                print("Job Title:", job_title, 
                      " || Salary:", salary,
                      " || Experience: ", experience,
                      " || Company:", company,
                      " || City:", city,
                      " || Street:", street,
                      " || Employees:", employees,
                      " || Date:", date,
                      " || Link:", link_elem
                )

                
                # Write the data to the CSV file
                writer.writerow([job_title, salary, experience, company, city, street, employees, date, link_elem])

            if page_number < total_pages:
                # Find all page buttons
                page_buttons = driver.find_elements(By.XPATH, '//a[@class="href-button css-1ok8g35"]')

                # Click on the next page button
                for button in page_buttons:
                    if int(button.text) == page_number + 1:
                        button.click()
                        break

                # Wait for the job listings to be visible on the new page
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="href-button css-hvwiok"]')))

            time.sleep(2)

except Exception as e:
    print("An error occurred:", e)

finally:
    # Quit the driver after finishing the task
    driver.quit()
