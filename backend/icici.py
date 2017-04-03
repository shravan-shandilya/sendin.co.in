#!/usr/binpython
import requests

ICICI_AUTH = "https://corporateapiprojectwar.mybluemix.net/corporate_banking/mybank/authenticate_client?client_id=%s&password=%s"
ICICI_DATA_MAPPER = "https://retailbanking.mybluemix.net/banking/icicibank/participantmapping?client_id=%s"
ICICI_CREATE_VPA = "https://upiservice.mybluemix.net/banking/icicibank/createVPA?client_id=%s&token=%s&accountNo=%s&vpa=%s"

token = ""
data_map = None
client_id = ""
vpa_dict = {}

def auth_init(iden,password):
    global client_id
    client_id = iden
    resp = requests.get(ICICI_AUTH%(iden,password))
    if resp.status_code == 200:
        global token
        token = resp.json()[0]['token']
        return True
    else:
        return False

def map_data(iden):
    resp = requests.get(ICICI_DATA_MAPPER%(iden))
    if resp.status_code == 200:
        global data_map
        data_map = resp.json()
        return True
    else:
        return False

def init(iden,password):
    if(not auth_init(iden,password)):
        print "Auth failed!"

    if(not map_data(iden)):
        print "Data map failed!"

def create_vpa(vpa):
    if not vpa.endswith("@icicibank"):
        return False
    resp = requests.get(ICICI_CREATE_VPA%(client_id,token,data_map[0]['account_no'],vpa))
    if resp.status_code == 200:
        vpa_dict[data_map[0]['account_no']] = vpa
        return True
    else:
        return False
