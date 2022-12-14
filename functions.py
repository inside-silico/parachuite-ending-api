import pandas as pd
from env import *
import datetime
from sqlalchemy import create_engine
from Fallen import *


engine = create_engine("mysql+pymysql://{user}:{pw}@{db_host}:{port}/{db}"
                .format(user=db_usr,pw=db_pass,db_host=db_host,
                    db=db_name,port=db_port,auth_plugin='mysql_native_password',))


def outer_quots():
    list_outer=["AAPL","AMD","AMZN","ARCO","AUY","BA","BABA","BBD","C","CSCO","CVX","DESP","DIS","EBAY","ERJ","FB","GE","GLOB","GOLD","GOOGL","HMY","IBM","INTC","ITUB","JNJ","JPM","KO","MCD","MELI","MSFT","NFLX","NVDA","PBR","PFE","QCOM","T","TS","TSLA","V","VALE","VIST","VZ","WFC","WMT","X"]
    yahoo_outer=  ','.join(map(str, list_outer))
    yahoo_outer='"'+yahoo_outer+'"'
    outer_quots=yahoo.get_quotes(yahoo_outer)
    return outer_quots


def lanzamiento_cubierto(underlying):
    df=pd.read_sql_table("options",con=engine)
    last_GGAL=pd.read_sql_table("bluechips_48hs",con=engine).set_index("symbol")
    last_underly=last_GGAL.at[underlying,"last"]

    df2=df[df["underlying_asset"].isin([underlying])]
    df2=df2[df2["kind"].isin(["CALL"])]
    df2=df2[["symbol","strike","bid","ask","expiration"]].copy()
    df2=df2.assign(eq=0.0)
    df2=df2.assign(Clas=0.0)
    df2=df2.assign(gain=0.0)
    df2=df2.assign(gain2=0.0)
    df2=df2.assign(gain3=0.0)
    df2=df2.assign(days_left=0.0)
    df2.bid=df2.bid.astype(float)
    df2['eq'] = (last_underly-df2['bid'])
    #df2.rename(columns={"eq": "Precio de Equilibrio"},inplace=True)
    def moneyness(x):
        if x <last_underly:
            return 'ITM'
        elif x > last_underly:
            return 'OTM'
        else:
            return 'ATM'
    df2['Clas'] = df2['strike'].apply(moneyness)
    df2.gain=(df2.bid+df2.strike-last_underly)*100
    df2.gain2=df2.gain/last_underly
    df2.days_left=(df2.expiration-datetime.datetime.now()).dt.days+1
    df2.gain3=(df2.gain2/df2.days_left)*365
    #df2.rename(columns={"gain2": "Ganancia Potencial en %"},inplace=True)
    #df2.rename(columns={"gain": "Ganancia Potencial"},inplace=True)
    #df2.rename(columns={"gain3": "Ganancia Potencial en % Anualizada"},inplace=True)
    #df2.rename(columns={"days_left": "Dias Restantes","symbol":"Ticker"},inplace=True)
    df2.drop(["expiration"],axis=1,inplace=True)
    df2=df2.set_index("symbol")
    df2=df2.round(2)
    df2=df2.round(2)
    df2.reset_index(inplace=True)
    return df2