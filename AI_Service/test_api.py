import requests

url = "http://127.0.0.1:8000/predict"

image_path = "test.jpg"

with open(image_path, "rb") as f:
    response = requests.post(url, files={"file": f})

print("Status code:", response.status_code)
print("Response JSON:", response.json())