import numpy as np
import plotly
import plotly.graph_objects as go
import plotly.express as px

def Ambiguity_2D(ambiguity,smooth=0.85):
    z = np.absolute(ambiguity)
    N,M = z.shape
    
    x=np.linspace(-1,1,M)
    fig = px.imshow(np.absolute(z))
    
    fig.show()

    fig = go.Figure(data =
        go.Contour(
            z = np.absolute(z),
            x = x,
            line_smoothing = smooth
        ))
    fig.show();

def slice_in_time(ambiguity):
    z = np.absolute(ambiguity)
    N,M = z.shape

    # Create figure
    fig = go.Figure()

    # Add slices for time delay
    for idx in range(0,N-1):
        fig.add_trace(
            go.Scatter(
                visible=False,
                line=dict(color="#00CED1", width=3),
                x=np.linspace(-1,1,M),
                y=z[idx,:],
            ))

    # Make the N/2 delay slice visible
    fig.data[int(N/2)].visible = True

    # Create and add slider
    steps = []

    for i in range(len(fig.data)):
        step = dict(
            method="restyle",
            label=str(i),
            args=["visible", [False] * len(fig.data)],
        )
        step["args"][1][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=int(N/2),
        currentvalue={"prefix": "Delay (samples): "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        title='Ambiguity Function Sliced in time: X(T=T<sub>0</sub>, f)',
        sliders=sliders
    )

    fig.show();

def slice_in_doppler(ambiguity):
    z = np.absolute(ambiguity)
    N,M = z.shape

    # Create figure
    fig = go.Figure()

    # Add slices for doppler shift
    for idx in range(0,M-1):
        fig.add_trace(
            go.Scatter(
                visible=False,
                line=dict(color="#00CED1", width=3),
                x=np.linspace(0,N-1,N),
                y=z[:,idx],
            ))

    # Make the M/2 doppler slice visible
    fig.data[int(M/2)].visible = True

    # Create and add slider
    steps = []

    for i in range(len(fig.data)):
        step = dict(
            method="restyle",
            label=str(i),
            args=["visible", [False] * len(fig.data)],
        )
        step["args"][1][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=int(M/2),
        currentvalue={"prefix": "Doppler (Frequency Index): "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        title='Ambiguity Function Sliced in doppler: X(T, f=f<sub>0</sub>)',
        sliders=sliders
    )

    fig.show();
