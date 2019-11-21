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

def dumpprivkey(addr):
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "dumpprivkey","params": ["{}"],"id": {}}}'.format(addr,int(time.time()))
    conn.request("POST","",body,{"Content-Type":"application/json",'Authorization' : 'Basic %s' %  userAndPass})
    resp = conn.getresponse()
    if resp.status != 200:
        print("{} | dumpprivkey error".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return None
    data = resp.read().decode()
    print("{} | dumpprivkey result: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),data))
    data = json.loads(data)
    conn.close()
    return data["result"]

def generatetoaddress(nblocks,address,maxtries,coinbase):
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "generatetoaddress","params": [{},"{}",{},"{}"],"id": {}}}'.format(nblocks,address,maxtries,coinbase,int(time.time()))
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

def gettime(block):
    t = 0
    if int(block / 100) & 1 == 0:
        t = random.randint(1*60,2*60)
    else:
        t = random.randint(11*60,15*60)
    return t

miner_count = 5
addr_count = 5

def main():
    addrpool = []
    for i in range(25):
        addr = getnewaddress()
        key = dumpprivkey(addr)
        addrpool.append([addr,key])

    for v in addrpool:
        print("addr: {}  key: {}".format(v[0],v[1]))
    
    pools = ["2/1THash&58COIN/","/Huobi/3","234/HotPool/34","rew/E2M & BTC.TOP/e","32fdxbtc.exx.com&bw.com45fgg"]
    count = int(args.count)
    if count == 0:
        count = 0xFFFFFFFF
    for i in range(count):
        r = random.randint(0,len(pools)-1)
        addr = addrpool[r*5+random.randint(0,addr_count-1)][0]
        generatetoaddress(1,addr,0x7FFFFFFF,pools[r])
        time.sleep(gettime(i))


if __name__ == '__main__':
  main()