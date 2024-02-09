import requests
import settings

class User:
    def __init__(self,bet_amount=100):
        self.is_loged_in=False
        self.bet_amount=bet_amount

    def is_logged(self):
        return self.is_loged_in
    

    def login(self,username,password):
        if self.is_loged_in:
            return False
        response=requests.post(settings.LOGIN_ENDPOINT_URL,data={"username":username,"password":password})
        json_data=response.json()
        if  response.status_code != 200:
            return False
        self.authorization_header ="Token "+ json_data["token"]
        self.balance = json_data["user"]["balance"]
        self.name = json_data["user"]["username"]
        self.is_loged_in=True
        return True


    def register(self,username,password):
        response=requests.post(settings.REGISTER_ENDPOINT_URL,data={"username":username,"password":password})

        return response.status_code == 200

    def get_authorization_header(self):
        return self.authorization_header
    

    def deposit(self,amount):
        if self.is_loged_in==False:
            return 0
        
        response=requests.post(settings.DEPOSIT_ENDPOINT_URL,headers={"Authorization":self.get_authorization_header()},data={"amount":amount})
        json_data=response.json()
        self.balance=json_data["balance"]
        return json_data["balance"]