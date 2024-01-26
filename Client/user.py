import requests
import settings

class User:
    def __init__(self, username, password):
        self.initialize_user_data(username,password)


    def initialize_user_data(self,username,password):
        response=requests.post(settings.LOGIN_ENDPOINT_URL,data={"username":username,"password":password})
        json_data=response.json()
        print(json_data)
        self.authorization_header ="Token "+ json_data["token"]
        self.balance = json_data["user"]["balance"]
        self.name = json_data["user"]["username"]


    def get_authorization_header(self):
        return self.authorization_header
    

    def deposit(self,amount):
        response=requests.post(settings.DEPOSIT_ENDPOINT_URL,headers={"Authorization":self.get_authorization_header()},data={"amount":amount})
        json_data=response.json()
        print(json_data)
        self.balance=json_data["balance"]
        return json_data["balance"]