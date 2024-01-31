import plotly.express as px
import pandas as pd
import streamlit as st

def plot_graphGIIHDI():
    hdi_gii_merged = pd.read_csv("hdi_gii_merged_data.csv")

    fig = px.scatter(hdi_gii_merged, 
                    y='GII', 
                    x='HDI_2021', 
                    text='Label', 
                    title='Scatter plot of GII vs. HDI',
                    labels={'GII':'GII Value', 'HDI_2021':'HDI Value'})

    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=False, 
                    xaxis_title="HDI Value", 
                    yaxis_title="GII Value",
                    title_x=0.5, 
                    height=600, 
                    width=800)

    fig.add_vline(x=0.73, line_width=2, line_dash="dash", line_color="red")
    fig.add_hline(y=0.38, line_width=2, line_dash="dash", line_color="red")
    fig.add_vrect(x0=0.73, x1=1, y0=0.46, y1=1, 
                annotation_text="HDI > 0.73, GII > 0.38", annotation_position="top left",
                fillcolor="green", opacity=0.25, line_width=0)


    st.plotly_chart(fig) 



