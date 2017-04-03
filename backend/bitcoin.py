#!/usr/bin/python
import requests,threading

TBTC_UTXO = "https://api.blocktrail.com/v1/tBTC/address/%s/transactions.csv?limit=200&api_key=CSV_EXPORT"

watch_list = {}
threads = {}
def init():
    threads["api_thread"] = threading.Thread(target="api_daemon")
    threads["watch_thread"] = threading.Thread(target="watch_daemon")
    threads["api_thread"].start()
    threads["watch_thread"].start()

def api_daemon():
    #Expose endpoint

def watch_daemon():
    #always watch the watchlist and notify if complete.

def create_new_tbtc_address():
    return ""

def add_watch(address,callback):
    watch_list[address] = callback


def stop():
    threads["api_thread"].stop()
