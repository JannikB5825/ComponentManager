import requests
import json

re = requests.get('https://wmsc.lcsc.com/wmsc/product/detail?productCode=C49274')
print(json.loads(re.text)["result"]["productModel"])