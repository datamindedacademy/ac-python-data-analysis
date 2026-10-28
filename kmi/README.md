# KMI observations of 2023

Fetched from the [KMI open data service](https://opendata.meteo.be) by `generate_data.py`, and kept in the
repository so the course works without network access. See [opendata.meteo.be](https://opendata.meteo.be)
for the terms.

| File | What it is |
| ---- | ---------- |
| `kmi_stations.parquet` | The KMI automatic weather stations, with their location and altitude |
| `kmi_hourly_2023.parquet` | Hourly observations of the stations nearest to the hobby stations |
| `kmi_daily_2023.parquet` | Daily observations of all stations |

Delete this folder and run `uv run python generate_data.py` to fetch them again.
