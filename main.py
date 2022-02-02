import requests
import datetime as dt
from twilio.rest import Client

change_plus = True
change_negative = False
CURRENT_DATE = dt.datetime.now()
YESTERDAY = int(CURRENT_DATE.strftime("%d"))-1
DAY_BEFORE_YESTERDAY = int(CURRENT_DATE.strftime("%d"))-2
# print(CURRENT_DATE.strftime("%d"))




alphavantage_api = "8KL1PE21LJ41H6E0"
STOCK = "TSLA"
COMPANY_NAME = "TESLA"

stock_params={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "outputsize":"compact",
    "apikey":alphavantage_api
}

response = requests.get("https://www.alphavantage.co/query", params=stock_params)
stock_data = response.json()

day_before = float(stock_data['Time Series (Daily)'][f"2021-11-{DAY_BEFORE_YESTERDAY}"]["4. close"])
last_night = float(stock_data['Time Series (Daily)'][f"2021-11-{YESTERDAY-2}"]["4. close"])

percent_diff = ((day_before-last_night)/day_before)*100
r_percent_diff = round(percent_diff, 2)
if percent_diff > 5:
    change = True
    # print("Get News")

news_api_key = "5a3d2ad30d834950bbc6866bc6b40257"
news_param = {
    "q":"Tesla",
    "apiKey":news_api_key
}

news_response = requests.get("https://newsapi.org/v2/everything", params = news_param)
news_data = news_response.json()
lst_titles = []
lst_links = []
for _ in range(3):
    lst_titles.append(news_data["articles"][_]["title"])
    lst_links.append(news_data["articles"][_]["url"])

twilio_phone = +16092933182
api_key = "a4df4ad2fddfb4afd58de1a9a365d120"
account_sid = "AC7912c27d3304d9ff29617d6cf0c014ba"
auth_token = "94daf7c8a8868d7849eb6b2e88d947c7"

if change_plus:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"Here's what's happening: {STOCK}🔺{r_percent_diff}%"
             f"\nHeadline: {lst_titles[0]}, Headline: {lst_titles[1]}, Headline: {lst_titles[2]}",
        from_='+16092933182',
        to='+17147424297'
    )
if change_negative:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"Here's what's happening: {STOCK}🔻{r_percent_diff}"
             f"n\Headline: {lst_titles[0]}, Headline: {lst_titles[1]}, Headline: {lst_titles[2]}",
        from_='+16092933182',
        to='+17147424297'
    )

