from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import requests
from tradingview_ta import TA_Handler, Interval, Exchange
import math
import time
import datetime
import requests
import logging
from binance.lib.utils import config_logging
from binance.cm_futures import CMFutures
client = Client("llz0nLG0mAooreP4EIiBV02jgTdFNMxjlhJyLqX3BdqIDzroU9pwr0Cz3F7wPQQm", "2ctEYBGIqZgPuCImCddMAgo9TleZ0mG3w7o5N5MmqCgzJkZmOG2li1GOiJBtIT90",)

cm_futures_client = CMFutures(key="llz0nLG0mAooreP4EIiBV02jgTdFNMxjlhJyLqX3BdqIDzroU9pwr0Cz3F7wPQQm", secret='2ctEYBGIqZgPuCImCddMAgo9TleZ0mG3w7o5N5MmqCgzJkZmOG2li1GOiJBtIT90')
asse=cm_futures_client.account()['assets']
config_logging(logging, logging.DEBUG)
#base_url='https://testnet.binancefuture.com'
#print(cm_futures_client.account()['assets'][btcpos])
leverage=5
response=None
response3=None
fabricacao=None

info = client.get_all_tickers()
df=pd.DataFrame(info)
df=df.set_index("symbol")
df["price"]=df["price"].astype("float")
df.index=df.index.astype("string")
baixo=0
cima=0
diasuteis=[0,1,2,3,4]

# Store the last order.
last_order = ''
posicao='buy'

# Instantiate TA_Handler.
handler = TA_Handler(
    symbol="ETHBUSD",
    exchange="binance",
    screener="crypto",
    interval="15m"
)
                                            
def te():
    response = requests.request("GET","https://fapi.binance.com")
    return(response.json())
def search():
    asse=cm_futures_client.account()['assets']
    print([x for x in asse if x['asset'] == ['ETH']])
def simbolo():
    asse=cm_futures_client.exchange_info()['symbols']
    keyValList=['ETHUSD_PERP']
    res=[d for d in asse if d['symbol'] in keyValList]
    return(float(res[0]['equalQtyPrecision']))

def saldodown():
    balance = client.get_asset_balance(asset='BUSD')
    return(print(balance))
def a():
    asse=client.futures_account()['assets']
    keyValList=['BUSD']
    res=[d for d in asse if d['asset'] in keyValList]
    return(float(res[0]['availableBalance']))#vezes5
