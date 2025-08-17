import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import Fullscreen
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from utide import solve, reconstruct

# ── Page Configuration ──────────────────────────────
st.set_page_config(page_title="🌊 Tsunami Monitoring Dashboard", layout="wide")
st.title("🌐 Integrated Tsunami Monitoring & Modeling")

# ── Tab Layout ──────────────────────────────────────
# ── Tab Layout (updated to include Tab6) ─────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📍 DART & IOC Monitoring", 
    "📊 Tsunami Analysis - DART", 
    "📈 Tsunami Analysis - Tide Gauge", 
    "🌀 Forward Tsunami Model", 
    "🔁 Inversion Tsunami Model",
    "🌬️ Volcano Lamb Wave Traveltime"
])
# ── Tab 1 ────────────────────────────────────────────
with tab1:
    st.header("📍 Real-Time Tsunami Buoy & Sea Level Station Monitoring")

    def load_station_ids(filepath="dart_code.txt"):
        try:
            with open(filepath, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            st.error(f"Failed to load station IDs from {filepath}: {e}")
            return []

    station_ids = load_station_ids()

    #station_ids = [
    #    "21413", "21414", "21415", "21416", "21417", "21418", "21419", "21420", 
    #    "32D12", "32D13", "43412", "43413", "46401", "46402", "46403"
    #]

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

    import math

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat/2)**2 +
             math.cos(math.radians(lat1)) *
             math.cos(math.radians(lat2)) *
             math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # 🌋 Kamchatka Earthquake Epicenter 52.512°N 160.324°E
    eq_lat = 52.512
    eq_lon = 160.324
    signed = "📌 Kamchatka Earthquake Epicenter"

    # ➡️ Find closest DART buoys
    df_dart["distance_km"] = df_dart.apply(lambda row: haversine(eq_lat, eq_lon, row["lat"], row["lon"]), axis=1)
    df_dart_closest = df_dart.nsmallest(15, "distance_km")

    # ➡️ Find closest IOC stations
    df_ioc["distance_km"] = df_ioc.apply(lambda row: haversine(eq_lat, eq_lon, row["lat"], row["lon"]), axis=1)
    df_ioc_closest = df_ioc.nsmallest(15, "distance_km")

    # 🌐 Tsunami wave speed in deep ocean (approximate)
    tsunami_speed_mps = 195  # meters per second

    # 🕒 Origin time of the Kamchatka earthquake (example)
    from datetime import datetime, timedelta
    eq_time = datetime.strptime("2025-07-29 23:24:52", "%Y-%m-%d %H:%M:%S")  # UTC

    def estimate_arrival_time(distance_km):
        travel_time_sec = (distance_km * 1000) / tsunami_speed_mps
        return eq_time + timedelta(seconds=travel_time_sec)

    # ⏱️ Add arrival time to DART and IOC stations
    df_dart_closest["arrival_time"] = df_dart_closest["distance_km"].apply(estimate_arrival_time)
    df_ioc_closest["arrival_time"] = df_ioc_closest["distance_km"].apply(estimate_arrival_time)

    st.subheader("🛰️ NDBC DART Tsunami Buoys (Live Coordinates)")
    tiles = "https://services.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}"
    m1 = folium.Map(location=[0, 180], zoom_start=2, tiles=tiles, attr="ESRI")
    Fullscreen(position="topright").add_to(m1)

    # 📍 Epicenter Marker
    folium.Marker(
        location=[eq_lat, eq_lon],
        popup=signed,
        icon=folium.Icon(color="red", icon="glyphicon-screenshot")
    ).add_to(m1)

    for _, buoy in df_dart.iterrows():
        folium.Marker(
            location=[buoy["lat"], buoy["lon"]],
            popup=f"{buoy['name']} ({buoy['station']})",
            icon=folium.Icon(color="orange", icon="info-sign")
        ).add_to(m1)
    folium_static(m1)
    st.markdown("#### 📋 15 DART Buoys Closest to Earthquake")
    #st.dataframe(df_dart)
    df_dart_closest.index = range(1, len(df_dart_closest)+1)
    st.dataframe(df_dart_closest)
    
    st.subheader("🌍 IOC Sea Level Monitoring Stations")
    
    m2 = folium.Map(location=[0, 180], zoom_start=2, tiles=tiles, attr="ESRI")
    Fullscreen(position="topright").add_to(m2)

    # 📍 Epicenter Marker
    folium.Marker(
        location=[eq_lat, eq_lon],
        popup=signed,
        icon=folium.Icon(color="red", icon="glyphicon-screenshot")
    ).add_to(m2)

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
    st.markdown("#### 📋 15 IOC Station Closest to Earthquake")
    #st.dataframe(df_ioc)
    df_ioc_revised = df_ioc_closest.copy()
    df_ioc_revised.rename(columns={"code": "station"}, inplace=True)
    df_ioc_revised["location_country"] = df_ioc_revised["location"] + " - " + df_ioc_revised["country"]
    df_ioc_revised = df_ioc_revised[["station", "lat", "lon", "location_country", "distance_km", "arrival_time"]]
    df_ioc_revised.index = range(1, len(df_ioc_revised)+1)
    st.dataframe(df_ioc_revised)

