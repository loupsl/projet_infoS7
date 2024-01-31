import plotly.graph_objs as go
import streamlit as st 


blue_palette = ["#D6EAF8", "#AED6F1", "#5DADE2", "#2E86C1", "#1B4F72"]

legend = go.Figure(data=[go.Bar(
    x=[1, 2, 3, 4, 5],
    y=[1, 1, 1, 1, 1],
    marker_color=blue_palette,
    marker_line_color=blue_palette,
    marker_line_width=1, 
    width=[0.5]*5  
)])
legend.update_layout(
    xaxis=dict(
        tickvals=[1, 2, 3, 4, 5],
        ticktext=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5'],
        tickmode='array',
        showgrid=False,
        showticklabels=True,
        tickfont=dict(size=10),
        range=[0.5, 5.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        showline=False,
        zeroline=False
    ),
    barmode='overlay',
    plot_bgcolor='white',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=20, b=20), 
    height=50,  # adjust height 
    width=400  
)
legend.update_layout(showlegend=False)

st.plotly_chart(legend)
