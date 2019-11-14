#!/usr/bin/env python3
#coding=utf-8 

import argparse
import http.client, urllib.parse
import time
import json
import random
from base64 import b64encode

parser = argparse.ArgumentParser(description='')
parser.add_argument('-host', default=None,
                      help='rpc host')
parser.add_argument('-rpcuser', default=None,
                      help='rpc user')
parser.add_argument('-rpcpassword', default=None,
                      help='rpc password')
parser.add_argument('-count', default=0,
                      help='gen count')
parser.add_argument('-time', default=600,
                      help='gen time')
args = parser.parse_args()
userAndPass = b64encode("{}:{}".format(args.rpcuser,args.rpcpassword).encode('utf-8')).decode("ascii")

def getnewaddress():
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "getnewaddress","params": ["","legacy"],"id": {}}}'.format(int(time.time()))
    conn.request("POST","",body,{"Content-Type":"application/json",'Authorization' : 'Basic %s' %  userAndPass})
    resp = conn.getresponse()
    if resp.status != 200:
        print("{} | getnewaddress error".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return None
    data = resp.read().decode()
    print("{} | getnewaddress result: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),data))
    data = json.loads(data)
    conn.close()
    return data["result"]

def generatetoaddress(nblocks,address,maxtries,coinbase):
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "generatetoaddress","params": [{},"{}",{},"{}"],"id": {}}}'.format(nblocks,address,maxtries,coinbase,int(time.time()))
    print(coinbase)
    conn.request("POST","",body,{"Content-Type":"application/json",'Authorization' : 'Basic %s' %  userAndPass})
    resp = conn.getresponse()
    if resp.status != 200:
        print("{} | generatetoaddress error".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return None
    data = resp.read().decode()
    print("{} | generatetoaddress result: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),data))
    data = json.loads(data)
    conn.close()
    return data


def main():
    addr = getnewaddress()
    pools = ["2/1THash&58COIN/","/Huobi/3","234/HotPool/34","rew/E2M & BTC.TOP/e","32fdxbtc.exx.com&bw.com45fgg"]
    count = int(args.count)
    if count == 0:
        count = 0xFFFFFFFF
    t = int(args.time)
    for _ in range(count):
        generatetoaddress(1,addr,0x7FFFFFFF,pools[random.randint(0,len(pools)-1)])
        time.sleep(t)


if __name__ == '__main__':
  main()