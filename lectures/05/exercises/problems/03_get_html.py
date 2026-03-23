"""Problem 03: GET request for HTML content.

Task:
1. Send GET to https://example.com
2. Print:
   - status code
   - Content-Type header
   - HTML body (response.text)
3. Verify content type contains text/html
4. Add raise_for_status()
"""

import requests

URL = "https://example.com"


def main() -> None:
    # TODO: implement GET request and print HTML response
    response = requests.get(URL)
    response.raise_for_status()
    print("Status code:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("HTML body:", response.text)
    if "text/html" in response.headers.get("Content-Type", ""):
        print("Content type is HTML.")
    else:
        print("Content type is not HTML.") 


if __name__ == "__main__":
    main()
