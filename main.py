from utils import get_query_engine
import json

query_engine = get_query_engine("handbook.pdf")


inputs = ["who is the president of India?","What is the name of the company?","Who is the CEO of the company?","What is their vacation policy?","What is the termination policy?"]
response = {}
for i in inputs:
    response[i] = query_engine.query(i).response

with open("response.json", "w") as f:
    json.dump(response,f,indent=2)