# ── Tab 2: Tsunami Analysis ─────────────────────────────
import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup

with tab2:
    st.header("🌊 DART Buoy Detiding Around Earthquake")
    st.markdown("Displays detided data from the 15 closest DART stations surrounding epicenter.")

    eq_time = datetime.strptime("2025-07-29 23:24:52", "%Y-%m-%d %H:%M:%S")  # UTC
    dart_start = "2025-07-29"
    dart_end = "2025-07-30"
    zoom_start = eq_time - pd.Timedelta(hours=4*24)
    zoom_end = eq_time + pd.Timedelta(hours=1*24)

    for _, row in df_dart_closest.sort_values("distance_km").head(15).iterrows():
        station = row["station"]
        url = f"https://www.ndbc.noaa.gov/station_page.php?station={station}&type=1&startdate={dart_start}&enddate={dart_end}"

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            h1_tag = soup.find("h1")
            title = h1_tag.text.strip() if h1_tag else f"DART {station}"
            script = soup.find("script", string=re.compile("currentstnid"))
            script_text = script.string if script else ""
            lat_match = re.search(r"currentstnlat\s*=\s*['\"](.*?)['\"]", script_text)
            lng_match = re.search(r"currentstnlng\s*=\s*['\"](.*?)['\"]", script_text)
            lat = float(lat_match.group(1)) if lat_match else 0.0
            lon = float(lng_match.group(1)) if lng_match else 0.0

            textarea = soup.find("textarea", attrs={"name": "data"})
            if not textarea:
                st.warning(f"⚠️ No data found for {station}")
                continue

            lines = textarea.text.strip().splitlines()[2:]
            parsed = [line.split() for line in lines if len(line.split()) == 8]
            df = pd.DataFrame(parsed, columns=['year','month','day','hour','minute','second','T','HEIGHT'])
            df = df.astype({'year':int, 'month':int, 'day':int, 'hour':int, 'minute':int, 'second':int, 'T':int, 'HEIGHT':float})
            df['datetime'] = pd.to_datetime(df[['year','month','day','hour','minute','second']])
            df.sort_values('datetime', inplace=True)

            df_window = df.copy()

            # Polynomial detiding
            timestamps = (df_window['datetime'] - df_window['datetime'].min()).dt.total_seconds().values
            heights = df_window['HEIGHT'].values

            # Fit high-order polynomial (e.g., degree 10)
            degree = 30
            poly_coeffs = np.polyfit(timestamps, heights, deg=degree)
            poly_func = np.poly1d(poly_coeffs)
            predicted_tide = poly_func(timestamps)

            df_window['predicted_tide'] = predicted_tide
            df_window['detrended'] = df_window['HEIGHT'] - predicted_tide

            # Plotting
            st.markdown(f"### 🌐 Station: {station} ({title})")
            fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

            axs[0].plot(df_window['datetime'], df_window['HEIGHT'], label='Observed', color='blue')
            axs[0].plot(df_window['datetime'], df_window['predicted_tide'], label=f'Poly Fit (deg={degree})', color='green', linestyle='--')
            axs[0].set_ylabel("Height (m)")
            axs[0].legend()
            axs[0].grid(True)

            axs[1].plot(df_window['datetime'], df_window['detrended'], label='Detided Signal', color='red')
            axs[1].axhline(0, color='black', linestyle='--')
            axs[1].set_xlabel("Datetime")
            axs[1].set_ylabel("Anomaly (m)")
            axs[1].legend()
            axs[1].grid(True)

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Error processing station {station}: {e}")

