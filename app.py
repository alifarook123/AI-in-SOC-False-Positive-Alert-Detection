import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.set_page_config(page_title="Streamlit Demo", page_icon="✨", layout="wide")
st.title("✨ Streamlit Demo")

# Sidebar controls
st.sidebar.header("Controls")
n = st.sidebar.slider("Number of points", 10, 1000, 200, step=10)
show_map = st.sidebar.checkbox("Show map (pydeck)", value=True)

# Random data & chart
rng = np.random.default_rng(42)
df = pd.DataFrame({
    "x": np.arange(n),
    "y": rng.normal(loc=0, scale=1, size=n).cumsum()
})
st.subheader("Line chart")
st.line_chart(df, x="x", y="y")

# File upload
st.subheader("Upload a CSV")
csv = st.file_uploader("Choose a CSV file", type=["csv"])
if csv:
    user_df = pd.read_csv(csv)
    st.write("Preview:", user_df.head())
    st.bar_chart(user_df.select_dtypes(include=[np.number]).iloc[:, :1])

# Pydeck map (uses your pydeck config)
if show_map:
    st.subheader("Pydeck Map")
    # Austin-ish random points
    base_lat, base_lon = 30.2672, -97.7431
    map_df = pd.DataFrame({
        "lat": base_lat + (rng.random(n) - 0.5) * 0.2,
        "lon": base_lon + (rng.random(n) - 0.5) * 0.2,
        "value": rng.integers(1, 10, size=n)
    })

    layer = pdk.Layer(
        "HexagonLayer",
        data=map_df,
        get_position='[lon, lat]',
        radius=1000,
        elevation_scale=50,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
    )
    view_state = pdk.ViewState(latitude=base_lat, longitude=base_lon, zoom=8, pitch=40)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text":"Value: {value}"}))

st.caption("Tip: edit this file and the app hot-reloads automatically.")

