from env import *
from sqlalchemy import create_engine
from flask_restful import  Resource
from flask import Response
import pandas as pd
import requests
from bs4 import BeautifulSoup
from Fallen import *
from functions import *

engine = create_engine("mysql+pymysql://{user}:{pw}@{db_host}:{port}/{db}"
                .format(user=db_usr,pw=db_pass,db_host=db_host,
                    db=db_name,port=db_port,auth_plugin='mysql_native_password',))

class Todo(Resource):
    def get(self, todo_id):
        var="todoss"+todo_id
        return var

class BCRA(Resource):
    def get(self):
        res = requests.get('http://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables.asp')
        soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.find_all('table')
        data = pd.read_html(str(table))[0]
        data.at[15,"Rubro"]="Préstamos Tit. Valores"
        data.dropna(subset=["Valor"],inplace=True)
        data.drop(["Rubro"],axis=1,inplace=True)
        data.rename(columns={"Unnamed: 0": "Nombre"},inplace=True)
        data.set_index("Nombre",inplace=True)
        data.drop("Tasas de interés",inplace=True)
        data.reset_index(inplace=True)
        data.Valor=data.Valor.str.replace(".", "").astype(float)
        row10=[28,30,31,32,33]
        row100=[1,2,3,4,5,6,7,11,12,13,14,15,16,17,35,36]
        row10000=[8,9,10,34]

        for i in range(len(row10)):
            data.at[row10[i],"Valor"]=data.at[row10[i],"Valor"]/10

        for i in range(len(row100)):
            data.at[row100[i],"Valor"]=data.at[row100[i],"Valor"]/100

        data.at[0,"Valor"]=data.at[0,"Valor"]/1000

        for i in range(len(row10000)):
            data.at[row10000[i],"Valor"]=data.at[row10000[i],"Valor"]/10000
        return Response(data.dropna().drop(5).to_json(orient="records"), mimetype='application/json')

class options(Resource):
    def get(self):
        return Response(pd.read_sql_table("options",con=engine).to_json(orient="records"), mimetype='application/json')

class options_lanzamiento(Resource):
    def get(self,underlying):
        return Response(lanzamiento_cubierto(underlying).to_json(orient="records"), mimetype='application/json')

class mep(Resource):
    def get(self):
        quots=pd.read_sql_table("bonds_48hs",con=engine).set_index("symbol")
        list_ticker=["AL29","AL30","AL35","AE38","AL41","GD29","GD30","GD35","GD38","GD41","GD46","AL29D","AL30D","AL35D","AE38D","AL41D","GD29D","GD30D","GD35D","GD38D","GD41D","GD46D"]
        df=pd.DataFrame(columns=['symbol',"bid",'ask',"last"])
        df.symbol=list_ticker
        df.set_index("symbol",inplace=True)
        df.update(quots)
        df_ars=df.head(11).reset_index()
        df_ars.rename({"symbol":"symbolARS","bid":"bidARS","ask":"askARS","last":"lastARS"},axis=1,inplace=True)
        df_usd=df.tail(11).reset_index()
        df_usd.rename({"symbol":"symbolUSD","bid":"bidUSD","ask":"askUSD","last":"lastUSD"},axis=1,inplace=True)
        result = pd.concat([df_ars, df_usd], axis=1, join="inner")
        result=result.reset_index().drop(["index"],axis=1)
        result=result.assign(MEPbid=0.0)
        result=result.assign(MEPask=0.0)
        result=result.assign(MEPlast=0.0)
        result.MEPlast=result.lastARS/result.lastUSD
        result.MEPlast=result.MEPlast.astype(float).round(2)

        result.MEPbid=result.askARS/result.bidUSD
        result.MEPbid=result.MEPbid.astype(float).round(2)

        result.MEPask=result.bidARS/result.askUSD
        result.MEPask=result.MEPask.astype(float).round(2)

        return Response(result.to_json(orient="records"), mimetype='application/json')