# ── Tab 3 ────────────────────────────────────────────
with tab3:
    st.header("📈 IOC Tide Gauge Detiding Around Kamchatka Event")
    st.markdown("Shows detided tide gauge plots from the 15 closest IOC stations using latest 1-days data window.")

    fixed_endtime = "2025-07-30T12:00"  # Set your target UTC endtime
    for _, row in df_ioc_closest.sort_values("distance_km").head(15).iterrows():
        selected_code = row["code"]

        try:
            # --- Fetch Tide Data ---
            data_url = f"https://www.ioc-sealevelmonitoring.org/bgraph.php?code={selected_code}&output=tab&period=1.0&endtime={fixed_endtime}"
            soup_data = BeautifulSoup(requests.get(data_url).content, "html.parser")
            rows = soup_data.find_all("tr")

            timestamps, levels = [], []
            for row_data in rows:
                cols = row_data.find_all("td")
                if len(cols) == 2:
                    try:
                        t = datetime.strptime(cols[0].text.strip(), "%Y-%m-%d %H:%M:%S")
                        timestamps.append(t)
                        levels.append(float(cols[1].text.strip()))
                    except:
                        continue

            if not timestamps:
                st.warning(f"⚠️ No tide data found for {selected_code}")
                continue

            # --- Metadata Extraction ---
            meta_url = f"https://www.ioc-sealevelmonitoring.org/station.php?code={selected_code}&period=0.5&endtime={fixed_endtime}"
            soup_meta = BeautifulSoup(requests.get(meta_url).content, "html.parser")

            def parse_coord(label):
                td_label = soup_meta.find("td", class_="field", string=lambda text: text and label in text)
                td_value = td_label.find_next_sibling("td", class_="nice")
                return float(td_value.text.strip()) if td_value else None

            lat = parse_coord("Latitude")
            lon = parse_coord("Longitude")

            # --- Detiding ---
            time_hours = np.array([(t - timestamps[0]).total_seconds() / 3600 for t in timestamps])
            levels_array = np.array(levels)
            coef = solve(time_hours, levels_array, lat=lat, method='ols', constit='auto')
            recon = reconstruct(time_hours, coef)
            detided = levels_array - recon.h

            # --- Plotting ---
            st.markdown(f"### 🏷️ Station: `{selected_code}` 🌐 Location: ({lat}, {lon})")
            fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

            axs[0].plot(timestamps, levels_array, label='Observed', color='royalblue')
            axs[0].plot(timestamps, recon.h, label='Predicted Tide', color='limegreen', linestyle='--')
            axs[0].set_ylabel("PWL (m)")
            axs[0].legend()
            axs[0].grid(True)

            axs[1].plot(timestamps, detided, label='Detided Signal', color='crimson')
            axs[1].axhline(0, color='black', linestyle='--')
            axs[1].set_xlabel("UTC Time")
            axs[1].set_ylabel("Residual (m)")
            axs[1].legend()
            axs[1].grid(True)

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Error processing IOC station `{selected_code}`: {e}")


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


