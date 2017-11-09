import json


with open('../data/reviews.json', 'r') as f:
    data = json.load(f)

    with open('../data/reviews_pretty.json', 'w') as w:
        w.write(json.dumps(data, indent=2))
