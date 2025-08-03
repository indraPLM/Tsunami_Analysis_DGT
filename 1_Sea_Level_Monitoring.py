import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from utide import solve, reconstruct

# ── Page Configuration ──────────────────────────────
st.set_page_config(page_title="🌊 Tsunami Monitoring Dashboard", layout="wide")
st.title("🌐 Integrated Tsunami Monitoring & Modeling")

# ── Tab Layout ──────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 DART & IOC Monitoring", 
    "📊 Tsunami Analysis - DART", 
    "📈 Tsunami Analysis - Tide Gauge", 
    "🌀 Forward Tsunami Model", 
    "🔁 Inversion Tsunami Model"
])

# ── Tab 1 ────────────────────────────────────────────
with tab1:
    st.header("📍 Real-Time Tsunami Buoy & Sea Level Station Monitoring")

    station_ids = [
        "21413", "21414", "21415", "21416", "21417", "21418", "21419", "21420", 
        "32D12", "32D13", "43412", "43413", "46401", "46402", "46403"
    ]

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

    df_dart = fetch_dart_metadata_v2(station_ids)

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
    status_colors = {"online": "green", "offline": "red"}

    st.subheader("🛰️ NDBC DART Tsunami Buoys (Live Coordinates)")
    m1 = folium.Map(location=[0, 160], zoom_start=2, tiles="CartoDB positron")
    for _, buoy in df_dart.iterrows():
        folium.Marker(
            location=[buoy["lat"], buoy["lon"]],
            popup=f"{buoy['name']} ({buoy['station']})",
            icon=folium.Icon(color="orange", icon="info-sign")
        ).add_to(m1)
    folium_static(m1)

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

    st.markdown("#### 📋 DART Buoy Metadata")
    st.dataframe(df_dart)

    st.markdown("#### 📋 IOC Station Metadata")
    st.dataframe(df_ioc)

# ── Tab 2 ────────────────────────────────────────────
import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import re
from bs4 import BeautifulSoup
from utide import solve, reconstruct
from matplotlib.backends.backend_pdf import PdfPages

# 📡 DART station list
station_numbers = [
    "21416", "21415", "21414", "21419", "21418", "21413", "21420",
    "52402", "46413", "46408", "46402", "46403", "51425"
]

# 📅 Date range
start_date = "2025-07-29"
end_date = "2025-07-31"

# 📄 Output PDF path
output_pdf_path = "dart_station_graphs_compiled.pdf"

