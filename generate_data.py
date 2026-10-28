"""Generate the course data in data/.

Five fictional hobby weather stations measure the 2023 weather in Belgium. Their
measurements are built from the real hourly observations of the nearest KMI
station, plus noise and a few sensor problems for you to discover.

Writes:
    data/raw/weather_export.csv     the half-hourly measurements, as the stations export them
    data/raw/hs01_hourly.csv        the hourly measurements of one station, as an online weather
                                    network exports them, in UTC
    data/raw/rain_logbook.xlsx      the volunteers' manual rain gauge readings
    data/checkpoints/*.parquet      cleaned versions, to start an exercise from
                                    when you did not finish the previous one; the hourly
                                    KMI sunshine is a separate file, for the API exercise

The KMI observations it starts from are in kmi/, in the repository, so no network is
needed. Delete that folder to fetch them again from the KMI open data service.

Run it from the root of the repository:

    uv run python generate_data.py
"""

from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from openpyxl import Workbook
from openpyxl.styles import Font

DATA = Path(__file__).parent / "data"
RAW = DATA / "raw"
CHECKPOINTS = DATA / "checkpoints"
KMI = Path(__file__).parent / "kmi"

KMI_URL = "https://opendata.meteo.be/service/ows"
YEAR = 2023
SEED = 2023
BATTERY_DRAIN = 0.003  # volt per half hour
BATTERY_CHARGE = 0.0011  # volt per minute of sunshine

# The hobby stations. Their flaws are not in the metadata, that would spoil the fun.
STATIONS = pd.DataFrame(
    [
        (
            "HS01",
            "Mechelen garden",
            51.031,
            4.482,
            9,
            "garden, 1.5 m above grass",
            "2021-04-17",
        ),
        (
            "HS02",
            "Gent rooftop",
            51.054,
            3.725,
            22,
            "flat roof, black bitumen",
            "2022-08-02",
        ),
        (
            "HS03",
            "Brugge schoolyard",
            51.209,
            3.225,
            8,
            "schoolyard fence",
            "2020-09-01",
        ),
        (
            "HS04",
            "Hasselt allotment",
            50.931,
            5.338,
            41,
            "allotment shed",
            "2019-05-30",
        ),
        (
            "HS05",
            "Durbuy cabin",
            50.353,
            5.456,
            205,
            "forest clearing, solar powered",
            "2022-11-12",
        ),
    ],
    columns=[
        "station",
        "name",
        "latitude",
        "longitude",
        "altitude_m",
        "mounting",
        "installed",
    ],
).assign(installed=lambda df: pd.to_datetime(df["installed"]))


