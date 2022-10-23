
from email.mime import application
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin 
from firebase_admin import credentials, firestore
#TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate('./iuh-20015491-7227c-firebase-adminsdk-2mln5-4b4ee44d7a.json')
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl-20015491').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("int")   

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__)
server = app.server

app.title = "Xây dựng danh mục sản phẩm tiềm năng"

doanhSo = sum(df['SALES'])
answerdoanhso = str(round(doanhSo,2))

loiNhuan = sum(df["SALES"]) - sum(df['QUANTITYORDERED']* df['PRICEEACH'])
answerloinhuan = str(round(loiNhuan,2))

TdoanhSo = df.groupby(['CATEGORY']).sum(numeric_only=True)
topDoanhSo = TdoanhSo['SALES'].max()
answertopDoanhSo = str(round(topDoanhSo,2))

df["PROFIT"] = df['SALES'] - df['QUANTITYORDERED']* df['PRICEEACH']
ln = df.groupby(['CATEGORY']).sum('PROFIT')
topLoiNhuan = ln['PROFIT'].max()
answertopLoiNhuan = str(round(topLoiNhuan, 2))

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
h1 = px.histogram(df, x= "YEAR_ID", y= "SALES", title="Doanh số bán hàng theo năm",
labels={'YEAR_ID': 'Năm', "SALES": "Doanh số"})

hk3 = df[df["YEAR_ID"]=='2003']
ln3 = sum(hk3['SALES'])- sum(hk3['QUANTITYORDERED']*hk3['PRICEEACH'])
hk4 = df[df["YEAR_ID"]=='2004']
ln4 = sum(hk4['SALES'])- sum(hk4['QUANTITYORDERED']*hk4['PRICEEACH'])
hk5 = df[df["YEAR_ID"]=='2005']
ln5 = sum(hk5['SALES'])- sum(hk5['QUANTITYORDERED']*hk5['PRICEEACH'])
d= pd.DataFrame({
    'YEAR_ID': [2003,2004,2005],
    'PROFIT':[ln3,ln4,ln5]
})

df["YEAR_ID"]= df["YEAR_ID"].astype("str")
h2 = px.line(d,x= "YEAR_ID", y="PROFIT",markers=True, labels={'YEAR_ID':'Năm','PROFIT':'Lợi nhuận'},
title='Lợi nhuận bán hàng theo năm')

h3 = px.sunburst(df, path=["YEAR_ID","CATEGORY"],values="SALES",
color= "SALES",
labels={'parent':'Năm', 'lables':'Doanh mục','PROFIT':'Lợi nhuận'},
title='Tỉ lệ doanh số theo danh mục trong từng năm')

df["PROFIT"]=df['SALES']-df["QUANTITYORDERED"]*df["PRICEEACH"]
h4=px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='PROFIT',
color='PROFIT',
labels={'parent':'Năm', 'labels':'Danh Mục','PROFIT':'Lợi Nhuận'},
title='Tỉ lệ lợi nhuận theo danh mục trong từng năm')

sp = df.groupby(['CATEGORY']).sum('SALES').sort_values(by="SALES", ascending=False).reset_index().head(1)['CATEGORY'][0]
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3(
                    children="Xây Dựng Danh Mục Sản Phẩm Tiềm Năng", className="header-title"
                ),
                html.P(
                   "IUH_DHHTTT16A_20015491_Phan Huy Phong",
                    className="info"
                ),  
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=html.Div(
                        children=[
                        html.P("DOANH SỐ SALES",className="title"),
                        html.P(answerdoanhso)
                        ],
                        className="lable"
                   ),
                    className="card c1"
                ),
                html.Div(
                    children=html.Div(
                        children=[
                            html.P("LỢI NHUẬN",className="title"),
                            html.P(answerloinhuan)
                        ],className="lable"
                    ),
                    className="card c1"
                ),
                html.Div(
                    children=html.Div(
                       children=[
                           html.P("TOP DOANH SỐ",className="title"),
                           html.P(sp+', '+answertopDoanhSo)
                       ],className="lable"
                    ),
                    className="card c1"
                ),
                html.Div(
                    children=html.Div(
                        children=[
                        html.P("TOP LỢI NHUẬN",className="title"),
                        html.P(sp+', '+answertopLoiNhuan)
                        ],className="lable"
                    ),
                    className="card c1"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=h1,
                        className="hist"
                    ),
                    className="card c2"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=h3,
                        className="hist"
                    ),
                    className="card c2"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=h2,
                        className="hist"
                    ),
                    className="card c2"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=h4,
                        className="hist"
                    ),
                    className="card c2"
                ),
            ], className="wrapper")
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8090)