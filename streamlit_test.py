#!/usr/bin/env python
# coding: utf-8

"""
THIS HAS BEEN DEPRECATED!
We propose you use st.form() instead:
https://blog.streamlit.io/introducing-submit-button-and-forms/
"""

import streamlit as st
import collections
import functools
import inspect
import textwrap

def cache_on_button_press(label, **cache_kwargs):
    """Function decorator to memoize function executions.
    Parameters
    ----------
    label : str
        The label for the button to display prior to running the cached funnction.
    cache_kwargs : Dict[Any, Any]
        Additional parameters (such as show_spinner) to pass into the underlying @st.cache decorator.
    Example
    -------
    This show how you could write a username/password tester:
    >>> @cache_on_button_press('Authenticate')
    ... def authenticate(username, password):
    ...     return username == "buddha" and password == "s4msara"
    ...
    ... username = st.text_input('username')
    ... password = st.text_input('password')
    ...
    ... if authenticate(username, password):
    ...     st.success('Logged in.')
    ... else:
    ...     st.error('Incorrect username or password')
    """
    internal_cache_kwargs = dict(cache_kwargs)
    internal_cache_kwargs['allow_output_mutation'] = True
    internal_cache_kwargs['show_spinner'] = False
    
    def function_decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            @st.cache(**internal_cache_kwargs)
            def get_cache_entry(func, args, kwargs):
                class ButtonCacheEntry:
                    def __init__(self):
                        self.evaluated = False
                        self.return_value = None
                    def evaluate(self):
                        self.evaluated = True
                        self.return_value = func(*args, **kwargs)
                return ButtonCacheEntry()
            cache_entry = get_cache_entry(func, args, kwargs)
            if not cache_entry.evaluated:
                if st.button(label):
                    cache_entry.evaluate()
                else:
                    raise st.ScriptRunner.StopException
            return cache_entry.return_value
        return wrapped_func
    return function_decorator

def confirm_button_example():
    @cache_on_button_press('Authenticate')
    def authenticate(username, password):
        return username == "iagshin" and password == "s97043133"

    username = st.text_input('username')
    password = st.text_input('password')

    if authenticate(username, password):
        st.success('You are authenticated!')
#        st.write(st.slider('Test widget'))
    else:
        st.error('The username or password you have entered is invalid.')

def display_func_source(func):
    code = inspect.getsource(confirm_button_example)
    code = '\n'.join(code.splitlines()[1:]) # remove first line
    st.code(textwrap.dedent(code))

if __name__ == '__main__':
#    st.write("""
#        This example shows a hack to create a "confirm button" in Streamlit, e.g.
#        to authenticate a username / password pair.
#        The correct answer is `buddha` / `s4msara`.
#    """)
#    display_func_source(confirm_button_example)
    confirm_button_example()
    
    
# In[1]:
from datetime import datetime, timedelta
from pykrx import stock
import pandas as pd
import streamlit as st

import plotly as py
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

# In[ ]:

# 현재 날짜 가져오기
end_day = datetime.today().strftime("%Y%m%d")
start_day = (datetime.today() - timedelta(1000)).strftime("%Y%m%d")

# 주식 정보 가져오기
# SAMSUNG = stock.get_market_ohlcv(start_day, end_day, "005930")
KODEX_dollar = stock.get_market_ohlcv(start_day, end_day, "261240")
KODEX_200 = stock.get_market_ohlcv(start_day, end_day, "069500")

# In[ ]:

st.write("Today :", end_day)

# Create figure with secondary y-axis
st.subheader('KODEX 200 vs KODEX 미국달러선물 ETF')

#df = KODEX_200["종가"]
#fig = px.line(df) # , x=df.index, y="lifeExp", title='Life expectancy in Canada')
#fig = go.Scatter(x=df.index, y=df)   # , name='KODEX 200')

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=KODEX_dollar.index, y=KODEX_dollar["종가"], name='KODEX 미국달러선물'),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=KODEX_200.index, y=KODEX_200["종가"], name='KODEX 200'),
    secondary_y=True,
)

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

# Plot!
st.plotly_chart(fig)  #, use_container_width=True)

