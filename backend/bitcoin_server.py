#!/usr/bin/python
from flask import Flask, url_for
from bitcoinlib.wallets import HDWallet
import time,random,string,requests,json,threading,icici
app = Flask(__name__)

watch_list = {}
completed_list = []
watch_daemon = None
wallet = HDWallet.create(name=time.ctime(),network='testnet')
json_data=open("credentials.json").read()
creds = json.loads(json_data)
icici.init(creds['id'],creds['pass'])

@app.route('/newaddress')
def new_address():
    return '{"address":"%s"}'%(wallet.new_account().address)

@app.route('/watch/<address_amount>')
def api_article(address_amount):
    address = address_amount.split("_")[0]
    amount_btc = address_amount.split("_")[1]
    amount_inr = address_amount.split("_")[2]
    token = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))
    watch_list[token]= {}
    watch_list[token]["address"] = address
    watch_list[token]["amount_btc"] = amount_btc
    watch_list[token]["amount_inr"] = amount_inr
    return '{"token":"%s"}'%(token)

@app.route('/status/<token>')
def send_status(token):
    if token == "test":
        return '{"status":"true","amount":"500"}'
    if token in completed_list:
        return '{"status":"true","amount":"%s"}'%(watch_list[token]["amount_inr"])
    try:
        resp = requests.get("http://tbtc.blockr.io/api/v1/address/info/%s"%(watch_list[token]['address']))
        data = json.loads(resp.text)['data']
        if (int(data["nb_txs"]) > 0 ) & (float(data["balance"]) >= float(watch_list[token]["amount_btc"])):
            completed_list.append(token)
            return '{"status":"true","amount":"%s"}'%(watch_list[token]["amount_inr"])
        else:
            return '{"status":"false"}'
    except KeyError:
            return '{"status":"false"}'

@app.route('/upi/<token_upi_amount>')
def send_in_upi(token_upi_amount):
    token_upi_amount = str(token_upi_amount)
    token = token_upi_amount.split("_")[0]
    upi = token_upi_amount.split("_")[1]
    amount = token_upi_amount.split("_")[2]
#    if token in completed_list:
    #watch_list[token]["upi"] = upi
    receipt = icici.pay(upi,amount)
    print receipt
    if receipt[0] :
        return '{"status":"true","receipt":"%s"}'%(receipt[1])
    else:
        return '{"status":"false"}'
#    else:
#            return '{"status":"false"}'


@app.route('/upi_status/<receipt>')
def send_upi_status(receipt):
    return '{"status":"true"}'

def watch_daemon():
    while True:
        print "Inside daemon"
        for watch in watch_list:
            data = json.loads(request.get("http://tbtc.blockr.io/api/v1/address/info/%s"%(watch['address'])))
            print data
            if data["nb_txs"] > 0 & data["balance"] >= watch["amount"]:
                completed_list.append(watch["token"])
        time.sleep(3)


if __name__ == '__main__':
    app.run()
    #watch_daemon = threading.Thread(target='watch_daemon')
    #watch_daemon.start()
