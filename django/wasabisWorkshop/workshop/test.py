
from rest_framework.response import Response
from requests import Request, post

response = post(
    url='http://127.0.0.1:8000/workshop/signup/',
    data={
        'email': 'dave@dave.dave',
        'name': 'dave',
                'password': 'dave',
    },
).json()
print(response)
