import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from ambiguity_function import ambiguity_function2
from ambiguity_function import ambiguity_function

def compute_ambiguity(pulse,N,M,fs,title,renderer='notebook',colorscale = px.colors.sequential.Plasma, fig_size = 800):
    #'browser' 
    #px.colors.sequential.Plasma
    #px.colors.sequential.thermal
    #px.colors.sequential.Jet
    #px.colors.sequential.haline
    z = ambiguity_function(pulse,N,M,fs)
    z_mag = np.absolute(z)
    sh_0, sh_1 = z_mag.shape
    #print(z_mag.shape)
    
    x, y = np.linspace(0, sh_0, sh_0), np.linspace(-1, 1, sh_1)


    fig = go.Figure(data=[go.Surface(z=z_mag,x=x,y=y,colorscale = colorscale)])

    fig.update_layout(title=title, autosize=True,
                        width=800, height=800,
                        scene = dict(
                        xaxis_title='Delay (samples)',
                        yaxis_title='Doppler (rad/pi)',
                        zaxis_title='Ambiguity'))

    fig.show(renderer=renderer,width=fig_size, height=fig_size)
    
    return z

def compute_ambiguity2(pulse,title,renderer='notebook',colorscale = px.colors.sequential.Plasma, fig_size = 800):#browser' 
    #px.colors.sequential.Plasma
    #px.colors.sequential.thermal
    #px.colors.sequential.Jet
    #px.colors.sequential.haline
    z = ambiguity_function2(pulse,True)
    z_mag = np.absolute(z)
    sh_0, sh_1 = z_mag.shape
    #print(z_mag.shape)
    
    x, y = np.linspace(0, sh_0, sh_0), np.linspace(-1, 1, sh_1)


    fig = go.Figure(data=[go.Surface(z=z_mag,x=x,y=y,colorscale = colorscale)])

    fig.update_layout(title=title, autosize=True,
                        width=800, height=800,
                        scene = dict(
                        xaxis_title='Delay (samples)',
                        yaxis_title='Doppler (rad/pi)',
                        zaxis_title='Ambiguity'))

    fig.show(renderer=renderer,width=fig_size, height=fig_size)
    return z
