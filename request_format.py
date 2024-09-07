import requests

url = "http://localhost:5000/chat"
data = {"question": "What is the capital of France?"}
response = requests.post(url, json=data)
print(response.json())


# Test it out on Postman via cURL

# curl -X POST \
#   http://localhost:5000/chat \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "question": "What is the capital of France?"
# }'