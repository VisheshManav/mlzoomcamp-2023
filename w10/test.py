import requests

data = {'url': 'http://bit.ly/mlbookcamp-pants'}

result = requests.post('http://localhost:9696/predict', json=data).json() 

print(result)