# ── Tab 6: Lamb Wave Simulation ─────────────────────
with tab6:
    st.header("🌬️ Surface Elevation Response to Atmospheric Lamb Wave")

    # Simulation Parameters
    P0 = 1200.0
    spread = 600.0
    c_lamb = 320.0
    rho_w = 1025.0
    decay_scale = 500 * 1000

    source_lat = st.sidebar.number_input("Source Latitude", value=-12.9)
    source_lon = st.sidebar.number_input("Source Longitude", value=45.7)
    source_coord = (source_lat, source_lon)

    # Region of Interest
    lat_min, lat_max = -60.0, 40.0
    lon_min, lon_max = 10.0, 160.0

    # Load Bathymetry Dataset
    import xarray as xr
    import numpy as np
    from haversine import haversine
    from cartopy import geodesic
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from matplotlib.colors import Normalize

    try:
        ds = xr.open_dataset(f"./resampled_bathymetry_5min.nc")
        depth = ds["resampled_elevation"].sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max))
        lat = depth["lat"].values
        lon = depth["lon"].values
    except:
        st.error("❌ Failed to load `resampled_bathymetry_5min.nc`. Please check the path or file format.")
        st.stop()

    # Distance Grid Calculation
    distance_grid = np.zeros(depth.shape)
    for i in range(len(lat)):
        for j in range(len(lon)):
            distance_grid[i, j] = haversine(source_coord, (lat[i], lon[j])) * 1000
    distance_km_grid = distance_grid / 1000

    # Simulate Wave Response
    st.info("🌀 Simulating surface elevation...")
    t = np.linspace(0, 86400, 480)
    eta_cube = np.zeros((len(t), *depth.shape))

    for k, t_now in enumerate(t):
        position = t_now * c_lamb
        decay = np.exp(-distance_grid / decay_scale)
        pulse = P0 * np.exp(-((distance_grid - position)**2) / (2 * (spread * c_lamb)**2))
        pressure = pulse * decay
        eta_cube[k] = pressure / (rho_w * 9.81) * 100  # Convert to cm

    # Max Elevation Plot
    max_eta = np.max(eta_cube, axis=0)
    max_distance_km = 12000
    masked_eta = np.ma.masked_where((max_eta < 0.001) | (distance_km_grid > max_distance_km), max_eta)

    st.subheader("🗺️ Maximum Surface Elevation Map")
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={"projection": ccrs.PlateCarree()})
    ax.set_extent([lon_min, lon_max, lat_min, lat_max])
    ax.add_feature(cfeature.NaturalEarthFeature("physical", "coastline", "10m", edgecolor="black", facecolor="none", linewidth=0.8))
    ax.add_feature(cfeature.BORDERS, linestyle=":", edgecolor="gray")
    ax.gridlines(draw_labels=True)

    levels = np.linspace(0.001, np.nanmax(masked_eta), 60)
    contour = ax.contourf(lon, lat, masked_eta, levels=levels, transform=ccrs.PlateCarree(),
                          cmap="viridis", extend="max", alpha=0.9)
    plt.colorbar(contour, ax=ax, orientation="vertical", pad=0.05,
                 label="Max Surface Elevation (cm)")

    # Travel Time Rings
    for hour in range(1, 10):
        radius_km = int(hour * 3600 * c_lamb / 1000)
        ring = geodesic.Geodesic().circle(lon=source_coord[1], lat=source_coord[0], radius=radius_km * 1000, n_samples=360)
        ax.plot(ring[:, 0], ring[:, 1], color="gray", linestyle=":", linewidth=0.6, transform=ccrs.PlateCarree())
        for idx in [0, 135, 225]:
            ring_lon, ring_lat = ring[idx]
            offset = {"x": 0.5 if idx == 135 else -0.5 if idx == 225 else 0.5, "y": -0.5 if idx in [135, 225] else 0}
            if lon_min < ring_lon < lon_max and lat_min < ring_lat < lat_max:
                ax.text(ring_lon + offset["x"], ring_lat + offset["y"], f"{hour} hr",
                        transform=ccrs.PlateCarree(), fontsize=7, color="gray",
                        bbox=dict(facecolor="white", edgecolor="none", alpha=0.5, boxstyle="round"))

    ax.set_title("Maximum Surface Elevation from Atmospheric Lamb Wave\n(Fani Maoré Event at 320 m/s)")
    plt.tight_layout()
    st.pyplot(fig)
