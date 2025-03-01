import requests
from bs4 import BeautifulSoup
import time

products_to_track = [
    {
        "product_url": "https://www.amazon.in/Samsung-Galaxy-Ocean-Blue-Storage/dp/B07HGJKDQL",
        "name": "Samsung M31",
        "target_price": 16000
    },
    {
        "product_url": "https://www.amazon.in/Test-Exclusive-668/dp/B07HGH88GL",
        "name": "Samsung M21 6GB 128GB",
        "target_price": 16000
    },
    {
        "product_url": "https://www.amazon.in/Test-Exclusive-553/dp/B0784D7NFQ",
        "name": "Redmi Note 9 Pro",
        "target_price": 17000
    },
    {
        "product_url": "https://www.amazon.in/Apple-iPhone-13-128GB-Blue/dp/B09G9HD6PD",
        "name": "Apple iPhone 13",
        "target_price": 50000
    },
    {
        "product_url": "https://www.amazon.in/OnePlus-Nord-128GB-Storage-Triple/dp/B097RD2G2Y",
        "name": "OnePlus Nord CE 5G",
        "target_price": 23000
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def get_product_price(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try both price IDs
        price_element = soup.find(id="priceblock_dealprice") or soup.find(id="priceblock_ourprice")
        
        if price_element:
            price_text = price_element.get_text().strip()
            price = int(''.join(filter(str.isdigit, price_text)))  # Extract numeric price
            return price
        else:
            print(f"Price not found for {url}")
            return None

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

with open('my_result_file.txt', 'w') as result_file:
    for product in products_to_track:
        price = get_product_price(product["product_url"])
        
        if price is not None:
            print(f"{product['name']}: ₹{price}")

            if price <= product["target_price"]:
                print("Available at your required price!")
                result_file.write(f"{product['name']} - Available at Target Price | Current Price: ₹{price}\n")
            else:
                print("Still at current price.")
        
        time.sleep(2)  # Add delay to prevent request blocking