def fetch_kmi(
    dataset: str, properties: list[str] | None = None, cql_filter: str | None = None
) -> pd.DataFrame:
    """Fetch one dataset from the KMI open data WFS service, as CSV."""
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeNames": dataset,
        "outputFormat": "csv",
    }
    if properties:
        params["propertyName"] = ",".join(properties)
    if cql_filter:
        params["CQL_FILTER"] = cql_filter
    response = requests.get(KMI_URL, params=params, timeout=120)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text))


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = (
        np.sin((lat2 - lat1) / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    )
    return 2 * 6371 * np.arcsin(np.sqrt(a))


def fetch_reference_data():
    """The KMI data the hobby stations are built from. Read from kmi/, or fetched when it is missing."""
    files = [
        KMI / name
        for name in (
            "kmi_stations.parquet",
            f"kmi_hourly_{YEAR}.parquet",
            f"kmi_daily_{YEAR}.parquet",
        )
    ]
    if all(file.exists() for file in files):
        print(f"Reading the KMI data in {KMI}")
        kmi_stations, hourly, daily = (pd.read_parquet(file) for file in files)
        return kmi_stations, nearest_kmi_station(kmi_stations), hourly, daily

    print("Fetching the KMI station list ...")
    kmi_stations = fetch_kmi("aws:aws_station")
    coords = (
        kmi_stations["the_geom"]
        .str.extract(r"POINT \((?P<latitude>[\d.]+) (?P<longitude>[\d.]+)\)")
        .astype(float)
    )
    kmi_stations = pd.concat(
        [kmi_stations[["code", "name", "altitude", "date_begin", "date_end"]], coords],
        axis=1,
    )
    kmi_stations = kmi_stations.rename(columns={"altitude": "altitude_m"})
    kmi_stations["date_begin"] = pd.to_datetime(kmi_stations["date_begin"])
    kmi_stations["date_end"] = pd.to_datetime(kmi_stations["date_end"])

    nearest = nearest_kmi_station(kmi_stations)
    codes = ",".join(str(code) for code in nearest["code"])

    print(f"Fetching hourly {YEAR} observations of KMI stations {codes} ...")
    hourly = fetch_kmi(
        "aws:aws_1hour",
        properties=[
            "code",
            "timestamp",
            "precip_quantity",
            "temp_dry_shelter_avg",
            "humidity_rel_shelter_avg",
            "sun_duration",
        ],
        cql_filter=f"code IN ({codes}) AND timestamp DURING {YEAR}-01-01T00:00:00Z/{YEAR + 1}-01-01T00:00:00Z",
    ).drop(columns="FID")
    hourly["timestamp"] = pd.to_datetime(hourly["timestamp"]).dt.tz_localize("UTC")
    # DURING includes both ends: drop the first hour of next year
    hourly = hourly[hourly["timestamp"] < pd.Timestamp(f"{YEAR + 1}-01-01", tz="UTC")]
    hourly = hourly.sort_values(["code", "timestamp"]).reset_index(drop=True)

    print(f"Fetching daily {YEAR} observations of all KMI stations ...")
    daily = fetch_kmi(
        "aws:aws_1day",
        properties=[
            "code",
            "timestamp",
            "precip_quantity",
            "temp_avg",
            "temp_min",
            "temp_max",
            "humidity_rel_shelter_avg",
            "wind_gusts_speed",
            "sun_duration",
        ],
        cql_filter=f"timestamp DURING {YEAR}-01-01T00:00:00Z/{YEAR + 1}-01-01T00:00:00Z",
    ).drop(columns="FID")
    daily["timestamp"] = pd.to_datetime(daily["timestamp"])
    daily = daily[daily["timestamp"] < f"{YEAR + 1}-01-01"]
    daily = daily.sort_values(["code", "timestamp"]).reset_index(drop=True)

    KMI.mkdir(exist_ok=True)
    for df, file in zip((kmi_stations, hourly, daily), files):
        df.to_parquet(file)
    print(f"Saved the KMI data in {KMI}")

    return kmi_stations, nearest, hourly, daily


def nearest_kmi_station(kmi_stations):
    # Only stations that measured during the whole year
    active = kmi_stations[
        (kmi_stations["date_begin"] <= f"{YEAR}-01-01")
        & (
            kmi_stations["date_end"].isna()
            | (kmi_stations["date_end"] >= f"{YEAR + 1}-01-01")
        )
    ]
    pairs = STATIONS.merge(active, how="cross", suffixes=("", "_kmi"))
    pairs["distance_km"] = haversine_km(
        pairs["latitude"],
        pairs["longitude"],
        pairs["latitude_kmi"],
        pairs["longitude_kmi"],
    )
    return pairs.loc[
        pairs.groupby("station")["distance_km"].idxmin(),
        ["station", "code", "altitude_m_kmi"],
    ]


def smooth_noise(rng, n, scale, memory=0.97):
    """Autocorrelated noise: a sensor error that wanders instead of jumping."""
    shocks = rng.normal(0, scale * np.sqrt(1 - memory**2), n)
    noise = np.empty(n)
    noise[0] = rng.normal(0, scale)
    for i in range(1, n):
        noise[i] = memory * noise[i - 1] + shocks[i]
    return noise


def simulate_station(rng, station, kmi):
    """Half-hourly 'true' measurements of one hobby station, in UTC and Celsius."""
    kmi = kmi.set_index("timestamp")
    index = pd.date_range(
        f"{YEAR}-01-01", f"{YEAR}-12-31 23:30", freq="30min", tz="UTC"
    )
    hours = (index - index[0]) / pd.Timedelta(hours=1)
    known = (kmi.index - index[0]) / pd.Timedelta(hours=1)

    def interp(column):
        values = kmi[column].astype(float)
        ok = values.notna().to_numpy()
        return np.interp(hours, known[ok], values[ok])

    n = len(index)
    lapse = -0.0065 * (station.altitude_m - station.altitude_m_kmi)
    temperature = (
        interp("temp_dry_shelter_avg")
        + lapse
        + smooth_noise(rng, n, 0.6)
        + rng.normal(0, 0.15, n)
    )
    humidity = (
        interp("humidity_rel_shelter_avg")
        + smooth_noise(rng, n, 3)
        + rng.normal(0, 0.8, n)
    )
    sun = np.clip(interp("sun_duration"), 0, 60)

    if station.station == "HS02":
        # Black roof: the sensor heats up in direct sunshine
        temperature += 0.07 * sun + rng.normal(0, 0.3, n) * (sun > 0)
    if station.station == "HS04":
        # The humidity sensor drifts upward, about 2 percentage points a month
        humidity += np.linspace(0, 24, n)

    if station.station == "HS05":
        # Solar-powered battery: charges in the sun, drains a little all the time
        battery = np.empty(n)
        level = 4.1
        for i in range(n):
            level = min(4.2, level - BATTERY_DRAIN + BATTERY_CHARGE * sun[i])
            battery[i] = level
    else:
        # Mains-powered stations report a steady, slightly noisy supply voltage
        battery = 4.1 + rng.normal(0, 0.01, n)

    return pd.DataFrame(
        {
            "station": station.station,
            "timestamp": index,
            "temperature": temperature.round(1),
            "humidity": np.clip(humidity, 0, 100).round(0),
            "battery_v": battery.round(2),
        }
    )


def to_export(rng, true):
    """Everything that goes wrong between the sensor and the CSV file."""
    df = true.copy()
    n = len(df)

    # Durbuy goes silent when its battery runs low
    df = df[~((df["station"] == "HS05") & (df["battery_v"] < 3.4))]

    # Brugge reports in Fahrenheit
    fahrenheit = df["station"] == "HS03"
    df.loc[fahrenheit, "temperature"] = (
        df.loc[fahrenheit, "temperature"] * 9 / 5 + 32
    ).round(1)

    # The export uses local time without saying so: summer time makes a gap and a repeat
    df["timestamp"] = (
        df["timestamp"].dt.tz_convert("Europe/Brussels").dt.strftime("%d/%m/%Y %H:%M")
    )

    # Failed readings: "ERR" or simply nothing
    df["temperature"] = df["temperature"].astype("object")
    df["humidity"] = df["humidity"].astype("object")
    n = len(df)
    for column in ["temperature", "humidity"]:
        glitch = rng.random(n) < 0.002
        empty = rng.random(n) < 0.003
        df.loc[glitch, column] = "ERR"
        df.loc[empty, column] = None

    # Retransmissions: the same row arrives twice
    repeats = df.sample(frac=0.004, random_state=SEED)
    df = pd.concat([df, repeats]).sort_index(kind="stable")
    return df


def write_export_csv(df, path):
    def fmt(value):
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return ""
        if value == "ERR":
            return value
        return f"{value:g}".replace(".", ",")

    lines = [
        "station;timestamp;temperature;humidity;battery_v",
    ]
    for row in df.itertuples(index=False):
        lines.append(
            ";".join(
                [
                    row.station,
                    row.timestamp,
                    fmt(row.temperature),
                    fmt(row.humidity),
                    fmt(row.battery_v),
                ]
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_network_csv(rng, true, path):
    """HS01 also uploads to an online weather network, which exports hourly readings in UTC."""
    df = true[(true["station"] == "HS01") & (true["timestamp"].dt.minute == 0)]

    def fmt(value):
        if rng.random() < 0.003:
            return "undefined"
        if rng.random() < 0.002:
            return ""
        return f"{value:g}".replace(".", ",")

    lines = ["time_utc|temperature|humidity"]
    for row in df.itertuples(index=False):
        time = row.timestamp.strftime("%Y-%m-%d %H:%M")
        lines.append(f"{time}|{fmt(row.temperature)}|{fmt(row.humidity)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def daily_rain(kmi, station):
    """Rain in the 24 hours before the 08:00 local reading, from the KMI hourly totals."""
    rain = kmi.set_index("timestamp")["precip_quantity"].fillna(0)
    local = rain.tz_convert("Europe/Brussels")
    # Shift so that 08:00 to 08:00 becomes one calendar day, labelled by the day of the reading
    shifted = local.copy()
    shifted.index = shifted.index - pd.Timedelta(hours=8) + pd.Timedelta(days=1)
    totals = shifted.groupby(shifted.index.date).sum()
    totals.index = pd.to_datetime(totals.index)
    return totals[(totals.index >= f"{YEAR}-01-01") & (totals.index <= f"{YEAR}-12-31")]


def rain_logbook(rng, kmi, station):
    """Daily rain gauge readings as the volunteer wrote them down."""
    true = daily_rain(kmi, station.station) * rng.normal(1.0, 0.05, 365)
    true = true.clip(lower=0).round(1)
    rows = []
    for day, amount in true.items():
        remark = ""
        value = amount
        if station.station == "HS04" and pd.Timestamp(
            f"{YEAR}-10-09"
        ) <= day < pd.Timestamp(f"{YEAR}-11-13"):
            value = round(amount * 0.25, 1)  # leaves in the funnel
            if day == pd.Timestamp(f"{YEAR}-11-12"):
                remark = "funnel full of leaves, cleaned"
        if station.station == "HS05" and pd.Timestamp(
            f"{YEAR}-12-08"
        ) <= day <= pd.Timestamp(f"{YEAR}-12-27"):
            continue  # not at the cabin
        if station.station == "HS05" and day.month in (1, 2) and rng.random() < 0.08:
            value, remark = None, "frozen"
        elif rng.random() < 0.006:
            value, remark = "?", "forgot to empty the gauge"
        rows.append((day, value, remark))
    return rows


def write_logbook(rng, hourly, nearest, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stations"
    ws.append([c.replace("_", " ") for c in STATIONS.columns])
    for row in STATIONS.itertuples(index=False):
        ws.append([*row[:-1], row.installed.to_pydatetime()])
    for cell in ws[1]:
        cell.font = Font(bold=True)

    clean = []
    for station in STATIONS.merge(nearest, on="station").itertuples(index=False):
        kmi = hourly[hourly["code"] == station.code]
        rows = rain_logbook(rng, kmi, station)
        ws = wb.create_sheet(station.station)
        ws["A1"] = f"Rain gauge logbook - {station.name}"
        ws["A1"].font = Font(bold=True, size=14)
        ws.merge_cells("A1:C1")
        ws.append([])
        ws.append(["Date", "Rain", "Remarks"])
        ws.append(["", "mm", ""])
        for cell in ws[3]:
            cell.font = Font(bold=True)
        for day, value, remark in rows:
            ws.append([day.to_pydatetime(), value, remark or None])
            ws.cell(row=ws.max_row, column=1).number_format = "DD/MM/YYYY"
            rain_mm = pd.to_numeric(value, errors="coerce") if value is not None else np.nan
            clean.append((station.station, day, rain_mm, remark or None))
        ws.column_dimensions["A"].width = 12
        ws.column_dimensions["C"].width = 32
    wb.save(path)
    return pd.DataFrame(clean, columns=["station", "date", "rain_mm", "remarks"])


def main():
    rng = np.random.default_rng(SEED)
    RAW.mkdir(parents=True, exist_ok=True)
    CHECKPOINTS.mkdir(parents=True, exist_ok=True)

    kmi_stations, nearest, hourly, daily = fetch_reference_data()
    stations = STATIONS.merge(
        nearest[["station", "code", "altitude_m_kmi"]], on="station"
    )

    true = pd.concat(
        [
            simulate_station(rng, station, hourly[hourly["code"] == station.code])
            for station in stations.itertuples(index=False)
        ],
        ignore_index=True,
    )
    export = to_export(rng, true)
    write_export_csv(export, RAW / "weather_export.csv")
    print(f"Wrote {RAW / 'weather_export.csv'} ({len(export):,} rows)")

    rain = write_logbook(rng, hourly, nearest, RAW / "rain_logbook.xlsx")
    print(f"Wrote {RAW / 'rain_logbook.xlsx'}")

    # A separate random generator, so the files above stay the same
    write_network_csv(np.random.default_rng(SEED + 1), true, RAW / "hs01_hourly.csv")
    print(f"Wrote {RAW / 'hs01_hourly.csv'}")

    # Checkpoints: what the cleaning exercises should end up with
    hobby = export.drop_duplicates().copy()
    hobby["timestamp"] = pd.to_datetime(hobby["timestamp"], format="%d/%m/%Y %H:%M")
    # In the repeated hour of October, the first reading is still summer time
    summer_time = ~hobby.duplicated(["station", "timestamp"])
    hobby["timestamp"] = (
        hobby["timestamp"]
        .dt.tz_localize("Europe/Brussels", ambiguous=summer_time)
        .dt.tz_convert("UTC")
    )
    hobby = hobby.sort_values(["station", "timestamp"])
    for column in ["temperature", "humidity"]:
        hobby[column] = pd.to_numeric(hobby[column], errors="coerce")
    fahrenheit = hobby["station"] == "HS03"
    hobby.loc[fahrenheit, "temperature"] = (
        (hobby.loc[fahrenheit, "temperature"] - 32) * 5 / 9
    ).round(1)
    hobby.reset_index(drop=True).to_parquet(CHECKPOINTS / "hobby_measurements.parquet")
    rain.to_parquet(CHECKPOINTS / "hobby_rain.parquet")
    STATIONS.to_parquet(CHECKPOINTS / "hobby_stations.parquet")
    kmi_stations.to_parquet(CHECKPOINTS / "kmi_stations.parquet")
    daily.to_parquet(CHECKPOINTS / f"kmi_daily_{YEAR}.parquet")
    # The hourly KMI data without the sunshine: that is what the API exercise fetches. The sunshine is
    # saved separately, as a fallback when the API cannot be reached.
    hourly.drop(columns="sun_duration").to_parquet(CHECKPOINTS / f"kmi_hourly_{YEAR}.parquet")
    hourly[["code", "timestamp", "sun_duration"]].to_parquet(
        CHECKPOINTS / f"kmi_sun_hourly_{YEAR}.parquet"
    )
    # A clean CSV for the first exercise: the daily KMI data, with the station names
    named = daily.merge(kmi_stations[["code", "name"]], on="code")
    columns = ["name", "timestamp", "temp_min", "temp_avg", "temp_max"]
    columns += ["precip_quantity", "sun_duration", "wind_gusts_speed"]
    named[columns].to_csv(RAW / f"kmi_daily_{YEAR}.csv", index=False)
    print(f"Wrote checkpoints to {CHECKPOINTS}")


if __name__ == "__main__":
    main()
