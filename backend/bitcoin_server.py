#!/usr/bin/python
from flask import Flask, url_for
from bitcoinlib.wallets import HDWallet
import time,random,string,requests,json,threading
app = Flask(__name__)

watch_list = {}
completed_list = []
watch_daemon = None
wallet = HDWallet.create(name=time.ctime(),network='testnet')

@app.route('/newaddress')
def new_address():
    return '{"address":"%s"}'%(wallet.new_account().address)

@app.route('/watch/<address_amount>')
def api_article(address_amount):
    address = address_amount.split("_")[0]
    amount = address_amount.split("_")[1]
    token = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))
    watch_list[token]= {}
    watch_list[token]["address"] = address
    watch_list[token]["amount"] = amount
    return '{"token":"%s"}'%(token)

@app.route('/status/<token>')
def send_status(token):
    resp = requests.get("http://tbtc.blockr.io/api/v1/address/info/%s"%(watch_list[token]['address']))
    data = json.loads(resp.text)['data']
    if (int(data["nb_txs"]) > 0 ) & (float(data["balance"]) >= float(watch_list[token]["amount"])):
        return '{"status":"true"}'
    else:
        return '{"status":"false"}'

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