def compra():
    #vezes1,005
    #return(client.futures_create_order(
    try:
        response = client.futures_create_order(
            symbol="ETHBUSD",
            side="SELL",
            type="MARKET",
            quantity=0.001,
            #timeInForce="GTC",
            #price=59808.0,
        )
        logging.info(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
#def venda():
    #vezes0,995
    #return(client.futures_create_order(
def liquida():
    #return(client.futures_liquidation_orders(
    try:
        response = client.futures_create_order(
            symbol="ETHBUSD",
            side="BUY",
            type="MARKET",
            quantity=1,
            reduceOnly=True,
            #timeInForce="GTC",
            #price=59808.0,
        )
        logging.info(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
def b():
    asse=client.futures_position_information()
    keyValList=['ETHBUSD']
    res=[d for d in asse if d['symbol'] in keyValList]
    if  float(res[0]['entryPrice'])>float(res[0]['liquidationPrice']):
        return('buy')
    elif  float(res[0]['entryPrice'])<float(res[0]['liquidationPrice']):
        return('sell')
    else:
        return('neutral')
def preco():
    asse=client.futures_position_information()
    keyValList=['ETHBUSD']
    res=[d for d in asse if d['symbol'] in keyValList]
    return(float(res[0]['markPrice']))
def quantidade():
    qta=float(a())*float(leverage)/float(preco())
    qty = float(round(qta, int(simbolo())-int(1)))
    return(qty)
def pegaposicao():
    global posicao
    posicao=b()
    print(posicao)
        
#search()
#simbolo()
#saldodown
#b()
#compra()
pegaposicao()
simbolo()
print(quantidade())
#print(client.futures_symbol_ticker())

def verificando():
    global baixo
    global cima
    global posicao
    try:
        baixo=saldodown()
    except Exception:
        pass
    try:
        cima=saldoup()
    except Exception:
        pass
    if baixo>int(10):
        posicao='sell'
        return('venda')
    elif int(10)<cima:
        posicao='buy'
        return('compra')
    elif baixo<int(10)and cima<int(10):
        posicao='neutral'
        return('neutro')
    else:
        return('neutro')
    
def dia():
    while datetime.datetime.today().weekday() in diasuteis:
        ping()
    time.sleep(120)
    vendertudo()
    return 'fim de semana'
#print('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m'

#response = requests.request("GET","https://api.binance.com/api/v3/ticker/price?symbol=BTCDOWNUSDT")
#print(response.json()['price'])


#(float(balance['free'])+float(balance['locked']))*float(response.json()['price'])
#(float(balance['free'])+float(balance['locked']))*float(response.json()['price'])

def mudanca():
    global posicao
    print('ok')
    order = None
    if last_order=='sell':
        #comprar btcdown
        try:
            response = client.futures_create_order(
                symbol="ETHBUSD",
                side="SELL",
                type="MARKET",
                quantity=quantidade(),
                #timeInForce="GTC",
                #price=59808.0,
            )
            logging.info(response)
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
        posicao='sell'
        print('short')
    if last_order=='neutral':
        print('cendertudo')
        pass
        #inserir pass
    elif last_order=='buy':
        #comprar btcup
        try:
            response = client.futures_create_order(
                symbol="ETHBUSD",
                side="BUY",
                type="MARKET",
                quantity=quantidade(),
                #timeInForce="GTC",
                #price=59808.0,
            )
            logging.info(response)
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
        posicao='buy'
        print('long')
def vendertudo():
    global posicao
    print('vendeutudo')
    order = None
    if posicao=='sell':
        #vender btcdown
        try:
            response = client.futures_create_order(
                symbol="ETHBUSD",
                side="BUY",
                type="MARKET",
                quantity=10,
                reduceOnly=True,
                #timeInForce="GTC",
                #price=59808.0,
            )
            logging.info(response)
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
        posicao='neutral'
    if posicao=='buy':
        #vender btcup
        try:
            response = client.futures_create_order(
                symbol="ETHBUSD",
                side="SELL",
                type="MARKET",
                quantity=10,
                reduceOnly=True,
                #timeInForce="GTC",
                #price=59808.0,
            )
            logging.info(response)
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
        posicao='neutral'
    if posicao=='neutral':
        pass
    else:
        if b()=='buy':
            #vende btcup
            try:
                response = client.futures_create_order(
                    symbol="ETHBUSD",
                    side="SELL",
                    type="MARKET",
                    quantity=10,
                    reduceOnly=True,
                    #timeInForce="GTC",
                    #price=59808.0,
                )
                logging.info(response)
            except ClientError as error:
                logging.error(
                    "Found error. status: {}, error code: {}, error message: {}".format(
                        error.status_code, error.error_code, error.error_message
                    )
                )
            posicao='neutral'
        if b()=='sell':
            #vende btdown
            try:
                response = client.futures_create_order(
                    symbol="ETHBUSD",
                    side="BUY",
                    type="MARKET",
                    quantity=10,
                    reduceOnly=True,
                    #timeInForce="GTC",
                    #price=59808.0,
                )
                logging.info(response)
            except ClientError as error:
                logging.error(
                    "Found error. status: {}, error code: {}, error message: {}".format(
                        error.status_code, error.error_code, error.error_message
                    )
                )
            posicao='neutral'
        else:
            pass

    
def verifica():
    #verifica se esta diferente e vende em caso positivo
    if posicao==last_order:
        pass
                 
    else:
        print('diferente')
        vendertudo()
        mudanca()
                 


def compr():

                 #ordem de compra se estiver diferente
    pass
    
def vend():
                 #ordem de venda se estiver diferente
    pass
def pegafluxo():
    url = 'https://api.binance.com/api/v3/klines'
    params = {
      'symbol': 'ETHBUSD',
      'interval': '1h'
    }
    params3 = {
      'symbol': 'ETHBUSD',
      'interval': '15m'
    }
    global response
    global response3
    global fabricacao
    response = requests.get(url, params=params)
    response3= requests.get(url, params=params3)
    now = datetime.datetime.now()
    fabricacao = datetime.datetime.now()
    return response
    

def ping():
    # Repeat forever.
    while True:
        # Retrieve recommendation.
        #rec = handler.get_analysis().summary["RECOMMENDATION"]
        global last_order
        global response
        end = datetime.datetime.now()
        duration = end - fabricacao
        tmpdemed= fabricacao
        now = datetime.datetime.now()
        if float(duration.total_seconds())<float(120):
            print('pode continuar')
            taxa=float(response.json()[-2][7])
            taxa1=float(response.json()[-1][7])
            #agora15r=float(response3.json()[-1][7])
            #passado15=float(response3.json()[-2][7])
            #taxa2= igual a taxa3 mas usando velas de 15 minutos
            #taxa3=float(response.json()[-1][7])/float(fabricacao.minute)*float(60)
            #taxa=float(response.json()[-1][7]/(float(fabricacao.minute)-float(datetime.datetime.fromtimestamp(float(response.json()[-2][0]/1000)))).minute)*float(60)
            #print(float(response.json()[-1][7])/(float(fabricacao.minute)-float(datetime.datetime.fromtimestamp(response.json()[-1][0]/1000).minute)*float(60)))
            #if taxa>float(120000000):
            if taxa>float(120000000):
            #or taxa1>float(160000000):
                pegaposicao()
                rec = handler.get_analysis().summary["RECOMMENDATION"]
                #if passado15>float(50000000) or agora15>float(50000000):
                print('liga')

                    # Create a buy order if the recommendation is "BUY" or "STRONG_BUY" and the last order is "sell".
                    # Create a sell order if the recommendation is "SELL" or "STRONG_SELL" and the last order is "buy".
                if "BUY" in rec:
                    # REPLACE COMMENT: Create a buy order using your exchange's API.

                    last_order = "buy"
                    print('compra')
                    print(last_order)
                    verifica()
            
                if "NEUTRAL" in rec:

                    last_order = "neutral"
                    print('neutro')
                    print(last_order)
                    verifica()
    
                elif "SELL" in rec :
                    # REPLACE COMMENT: Create a sell order using your exchange's API.

                    last_order = "sell"
                    print('venda')
                    print(last_order)
                    verifica()
                #else:
                    #print('desliga')
                    #if posicao!='neutral':
                        #vendertudo()
            else:
                print('desliga')
                if posicao!='neutral':
                    vendertudo()
        else:
            pegafluxo()
            print('renovou')

        # Wait for x seconds before retrieving new analysis.
        # The time should be the same as the interval.
        time.sleep(5)

def attempts():
    while True:
        try:
            dia()
            break #breaks the loop when sucessful
        except Exception:
            print('tentando de novo...')
            time.sleep(5)
            attempts() #recalls this function, starting back at the try statement
            break
b()
pegaposicao()
pegafluxo()
while True:
    attempts()
