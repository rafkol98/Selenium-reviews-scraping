# Scrapes reviews for a company from trustpilot.com using selenium and beautiful soup.
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from dateutil import parser
import csv
import time

# Convert date to numerical format from string.
def convert_date(date_string_scraped):
    date_regex = r"\b\d{1,2}\s[A-Z][a-z]{2,8}\s\d{4}\b"
    match = re.search(date_regex, date_string_scraped)
    if match:
        date = match.group()
        date_parsed = parser.parse(date)
        # Convert to numerical format.
        date_numerical = date_parsed.strftime("%d/%m/%Y")
        return date_numerical
    else:
        print("No date found.")
        return "-"


# Set up selenium driver.
driver = webdriver.Chrome()

# Find reviews and dates.
all_reviews = []

counter = 1

# Loop through the pages.
while counter <= 34:
    print(counter)
    if counter == 1:
        url = "https://uk.trustpilot.com/review/valdaenergy.com"
        driver.get(url)
        driver.find_element("id", "onetrust-accept-btn-handler").click()

    else:
        url = "https://uk.trustpilot.com/review/valdaenergy.com?page=" + str(counter)
        driver.get(url)
       
    # Wait for the page to load.
    time.sleep(3)

    # Get the page source.
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the reviews and dates in the current page.
    reviews_text = soup.find_all("p",class_="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn",)
    experiences_dates = soup.find_all("p",class_="typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_color-black__5LYEn",)

    # Get the review text and date, store them in the array..
    for container_text, container_dates in zip(reviews_text, experiences_dates):
        rev = container_text.text.strip()
        # Convert date to numerical format.
        rev_date = convert_date(container_dates.text.strip())

        all_reviews.append((rev, str(rev_date)))

    # Increment counter, go to the next page.
    counter += 1


# Open a file for writing
with open("scraped_reviews.csv", "w", newline="") as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    # Write the header row
    writer.writerow(["Review", "Date"])
    # Write the data to the file
    writer.writerows(all_reviews)


# Close the driver.
driver.close()

driver.quit()
