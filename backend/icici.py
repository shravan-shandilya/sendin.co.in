#!/usr/binpython
import requests,string,random

ICICI_AUTH = "https://corporateapiprojectwar.mybluemix.net/corporate_banking/mybank/authenticate_client?client_id=%s&password=%s"
ICICI_DATA_MAPPER = "https://retailbanking.mybluemix.net/banking/icicibank/participantmapping?client_id=%s"
ICICI_CREATE_VPA = "https://upiservice.mybluemix.net/banking/icicibank/createVPA?client_id=%s&token=%s&accountNo=%s&vpa=%s"
ICICI_SEND_VIA_UPI = "https://upiservice.mybluemix.net/banking/icicibank/upiFundTransferVToV?client_id=%s&token=%s&payerCustId=%s&payerVPA=%s&payeeVPA=%s&amount=%s&remarks=%s"

token = ""
data_map = None
client_id = ""
vpa_dict = {}
payer_vpa = ""
payer_account = ""

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
    global payer_vpa,payer_account
    payer_vpa = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))+"@icicibank"
    payer_account = data_map[0]['cust_id']
    create_vpa(payer_vpa)

def create_vpa(vpa):
    if not vpa.endswith("@icicibank"):
        return False
    resp = requests.get(ICICI_CREATE_VPA%(client_id,token,data_map[0]['account_no'],vpa))
    if resp.status_code == 200:
        vpa_dict[data_map[0]['account_no']] = vpa
        return True
    else:
        return False

def create_recipient_vpa(vpa):
        if not vpa.endswith("@icicibank"):
            return False
        resp = requests.get(ICICI_CREATE_VPA%(client_id,token,data_map[2]['account_no'],vpa))
        if resp.status_code == 200:
            vpa_dict[data_map[2]['account_no']] = vpa
            return True
        else:
            return False

def pay(payee_vpa,amount):
    create_recipient_vpa(payee_vpa)
    query = ICICI_SEND_VIA_UPI%(client_id,token,payer_account,payer_vpa,payee_vpa,amount,"Sent via sendin.co.in")
    resp = requests.get(query)
    print resp.json()
    if (resp.status_code == 200) and (resp.json()[1]['status'] == "SUCCESS"):
        return (True,resp.json()[1]["transaction_id"])
    else:
        return False
