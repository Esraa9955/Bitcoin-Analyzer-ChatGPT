from openai import OpenAI
import json
import requests
import http.client
import streamlit as st
client = OpenAI()
def get_completion(prompt, model='gpt-3.5-turbo'):
  mesages = [{'role':'user','content':prompt}]
  response = client.chat.completions.create(
    model=model,
    messages=mesages,
    temperature=0
  )
  return response.choices[0].message.content

st.title('Bitcoin Analyzer with ChatGPT')
st.subheader('Example: Analyzeing Live Crypto Prices')

def get_bitcoin_prices():
  url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
  querystring = {"referenceCurrencyUuid": "yhjMzLPhuIDl", "timePeriod": "7d"}

  headers = {
      'x-rapidapi-key': "903bad1aa3msh339eb35bf2ed0fbp1f79e8jsn3e3c32c14d28",
      'x-rapidapi-host': "coinranking1.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers, params=querystring)
  data = response.json()
  
  history = data['data']['history']
  prices = [change['price'] for change in history]
  
  return prices


if st.button('Analyze'):
  with st.spinner('Getting Bitcoin Prices...'):
    bitcoin_prices =  get_bitcoin_prices()
    st.success("Done!")
  with st.spinner('Analyzing Bitcoin Prices ...'):
    chatGPTPrompt = f""" You are an expert crypto trader with more than 10 years of experience,
      I will provide you with a list of bitcoin prices for the last 7 days
      can you provide me with a technical analysis of Bitcoin
      based on these prices. here is what I want:
      - Price Overview
      - Moving Averages
      - Relative Strength Index (RSI)
      - Advice and Suggestions
      - Do I buy or sell?
      pleas be as detailed as much as you can and explain in a way any beginner can understand.
      and here is the price list {bitcoin_prices}
      """
    response = get_completion(chatGPTPrompt)
    st.text_area("Analysis",response,
                height=500 )
    st.success("Done!")





