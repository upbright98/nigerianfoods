import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# check imports
print('ready')

# get the data
def get_data():
    url= './datasets/nigeria_food_prices.csv'
    df =pd.read_csv(url)
    cols_to_drop=['adm0_id','adm1_id', 'mkt_id', 'cm_id', 'cur_id','pt_id', 'um_id','mp_commoditysource']
    df= df.drop(columns=cols_to_drop)
    new_names = {'adm0_name': 'country',
             'adm1_name': 'state',
             'cm_name': 'produce',
             'cur_name': 'currrency',
             'mp_month': 'month',
             'mp_year': 'year',
             'mp_price': 'price',
             'pt_name': 'market_type',
             'um_name': 'quantity',
             'mkt_name': 'market'}
    df=df.rename(columns= new_names)
    return df

# display the results using python
print(get_data())

#title
st.write("# Nigerian Food Prices App")

# dispay the results using streamlit



# df # magic command and is actually ==st.write(df)

# create a structure for the app
# sidebar
try:
    st.sidebar.header(" user input controls")
    df= get_data()
    
    states = st.sidebar.multiselect("Choose state",df.state.unique(),"Abia")
    product = st.sidebar.selectbox('Choose product',df.produce.unique())
    
    # error checking
    if not states:
        st.sidebar.error("Please select at least one state" )
    else:
        for i, indx in enumerate(states):
            data = df[df.state == states[i]]
            st.write(f"### Prices of Goods in {states[i]} Markets", data.head())
            # using the data tet's build a line chart
            # we build a pivot table
            pvt = pd.pivot_table(data, index=['state','market','produce','year'],values=['price'],aggfunc='mean')
            pvt_df = pvt.reset_index()
            selected_state = states[i]
            st.write(selected_state)
            pvt_df = pvt_df[pvt_df['state'] == selected_state]
            # selected product
            selected_product = product
            pvt_df = pvt_df[pvt_df["produce"] == selected_product]
            # line chart
            chart = alt.Chart(pvt_df).mark_area().encode(
            x='year', y='price', tooltip=['market','price'])
            st.write(f"### Price Chart {selected_product} in {selected_state}")
            st.altair_chart(chart, use_container_width=True)
            # Area charts eith differents markets
            chart = alt.Chart(pvt_df).mark_area().encode(
                x='year', color='market',y='price', tooltip=['market','price']).interactive()
            st.write(f"### Price Chart {selected_product} in {selected_state}")
            st.altair_chart(chart, use_container_width=True)
except RuntimeError as e:
    st.error(e.reason)
                
                


