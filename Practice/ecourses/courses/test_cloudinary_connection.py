import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

url = "https://api.cloudinary.com/v1_1/dvxzmwuat/image/upload"

try:
    response = requests.get(url)
    response.raise_for_status()  # Kiểm tra lỗi HTTP
    print("Connection successful!")
except ConnectionError:
    print("Failed to connect to Cloudinary API.")
except Timeout:
    print("The request timed out.")
except RequestException as e:
    print(f"An error occurred: {e}")