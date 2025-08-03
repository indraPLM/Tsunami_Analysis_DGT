import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import requests
from bs4 import BeautifulSoup
import re

# ── Page Configuration ──────────────────────────────
st.set_page_config(page_title="Global Monitoring Maps", layout="wide")
st.title("🌊 Tsunami Buoys & IOC Sea Level Monitoring Stations")

# ── Station IDs for DART Buoys ─────────────────────
station_ids = [
    "21413", "21414", "21415", "21416", "21417", "21418", "21419", "21420", 
    "32D12", "32D13", "43412", "43413", "46401", "46402", "46403"
]  # Add more IDs as needed

@st.cache_data(show_spinner="📡 Fetching DART Buoy Metadata...")
def fetch_dart_metadata_v2(station_ids, startdate="2025-07-29", enddate="2025-07-31"):
    base_url = "https://www.ndbc.noaa.gov/station_page.php"
    buoy_data = []

    for station in station_ids:
        try:
            params = {
                "station": station,
                "type": "1",
                "startdate": startdate,
                "enddate": enddate
            }
            response = requests.get(base_url, params=params, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract <script> tag containing station metadata
            script_tag = soup.find("script", string=re.compile("currentstnid"))
            script_text = script_tag.string if script_tag else ""

            metadata = {}
            for key in ['currentstnid', 'currentstnlat', 'currentstnlng', 'currentstnname']:
                match = re.search(f"{key}\\s*=\\s*['\"](.*?)['\"]", script_text)
                if match:
                    metadata[key] = match.group(1)

            lat = float(metadata.get("currentstnlat", 0))
            lng = float(metadata.get("currentstnlng", 0))
            buoy_name = metadata.get("currentstnname", f"Buoy {station}")

            if lat != 0 and lng != 0:
                buoy_data.append({
                    "station": station,
                    "name": buoy_name,
                    "lat": lat,
                    "lon": lng
                })

        except Exception:
            continue

    return pd.DataFrame(buoy_data)


df_dart = fetch_dart_metadata(station_ids)

# ── Scrape IOC Station Metadata ─────────────────────
@st.cache_data
def fetch_ioc_data():
    url = "https://www.ioc-sealevelmonitoring.org/list.php?operator=&showall=a&output=contacts"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find_all("tr")
    data = []

    for row in rows:
        cells = row.find_all("td", class_="nice")
        if len(cells) >= 9:
            try:
                code = cells[0].text.strip()
                lat = float(cells[2].text.strip())
                lon = float(cells[3].text.strip())
                country = cells[4].text.strip()
                location = cells[5].text.strip()
                method = cells[6].text.strip()
                operator = cells[7].text.strip()
                status = "online" if "open" in cells[8].text.lower() else "offline"
                data.append({
                    "code": code,
                    "lat": lat,
                    "lon": lon,
                    "country": country,
                    "location": location,
                    "method": method,
                    "operator": operator,
                    "status": status
                })
            except Exception:
                continue
    return pd.DataFrame(data)

df_ioc = fetch_ioc_data()

# ── Map Colors ──────────────────────────────────────
status_colors = {"online": "green", "offline": "red"}

# ── Layout: Two Columns ─────────────────────────────
col1, col2 = st.columns(2)

# ── Map 1: DART Buoys ───────────────────────────────
with col1:
    st.subheader("🛰️ NDBC DART Tsunami Buoys (Live Coordinates)")
    m1 = folium.Map(location=[0, 160], zoom_start=2, tiles="CartoDB positron")
    for _, buoy in df_dart.iterrows():
        folium.Marker(
            location=[buoy["lat"], buoy["lon"]],
            popup=f"{buoy['name']} ({buoy['station']})",
            icon=folium.Icon(color="orange", icon="info-sign")
        ).add_to(m1)
    folium_static(m1)

# ── Map 2: IOC Sea Level Monitoring ─────────────────
with col2:
    st.subheader("🌍 IOC Sea Level Monitoring Stations")
    m2 = folium.Map(location=[0, 0], zoom_start=2, tiles="CartoDB positron")
    for _, station in df_ioc.iterrows():
        color = status_colors.get(station["status"], "gray")
        popup_text = f"{station['location']}, {station['country']}<br>Lat: {station['lat']}, Lon: {station['lon']}<br>Status: {station['status'].capitalize()}<br>Method: {station['method']}"
        folium.CircleMarker(
            location=[station["lat"], station["lon"]],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(m2)
    folium_static(m2)

# ── Optional Data Preview ───────────────────────────
st.markdown("#### 📋 DART Buoy Metadata")
st.dataframe(df_dart)

st.markdown("#### 📋 IOC Station Metadata")
st.dataframe(df_ioc)
