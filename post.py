data = [{"age": 17,
        "job": "blue-collar",
        "marital": "married",
        "education": "tertiary",
        "default": "no",
        "balance": 3050,
        "housing": "yes",
        "loan": "yes",
        "contact": "unknown",
        "day": 3,
        "month": "may",
        "campaign": 1,
        "pdays": 999,
        "poutcome": "failure",
        "previous": 0,
        }]

import requests
res = requests.post('http://localhost:8000/api/predict', json=data)
if res.ok:
    print(res.json())