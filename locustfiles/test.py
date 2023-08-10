from locust import HttpUser,task
import random
import copy
import json

with open("raw_datas.json","r") as json_file:

    raw_datas=json.load(json_file)
data_len =len(raw_datas)

headers= {'content-type':'application/json'}

data_len =len(raw_datas)-1

def get_request_body():
    data_num = random.randint(0,data_len)
    input_data= raw_datas[data_num]
    template={
        "id":input_data

    }
    return copy.deepcopy(template)

class websiteUser(HttpUser):

    @task(1)
    def test1(self):
        body = get_request_body()
        self.client.post("/test",data=json.dumps(body),headers=headers)
