import json

import requests

# Test query
query = {"message": "Hola, quiero saber los beneficios de la tarjeta de débito"}

response = requests.post("http://localhost:8000/chat", json=query)
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