class ccl(Resource):
    def get(self):
        source=pd.read_sql_table("cedear_48hs",con=engine)
        source.rename({"last":"Cedear","symbol":"Ticker"},axis=1,inplace=True)
        source.set_index("Ticker",inplace=True)

        list_ticker=["AAPL","AMD","AMZN","ARCO","AUY","BA","BABA","BBD","C","CSCO","CVX","DESP","DISN","EBAY","ERJ","FB","GE","GLNT","GOLD","GOOGL","HMY","IBM","INTC","ITUB","JNJ","JPM","KO","MCD","MELI","MSFT","NFLX","NVDA","PBR","PFE","QCOM","T","TEN","TSLA","V","VALE","VIST","VZ","WFC","WMT","X"]
        list_outer=["AAPL","AMD","AMZN","ARCO","AUY","BA","BABA","BBD","C","CSCO","CVX","DESP","DIS","EBAY","ERJ","FB","GE","GLOB","GOLD","GOOGL","HMY","IBM","INTC","ITUB","JNJ","JPM","KO","MCD","MELI","MSFT","NFLX","NVDA","PBR","PFE","QCOM","T","TS","TSLA","V","VALE","VIST","VZ","WFC","WMT","X"]
        yahoo_outer=  ','.join(map(str, list_outer))
        yahoo_outer='"'+yahoo_outer+'"'
        list_fc=[10.0,0.5,144.0,0.5,1.0,6.0,9.0,1.0,3.0,5.0,8.0,1.0,4.0,2.0,1.0,8.0,1.0,6.0,1.0,58.0,1.0,5.0,5.0,1.0,5.0,5.0,5.0,8.0,60.0,10.0,16.0,24.0,1.0,2.0,11.0,3.0,1.0,15.0,6.0,2.0,0.2,2.0,5.0,6.0,3.0]

        ccl_columns=["Ticker","TickerUS","FC","Cedear","Stock","CCL"]
        ccl=pd.DataFrame(columns=ccl_columns)
        ccl.Ticker=list_ticker
        ccl.TickerUS=list_outer
        ccl.FC=list_fc
        ccl.FC=ccl.FC.astype(float)

        outer_quots=yahoo.get_quotes(yahoo_outer)
        outer_quots.rename({"last":"Stock","symbol":"Ticker"},axis=1,inplace=True)
        ccl.set_index("TickerUS",inplace=True)
        ccl.update(outer_quots.set_index("Ticker"))
        ccl.reset_index(inplace=True)
        ccl.set_index("Ticker",inplace=True)
        ccl.update(source)
        ccl.reset_index(inplace=True)
        ccl.CCL=(ccl.Cedear/ccl.Stock)*ccl.FC
        ccl.CCL=ccl.CCL.astype(float).round(2)
        return Response(ccl.to_json(orient="records"), mimetype='application/json')

class dolarHoy(Resource):
    def get(self):
        res = requests.get('https://dolarhoy.com/cotizaciondolarbolsa')
        soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.find_all("div",{"class":"tile cotizaciones_more"})

        titleList=table[0].find_all('div', {'class': 'title'})
        compraList=table[0].find_all('div', {'class': 'compra'})
        ventaList=table[0].find_all('div', {'class': 'venta'})

        for i in range(len(titleList)):
            titleList[i]=titleList[i].getText()
        for i in range(len(titleList)):
            compraList[i]=compraList[i].getText()
        for i in range(len(titleList)):
            ventaList[i]=ventaList[i].getText()

        df=pd.DataFrame(columns=["moneda","compra","venta"])
        df.moneda=titleList
        df.compra=compraList
        df.venta=ventaList
        return Response(df.drop([0,6]).to_json(orient="records"), mimetype='application/json')

class bonistas(Resource):
    __dictt={"fixedPesos":0,"cer":3,"fixedDolar":5,"fixedDolarC":7,"dolarC":8}
    def get (self, panel_id):
        url="http://www.bonistas.com/"
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all('table')
        data = pd.read_html(str(table))[self.__dictt[panel_id]]
        return data.to_json(orient="records")


class argy_quots(Resource):
    def get(self, panel_id,settlement_id):
        var=panel_id+'_'+settlement_id
        return Response(pd.read_sql_table(panel_id+'_'+settlement_id,con=engine).to_json(orient="records"), mimetype='application/json')
