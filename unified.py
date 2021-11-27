#UNIFIED
import json
import asyncio
import websockets


class request(object):
    def __init__(self,n):
        self.nn=["Ping",                #0
                         "AuthenticateUser",    #1
                         "SubscribeTrades",     #2
                         "SubscribeLevel2",     #3
                         "SendOrder",           #4
                         "SendOrder",           #5
                         "GetOrderStatus", #6
                         "CancelOrder",       #7
                         "GetAccountTrades"]    #8

        self.oo=["",                    #0
                         "OMSId",               #1
                         "UserId",              #2
                         "Permissions",         #3
                         "AccountId",           #4
                         "Depth",               #5
                         "APIKey",              #6
                         "Nonce",               #7
                         "Signature",           #8
                         "InstrumentId",        #9
                         "IncludeLastCount",    #10
                         "ClientOrderId",       #11
                         "Quantity",            #12
                         "DisplayQuantity",     #13
                         "UseDisplayQuantity",  #14
                         "LimitPrice",          #15
                         "OrderIdOCO",          #16
                         "OrderType",           #17
                         "PegPriceType",        #18
                         "InstrumentId",        #19
                         "TrailingAmount",      #20
                         "LimitOffset",         #21
                         "Side",                #22
                         "StopPrice",           #23
                         "TimeInForce",         #24
                         "OrderId"]             #25
        self.serial={}
        self.n = n
        
    def send(self,m,i,o,p):
        self.frame = {
                "m":m,
                "i" : i,
                "n":self.nn[self.n],
                "o":""
                }
        self.load={}                
        for i in range(len(o)):
            self.load[self.oo[o[i]]]=p[i]
        self.frame["o"]=json.dumps(self.load)
        self.serial=json.dumps(self.frame)
        #print(self.serial)
        return self.serial
        
    def receive(self,message):
        self.messages=json.loads(message)
        if self.messages["i"]==1:
            if self.messages["n"]==self.nn[self.n]:
                self.info = json.loads(self.messages["o"])
                return self.info


    
class communication(object):
        def __init__(self):
                self.read=[]

        async def intro(uri,message,select):
            async with websockets.connect(uri) as ws:
                read = []
                nn=["Ping",                #0
                         "AuthenticateUser",    #1
                         "SubscribeTrades",     #2
                         "SubscribeLevel2",     #3
                         "SendOrder",           #4
                         "SendOrder",           #5
                         "GetOrderStatus", #6
                         "CancelOrder",       #7
                         "GetAccountTrades"]    #8
                for i in range(len(message)):
                    await ws.send(message[i])
                    t = await ws.recv()
                    h=json.loads(t)
                    try:
                        readable=json.loads(h["o"])
                        reply = json.dumps(readable,indent=4)
                        #print(reply)
                        if h["n"] == str(nn[select]):
                            read.append(readable)
                            return read
                    except Exception as err:
                        if h["n"] == str(nn[select]):
                            print(err)
                        else:
                            print(json.dumps(h,indent=4))
                            print(err)

        def subscribe_trades(arg):
            ret = asyncio.get_event_loop().run_until_complete(arg)
            cont_1= ret[0]
            cont_2=[]
            for i in range(len(cont_1)):
                cont_2.append(cont_1[i][3])
            return cont_2
        def subscribe_level2(arg,side):
            ret = asyncio.get_event_loop().run_until_complete(arg)
            if side == "buy":
                group0 = ret[0]
                group1 = group0[1]
                price = group1[6]
                return price
            if side == "sell":
                group0 = ret[0]
                group1 = group0[0]
                price = group1[6]
                return price

        def send_order(arg):
            ret = asyncio.get_event_loop().run_until_complete(arg)
            dictionary = ret[0]
            listings = list(dictionary.values())
            output = []
            for i in range(len(listings)):
                if i == 0 or i == 2:
                   output.append(listings[i]) 
            return output

        def order_status(arg):
            ret = asyncio.get_event_loop().run_until_complete(arg)
            dictionary = ret[0]
            listings = list(dictionary.values())
            output = []
            for i in range(len(listings)):
                if i == 1 or i == 8:
                   output.append(listings[i]) 
            return output

        def cancel_order(arg):
            ret = asyncio.get_event_loop().run_until_complete(arg)
            dictionary = ret[0]
            listings = list(dictionary.values())
            output = listings[0] 
            return output

        def Authenticate_User(arg):
            ret = asyncio.get_event_loop().run_until_complete(arg)
            return ret

"""
hmac_example.py

Sign a request using an API_KEY and an API_SECRET.
"""
import hashlib
import hmac
import time

def get_nonce():
    """Return a nonce based on the current time.
  
    A nonce should only use once and should always be increasing.
    Using the current time is perfect for this.
    """
    # Get the current unix epoch time, and convert it to milliseconds
    return int(time.time() * 1e6)

  
