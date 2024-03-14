import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Create new data frame
df = pd.DataFrame(columns=['Product', 'Price', 'Rating'])

# enable headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get('https://www.amazon.com/')

    query = input('Enter your query: ')

    # Enter the search query into the search box and submit the form
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    search_box.send_keys(query)
    search_box.submit()

    # Find Product
    products = driver.find_elements(By.XPATH, "//div[contains(@data-component-type, 's-search-result')]")

    # Iterate through every product
    for product in products:
        # Product name
        product_name = product.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']")
        name = product_name.text.strip()

        # Product price
        try:
            product_price = product.find_element(By.XPATH, ".//span[@class='a-price']/span[@class='a-offscreen']")
            price = product_price.get_attribute('innerText').strip()
        except:
            price = 'Price not available'

        # Product rating
        try:
            product_rating = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']")
            rating = product_rating.get_attribute('innerHTML').split()[0]
        except:
            rating = 'Rating not available'

        # Storing data in csv file
        with open('products.csv', mode='a', newline='', encoding='utf-8') as file:
            file.write(f'Product: {name}, Price: {price}, Rating: {rating}\n')

        print(f"Product: {name}, Price: {price}, Rating: {rating}")
        print("=" * 100)

finally:
    driver.quit()
