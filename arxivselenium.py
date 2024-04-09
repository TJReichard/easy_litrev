from selenium import webdriver
from selenium.webdriver.common.by import By

# This is a helper script to work around the old arxiv export api. Use fixed search urls of advanced search to crawl the arxiv_ids using selenium. Then lookup metadata via arxiv python library


# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no browser window)
driver = webdriver.Chrome(options=options)

# Website URL
url = ['https://arxiv.org/search/advanced?advanced=&terms-0-term=prompt*&terms-0-operator=AND&terms-0-field=title&terms-1-term=AI+OR+artificial+intelligence+OR+LLM+OR+Large+language+model+OR+machine+learning+OR+ML+OR+machine+intelligence+OR+MI&terms-1-operator=AND&terms-1-field=title&classification-computer_science=y&classification-economics=y&classification-eess=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=date_range&date-year=&date-from_date=2019&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first',
       'https://arxiv.org/search/advanced?advanced=&terms-0-term=prompt%2A&terms-0-operator=AND&terms-0-field=title&terms-1-term=AI+OR+artificial+intelligence+OR+LLM+OR+Large+language+model+OR+machine+learning+OR+ML+OR+machine+intelligence+OR+MI&terms-1-operator=AND&terms-1-field=title&classification-computer_science=y&classification-economics=y&classification-eess=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=date_range&date-year=&date-from_date=2019&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&start=200',
       'https://arxiv.org/search/advanced?advanced=&terms-0-term=prompt%2A&terms-0-operator=AND&terms-0-field=title&terms-1-term=AI+OR+artificial+intelligence+OR+LLM+OR+Large+language+model+OR+machine+learning+OR+ML+OR+machine+intelligence+OR+MI&terms-1-operator=AND&terms-1-field=title&classification-computer_science=y&classification-economics=y&classification-eess=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=date_range&date-year=&date-from_date=2019&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&start=400']
id_list = []

# Open the URL
for u in url:
    driver.get(u)

    # Find all list items with the class "arxiv-result"
    results = driver.find_elements(By.CLASS_NAME, 'arxiv-result')

    # Initialize a list to store href attributes

    # Extract href attribute of the first anchor tag within each result
    for result in results:
        href = result.find_element(By.TAG_NAME, 'a').text
        colon_index = href.find(':')
        after_colon = href[colon_index + 1:]
        id_list.append(after_colon)

    # Close the WebDriver
driver.quit()

print(id_list)
