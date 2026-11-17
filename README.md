# Academy course: Python Data Analysis

[![Dataminded Academy](https://raw.githubusercontent.com/datamindedacademy/branding/main/assets/badge.svg)](https://github.com/datamindedacademy)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/datamindedacademy/ac-python-data-analysis)

A hands-on course on data analysis and scientific computing with Python: pandas, NumPy, SciPy,
Matplotlib and scikit-learn. You analyse a year of Belgian weather: five fictional hobby weather stations
with a few problems built in on purpose, compared against the official observations of the Royal
Meteorological Institute (KMI).

It assumes you know the basics of Python (variables, functions, conditionals, loops, imports).

## Getting started in GitHub Codespaces

Click the badge above, or **Code → Codespaces → Create codespace on main** on the repository page. The
devcontainer builds Python 3.13 and `uv`, then runs `uv sync`. The first build takes a few minutes.

## Getting started locally

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). Then:

```bash
uv sync
```

Open the notebooks in VS Code and pick the `.venv` kernel.

## The data

Generate it once, from the root of the repository:

```bash
uv run python generate_data.py
```

This builds the hobby station files from the 2023 KMI observations in [`kmi/`](kmi/), and writes
everything to `data/`, which Git ignores. It needs no network access:

| Path | What it is |
| ---- | ---------- |
| `data/raw/weather_export.csv` | Half-hourly measurements of the hobby stations, as they export them |
| `data/raw/hs01_hourly.csv` | Hourly measurements of one hobby station, as an online weather network exports them, in UTC |
| `data/raw/rain_logbook.xlsx` | The rain gauge readings the volunteers write down every morning |
| `data/raw/kmi_daily_2023.csv` | The daily KMI observations, clean, for the first exercise |
| `data/checkpoints/` | Clean versions of the generated data, used by `generate_data.py` |

To fetch the KMI observations again from the KMI open data service, delete `kmi/` and run it again.

## The exercises

Each exercise is a notebook in [`exercises/`](exercises/), and its solution has the same folder name in
[`solutions/`](solutions/). Every exercise starts from a file, so you can do them independently.

| Folder | Topic |
| ------ | ----- |
| [`01-exploring`](exercises/01-exploring/) | Reading a clean CSV, summarizing, selecting columns and rows, missing values |
| [`02-statistics-and-plotting`](exercises/02-statistics-and-plotting/) | Statistics of a column, sorting, plotting with pandas |
| [`03-cleaning`](exercises/03-cleaning/) | Checking for duplicates, counting values, new columns with `assign` and `case_when` |
| [`04-data-types`](exercises/04-data-types/) | A messy CSV: separator, decimal sign, missing values, data types, dates and time zones |
| [`05-aggregations`](exercises/05-aggregations/) | Statistics per KMI station with `groupby`, `agg` and pivot tables |
| [`06-file-formats`](exercises/06-file-formats/) | Reading a rain logbook in Excel, combining sheets, writing Parquet |
| [`07-joins`](exercises/07-joins/) | Joining the KMI data with the station list: altitude and temperature |
| [`08-regression`](exercises/08-regression/) | Estimating the temperature in the Ardennes from Brussels |
| [`09-fetching-from-an-api`](exercises/09-fetching-from-an-api/) | Fetching data from the KMI's API |
| [`10-scipy`](exercises/10-scipy/) | Fitting the yearly and the daily cycle with SciPy |

The last part of the day, best practices for keeping an analysis in Git, has no exercise.

To check that the exercises have no outputs and that every solution still runs, for example after changing
the data or upgrading pandas: `make check`.

## The slides

The deck is in [`docs/slides.md`](docs/slides.md), written in [Slidev](https://sli.dev). To present it:

```bash
make present   # live on http://localhost:3030, press "p" for presenter mode
make pdf       # export to docs/slides.pdf
```

## Reference

- [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html) and
  [API reference](https://pandas.pydata.org/docs/reference/index.html)
- [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [SciPy user guide](https://docs.scipy.org/doc/scipy/tutorial/index.html)
- [Matplotlib quick start](https://matplotlib.org/stable/users/explain/quick_start.html) and
  [cheat sheets](https://matplotlib.org/cheatsheets/)
- [scikit-learn: linear models](https://scikit-learn.org/stable/modules/linear_model.html)
- [KMI open data](https://opendata.meteo.be): the source of the weather observations

## License

Code: [MIT](LICENSE). Weather observations: KMI open data, see
[opendata.meteo.be](https://opendata.meteo.be) for the terms.
