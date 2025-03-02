import json
import requests
import os

list_product_id = "/Users/austin/Desktop/Projects/REST API/.venv/data/products-0-200000(in).csv"
output_folder = "/Users/austin/Desktop/Projects/REST API/.venv/data"
list_prd = []

with open(list_product_id, "r") as id_file:
    next(id_file)
    for line in id_file:
        product_id = line.strip()
        list_prd.append(product_id)

responses = []
index = 1
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

for i in range(len(list_prd)):
    url = f"https://api.tiki.vn/product-detail/api/v1/products/{list_prd[i]}"
    res = requests.get(url, headers=headers)
    print(f"Fetching Product ID: {list_prd[i]}, Status Code: {res.status_code}")

    if res.status_code == 200 and res.text.strip():
        if res.headers.get('Content-Type', '').startswith('application/json'):
            response_data = res.json()
            responses.append(response_data)
        else:
            print(f"Unexpected content type for Product ID: {product_id}")
    else:
        print(
            f"Failed request for Product ID: {product_id}, Status Code: {res.status_code}, Response: {res.text.strip()}")

    if len(responses) == 1000:
            filename = os.path.join(output_folder, f"product{index}.json")
            with open(filename, "w") as file:
                json.dump(responses, file, indent = 4)
            responses = []
            index += 1

if responses:
    filename = os.path.join(output_folder, f"response_{index}.json")
    with open(filename, "w") as file:
        json.dump(responses, file, indent=4)