# 🖼️ PDF compilation
with PdfPages(output_pdf_path) as pdf:
    for station_id in station_numbers:
        print(f"🔄 Processing station {station_id}...")

        # --- Step 1: Fetch NOAA Buoy Page ---
        url = f"https://www.ndbc.noaa.gov/station_page.php?station={station_id}&type=1&startdate={start_date}&enddate={end_date}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # --- Step 2: Extract Metadata ---
        h1_tag = soup.find("h1")
        station_title = h1_tag.text.strip() if h1_tag else f"DART {station_id}"

        script_tag = soup.find("script", string=re.compile("currentstnid"))
        script_text = script_tag.string if script_tag else ""
        lat_match = re.search(r"currentstnlat\s*=\s*['\"](.*?)['\"]", script_text)
        lng_match = re.search(r"currentstnlng\s*=\s*['\"](.*?)['\"]", script_text)
        lat = float(lat_match.group(1)) if lat_match else 0.0
        lng = float(lng_match.group(1)) if lng_match else 0.0

        # --- Step 3: Extract Observational Data ---
        textarea = soup.find("textarea", attrs={"name": "data"})
        if not textarea:
            print(f"⚠️ No data found for station {station_id}")
            continue

        lines = textarea.text.strip().splitlines()[2:]
        parsed = [line.split() for line in lines if len(line.split()) == 8]
        df = pd.DataFrame(parsed, columns=['year','month','day','hour','minute','second','T','HEIGHT'])
        df = df.astype({'year':int, 'month':int, 'day':int, 'hour':int,
                        'minute':int, 'second':int, 'T':int, 'HEIGHT':float})
        df['datetime'] = pd.to_datetime(df[['year','month','day','hour','minute','second']])
        df.sort_values('datetime', inplace=True)
        df.reset_index(drop=True, inplace=True)

        # --- Step 4: Tidal Prediction & Detiding ---
        time_array = np.array(df['datetime'].to_list())
        coef = solve(time_array, df['HEIGHT'].values, lat=lat, method='ols', conf_int='MC')
        recon = reconstruct(time_array, coef)
        df['predicted_tide'] = recon.h
        df['detrended'] = df['HEIGHT'] - df['predicted_tide']

        # --- Step 5: Plot Full Time Series ---
        fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        axs[0].plot(df['datetime'], df['HEIGHT'], label='Observed HEIGHT', color='blue')
        axs[0].plot(df['datetime'], df['predicted_tide'], label='Predicted Tide', color='green', linestyle='--')
        axs[0].set_title(f"{station_title}\nObserved vs. Predicted Tidal Height (Lat: {lat}, Lon: {lng})")
        axs[0].set_ylabel("Height (m)")
        axs[0].legend()
        axs[0].grid(True)

        axs[1].plot(df['datetime'], df['detrended'], label='Detided Signal', color='red')
        axs[1].axhline(0, color='black', linestyle='--')
        axs[1].set_title(f"{station_title}\nDetided Anomaly Signal")
        axs[1].set_xlabel("DateTime")
        axs[1].set_ylabel("Anomaly Height (m)")
        axs[1].legend()
        axs[1].grid(True)

        plt.xticks(rotation=45)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        # --- Step 6: Plot 12-Hour Isolated Window ---
        start_time = pd.Timestamp("2025-07-29 23:00:00")
        end_time = start_time + pd.Timedelta(hours=12)
        df_window = df[(df['datetime'] >= start_time) & (df['datetime'] <= end_time)]

        fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        axs[0].plot(df_window['datetime'], df_window['HEIGHT'], label='Observed HEIGHT', color='blue')
        axs[0].plot(df_window['datetime'], df_window['predicted_tide'], label='Predicted Tide', color='green', linestyle='--')
        axs[0].set_title(f"{station_title}\nObserved vs. Predicted Tidal Height\n{start_time} to {end_time}")
        axs[0].set_ylabel("Height (m)")
        axs[0].legend()
        axs[0].grid(True)

        axs[1].plot(df_window['datetime'], df_window['detrended'], label='Detided Signal', color='red', linestyle=':')
        axs[1].axhline(0, color='black', linestyle='--', linewidth=0.8)
        axs[1].set_title("Detided Anomaly Signal")
        axs[1].set_xlabel("DateTime")
        axs[1].set_ylabel("Anomaly Height (m)")
        axs[1].legend()
        axs[1].grid(True)

        plt.xticks(rotation=45)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

print(f"✅ All station plots compiled into: {output_pdf_path}")

# ── Tab 3 ────────────────────────────────────────────
with tab3:
    st.header("📈 Tsunami Analysis Using Tide Gauge Data")
    uploaded_file = st.file_uploader("Upload Tide Gauge Data (CSV)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        time_col = st.selectbox("Time Column", options=df.columns)
        height_col = st.selectbox("Water Level Column", options=df.columns)
        st.subheader("Harmonic Analysis (UTide)")
        coef = solve(df[time_col], df[height_col], lat=0, method='ols')
        tide, _ = reconstruct(df[time_col], coef)
        fig, ax = plt.subplots(2, 1)
        ax[0].plot(df[time_col], df[height_col], label="Observed")
        ax[0].plot(df[time_col], tide, label="Predicted", alpha=0.6)
        ax[0].legend()
        ax[0].set_title("Observed vs Predicted Tide")
        anomaly = df[height_col] - tide
        ax[1].plot(df[time_col], anomaly, color="red")
        ax[1].set_title("Tsunami Signal (Anomaly)")
        st.pyplot(fig)

# ── Tab 4 ────────────────────────────────────────────
with tab4:
    st.header("🌀 Forward Tsunami Propagation Model")
    st.markdown("Input fault geometry to simulate tsunami wave propagation.")
    length = st.slider("Fault Length (km)", 10, 200, 100)
    width = st.slider("Fault Width (km)", 10, 100, 50)
    slip = st.slider("Slip Amount (m)", 0.1, 20.0, 2.0)
    depth = st.slider("Depth (km)", 5, 50, 20)
    st.button("Run Simulation")
    st.info("🖼️ Simulation results would be visualized here.")

# ── Tab 5 ────────────────────────────────────────────
with tab5:
    st.header("🔁 Tsunami Source Inversion")
    uploaded_file = st.file_uploader("Upload Tide Gauge Observations (CSV)", type=["csv"])