def sign_request(userId, nonce):
    r = "data.txt"
    o = open(r)
    api_data = o.read()
    s= api_data.split("\n")
    API_KEY = s[0]
    API_SECRET = s[1]
    o.close()
    """Return an HMAC signature based on the request."""
    message = str(nonce) + userId + API_KEY
   
    return str(
        hmac.new(
            API_SECRET.encode('ascii'),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
    )

# functions:
#       0-ping
#       1-authenticate account
#       2-request market price
#       3-request requested price on order book
#       4-send order(buy)
#       5-send order(sell)
#       6-get order status
#       7-cancel order
def process_request(function,side="buy",order_ID=999,):
    while True:
        try:
            raw = "data.txt"
            op = open(raw)
            api_data = op.read()
            sp= api_data.split("\n")
            API_KEY = sp[0]
            API_SECRET = sp[1]
            buy_quantity = sp[2]
            sell_quantity = sp[3]
            op.close()
            nonce = get_nonce()
            ky = API_KEY
            sig = sign_request('113273',nonce)
            f = request(1)
            hi = request(function)

            o = [
                [],         #0
                [2,6,7,8],  #1
                [1,9,10],   #2
                [1,9,5],    #3
                [1,4,11,14,12,13,17,19,22,24],         #4
                [1,4,11,14,12,13,17,19,22,24],         #5
                [1,4,25],         #6
                [1,4,25],         #7
                [0],        #8
                [1,4],      #9
                []          #10
                ]

            p = [
                [],         #0
                ['113273',ky,str(nonce),sig], #1
                [1,6,1],    #2
                [1,6,1],    #3
                [1,113313,888,False,buy_quantity,0,1,6,0,1],         #4
                [1,113313,888,False,sell_quantity,0,1,6,1,1],         #5
                [1,113313,order_ID],         #6
                [1,113313,order_ID],         #7
                [""],       #8
                [1,113313], #9
                [1,6,100]   #10
                ]

            authenticate = f.send(0,0,o[1],p[1])
            g = hi.send(0,2,o[function],p[function])
            msg = [authenticate,g]
            mm = communication.intro('wss://api.coins.asia/WSGateway/',msg,function)

            if function == 1:
                ret_data = communication.Authenticate_User(mm)
                #print(ret_data)
                return ret_data
            if function == 2:
                ret_data = communication.subscribe_trades(mm)
                return ret_data
            if function == 3:
                ret_data = communication.subscribe_level2(mm,side)
                print(ret_data)
                return ret_data
            if function == 4 or function == 5:
                ret_data = communication.send_order(mm)
                return ret_data
                print(ret_data)
            if function == 6:
                ret_data = communication.order_status(mm)
                return ret_data
                print(ret_data)
            if function == 7:
                ret_data = communication.order_status(mm)
                return ret_data
                print(ret_data)

        except IndexError as err:
            buy_price = int(input("Input price of quantity you want to buy: "))
            sell_price = int(input("Input price of quantity you want to sell: "))
            #sending module for orderbook price
            hi = request(3)
            g = hi.send(0,0,[1,9,5],[1,6,1])
            msg = [g]
            mm = communication.intro('wss://api.coins.asia/WSGateway/',msg,3)
            ret_databuy = communication.subscribe_level2(mm,"buy")
            mmm = communication.intro('wss://api.coins.asia/WSGateway/',msg,3)
            ret_datasell = communication.subscribe_level2(mmm,"sell")
            #print(ret_databuy)
            
            #append the data.txt
            raw = "data.txt"
            op = open(raw,'a+')
            qty1 = str(buy_price/ret_databuy)
            qty2 = str(sell_price/ret_datasell)
            op.write(qty1 + "\n")
            op.write(qty2 + "\n")
            op.close()

##RUN
#pr = process_request(1)
#print(pr)

def collect_data(n_samples=3):
    prices=process_request(2)
    latest_price= prices[len(prices)-1]
    samples=[]
    for u in range(n_samples):
        samples.append(prices[len(prices)-(1+u)])
    #print(samples,latest_price)
    return samples

def orderbook_price(side):
    prices = process_request(3,side = str(side))
    return prices
    #print(prices)

def process_data(samples=0,threshold=10,side="buy",recent=None,
                 wanted_price=None):
    percent_factor = 0.01 * threshold
    present_price=samples
    if recent == None:
        if wanted_price == None:
            wanted_price = input("enter the price where you want to buy,current price is "+str(present_price)+": ")
            return ['wait','buy',None,float(wanted_price)]
        else:
            if wanted_price >= present_price:
                return ['buy','sell',float(present_price),float(present_price)]
            else:
                return ['wait','buy',None,float(wanted_price)]
    else:
        recent_percentage = percent_factor * wanted_price
        if side == 'buy':
            difference = wanted_price - present_price
            if recent_percentage <= difference:
                return ['buy','sell',float(present_price),float(present_price)]
            else:
                return ['wait','buy',float(present_price),float(wanted_price)]
        else:
            difference = present_price - wanted_price
            if recent_percentage <= difference:
                return ['sell','buy',float(present_price),float(present_price)]
            else:
                return ['wait','sell',float(present_price),float(wanted_price)]



def confirm_action(command):
    if command == 'wait':
        return command
    elif command == 'buy':
        loop = 0
        while True:
            request = process_request(4,side=command)
            loop = loop + 1
            print(loop,request)
            if loop == 5:
                return "no funds"
                #print("no money")
            if request[0] == "Accepted":
                while True:
                    stat = process_request(6,order_ID=request[1])
                    #print(stat)
                    if stat[1] == "FullyExecuted":
                        break
                break
            
    elif command == 'sell':
        loop = 0
        while True:
            request = process_request(5,side=command)
            loop = loop + 1
            print(loop,request)
            if loop == 5:
                return "no funds"
                #print("no money")
            if request[0] == "Accepted":
                while True:
                    stat = process_request(6,order_ID=request[1])
                    #print(stat)
                    if stat[1] == "FullyExecuted":
                        break
                break

def analyzer_1(default_threshold=3,present_price=0,recent_price=None,
               trade_price=0,present_max=0,threshold_on_max=5,side='buy'):
    if recent_price == None:
        return [default_threshold,present_max]
    else:
        if side == 'buy':
            threshold = ((trade_price-present_price)/(0.01*trade_price))+0.01
            threshold_trigger = ((trade_price-present_price)/(0.01*trade_price))-0.01
            threshold_max = threshold_on_max * (trade_price - present_max) * 0.01
            difference_trend = present_price - present_max
            if trade_price <= present_price:
                return [default_threshold,trade_price]
            else:
                if recent_price > present_price:
                    return [threshold,present_price]
                elif recent_price < present_price:
                    if threshold_max <= difference_trend:
                        return [threshold_trigger,trade_price]
                    else:
                        return [threshold,present_max]
                elif recent_price == present_price:
                    return [default_threshold,present_max]

        elif side == 'sell':
            threshold = ((present_price-trade_price)/(0.01*trade_price))+0.01
            threshold_trigger = ((present_price-trade_price)/(0.01*trade_price))-0.01
            threshold_max = threshold_on_max * (present_max - trade_price) * 0.01
            difference_trend = present_max - present_price
            if trade_price >= present_price:
                return [default_threshold,trade_price]
            else:
                if recent_price < present_price:
                    return [threshold,present_price]
                elif recent_price > present_price:
                    if threshold_max <= difference_trend:
                        return [threshold_trigger,trade_price]
                    else:
                        return [threshold,present_max]
                elif recent_price == present_price:
                    return [default_threshold,present_max]


th=3
maxx=0
sid='buy'
rec=None
wp=None

while True:
#will check first for api key
    try:
        data_file = open("data.txt")
        break
#If there is no api key data it will prompt the user to enter api data and save it
    except Exception as ex:
        api_key = str(input("enter API KEY: "))
        api_secret = str(input("enter API SECRET: "))
        data_file = open("data.txt","w")
        data_file.write(api_key + "\n")
        data_file.write(api_secret + "\n")
        data_file.close()

#exception will raise if credentials are incorrect
while True:
    try:
        #process loop
        while True:
            p = orderbook_price(sid)
            #p=float(input('enter price: '))
            price = p

        #initial price analyzer for threshold determination for process
            aa = analyzer_1(present_price=price,recent_price=rec,trade_price=wp,
                  present_max=maxx,side=sid)
        #variable assignation from analyzer 
            th = aa[0]
            maxx = aa[1]
            #print("analyzer output:",aa)

        #process computation
            l = process_data(samples=price,side=sid,recent=rec,wanted_price=wp,
                   threshold=th)
#variable assignation for return loop 
            sid = l[1]
            rec = l[2]
            wp = l[3]
            ret = l[0]
            print(ret,sid,rec,wp)

#loop interruptor, external commander
            action = confirm_action(ret)
            if action == "no funds":
                break
        print("loop has broken"+"\n"+"you have "+action)
        break

    except TypeError as ex:
        api_key = str(input("wrong credentials, enter API KEY: "))
        api_secret = str(input("enter API SECRET: "))
        data_file = open("data.txt","w")
        data_file.write(api_key + "\n")
        data_file.write(api_secret + "\n")
        data_file.close()
        sid = 'buy'
