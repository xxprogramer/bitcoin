#!/usr/bin/env python3
# coding=utf-8

import argparse
import http.client
import urllib.parse
import time
import json
import random
from base64 import b64encode
import threading

json.encoder.FLOAT_REPR = lambda x: format(x, '.8f')
parser = argparse.ArgumentParser(description='')
parser.add_argument('-host', default=None,
                    help='rpc host')
parser.add_argument('-rpcuser', default=None,
                    help='rpc user')
parser.add_argument('-rpcpassword', default=None,
                    help='rpc password')
parser.add_argument('-count', default=0,
                    help='gen count')
parser.add_argument('-time', default=0,
                    help='gen time')
parser.add_argument('-tx_time', default=240,
                    help='gen tx time')
parser.add_argument('-send', default=0,
                    help='send asimov tx')
args = parser.parse_args()
userAndPass = b64encode("{}:{}".format(
    args.rpcuser, args.rpcpassword).encode('utf-8')).decode("ascii")
print(userAndPass)

def getnewaddress():
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "getnewaddress","params": ["","legacy"],"id": {}}}'.format(
        int(time.time()))
    conn.request("POST", "", body, {
                 "Content-Type": "application/json", 'Authorization': 'Basic %s' % userAndPass})
    resp = conn.getresponse()
    data = resp.read().decode()
    if resp.status != 200:
        print("{} | getnewaddress error,data: {}".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
        return None
    print("{} | getnewaddress result: {}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
    data = json.loads(data)
    conn.close()
    return data["result"]


def dumpprivkey(addr):
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "dumpprivkey","params": ["{}"],"id": {}}}'.format(
        addr, int(time.time()))
    conn.request("POST", "", body, {
                 "Content-Type": "application/json", 'Authorization': 'Basic %s' % userAndPass})
    resp = conn.getresponse()
    data = resp.read().decode()
    if resp.status != 200:
        print("{} | dumpprivkey error,data: {}".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
        return None

    print("{} | dumpprivkey result: {}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
    data = json.loads(data)
    conn.close()
    return data["result"]


def importprivkey(key):
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "importprivkey","params": ["{}"],"id": {}}}'.format(
        key, int(time.time()))
    conn.request("POST", "", body, {
                 "Content-Type": "application/json", 'Authorization': 'Basic %s' % userAndPass})
    resp = conn.getresponse()
    data = resp.read().decode()
    if resp.status != 200:
        print("{} | importprivkey error,data: {}".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
        return None
    print("{} | importprivkey result: {}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
    data = json.loads(data)
    conn.close()
    return data


def generatetoaddress(nblocks, address, maxtries, coinbase):
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "generatetoaddress","params": [{},"{}",{},"{}"],"id": {}}}'.format(
        nblocks, address, maxtries, coinbase, int(time.time()))
    conn.request("POST", "", body, {
                 "Content-Type": "application/json", 'Authorization': 'Basic %s' % userAndPass})
    resp = conn.getresponse()
    data = resp.read().decode()
    if resp.status != 200:
        print("{} | generatetoaddress error,,data".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
        return None
    print("{} | generatetoaddress result: {}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
    data = json.loads(data)
    conn.close()
    return data


def listunspent(addrs):
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "listunspent","params": [{},{},{}],"id": {}}}'.format(
        100, 0x7FFFFFFF, json.dumps(addrs), int(time.time()))
    conn.request("POST", "", body, {
                 "Content-Type": "application/json", 'Authorization': 'Basic %s' % userAndPass})
    resp = conn.getresponse()
    data = resp.read().decode()
    if resp.status != 200:
        print("{} | listunspent error,data: {}".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
        return None
    print("{} | listunspent result: {}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
    data = json.loads(data)
    conn.close()
    return data["result"]


def createrawtransaction(inputs, outputs):
    conn = http.client.HTTPConnection(args.host)

    body = r'{{"jsonrp": "1.0","method": "createrawtransaction","params": [{},{}],"id": {}}}'.format(
        json.dumps(inputs), json.dumps(outputs), int(time.time()))
    # body.replace("1.234e-05","0.00001234")
    conn.request("POST", "", body, {
                 "Content-Type": "application/json", 'Authorization': 'Basic %s' % userAndPass})
    resp = conn.getresponse()
    data = resp.read().decode()
    if resp.status != 200:
        print("{} | createrawtransaction error,data: {},  send body: {}".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data, body))
        return None
    print("{} | createrawtransaction result: {}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
    data = json.loads(data)
    conn.close()
    return data["result"]


def signrawtransactionwithkey(hex, keys):
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "signrawtransactionwithkey","params": ["{}",{}],"id": {}}}'.format(
        hex, json.dumps(keys), int(time.time()))
    conn.request("POST", "", body, {
                 "Content-Type": "application/json", 'Authorization': 'Basic %s' % userAndPass})
    resp = conn.getresponse()
    data = resp.read().decode()
    if resp.status != 200:
        print("{} | signrawtransactionwithkey error,data :{}".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
        return None
    print("{} | signrawtransactionwithkey result: {}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
    data = json.loads(data)
    conn.close()
    return data["result"]["hex"]


def sendrawtransaction(hex):
    conn = http.client.HTTPConnection(args.host)
    body = r'{{"jsonrp": "1.0","method": "sendrawtransaction","params": ["{}"],"id": {}}}'.format(
        hex, int(time.time()))
    conn.request("POST", "", body, {
                 "Content-Type": "application/json", 'Authorization': 'Basic %s' % userAndPass})
    resp = conn.getresponse()
    data = resp.read().decode()
    if resp.status != 200:
        print("{} | sendrawtransaction error,resp: {} ,send body: {}".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data, body))
        return None
    print("{} | sendrawtransaction result: {}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data))
    data = json.loads(data)
    conn.close()
    return data["result"]


def makeasimovtx(pools, asimov_addr):
    addrs = []
    keys = []
    for v in pools:
        addrs.append(v[0])
        keys.append(v[1])
    unspents = listunspent(addrs)
    if len(unspents) == 0:
        return
    r = min(len(pools), len(unspents))
    inputs = unspents[:r]
    sum = 0
    for v in inputs:
        sum = sum + float(v["amount"])
    outputs = {}
    outputs[asimov_addr] = 0.00001234
    outputs[addrs[0]] = int((sum - 0.01) * 10000) / 10000
    hex = createrawtransaction(inputs, outputs)
    hex = signrawtransactionwithkey(hex, keys)
    return sendrawtransaction(hex)


miner_count = 5
addr_count = 5
addrpool = [
    ["n1zBZ4W7av1UYiHMmygizfDVwFx2CsAwRV",
        "cQBamwYCi1VxPJs3iW792oJ3cMzaxiRTeV1MBqQjSx7ssU1Tudhz"],
    ["n2sKqBfxwuuxXGQRPbcL2rLmqWom7hnBX1",
        "cQf3Ynv79vHMRC9dSa41EiRJYPnrmbRrCcEWPxpfF8jZPthHV8gc"],
    ["mmzT9tM4rqoieTKWo7iG7sHB1v6PNAKzEx",
        "cUdKskWFKNtFB7zsXKcNtZXGpnhgMQ7EiaiL8CRjSLiba51TuoPg"],
    ["myMg4EEsvZkCG6jePCfhwPNCzyM7UjMCqB",
        "cUm5AW8L8ybt49cXCt4xzembU71pRXFAwax4dRMT7v1WXvaDsyV1"],
    ["mpWbtgLnEADh7ZEmCXZyaSKx3rjCZE2KbS",
        "cVxn8QfuwSSv5eQ174An1tDyPpX2JtGenUQ1yRsBCdqjrGz2H9fM"],
    ["mvLhjerWCSbf5Qyzou2zvehFqQXyY2skP7",
        "cV47MYUbRKU1acWQzTZfov6kmaKTeGRDrKQHG4dNYk4vRksoEuFr"],
    ["muKLrjfkYZMfzFtpfEzyKWHtYSyeZ23skW",
        "cNhHpfwaT1eo6qL7iUfgkpJt3YozuC3gpDnDWPfpdfEdypcdJrEf"],
    ["n2H7T7ELRSPFAwRY2HDNK9vRqbfA7DJUjz",
        "cR2vp9YwXa2Jo4t2Gh9YZDJUunzY4k4z6wsdjsWbkGKDKnzsKbFD"],
    ["mvz3s31YY8oZPj2ELguuZ1fJVCuooLP5hb",
        "cVF8v19zg6nbaMxne4n9ZVQMzxfK53761aH5JWKR5z31QCQHWAgC"],
    ["n4nkozCwSZvNri8wrDhosCzksoeawjSNR9",
        "cT4gWcGKieDHsfnA2Hjkiiq8jDPiLuRvi245sANKqfvQhRb5HvbA"],
    ["mqLKvNuKrArWcXB8aoN6jSyjHvwTXPmvpr",
        "cNjacXUS3Sbb6G1v18PqrvX1sZQA2R8hybb1pnJkkTKcPh6T23tf"],
    ["n3yaZW1TNgn68o814ZChCV9jjuimg7EKSy",
        "cSRaf5Rat3JDkQqW2XA6amwYEbnjHoPaaKxqWGnF8LVtPmHJPZ2g"],
    ["n1E2xCx2SkNqpfTZLJMbinmmz46RpzEUps",
        "cPPzZK7mpMcUDvxfqb9QRCbAb5cNXqQeTgkrLFydJXyEp5wLEWNb"],
    ["musm3D8RL2QsPfUBs8MMJqfL3awHp48eUH",
        "cVxikfok4CGrptGtRTC8NJoTWtnvsiFDaKjCi9zDSsznhQNwy17E"],
    ["muDdeHtn97EYBavQgf2Tfp5kTXXkkLC6wR",
        "cVuATMgeviQUT5nCtMJkACVdpyMapht5ueA1BvMZgqoZ2q9Jgdkz"],
    ["n3EmX7t7a9LMkauSzeWYPaP3mntZvMKy11",
        "cSEANDU4YaoQCe5PnDs3AFxUC2pSQopF8P5CwVLhCxpqLv8HZ3ty"],
    ["mx1hDzqbNNMbgonhvuePJEkpNQ4Hg77Cy8",
        "cTV1p4zezs5UQs3USeBXSXu5uuarLPPVxFU6ytcW8zgKR5AS698P"],
    ["mnhwoDDravQUTKUT3xR7C18r3YLmbU9zUe",
        "cSrHrj3zGcMv2ow3ezKAP6e6jw9eeAa8Rzf813BpNNGvsrmMTe6F"],
    ["mut8cnX84kWQesCsvMeJmT1V8xVHRGDdWd",
        "cVe2k5Bngnh9JNseDYi8L2RftAaKeMidsotzCr399HGzEpopkpKs"],
    ["mzEzmUSqQ8hXtVQtbEtgq7C4crNjSMr3aS",
        "cQxyUoCZi1TzMRueLiLi4wqQeTP9cx4PCd1nT54bAzGW98AQ7U3S"],
    ["mmPm5w4HoDDmkvt9GxiUbavrr3BnvasTux",
        "cQZJXBrYpeE6pkH4xebA2GgAV4qWhwoabeqpwXLdiKRTfr96dnpM"],
    ["mx3LxVqzh1ke9FgoXCwMZhzqzhAXoGu2Vj",
        "cQPCLXgp2BPxBeHfwuUoYwUwqhf2tKoe6WfrnBQoAeMKf2oKJm6m"],
    ["msUteSN4rvbwSQEmrKcrDJ9uZhLEALSveT",
        "cVgMsmzQqfJEK3Z8az4x4WoogErEqXM9k9HvSL3acMZQhHNBSzMs"],
    ["mxhRNrCenzUnbZbvJU6MYoqRTTe6ysiccu",
        "cSkTKhG36swB9uLzFBSVmfbauaJjWgjMFDFR2tgJX7yNTWY66aAr"],
    ["muWVqQApdTXbiaY5ugz9qHJuCBjERerYrH",
        "cREBk8hgpRsdNzVAfoya3XU9b2k5Rw6iZYu13cjHX31Gf8v3GKux"],
]

asimove_addr = [
    ["mtGP4RbEndRKLJjJFQUTcAumEjTefo45sG",
     "cShhuRhRfnTVSdNyQNqySNdvG5ixEW8EM6fYXe5hUsoVciPGnmFn",
     "0x73e3d620dc4be4d5d99b08d1ccf810c58c11d88b",
        "0x98ca5264f6919fc12536a77c122dfaeb491ab01ed657c6db32e14a252a8125e3"],
    ["n2kUTtWS3nDbZ73fuPndd4BQfJJAJ8vztt",
     "cPyYLL5VsmSzKpsG9SMyMTfqJQeYyh1szXvZZXoDaBhFES8yDp5A",
     "0xc5201b984adf756a731557cb8c70de2ab63be9e8",
     "0x476c9b84ae64d263465152e91acb5f3076112f927a9c8dc8852ea67a9990f729"],
    ["mwpL7DmjbVUpwF3mkQSSUtcY68qCJBs82Q",
     "cN8KHMs8gGUVrgRiM4WiyMCis7sHb99i16fuoSU6EV9wVMq5Ch64",
     "0xc03e98c7fef0f04aaa546e4491a2a452eb4acbb2",
     "0x10437dafd473a7fc2c01fd205f3a3ab0b02558e85f24a01d129af26ca49822c0"],
    ["msPtCzzuM1ixoRtArWsgwQnv1jtk4M4fUs",
     "cVeR6pc3HsssoZMzAZRRtAm7uTAuR35rQFhpD8cRHdMJfqpFKUTw",
     "0xf0924de66fd3fcadc4664f3e9c7111fd972f4b82",
     "0xf09c331d8b4ee7c1df83d7d5fd7b9c27220157d14d5ba0c4c8c319e3850cd0a7"],
    ["dc1q3m7z6zy85x05m6fd482z4869xz3g2s3fsgmydy",
     "cQFbS9jEcD4BWERktvMnsb56PQrGg57FBCHb1ucmntPnvvhEyGJv",
     "",
     "0x4faec8e81ca587e19741f431ceda8012f909ff90881e377cef3e95af58000959"],
]


def gettime(block):
    t = 0
    if int(block / 100) & 1 == 0:
        t = random.randint(1*60, 2*60)
    else:
        t = random.randint(11*60, 15*60)
    return t


def asimovetx(addrpool):
    t = int(args.tx_time)
    while True:
        r = random.randint(0, miner_count * addr_count-1)
        rl = random.randint(1, 3)
        addr = getnewaddress()
        makeasimovtx(addrpool[r:min(r+rl, miner_count * addr_count)], addr)
        time.sleep(t)


def sendasimov():
    makeasimovtx([addrpool[0]], asimove_addr[0][0])
    makeasimovtx([addrpool[5]], asimove_addr[1][0])
    makeasimovtx([addrpool[10]], asimove_addr[2][0])
    makeasimovtx([addrpool[11]], asimove_addr[3][0])
    makeasimovtx([addrpool[24]], asimove_addr[4][0])


def main():

    # for i in range(miner_count * addr_count):
    #     addr = getnewaddress()
    #     key = dumpprivkey(addr)
    #     addrpool.append([addr, key])

    # for v in addrpool:
    #     print("addr: {}  key: {}".format(v[0], v[1]))

    for pair in addrpool:
        importprivkey(pair[1])

    if int(args.send) > 0:
        sendasimov()
        return

    #threading.Thread(target=asimovetx, args=(addrpool,)).start()

    pools = ["2/1THash&58COIN/", "/Huobi/3", "234/HotPool/34",
             "rew/E2M & BTC.TOP/e", "32fdxbtc.exx.com&bw.com45fgg"]
    count = int(args.count)
    if count == 0:
        count = 0xFFFFFFFF
    gen_thread = None
    for i in range(count):
        r = random.randint(0, miner_count * addr_count-1)
        addr = addrpool[r][0]
        pool = pools[int(r/addr_count)]

        t = int(args.time)
        if int(args.time) == 0:
            t = gettime(i)

        if gen_thread != None:
            gen_thread.join()
        gen_thread = threading.Thread(target=generatetoaddress, args=(
            1, addr, 0x7FFFFFFF, pool,))
        gen_thread.start()
        #generatetoaddress(1, addr, 0x7FFFFFFF, pool)

        time.sleep(t)


if __name__ == '__main__':
    main()
# 9135
