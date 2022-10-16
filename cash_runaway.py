# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 01:23:19 2022

@author: User
"""
import streamlit as st
import hydralit_components as hc
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
tickers_cik = pd.read_csv('listed_companies.csv')
tickers_cik['cik_str'] = tickers_cik['cik_str'].astype('string')
companies_bio = pd.read_csv('companies_biodata.csv')

import os
st.write(os.listdir()[:])

def burnrate(df):
    c1,c2 = st.columns(2)
    a = df.rolling(3).mean()
    b = df.iloc[::-1].rolling(3).mean()
        
    with c1:
        df = a.fillna(b).fillna(df).interpolate(method='nearest').ffill().bfill()
        
        import numpy as np
        x = range(min(50,len(df['OperatingExpenses'].index)))
        y = df['OperatingExpenses'][-min(50,len(df['OperatingExpenses'].index)):]
        z = np.polyfit(x, y, 3)
        f = np.poly1d(z)
        
        x_new = np.linspace(max(x), max(x)+11, 12)
        y_new = f(x_new)
        x_tot = np.linspace(len(df['OperatingExpenses'].index),len(df['OperatingExpenses'].index)+11, 12)
        
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x = list(range(len(df['OperatingExpenses'].index))),
            y=df['OperatingExpenses'].values,
            name='Recorded',
        ))
        
        fig.add_trace(go.Scatter(
            x = x_tot,
            y=  y_new,
            name='Projected',
        ))
        
        fig.add_trace(go.Scatter(
            x = x_tot,
            y=  [y[-1]]*12,
            name='Current Scenario',
        ))
        
        fig.update_layout(
                
                paper_bgcolor='white',
                plot_bgcolor='#fafafa',
                hovermode='closest',
                width = 800,
                height=500,
                title='Operating Expenses',
                xaxis = dict(
                    title="Quarters"
                ),
                yaxis = dict(
                    title="Total value (USD)"
                ),
                legend=dict(yanchor="top", y=1, xanchor="left", x=0),
                showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        assests_projected = df['Assets'].tolist()[-1:]
        assests_curr = df['Assets'].tolist()[-1:]
        
        for x in y_new:
            assests_projected.append(assests_projected[-1]-x)
        for x in [y[-1]]*12:
            assests_curr.append(assests_curr[-1]-x)
        
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Scatter(
            x = list(range(len(df['Assets'].index))),
            y=df['Assets'].values,
            name='Recorded',
        ))
        
        fig.add_trace(go.Scatter(
            x = x_tot,
            y = assests_projected[1:],
            name='With Projected Expenses',
        ))
        
        fig.add_trace(go.Scatter(
            x = x_tot,
            y = assests_curr[1:],
            name='With Current Expenses',
        ))
        
        fig.update_layout(
                
                paper_bgcolor='white',
                plot_bgcolor='#fafafa',
                hovermode='closest',
                width = 800,
                height=500,
                title='Projected Assests if company has no income but only the expenses.',
                xaxis = dict(
                    title="Quarters"
                ),
                yaxis = dict(
                    title="Total value (USD)"
                ),
                legend=dict(yanchor="top", y=1, xanchor="left", x=0),
                showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
    lasts = 0
    for x in assests_projected[1:]:
        if x>0:
            lasts += 1
    lasts1 = 0
    for x in assests_curr[1:]:
        if x>0:
            lasts1 += 1
    st.write('Will company sustain for next 12 quarters?')
    st.write(f'Company can sustain for more {lasts} quarters with extrapolated operational expenses.')
    st.write(f'Company can sustain for more {lasts1} quarters with current operational expenses.')
    

def lineplot(df,name):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x = df.index,
        y=df[name],
        name='Total value (USD)',
    ))
    fig.update_layout(
        
        paper_bgcolor='white',
        plot_bgcolor='#fafafa',
        hovermode='closest',
        width = 800,
        height=500,
        title=name,
        xaxis = dict(
            title="Time"
        ),
        yaxis = dict(
            title="Total value (USD)"
        ),
        showlegend=False)
    return fig

def areaplot(df,names):
    import plotly.graph_objects as go
    fig = go.Figure()
    for name in names:
        fig.add_trace(go.Scatter(
    	name = name,
    	x = df.index,
    	y = df[name],
    	stackgroup='one'
        ))
    fig.update_layout(
        
        paper_bgcolor='white',
        plot_bgcolor='#fafafa',
        #hovermode='closest',
        width = 800,
        height=500,
        title=name,
        xaxis = dict(
            title="Time"
        ),
        yaxis = dict(
            title="Total value (USD)"
        ),
        legend=dict(yanchor="top", y=1, xanchor="left", x=0),
        showlegend=True)
    return fig
    
def normal(select):
    
    if select == 'Home':
        col1, col2 = st.columns(2)
        with col1:
            method = st.radio(
        "How do you want to search?",
        ('Ticker Symbol', 'CIK'))
        show = 0
        with col2:
            if method == 'Ticker Symbol':
                ticker = st.text_input('Enter the ticker name.', value="AAPL")
                if ticker in tickers_cik['ticker'].values:
                    st.write('Showing Results For')
                    st.write('Title : ',tickers_cik[tickers_cik['ticker'] == ticker]['title'][0])
                    st.write('Ticker Symbol : ',tickers_cik[tickers_cik['ticker'] == ticker]['ticker'][0])
                    st.write('CIK : ',tickers_cik[tickers_cik['ticker'] == ticker]['cik_str'][0])
                    cik = tickers_cik[tickers_cik['ticker'] == ticker]['cik_str'][0]
                    cik_act = '0'*(10-len(cik))+cik
                    show = 1
                else:
                    st.write('No such Ticker exists in our database.')
            elif method == 'CIK':
                cik = str(int(st.text_input('Enter the CIK.', value="0000320193")))
                cik_act = '0'*(10-len(cik))+cik
                if cik in tickers_cik['cik_str'].values:
                    st.write('Showing Results For')
                    st.write('Title : ',tickers_cik[tickers_cik['cik_str'] == cik]['title'][0])
                    st.write('Ticker Symbol : ',tickers_cik[tickers_cik['cik_str'] == cik]['ticker'][0])
                    st.write('CIK : ',tickers_cik[tickers_cik['cik_str'] == cik]['cik_str'][0])
                    show = 1
                else:
                    st.write('No such CIK exists in our database.')
            
        if show and len(pd.read_csv(r'values\CIK'+cik_act+'_VALUES.csv'))!=0:
            st.dataframe(companies_bio[companies_bio['CIK'] == cik_act])
            df = pd.read_csv(r'values\CIK'+cik_act+'_VALUES.csv')
            #Fill Null Values Strategically
            df['Date'] = df['Unnamed: 0']
            
            
            
            df.index = pd.to_datetime(df['Date'], format="%B %Y")
        
            for col in ['OperatingExpenses','ResearchAndDevelopmentExpense','SellingGeneralAndAdministrativeExpense','NetIncomeLoss','Assets','AssetsCurrent','AssetsNoncurrent']:
                if col not in df.columns:
                    df[col] = [None]*len(df)
            c1, c2, c3 = st.columns(3)
            with c1:
                fig = lineplot(df,'OperatingExpenses')
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig = areaplot(df,['ResearchAndDevelopmentExpense','SellingGeneralAndAdministrativeExpense'])
                st.plotly_chart(fig, use_container_width=True)
            with c3:
                fig = lineplot(df,'NetIncomeLoss')
                st.plotly_chart(fig, use_container_width=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                fig = lineplot(df,'Assets')
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig = lineplot(df,'AssetsCurrent')
                st.plotly_chart(fig, use_container_width=True)
            with c3:
                fig = lineplot(df,'AssetsNoncurrent')
                st.plotly_chart(fig, use_container_width=True)
            
            burnrate(df)
                
            
            
    if select == 'Implementation':
        pass 

CURRENT_THEME = 'light'
st.set_page_config(layout='wide',page_title='Cash Flow')
st.title("Company Facts")

over_theme = {'txc_inactive': '#FFFFFF','menu_background':'purple','txc_active':'black','option_active':'white'}
#over_theme = {'txc_inactive': '#FFFFFF'}
m1 = []
                                                                                                                                                                                               
menu_id = hc.nav_bar(menu_definition=m1,home_name='Home',override_theme=over_theme,hide_streamlit_markers=False) 
normal(menu_id)




