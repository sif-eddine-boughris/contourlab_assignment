import requests

def test_recommend_endpoint():
    base_url = "http://127.0.0.1:5000"
    body_type = "hourglass"
    endpoint = f"{base_url}/recommend?bodytype={body_type}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        print("Recommended Items:")
        for item in data.get("recommended_items", []):
            print(f"Barcode: {item.get('barcode')}, Image URL: {item.get('image_url')}")
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    test_recommend_endpoint()
