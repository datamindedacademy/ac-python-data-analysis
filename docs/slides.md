---
theme: dataminded
title: Python for Data Analysis
info: Data analysis and scientific computing with pandas, NumPy, SciPy, Matplotlib and scikit-learn. Dataminded Academy.
fonts:
  serif: El Messiri
  sans: DM Sans
transition: slide-left
layout: cover
subtitle: Dataminded Academy
---

# Python for <span class="dm-accent">Data Analysis</span>

<!--
Good morning, and welcome. Today is about doing data analysis in Python: reading data, cleaning it,
combining it, calculating with it, plotting it, and fitting a simple model.

You will write a lot of code yourself today. I talk for a bit, then you practise, and that repeats all day.
The slides and the solutions are in the repository, so you do not need to take notes on the code.
-->

---
layout: agenda
label: Contents
---

# Contents

1. Exploring and plotting a DataFrame
2. Cleaning, data types and missing values
3. Grouping and aggregating
4. File formats
5. Joins, regression and APIs
6. NumPy and SciPy
7. Best practices

<!--
This is the plan for today. We start by looking at data that is already clean, so you are working with
pandas within the first half hour. Then the harder part of real data: data types and missing values, and
cleaning. Once the data is clean, we summarize it per group. After that, file formats: Excel and Parquet.
Then we combine tables with joins, build a regression model, and fetch data from an API. At the
end, a few calculations and statistics with NumPy and SciPy, and a few best practices for keeping an
analysis in Git.

Every part has a short talk and then an exercise. Breaks are around half past ten, lunch around half past
twelve, and another break mid-afternoon.
-->

---
layout: default
label: Introduction
---

# Let's analyze one year of Belgian weather

<DmColumns class="mt-2">
<DmColumn header="Five hobby weather stations" tone="navy">

- **Fictional** data, with a few problems built in on purpose
- Temperature, humidity and battery voltage, every half hour
- A rain logbook, kept by hand in Excel

</DmColumn>
<DmColumn header="The KMI" tone="violet" divider>

- **Real** data, fetched from the KMI API
- The Royal Meteorological Institute of Belgium
- Official weather stations across the country
- Hourly and daily observations
- Open data

</DmColumn>
</DmColumns>

<!--
Our data for today is a year of Belgian weather, 2023.

On the left: five hobby weather stations. These are fictional: I generated them from real measurements, and
I built in a few problems on purpose, the kind of problems real sensors have. They measure temperature,
humidity and their battery voltage every half hour, and the volunteers also keep a rain logbook in Excel.

On the right: the KMI, the Royal Meteorological Institute. That data is real, and we fetch it from their API.
Official stations, hourly and daily, open data.
-->

---
layout: default
label: Introduction
---

# The Python libraries for data analysis

<DmComparison
  class="mt-2 compact"
  :rows="['pandas', 'NumPy', 'SciPy', 'Matplotlib', 'scikit-learn']"
  :cols="['What it does', 'Today we use it to']"
>
  <template #r0c0>manipulate data: reading files (CSV, Excel, Parquet, ...), combining, aggregating, etc</template>
  <template #r0c1>read and clean the measurements, compare stations</template>
  <template #r1c0>fast calculations on arrays of numbers</template>
  <template #r1c1>as the engine underneath our calculations</template>
  <template #r2c0>scientific methods: interpolation, curve fitting, statistics</template>
  <template #r2c1>fit the yearly cycle of the temperature</template>
  <template #r3c0>plotting</template>
  <template #r3c1>plotting</template>
  <template #r4c0>machine learning models, including regression</template>
  <template #r4c1>estimate missing measurements</template>
</DmComparison>

<!--
These are the five libraries we use today. You will see them in almost every data analysis in Python.

pandas is the one we spend most time with: tables, reading files, cleaning, combining, summarizing. NumPy does
fast calculations on arrays of numbers; pandas is built on top of it. SciPy has the scientific methods:
interpolation, fitting curves, statistical tests. Matplotlib makes the plots. And scikit-learn has machine
learning models; we only use the simplest one, a linear regression.

They are made to work together: you can pass a pandas column straight to SciPy, Matplotlib or scikit-learn.
-->

---
layout: default
label: Introduction
---

# A <span class="dm-accent">DataFrame</span> is a table with named, typed columns

<DmColumns>
<DmColumn header="Example DataFrame in pandas" tone="navy">

```py
import pandas as pd

df = pd.DataFrame({
    "station": ["HS01", "HS01", "HS02"],
    "temperature": [16.0, 15.8, 14.6],
})
```

<div class="df-diagram">
  <table>
    <thead><tr><th class="df-index"></th><th>station</th><th class="df-series">temperature</th></tr></thead>
    <tbody>
    <tr><td class="df-index">0</td><td>HS01</td><td class="df-series">16.0</td></tr>
    <tr><td class="df-index">1</td><td>HS01</td><td class="df-series">15.8</td></tr>
    <tr><td class="df-index">2</td><td>HS02</td><td class="df-series">14.6</td></tr>
    </tbody>
  </table>
  <div class="df-labels">
    <span class="df-label-index">in grey: the <b>index</b>, the labels of the rows</span>
    <span class="df-label-series">one column: a Series</span>
  </div>
</div>

</DmColumn>
<DmColumn header="The type of every column" tone="violet" divider>

```py
df.dtypes
```

<div class="output">

```text
station            str
temperature    float64
```

</div>

- `str`: text
- `float64`: a floating-point number
- `int64`: an integer
- `datetime64`: a date and time
- `bool`: `True` or `False`

These are pandas data types, not Python types.<br>
We go into data types in depth in part 4.

</DmColumn>
</DmColumns>

<p class="docs absolute bottom-16 right-14">📖 <a href="https://pandas.pydata.org/docs/user_guide/basics.html#dtypes" target="_blank">https://pandas.pydata.org/docs/user_guide/basics.html#dtypes</a></p>

<!--
The central idea of today: a DataFrame. A table, where every column has a name and a type.

On the left, I make one by hand, from a dictionary: column names as keys, lists of values. You will rarely do
this in practice; usually you read a DataFrame from a file. But it shows the structure.

The grey numbers on the left are the index: the labels of the rows. By default they are just 0, 1, 2. One
column on its own, like temperature here, is called a Series.

On the right, dtypes: the type of every column. str for text, float64 for a floating-point number, int64 for
an integer, datetime64 for a date and time, bool for True or False. Every value in a column has the same
type. These are pandas data types, not Python types. Remember dtypes: it is the first thing to check when something looks odd. We go into data types in depth in
part 4.
-->

---
layout: section
---

# Exploring a DataFrame

<!--
Let's start working with data right away, with a file that is already clean. These are the things you will
do every single day with pandas: read a file, look at it and summarize it, select columns, filter rows, and
find the missing values.
-->

---
layout: default
label: 1 · Exploring a DataFrame
---

# Reading a <span class="dm-accent">CSV</span> file

<div class="grid gap-x-6 gap-y-2 items-start" style="grid-template-columns: minmax(0, 21fr) minmax(0, 19fr)">
<div style="grid-column: 1 / -1">

<div class="csv-file"><pre class="slidev-code csv"><span class="csv-c0">station</span><span class="csv-sep">,</span><span class="csv-c1">timestamp</span><span class="csv-sep">,</span><span class="csv-c2">temperature</span><span class="csv-sep">,</span><span class="csv-c3">humidity</span>
<span class="csv-c0">HS01</span><span class="csv-sep">,</span><span class="csv-c1">2023-01-01 00:00:00</span><span class="csv-sep">,</span><span class="csv-c2">16.0</span><span class="csv-sep">,</span><span class="csv-c3">49.0</span>
<span class="csv-c0">HS01</span><span class="csv-sep">,</span><span class="csv-c1">2023-01-01 00:30:00</span><span class="csv-sep">,</span><span class="csv-c2">16.0</span><span class="csv-sep">,</span><span class="csv-c3">51.0</span>
...</pre><span class="csv-name">measurements.csv</span></div>

</div>
<div>

```py
pd.read_csv("measurements.csv")
```

<div class="output">

```text
      station            timestamp  temperature  humidity
0        HS01  2023-01-01 00:00:00         16.0      49.0
1        HS01  2023-01-01 00:30:00         16.0      51.0
2        HS01  2023-01-01 01:00:00         15.8      52.0
3        HS01  2023-01-01 01:30:00         16.0      53.0
4        HS01  2023-01-01 02:00:00         15.6      55.0
...       ...                  ...          ...       ...
86274    HS05  2023-12-23 01:30:00          8.7      93.0
86275    HS05  2023-12-23 02:00:00          8.5      96.0
86276    HS05  2023-12-23 02:30:00          8.7      97.0
86277    HS05  2023-12-23 03:00:00          8.5      96.0
86278    HS05  2023-12-23 03:30:00          8.8      98.0
[86279 rows x 4 columns]
```

</div>

</div>
<div>

```py
df = pd.read_csv("measurements.csv")
df.dtypes
```

<div class="output">

```text
station            str
timestamp          str
temperature    float64
humidity       float64
dtype: object
```

</div>

pandas infers the data types.<br>
For now: note that `timestamp` is inferred as a string.<br>
More on reading CSV files and on data types later.

<p class="docs" style="margin-top: 8px">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html</a></p>

</div>
</div>

<!--
Here is a clean CSV file with the measurements of the hobby stations: a station code, a timestamp, the
temperature and the humidity, separated by commas. read_csv reads it into a DataFrame. For a clean file,
that's all you need; the messy files come later today.

On the left, read_csv on its own: the notebook shows the result, the first and last five rows, and the size:
86 thousand rows, 4 columns. On the right, we keep it under a name, df, as you will always do. And dtypes shows
that pandas decided on a type for every column: numbers, text. We will look at that closely later, because that
is where real files go wrong.
-->

---
layout: default
label: 1 · Exploring a DataFrame
---

# A first look at a DataFrame

<div class="grid gap-x-6 items-start" style="grid-template-columns: minmax(0, 21fr) minmax(0, 19fr)">
<div>
<DmColumn header="Selecting the first or last rows" tone="navy">

```py
df.head(3)
```

<div class="output no-label">

```text
  station           timestamp  temperature  humidity
0    HS01 2023-01-01 00:00:00         16.0      49.0
1    HS01 2023-01-01 00:30:00         16.0      51.0
2    HS01 2023-01-01 01:00:00         15.8      52.0
```

</div>

`df.head(n)`: the first n rows (5 by default)<br>
`df.tail(n)`: the last n rows

</DmColumn>
<DmColumn header="Getting the number of rows" tone="navy" class="mt-3" v-click>

```py
len(df)
```

<div class="output">

```text
86279
```

<span class="output-type">output, type: int</span>
</div>

</DmColumn>
</div>
<DmColumn header="Calculating summary statistics" tone="violet" divider v-click>

```py
df.describe()
```

<div class="output">

```text
        temperature      humidity
count  85846.000000  85814.000000
mean      12.462522     81.444601
std        6.745073     15.586545
min       -6.300000     20.000000
25%        7.900000     72.000000
50%       11.800000     85.000000
75%       17.300000     94.000000
max       37.800000    100.000000
```

</div>

`count`: the number of values that are not missing<br>
`50%`: the median

</DmColumn>
</div>

<!--
head shows the first five rows, head(10) the first ten; tail shows the last ones. So: a station code, a
timestamp every half hour, temperature in degrees, humidity in percent. len gives the number of rows.

And describe summarizes every number column: how many values, the mean, the standard deviation, the minimum
and maximum, and the quartiles.

Look at count: about 85 thousand, not 86 thousand. count only counts values that are not missing, so some
temperatures and humidities are missing. And the min and max are a quick sanity check: 37.8 degrees in
Belgium? We will come back to that. Never trust data you have not looked at.
-->

---
layout: default
label: 1 · Exploring a DataFrame
---

# Selecting <span class="dm-accent">columns</span>

<div class="csv-file"><pre class="slidev-code input">  station           timestamp  temperature  humidity
0    HS01 2023-01-01 00:00:00         16.0      49.0
1    HS01 2023-01-01 00:30:00         16.0      51.0
2    HS01 2023-01-01 01:00:00         15.8      52.0</pre><span class="csv-name">df</span></div>

<DmColumns class="mt-2">
<DmColumn header="Selecting one column" tone="navy">

```py
df["temperature"]
```

<div class="output">

```text
0    16.0
1    16.0
2    15.8
Name: temperature, dtype: float64
```

<span class="output-type">output, type: Series</span>
</div>

</DmColumn>
<DmColumn header="Selecting several columns" tone="violet" divider>

```py
df[["station", "temperature"]]
```

<div class="output">

```text
  station  temperature
0    HS01         16.0
1    HS01         16.0
2    HS01         15.8
```

<span class="output-type">output, type: DataFrame</span>
</div>

Note the double brackets: the inner ones make a list, the outer ones select the columns in it.

</DmColumn>
</DmColumns>


<!--
To work with one column, put its name in square brackets. You get a Series: the values, with the index on
the left.

To select several columns, you pass a list of names. That gives the double brackets on the right: the inner
brackets make a Python list, the outer brackets select. The result is again a DataFrame, just with fewer
columns.

People mix these up all the time, so look at the type: one name gives a Series, a list gives a DataFrame,
even a list with one name in it.
-->

---
layout: default
label: 1 · Exploring a DataFrame
---

# Selecting <span class="dm-accent">rows</span> with a condition

<DmColumns>
<DmColumn header="Step 1: True or False per row" tone="navy">

<div class="csv-file"><pre class="slidev-code input">  station  temperature
0    HS01          0.4
1    HS01         -0.1
2    HS05          1.2
3    HS05         -0.5</pre><span class="csv-name">df</span></div>

```py
df["temperature"] < 0
```

<div class="output">

```text
0    False
1     True
2    False
3     True
Name: temperature, dtype: bool
```

<span class="output-type">output, type: Series</span>
</div>

</DmColumn>
<DmColumn header="Step 2: keep the True rows" tone="violet" divider>

```py
df[df["temperature"] < 0]
```

<div class="output">

```text
  station  temperature
1    HS01         -0.1
3    HS05         -0.5
```

<span class="output-type">output, type: DataFrame</span>
</div>

<p class="note">⚠️ The rows keep their index: 1 and 3.</p>

<v-click>

To renumber them:

```py
df[df["temperature"] < 0].reset_index(drop=True)
```

<div class="output">

```text
  station  temperature
0    HS01         -0.1
1    HS05         -0.5
```

</div>

`drop=True`: without it, the old index becomes a column.

</v-click>

</DmColumn>
</DmColumns>

<!--
Filtering rows takes two steps, and it is worth seeing them separately once.

Step one: a comparison on a column. temperature smaller than zero. That compares every value, and gives a
Series of booleans: one True or False per row.

Step two: put that between the square brackets of the DataFrame. pandas keeps the rows where it says True.
So: only the readings below zero.

Look at the index of the result: 1 and 3. The rows keep their labels from df; pandas does not renumber them.
That is usually what you want, but it surprises people, for example in a plot, where the index is the x-axis,
as you will see later.
If you want 0, 1, 2 again, use reset_index with drop=True. Without drop=True, the old index is kept as an
extra column.

The same pattern works with any comparison: double equals, not equals, greater than. You will write this
dozens of times today.
-->

---
layout: default
label: 1 · Exploring a DataFrame
---

# Several conditions

<div class="csv-file"><pre class="slidev-code input">  station  temperature
0    HS01          0.4
1    HS02         -0.1
2    HS05         -0.5
3    HS05          1.2</pre><span class="csv-name">df</span></div>

<DmColumns class="mt-2">
<DmColumn header="Combining conditions with &" tone="navy">

```py
df[(df["station"] == "HS05") & (df["temperature"] < 0)]
```

<div class="output">

```text
  station  temperature
2    HS05         -0.5
```

</div>

</DmColumn>
<DmColumn header="Matching one of several values with isin" tone="violet" divider>

```py
df[df["station"].isin(["HS01", "HS05"])]
```

<div class="output">

```text
  station  temperature
0    HS01          0.4
2    HS05         -0.5
3    HS05          1.2
```

</div>

</DmColumn>
</DmColumns>

<p class="note"><code>&</code> for and, <code>|</code> for or, <code>~</code> for not. Put brackets around each condition.</p>

<!--
Two conditions at once: station HS05 and below zero. In pandas you combine conditions with the ampersand for
and, the vertical bar for or, and the tilde for not. Not the Python words and, or, not: those do not work on
whole columns.

And you need brackets around each condition. Without them, Python evaluates the ampersand first, and you get
a confusing error.

On the right: isin. Is the station one of these? That is shorter than three conditions with or.
-->

---
layout: default
label: 1 · Exploring a DataFrame
---

# Counting <span class="dm-accent">missing values</span>

<div class="csv-file"><pre class="slidev-code input">  station  temperature  humidity
0    HS01         16.0      49.0
1    HS01          NaN      51.0
2    HS01          NaN       NaN
3    HS01          NaN      53.0</pre><span class="csv-name">df</span></div>

<DmColumns class="mt-2">
<DmColumn header="Step 1: .isna()" tone="navy">

```py
df.isna()
```

<div class="output">

```text
   station  temperature  humidity
0    False        False     False
1    False         True     False
2    False         True      True
3    False         True     False
```

</div>

</DmColumn>
<DmColumn header="Step 2: .sum()" tone="violet" divider>

```py
df.isna().sum()
```

<div class="output">

```text
station        0
temperature    3
humidity       1
dtype: int64
```

</div>

In a sum, `True` counts as 1 and `False` as 0.

</DmColumn>
</DmColumns>

<p class="note">As a condition: <code>df[df["temperature"].isna()]</code> keeps the rows where the temperature is missing.</p>

<!--
How many values are missing? Two steps, the same pattern as filtering.

NaN, not a number, is how pandas shows a missing value: an empty cell in the file, for example.

isna gives, for every cell, True if it is missing and False if not.

Then sum. In a sum, True counts as one and False as zero, so the sum of a True/False column is the number of
Trues. Here: temperature is missing three times, humidity once.

isna().sum() is probably the line you will type most often after loading data. Make it a habit.

And isna on one column gives a True/False Series, so it works as a condition: put it between square brackets,
and you see the rows where the temperature is missing. Often the first thing you want to do.
-->

---
layout: default
label: 1 · Exploring a DataFrame
---

# Working in a notebook

<DmColumns>
<DmColumn header="A cell and its output" tone="navy">

```py
x = 3
x * 2
```

<div class="output">

```text
6
```

</div>

Only the value of the **last line** is shown. To show more, use `print(...)`.

</DmColumn>
<DmColumn header="How it works" tone="violet" divider>

- Run a cell with **Shift+Enter**
- Variables stay in memory, in the order you ran the cells
- Lost track? **Restart** the kernel and **run all** cells from the top

</DmColumn>
</DmColumns>

<!--
Before you start the exercise, a word on notebooks. We work in Jupyter notebooks today, inside VS Code. A
notebook is a list of cells. You run a cell with Shift+Enter, and the result appears right below it.

One thing that surprises people: only the value of the last line is shown. Here x times 2 is the last line,
so you see 6. If you want to see something from the middle of a cell, wrap it in print.

The variables stay in memory, in the order in which you ran the cells, not the order in which they appear on
the screen. If you ran cells out of order and things get confusing, restart the kernel and run everything from
the top. That is also the test that your notebook works: restart, run all, no errors.
-->

---
layout: statement
title: Exercise - exploring a DataFrame
---

# Exercise time: exploring a DataFrame

<p class="mt-6 text-lg opacity-80"><code>exercises/01-exploring/</code></p>
<p class="mt-4 opacity-80">First generate the data: <code>uv run python generate_data.py</code></p>
<p class="mt-4 opacity-80">Explore the daily KMI weather of 2023: its size, its extremes and its missing values.</p>
<p class="mt-1 opacity-60">About 20 minutes</p>

<!--
Time for the first exercise. Generate the data first, it takes a few seconds: the command is on the slide and
in the README.

The exercise uses the KMI daily data, which is clean. Do the questions in order; the bonus at the
end is for those who are fast, it is fine not to get to it.

About 20 minutes.
-->

---
layout: section
---

# Statistics, sorting and plotting

<!--
You can read a file, look at it, and select the rows and columns you need. Now we do something with them:
compute a statistic of a column, sort the rows to find the extremes, and make a first plot.
-->

---
layout: default
label: 2 · Statistics, sorting and plotting
---

# Statistics of one column

<div class="grid gap-8 items-start" style="grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)">
<DmColumn header="Calculating the mean, min, max and more" tone="navy">

```py
df["temperature"].mean()
```

<div class="output">

```text
12.462522423875313
```

</div>

- `.min()`: the lowest value
- `.max()`: the highest value
- `.median()`: the median
- `.std()`: the standard deviation
- `.sum()`: the sum

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/series.html" target="_blank">https://pandas.pydata.org/docs/reference/series.html</a></p>

</DmColumn>
<div class="aside-box">
<div class="aside-title">Side note: np.float64</div>

If you run the code on the left in a <b>notebook</b>, you actually see:

<div class="output no-label">

```text
np.float64(12.462522423875313)
```

</div>

This is because pandas uses NumPy under the hood. This is a NumPy number. It works just like a normal Python number.

To show just the number, use `print`:

```py
print(df["temperature"].mean())
```

<div class="output no-label">

```text
12.462522423875313
```

</div>

</div>
</div>

<!--
Once you have a column, you can ask it for a statistic: mean, min, max, median, std for the standard
deviation, sum. Each gives one number. The mean temperature over the whole year: about 12 and a half degrees,
the same as in describe.

A side note, on the right, because you will run into it: the notebook shows it as np.float64, with the number
in brackets. That is just the type: pandas does its calculations with NumPy, so you get a NumPy number back.
You can calculate with it like with any number. If you only want to see the number, print it.
-->

---
layout: default
label: 2 · Statistics, sorting and plotting
---

# Sorting rows

```py
df.sort_values("temperature", ascending=False).head(3)
```

<div class="output">

```text
      station           timestamp  temperature  humidity
29600    HS02 2023-09-09 16:00:00         37.8      44.0
29596    HS02 2023-09-09 14:00:00         37.6      48.0
29599    HS02 2023-09-09 15:30:00         37.0      43.0
```

</div>

<p class="note">The three highest temperatures of the year: all HS02, on the same afternoon.</p>

<p class="note"><code>sort_values</code> returns a <b>new</b> DataFrame, and <code>df</code> stays the same. To keep the result, give it a name:<br><code>sorted_df = df.sort_values(...)</code></p>

<!--
sort_values sorts the rows by a column. Ascending is the default; ascending=False puts the highest first.
Then head(3): the three warmest readings of the year.

And they are all HS02, on one afternoon in September. 37.8 degrees.

Important, and this trips up everyone: sort_values does not change df. It returns a new, sorted DataFrame.
The notebook shows it, and then it is gone. If you want to keep it, give it a name: sorted_df equals
df dot sort_values. Almost every pandas method works like that.
-->

---
layout: default
label: 2 · Statistics, sorting and plotting
---

# A first plot with <span class="dm-accent">.plot()</span>

<div class="grid grid-cols-2 gap-8 items-center">
<div>

```py
daily = pd.read_csv("kmi_daily_2023.csv")
zeebrugge = daily[daily["name"] == "ZEEBRUGGE"]

zeebrugge[["temp_min", "temp_max"]].plot(
    xlabel="Row number",
    ylabel="Temperature (°C)",
)
```

<p class="note"><code>xlabel</code> and <code>ylabel</code> are optional, but recommended.<br>The x-axis is the index: here the row numbers of <code>daily</code>.</p>

</div>
<div>

<img src="/img/first-plot.png" alt="The lowest and highest temperature of every day in Zeebrugge, plotted against the row number" style="width: 100%" />

</div>
</div>

<!--
Numbers are useful, but a year of numbers you cannot read. One line of code shows them all: dot plot.

Here the real KMI weather of 2023, one row per day and station, as in exercise 1. I keep the rows of
Zeebrugge, and plot two columns: the lowest and the highest temperature of every day. One line per column.
The x-axis is the index: the row numbers, which are 365 to 729, because Zeebrugge is the second station in the
file. The rows are in time order, so from left to right you see the year.

Other kinds of plots are on the next slides.
-->

---
layout: default
label: 2 · Statistics, sorting and plotting
---

# Other kinds of plots: <span class="dm-accent">scatter</span> and <span class="dm-accent">hist</span>

<DmColumns class="mt-6 code-11">
<DmColumn>

```py
zeebrugge.plot(x="temp_min", y="temp_max", kind="scatter")
```

<img src="/img/plot-scatter.png" alt="Scatter plot of the highest against the lowest temperature of every day in Zeebrugge" style="width: 100%; margin-top: 12px" />

</DmColumn>
<DmColumn divider>

```py
zeebrugge.plot(y="temp_max", kind="hist")
```

<img src="/img/plot-hist.png" alt="Histogram of the highest temperature of the day in Zeebrugge" style="width: 100%; margin-top: 12px" />

</DmColumn>
</DmColumns>

<!--
kind chooses the type of plot. On the left a scatter plot: x and y are two columns, and every row, every day,
is a dot. A warm minimum usually comes with a warm maximum. On the right a histogram: how often each highest
temperature occurs.
-->

---
layout: default
label: 2 · Statistics, sorting and plotting
---

# Other kinds of plots: <span class="dm-accent">bar</span> and <span class="dm-accent">box</span>

<DmColumns class="mt-6 code-11">
<DmColumn>

```py
zeebrugge.head(7).plot(
    x="timestamp", y="precip_quantity", kind="bar"
)
```

<img src="/img/plot-bar.png" alt="Bar chart of the rain on the first seven days of 2023 in Zeebrugge" style="width: 100%; margin-top: 12px" />

</DmColumn>
<DmColumn divider>

```py
zeebrugge.plot(
    y=["temp_min", "temp_max"], kind="box"
)
```

<img src="/img/plot-box.png" alt="Box plots of the lowest and the highest temperature of the day in Zeebrugge" style="width: 100%; margin-top: 12px" />

</DmColumn>
</DmColumns>

<!--
On the left a bar chart: one bar per row, here the rain of the first seven days. On the right box plots, one
per column: the box holds the middle half of the values, the line in it is the median.
-->

---
layout: default
label: 2 · Statistics, sorting and plotting
---

# <span class="dm-accent">Saving</span> a plot

```py
ax = zeebrugge["temp_max"].plot()
ax.figure.savefig("zeebrugge.png", dpi=200)
```

<p class="note"><code>.plot()</code> returns the plot, and <code>.figure</code> is the whole image around it.</p>

Supported file formats:

<DmColumns class="mt-2">
<DmColumn header="Raster formats" tone="navy">

`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.tif`, `.tiff`, `.avif`, `.raw`, `.rgba`

Set `dpi` to control the resolution.

</DmColumn>
<DmColumn header="Vector formats" tone="violet" divider>

`.pdf`, `.svg`, `.svgz`, `.eps`, `.ps`, `.pgf`

Sharp at any resolution.

</DmColumn>
</DmColumns>

<p class="docs">📖 <a href="https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html" target="_blank">https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html</a></p>

<!--
To save a plot, give the result of plot a name. It is the plot itself; dot figure is the whole image, and
savefig writes it to a file. The extension of the file name sets the format. PNG and JPG are pixels: dpi sets how many. PDF and SVG
are vector images: they stay sharp however far you zoom in, so dpi does not matter for them.
-->

---
layout: default
label: 2 · Statistics, sorting and plotting
---

# Seaborn and Plotly

<DmColumns>
<DmColumn header="Seaborn: more statistical plots" tone="navy">

```py
import seaborn as sns
sns.violinplot(data=daily, x="temp_avg", y="name")
```

<img src="/img/seaborn-violin.png" alt="Violin plot of the mean temperature of the day, per KMI station" style="height: 205px; margin: 6px auto 0" />

A different interface: a function that takes the DataFrame and the column names.

<p class="docs">📖 <a href="https://seaborn.pydata.org/examples/" target="_blank">https://seaborn.pydata.org/examples/</a></p>

</DmColumn>
<DmColumn header="Plotly: interactive plots" tone="violet" divider>

```py
zeebrugge["temp_max"].plot(backend="plotly")
```

<img src="/img/plotly-backend.png" alt="Plotly line plot of the highest temperature in Zeebrugge, with a hover box showing one value" style="height: 190px; margin: 6px auto 0" />

The same `.plot()`, drawn by Plotly: hover for the values, drag to zoom.

<p class="note">Another commonly used plotting library: Altair.</p>

<p class="docs">📖 <a href="https://altair-viz.github.io/" target="_blank">https://altair-viz.github.io/</a></p>

</DmColumn>
</DmColumns>

<!--
Two libraries you will run into. Seaborn has more statistical plots, like this violin plot: the distribution of
the mean temperature of the day, per station. It works a bit differently: a function to which you give the DataFrame and the
column names.

Plotly makes interactive plots. You do not even need to learn a new interface: give plot the backend plotly,
and you get the same plot, in which you can hover over the values and zoom in.

Another commonly used plotting library is Altair.
-->

---
layout: statement
title: Exercise - statistics, sorting and plotting
---

# Exercise time: statistics, sorting and plotting

<p class="mt-6 text-lg opacity-80"><code>exercises/02-statistics-and-plotting/</code></p>
<p class="mt-4 opacity-80">Zoom in on one station: its mean temperature, its hottest days, and plots of the year.</p>
<p class="mt-1 opacity-60">About 15 minutes</p>

<!--
The same KMI daily data, now for one station: its mean temperature, its hottest days, and plots of the
year. The bonus at the end is for those who are fast, it is fine not to get to it.

About 15 minutes.
-->

---
layout: section
---

# Cleaning data

<!--
Before you analyze data, you check it and fix what is wrong. Rows that arrived twice, a station that is short
of measurements, a station that measures in the wrong unit. In this part: the tools to find and fix that.
-->

---
layout: default
label: 3 · Cleaning data
---

# Counting rows with <span class="dm-accent">value_counts</span>

<DmColumns>
<DmColumn header="Input: one row per measurement" tone="navy">

<div class="csv-file"><pre class="slidev-code input">  station  temperature
0    HS01         16.0
1    HS01         15.8
2    HS01         16.5
3    HS02         14.6
4    HS02         15.0</pre><span class="csv-name">df</span></div>

</DmColumn>
<DmColumn header="Counting rows per station" tone="violet" divider>

```py
df["station"].value_counts()
```

<div class="output">

```text
station
HS01    3
HS02    2
Name: count, dtype: int64
```

</div>

Sorted from most to least.

</DmColumn>
</DmColumns>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html</a></p>

<!--
How many rows per value? value_counts. Here: how many measurements per station. HS01 has three, HS02 has
two.

The result is sorted from most to least. On the real data, it immediately tells you whether a station is
missing measurements: a full year every half hour is 17 520.

You will use this on almost every text column you meet, to see which values occur.
-->

---
layout: default
label: 3 · Cleaning data
---

# Duplicate rows

<div class="grid gap-8 items-center" style="grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)">
<div class="csv-file"><pre class="slidev-code input">  station         timestamp  temperature
0    HS01  01/01/2023 01:00         16.0
1    HS01  01/01/2023 01:30         16.0
2    HS01  01/01/2023 01:30         16.0
3    HS01  01/01/2023 01:30         15.9
4    HS01  01/01/2023 02:00         15.8</pre><span class="csv-name">df</span></div>
<div>

`df.drop_duplicates()` removes the copies, in a new DataFrame. It also takes `subset`.

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html</a></p>

</div>
</div>

<DmColumns class="mt-2">
<DmColumn header="Finding exact copies" tone="navy">

```py
df.duplicated()
```

<div class="output small no-label">

```text
0    False
1    False
2     True
3    False
4    False
dtype: bool
```

</div>

`True` for a copy of an earlier row.

</DmColumn>
<DmColumn header="Comparing only some columns" tone="violet" divider>

```py
df.duplicated(subset=["station", "timestamp"])
```

<div class="output small no-label">

```text
0    False
1    False
2     True
3     True
4    False
dtype: bool
```

</div>

Only `station` and `timestamp` have to match.

</DmColumn>
</DmColumns>

<!--
Exports often contain rows twice: a sensor sends a message again, two exports overlap.

On the left: duplicated marks every row that is an exact copy of an earlier row. Row 2 is a copy of row 1, so it
is True. With sum, you count them.

On the right: with subset, only the columns you name have to match. Rows 2 and 3 have the same station and
timestamp as row 1, so both are True, even though row 3 has another temperature. Two different readings for the
same station and time: that is worth looking into.

At the top right: drop_duplicates removes the copies. It returns a new DataFrame, and df stays the same. It also
takes subset, if you want to remove rows that only match on some columns.
-->

---
layout: default
label: 3 · Cleaning data
---

# Adding a column

<div class="csv-file"><pre class="slidev-code input">  station  temperature
0    HS01         16.0
1    HS01         -0.5
2    HS02         14.6</pre><span class="csv-name">df</span></div>

<DmColumns class="mt-2">
<DmColumn header="Adding a calculation" tone="navy">

```py
df["temp_f"] = df["temperature"] * 9 / 5 + 32
df
```

<div class="output">

```text
  station  temperature  temp_f
0    HS01         16.0   60.80
1    HS01         -0.5   31.10
2    HS02         14.6   58.28
```

</div>

</DmColumn>
<DmColumn header="Adding a condition" tone="violet" divider>

```py
df["frost"] = df["temperature"] < 0
df
```

<div class="output">

```text
  station  temperature  frost
0    HS01         16.0  False
1    HS01         -0.5   True
2    HS02         14.6  False
```

</div>

</DmColumn>
</DmColumns>

<p class="note">The calculation works on the whole column: no loop needed.</p>

<!--
To add a column, assign to a new column name. On the left: Fahrenheit, calculated from the temperature. You
write the formula once, for the whole column, and pandas does it for every row. No loop.

On the right: a condition as a column. The True or False from filtering, stored as a column. Handy to count
later: the sum of a True/False column is the number of Trues.

If a column with that name already exists, it is replaced.

If you come from Polars: pandas also has assign, which looks like with_columns. We come to it in a few slides.
-->

---
layout: default
label: 3 · Cleaning data
---

# Changing values with <span class="dm-accent">loc</span>

<p>Station HS03 reports in Fahrenheit. Convert its readings to Celsius:</p>

```py
is_hs03 = df["station"] == "HS03"
df.loc[is_hs03, "temperature"] = (df.loc[is_hs03, "temperature"] - 32) * 5 / 9
```

<DmColumns class="mt-4">
<DmColumn header="What loc does" tone="navy">

```py
df.loc[rows, columns]
```

- `rows`: a True/False condition, one value per row
- `columns`: a column name, or a list of names
- Assigning to it changes those values in `df` itself

</DmColumn>
<DmColumn header="Run the cell twice?" tone="violet" divider>

<div class="output no-label">

```text
                 HS03 temperature
before                       60.8
after one run                16.0
after two runs               -8.9
```

</div>

The second run converts the converted values again: wrong, and without any error.

</DmColumn>
</DmColumns>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html</a></p>

<!--
Sometimes you need to change only some rows. Station HS03 reports in Fahrenheit, and we want Celsius.

First, the condition: is the station HS03? Then loc. loc takes two things: which rows, and which columns. The
rows are our condition, the column is temperature. On the right side of the equals sign, the same selection,
converted. Assigning to it changes exactly those values in df.

You will see this everywhere, so you need to be able to read it. But it has a trap, especially in a notebook.
Run the cell a second time, and it converts again: 60.8 becomes 16, and then 16 becomes minus 8.9. No error,
no warning. And in a notebook, running a cell twice happens all the time.
-->

---
layout: default
label: 3 · Cleaning data
---

# Make every cell <span class="dm-accent">idempotent</span>

<p><b>Idempotent:</b> running it twice gives the same result as running it once.</p>

<DmColumns class="mt-2">
<DmColumn header="Idempotent" tone="violet">

```py
df["temp_f"] = df["temperature"] * 9 / 5 + 32
deduped = df.drop_duplicates()
sorted_df = df.sort_values("temperature")
```

A new column from columns that do not change, or a result with a new name.

</DmColumn>
<DmColumn header="Not idempotent" tone="navy" divider>

```py
df["temperature"] = df["temperature"] * 9 / 5 + 32
df = df.merge(stations, on="station")
```

A value computed from itself, or a name reused for its own result: the second run starts from the first.

</DmColumn>
</DmColumns>

<p class="note">The rule: never change your input. Give every result a new name.</p>

<!--
There is a word for what went wrong: the cell was not idempotent. Idempotent means: running it twice gives the
same result as running it once.

On the left, cells that are fine. A new column calculated from a column that does not change: run it twice,
you get the same column twice. And results with a new name: deduped, sorted_df. df itself never changes,
so the second run does exactly the same as the first.

On the right, the trouble. The first line is the same formula as on the left, but it overwrites temperature
with a value computed from temperature itself: the second run converts the already converted values again. And
df equals df dot merge: the second run merges again, and you get every station column twice.

So the rule for today: never change your input. Every result gets a new name. That also means you can always
look back at the data before a step.
-->

---
layout: default
label: 3 · Cleaning data
---

# A value per condition with <span class="dm-accent">case_when</span>

<div class="csv-file"><pre class="slidev-code input">  station  temperature
0    HS01          4.2
1    HS02         12.5
2    HS04         23.1
3    HS05         19.9</pre><span class="csv-name">df</span></div>

<DmColumns class="mt-2">
<DmColumn header="Calculating a label per temperature" tone="navy">

```py
df["temperature"].case_when([
    (df["temperature"] < 10, "cold"),
    (df["temperature"] < 20, "mild"),
    (df["temperature"] >= 20, "warm"),
])
```

<div class="output">

```text
0    cold
1    mild
2    warm
3    mild
Name: temperature, dtype: object
```

<span class="output-type">output, type: Series</span>
</div>

</DmColumn>
<DmColumn header="How it works" tone="violet" divider>

- A list of pairs: (condition, new value)
- The first condition that is True wins: 4.2 is also below 20, but it is cold
- Where no condition is True, the original value stays
- The result is a new Series: `df` stays the same

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.Series.case_when.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.Series.case_when.html</a></p>

</DmColumn>
</DmColumns>

<!--
So how do we change values per condition, without changing df? With case_when.

You call it on a column, and give it a list of pairs: a condition, and the value to use where the condition is
True. Here three pairs: below 10 degrees is cold, below 20 is mild, 20 or more is warm.

The conditions are checked in order, and the first one that is True wins, like if, elif, elif. 4.2 is also
below 20, but the first condition already matched, so it is cold. 19.9 is not below 10, but it is below 20:
mild. Where no condition is True, the original value stays; here every row matches one of them.

The result is a new Series. df is not changed. For HS03, one pair is enough: where the station is HS03, the
temperature converted to Celsius. You will see that on the next slide.

If you know SQL: this is CASE WHEN.
-->

---
layout: default
label: 3 · Cleaning data
---

# New DataFrames with <span class="dm-accent">assign</span>

```py
corrected = df.assign(
    temperature=df["temperature"].case_when([
        (df["station"] == "HS03", (df["temperature"] - 32) * 5 / 9),
    ]),
)
```

<DmColumns class="mt-4">
<DmColumn header="assign" tone="navy">

- Returns a **new** DataFrame, with the columns you name added or replaced
- `df` stays the same: this cell is idempotent

</DmColumn>
<DmColumn header="A column, not a text" tone="violet" divider>

```py
df.assign(x="temperature")
df.assign(x=df["temperature"])
```

The first puts the text "temperature" in every row.<br>
The second takes the values of the column.

</DmColumn>
</DmColumns>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.assign.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.assign.html</a></p>

<!--
Now the HS03 conversion: case_when with one pair, and the result back into a DataFrame, without touching df.
That is what assign does. assign returns a new DataFrame with the columns you name added, or replaced if they
already exist. Here we replace temperature by its converted version, and call the result corrected. df stays
the same, so you can run this cell as often as you like.

One trap, on the right. In assign, the name before the equals sign is the name of the new column. What comes
after it is the value. If you write the text "temperature" there, pandas puts that text in every row. For the
values of the column, you write df square brackets temperature, as everywhere else.

You will see df["x"] = ... and loc everywhere: that is fine to read, and fine for adding a new column. Just do
not change your input.
-->

---
layout: default
label: 3 · Cleaning data
---

# Method chaining with <span class="dm-accent">pd.col</span>

<p>Five steps: read the file, drop duplicates, mark the warm readings, keep only those, sort.</p>

<DmColumns class="mt-2">
<DmColumn header="A name for every step" tone="navy">

<pre class="marked-code">df1 = pd.read_csv("measurements.csv")
df2 = <span class="mark-name">df1</span>.drop_duplicates()
df3 = <span class="mark-name">df2</span>.assign(is_warm=<span class="mark-name">df2</span>["temperature"] &gt; 25)
df4 = <span class="mark-name">df3</span>[<span class="mark-name">df3</span>["is_warm"]]
df5 = <span class="mark-name">df4</span>.sort_values("temperature")</pre>

You have to name the right DataFrame, again and again.

⚠️ Write `df3` instead of `df4` by accident, and the result is silently wrong.

</DmColumn>
<DmColumn header="One chain, no names" tone="violet" divider>

<pre class="marked-code">df5 = (
    pd.read_csv("measurements.csv")
    .drop_duplicates()
    .assign(is_warm=<span class="mark-col">pd.col("temperature")</span> &gt; 25)
    [<span class="mark-col">pd.col("is_warm")</span>]
    .sort_values("temperature")
)</pre>

`pd.col("is_warm")` means the column `is_warm` of the DataFrame **at this step**, even though that DataFrame has no name.

</DmColumn>
</DmColumns>

<!--
Every analysis is a series of steps. Here five: read the file, drop the duplicates, add a column that says
whether a reading is warm, keep only the warm readings, and sort them.

On the left, the way you know: every step gets a name, df1 to df5. Look at what is marked in red: in every step,
you have to say which DataFrame you mean, sometimes twice. df2 dot assign, with df2 square brackets
temperature. df3 square brackets, df3 square brackets is_warm. That is a lot of names to keep straight. And a mistake is silent: write
df3 instead of df4 in the last step, and you sort all readings, the cold ones too. No error, just a wrong result.

On the right, exactly the same five steps, as one chain. Every step works on the result of the step before, so
the DataFrames in between never get a name. Then how do you refer to a column? That is what pd.col is for,
marked in green. pd.col temperature means: the column temperature of the DataFrame at this step. And look at
the filter: pd.col is_warm, the column we made one step earlier. With df square brackets, that is impossible:
there is no df.

The round brackets around the whole thing let you put one step per line. You read it from top to bottom, like a
recipe, and there are no names to mix up. Both give exactly the same df5.

While you are still exploring, the left version is handy: you can look at every step. Once the steps are clear,
the chain is cleaner.
-->

---
layout: statement
title: Exercise - cleaning data
---

# Exercise time: cleaning data

<p class="mt-6 text-lg opacity-80"><code>exercises/03-cleaning/</code></p>
<p class="mt-4 opacity-80">Check the daily KMI data for gaps and duplicates, then add the temperature range and a label per day.</p>
<p class="mt-1 opacity-60">About 20 minutes</p>

<!--
Check the daily KMI data for gaps and duplicates, add the temperature range of every day, and give every day
a label: cold, mild or warm. About 20 minutes.
-->

---
layout: section
---

# Data types and missing values

<!--
That file was clean. Real files are not. In this part, we read the measurements the hobby stations
export, and we look at what can go wrong: the type of a column, and values that are missing.
-->

---
layout: default
label: 4 · Data types and missing values
---

# Specifying the <span class="dm-accent">separator</span> and <span class="dm-accent">decimal sign</span>

<div class="csv-file"><pre class="slidev-code csv"><span class="csv-c0">station</span><span class="csv-sep">;</span><span class="csv-c1">timestamp</span><span class="csv-sep">;</span><span class="csv-c2">temperature</span><span class="csv-sep">;</span><span class="csv-c3">humidity</span><span class="csv-sep">;</span><span class="csv-c4">battery_v</span>
<span class="csv-c0">HS01</span><span class="csv-sep">;</span><span class="csv-c1">01/01/2023 01:00</span><span class="csv-sep">;</span><span class="csv-c2">16</span><span class="csv-sep">;</span><span class="csv-c3">49</span><span class="csv-sep">;</span><span class="csv-c4">4,15</span>
<span class="csv-c0">HS01</span><span class="csv-sep">;</span><span class="csv-c1">01/01/2023 01:30</span><span class="csv-sep">;</span><span class="csv-c2">16</span><span class="csv-sep">;</span><span class="csv-c3">51</span><span class="csv-sep">;</span><span class="csv-c4">4,1</span>
<span class="csv-c0">HS01</span><span class="csv-sep">;</span><span class="csv-c1">02/01/2023 08:30</span><span class="csv-sep">;</span><span class="csv-c2">ERR</span><span class="csv-sep">;</span><span class="csv-c3">87</span><span class="csv-sep">;</span><span class="csv-c4">4,08</span></pre><span class="csv-name">weather_export.csv</span></div>

```py
df = pd.read_csv(
    "weather_export.csv",
    sep=";",       # columns are separated by ;
    decimal=",",   # the decimal sign is a comma
)
```

<p class="note">By default, pandas expects a comma between columns and a dot as decimal sign. A CSV exported from
Excel with Belgian settings has neither.</p>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html</a></p>

<!--
This is what the export of the hobby stations looks like. It is a CSV file, but not the way pandas expects it.

The columns are separated by semicolons, and the decimal sign is a comma: 4,15. That is what Excel produces
with Belgian or most European settings, because the comma is already the decimal sign.

So we tell pandas: sep is a semicolon, decimal is a comma. Without these two, read_csv either fails with an
error, or reads everything as one column.

read_csv has dozens of options; the link at the bottom lists them all. You will only need a few.
-->

---
layout: default
label: 4 · Data types and missing values
---

# pandas infers the <span class="dm-accent">data types</span>

<div class="csv-file"><pre class="slidev-code csv"><span class="csv-c0">station</span><span class="csv-sep">;</span><span class="csv-c1">timestamp</span><span class="csv-sep">;</span><span class="csv-c2">temperature</span><span class="csv-sep">;</span><span class="csv-c3">humidity</span><span class="csv-sep">;</span><span class="csv-c4">battery_v</span>
<span class="csv-c0">HS01</span><span class="csv-sep">;</span><span class="csv-c1">01/01/2023 01:00</span><span class="csv-sep">;</span><span class="csv-c2">16</span><span class="csv-sep">;</span><span class="csv-c3">49</span><span class="csv-sep">;</span><span class="csv-c4">4,15</span>
<span class="csv-c0">HS01</span><span class="csv-sep">;</span><span class="csv-c1">01/01/2023 01:30</span><span class="csv-sep">;</span><span class="csv-c2">16</span><span class="csv-sep">;</span><span class="csv-c3">51</span><span class="csv-sep">;</span><span class="csv-c4">4,1</span>
<span class="csv-c0">HS01</span><span class="csv-sep">;</span><span class="csv-c1">02/01/2023 08:30</span><span class="csv-sep">;</span><span class="csv-c2">ERR</span><span class="csv-sep">;</span><span class="csv-c3">87</span><span class="csv-sep">;</span><span class="csv-c4">4,08</span></pre><span class="csv-name">weather_export.csv</span></div>

```py
df = pd.read_csv("weather_export.csv", sep=";", decimal=",")
```

<DmColumns class="mt-2">
<DmColumn divider>

```py
df.dtypes
```

<div class="output">

```text
station            str
timestamp          str
temperature        str
humidity         int64
battery_v      float64
dtype: object
```

</div>

⚠️ `temperature` is text (`str`), not a number. One `ERR` is enough, even in a file of 86 000 rows.

</DmColumn>
<DmColumn divider>

```py
pd.read_csv(..., na_values=["ERR"])
```

<div class="output small no-label">

```text
  station         timestamp  temperature  humidity  battery_v
0    HS01  01/01/2023 01:00         16.0        49       4.15
1    HS01  01/01/2023 01:30         16.0        51       4.10
2    HS01  02/01/2023 08:30          NaN        87       4.08
```

</div>

`na_values`: values interpreted as missing, on top of the defaults: an empty string, `NA`, `null`, `NaN`, `#N/A`, ...

</DmColumn>
</DmColumns>

<!--
pandas looks at the values in every column and decides on a type. Let's check: dtypes. station is text,
timestamp is text, battery_v is a float, humidity an integer. But temperature is text, not a number.

Why? Look at the last row of the file: ERR. The stations write ERR when a reading failed. One single value
that is not a number, and pandas has no choice but to make the whole column text. And then you cannot
calculate with it.

The fix is on the right: na_values. You tell pandas: ERR means missing. Now temperature is a number column,
with NaN where the ERR was: a missing value, as you saw this morning.

pandas already treats some values as missing by default: an empty string, NA, NaN and a few more. na_values
adds your own on top of those.
-->

---
layout: default
label: 4 · Data types and missing values
---

# Setting data types yourself

<div class="grid gap-8 items-center" style="grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)">
<div class="csv-file"><pre class="slidev-code input">  station humidity
0    HS01       49
1    HS01       51
2    HS01      ERR</pre><span class="csv-name">df</span></div>

<div>

`humidity` should hold whole numbers, but because of one `ERR` the whole column is text. The best fix is while reading the file:

```py
pd.read_csv(..., na_values=["ERR"],
            dtype={"humidity": "Int64"})
```

</div>
</div>

<p class="mt-3 mb-0">For a column that is already text, there are two ways:</p>

<DmColumns class="mt-2">
<DmColumn header="Casting with astype" tone="navy">

```py
df["humidity"].astype("Int64")
```

<div class="output small no-label">

```text
ArrowInvalid: Failed to parse string:
'ERR' as a scalar of type int64
```

</div>

`astype` stops with an error as soon as one value cannot be converted.

</DmColumn>
<DmColumn header="Converting text with pd.to_numeric" tone="violet" divider>

```py
pd.to_numeric(df["humidity"], errors="coerce")
```

<div class="output small no-label">

```text
0    49.0
1    51.0
2     NaN
Name: humidity, dtype: float64
```

</div>

With `errors="coerce"`, every value that cannot be converted becomes missing, without a warning.

</DmColumn>
</DmColumns>

<!--
Here is a humidity column that should hold whole numbers. But one value is ERR, and because of that one value,
the whole column is text.

The best fix is while reading the file. na_values says that ERR means missing, and dtype gives the type per
column, here Int64: a whole number that can also be missing. Then the DataFrame is right from the start.

For a column that is already text, there are two ways. On the left: astype. Converting a column to another type is called casting. You give the type you want, here
Int64 again. But astype stops with an error as soon as one value cannot be
converted. ERR cannot, so you get this error.

On the right: pd.to_numeric, for text that should be numbers. With errors="coerce", every value that cannot be
converted becomes missing, instead of giving an error. Useful, but careful: it does that without a warning,
whatever the value was.
-->

---
layout: default
label: 4 · Data types and missing values
---

# Two families of data types

<DmComparison
  class="types-cmp mt-2"
  :rows="['Integers', 'Floats', 'Text', 'True/False']"
  :groups="[{ label: 'Default', span: 2 }, { label: 'Nullable', span: 2 }]"
  :cols="['Type', 'Missing value', 'Type', 'Missing value']"
>
  <template #r0c0><code>int64</code></template>
  <template #r0c1>not possible</template>
  <template #r0c2><code>Int64</code></template>
  <template #r0c3><code>pd.NA</code></template>
  <template #r1c0><code>float64</code></template>
  <template #r1c1>floating-point NaN</template>
  <template #r1c2><code>Float64</code></template>
  <template #r1c3><code>pd.NA</code></template>
  <template #r2c0><code>str</code></template>
  <template #r2c1>floating-point NaN (!)</template>
  <template #r2c2><code>string</code></template>
  <template #r2c3><code>pd.NA</code></template>
  <template #r3c0><code>bool</code></template>
  <template #r3c1>not possible</template>
  <template #r3c2><code>boolean</code></template>
  <template #r3c3><code>pd.NA</code></template>
</DmComparison>

<div class="missing-flow">
  <div class="mf-question">Is a missing value equal to 49?</div>
  <div class="mf-answer"><code>np.nan == 49</code><span class="mf-arrow">→</span><b>No</b> (<code>False</code>)</div>
  <div class="mf-answer"><code>pd.NA == 49</code><span class="mf-arrow">→</span><b>Unknown</b> (<code>pd.NA</code>)</div>
</div>

<p class="note">Use <code>pd.read_csv(..., dtype_backend="numpy_nullable")</code> to get nullable types for every column.<br>Use <code>pd.isna(x)</code> to check if a value is missing.</p>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/user_guide/missing_data.html" target="_blank">https://pandas.pydata.org/docs/user_guide/missing_data.html</a></p>

<!--
Int64 is not a one-off. pandas has two families of types.

The default family, on the left, comes from NumPy. Integers and True/False cannot hold a missing value at
all, and the missing value of the others is NaN, a special floating-point value. Even for text, which is odd:
a text column whose missing value is a float. pandas did that on purpose, so that older code keeps working.
This is what pandas gives you unless you ask otherwise, and what you will see in almost every example online.

The nullable family, on the right, was added later. Every type can hold a missing value, and it is always
the same one: NA. In code you write it as pd.NA; in an output, pandas shows it as NA between angle
brackets, as you saw on the previous slide. You recognise the nullable types by the capital letter or the
written-out name.

The difference is not just how a missing value looks. It is what it means. Is a missing value equal to 49?
NaN says no: False. NA says: I don't know, the answer is NA. That is how NULL works in SQL. It matters when
you count or filter: count the readings that are not 49, and with NaN the unknown readings are counted as
"not 49", with NA they are left out. And to check whether a value is missing, do not compare it with
anything: use pd.isna. It works for NaN and NA alike.

If you want the nullable types everywhere, dtype_backend does that while reading. For today, the defaults
are fine. Just know that both exist when you see a capital Int64 somewhere.
-->

---
layout: default
label: 4 · Data types and missing values
---

# Reading <span class="dm-accent">dates and times</span>

<div class="csv-file"><pre class="slidev-code csv"><span class="csv-c0">timestamp</span>
<span class="csv-c0">01/02/2023 08:00</span>
<span class="csv-c0">13/02/2023 14:30</span></pre><span class="csv-name">timestamps.csv</span></div>

<DmColumns class="mt-2">
<DmColumn header="Parsing dates while reading a CSV" tone="navy">

```py
pd.read_csv("timestamps.csv",
            parse_dates=["timestamp"],
            date_format="%d/%m/%Y %H:%M")
```

<div class="output">

```text
            timestamp
0 2023-02-01 08:00:00
1 2023-02-13 14:30:00
```

</div>

`%d/%m/%Y %H:%M` means day/month/year hour:minute.

<p class="docs">📖 <a href="https://docs.python.org/3/library/datetime.html#format-codes" target="_blank">https://docs.python.org/3/library/datetime.html#format-codes</a></p>

</DmColumn>
<DmColumn header="Converting a string column to datetime" tone="violet" divider>

```py
pd.to_datetime(df["timestamp"],
               format="%d/%m/%Y %H:%M")
```

<div class="output">

```text
0   2023-02-01 08:00:00
1   2023-02-13 14:30:00
Name: timestamp, dtype: datetime64[us]
```

</div>

Use this when a column is still text, for example because you read the file without `parse_dates`.

⚠️ Always give the format. Without it, pandas guesses, and it can guess wrong.

</DmColumn>
</DmColumns>

<!--
Here is a small file with two timestamps: the first and the thirteenth of February. In the file, they are
text. To calculate with time, they have to become real dates and times. There are two ways.

On the left, the best one: while reading. parse_dates says which columns hold dates and times, and date_format
says how they are written. Day, month, year, then hours and minutes, with these percent codes. The link below
lists all the codes.

On the right: a column that is already in a DataFrame as text, for example because you read the file without
parse_dates. pd.to_datetime converts it, with the same format codes. Like astype, it gives a new Series. The
result is the same, and here you see the type: datetime64. A naive date and time, because the file does not say
which time zone it is in. More on that on the next slide.

Always give the format. Without it, pandas guesses, and it guesses the American order, month first. So 1
February becomes 2 January. And if somewhere further down there is a date that does not fit its guess, like the
13th of February, pandas gives up and leaves the whole column as text. In neither case do you get a warning.
-->

---
layout: default
label: 4 · Data types and missing values
---

# <span class="dm-accent">Naive</span> and <span class="dm-accent">time-zone-aware</span> datetimes

<DmColumns class="mt-2">
<DmColumn header="Naive" tone="navy">

<div class="csv-file"><pre class="slidev-code input">2023-07-01 14:00:00</pre><span class="csv-name">df["naive"] (example)</span></div>

A date and a clock time, without a time zone.

pandas calls this type `datetime64[us]`.

</DmColumn>
<DmColumn header="Time-zone aware" tone="violet" divider>

<div class="csv-file"><pre class="slidev-code input">2023-07-01 14:00:00<span style="background: #e6f2e7; color: #2e7d32; border-radius: 3px; font-weight: 700">+02:00</span></pre><span class="csv-name">df["aware"] (example)</span></div>

An exact moment in time, with its time zone. The time zone is part of the type.

<p>pandas calls this type <code style="white-space: nowrap">datetime64[us, Europe/Brussels]</code>.</p>

</DmColumn>
</DmColumns>

<DmColumns class="mt-2">
<DmColumn header="Converting between the two" tone="plain">

<div class="grid gap-x-6 gap-y-0 items-center" style="grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr)">
<div>

```py
df["naive"].dt.tz_localize("Europe/Brussels")
```

</div>
<div>

Naive → aware: `2023-07-01 14:00:00+02:00`

</div>
<div>

```py
df["aware"].dt.tz_localize(None)
```

</div>
<div>

Aware → naive: `2023-07-01 14:00:00`

</div>
<div>

```py
df["aware"].dt.tz_convert("UTC")
```

</div>
<div>

Aware → aware: `2023-07-01 12:00:00+00:00` (same moment in time)

</div>
</div>

</DmColumn>
</DmColumns>

<!--
The dates and times we just read are naive. On the left: a date and a clock time, two o'clock in the
afternoon, but without a time zone. Two o'clock in Brussels is a different moment than two o'clock in New York,
and a naive datetime does not say which one it is. In pandas, its type is datetime64, with us for microseconds.

On the right, time-zone aware: the same clock time, plus the offset from UTC, plus two hours. That is one exact
moment. And pandas also keeps the time zone itself: it is part of the type, here Europe/Brussels. That is not
the same everywhere: Spark's TIMESTAMP, for example, stores the moment but not the time zone.

At the bottom, how to go from one to the other. tz_localize sets the time zone, and keeps the clock time: the
naive two o'clock becomes two o'clock Brussels time, plus two hours in summer. Give it None, and it removes the
time zone again, still keeping the clock time. pandas knows the
rules of each time zone, so in winter it would be plus one hour.

tz_convert changes the time zone, and keeps the moment. Only the clock time and the offset change: two
o'clock in Brussels is twelve o'clock UTC. So the difference: tz_localize keeps the clock time, tz_convert keeps
the moment.

Python uses the same words, naive and aware. In the exercise, you will see what summer time does to a day.
-->

---
layout: default
label: 4 · Data types and missing values
---

# Two families of data types, <span class="dm-accent">with dates and times</span>

<DmComparison
  class="types-cmp mt-2"
  :rows="['Integers', 'Floats', 'Text', 'True/False']"
  :groups="[{ label: 'Default', span: 2 }, { label: 'Nullable', span: 2 }]"
  :cols="['Type', 'Missing value', 'Type', 'Missing value']"
>
  <template #r0c0><code>int64</code></template>
  <template #r0c1>not possible</template>
  <template #r0c2><code>Int64</code></template>
  <template #r0c3><code>pd.NA</code></template>
  <template #r1c0><code>float64</code></template>
  <template #r1c1>floating-point NaN</template>
  <template #r1c2><code>Float64</code></template>
  <template #r1c3><code>pd.NA</code></template>
  <template #r2c0><code>str</code></template>
  <template #r2c1>floating-point NaN (!)</template>
  <template #r2c2><code>string</code></template>
  <template #r2c3><code>pd.NA</code></template>
  <template #r3c0><code>bool</code></template>
  <template #r3c1>not possible</template>
  <template #r3c2><code>boolean</code></template>
  <template #r3c3><code>pd.NA</code></template>
</DmComparison>

<div class="types-extra">
  <div class="tx-label">Date and time, naive</div>
  <div class="tx-cell"><code>datetime64[us]</code></div>
  <div class="tx-cell tx-missing"><code>NaT</code> (not a time)</div>
  <div class="tx-none">No nullable version yet.<br>Proposed in PDEP-16, still under discussion.</div>
  <div class="tx-label">Date and time, with time zone</div>
  <div class="tx-cell"><code>datetime64[us, UTC]</code></div>
  <div class="tx-cell tx-missing"><code>NaT</code></div>
</div>

<p class="note">There is no separate type for a date without a time: 01/07/2023 becomes 2023-07-01 00:00:00.</p>

<p class="docs">📖 <a href="https://github.com/pandas-dev/pandas/pull/58988" target="_blank">https://github.com/pandas-dev/pandas/pull/58988</a></p>

<!--
Back to the two families of types, now with dates and times added at the bottom.

In the default family, a date and time is datetime64: naive, or with a time zone in the type, like UTC. Its
missing value is not NaN but NaT: not a time. It behaves like NaN: isna finds it, and it is never equal to
anything.

On the nullable side, there is nothing, marked in red. pandas has no nullable date and time type yet. Even if
you read with dtype_backend numpy_nullable, a date and time column stays datetime64, with NaT. There is a
proposal to make every type use the same missing value, NA, including dates and times: PDEP-16. It is still under
discussion, so do not expect it soon. The link at the bottom is that proposal.

One more thing: pandas has no separate type for a date without a time. A date like the first of July becomes
the first of July at midnight. Usually that is exactly what you want.
-->

---
layout: default
label: 4 · Data types and missing values
---

# Working with dates and times

<div class="csv-file"><pre class="slidev-code input">            timestamp  temperature
0 2023-07-01 14:00:00         24.1
1 2023-07-05 03:30:00         15.2
2 2023-07-09 14:00:00         27.3</pre><span class="csv-name">df</span></div>

<DmColumns class="mt-2">
<DmColumn header="Parts of a date with .dt" tone="navy">

```py
df["timestamp"].dt.hour
```

<div class="output">

```text
0    14
1     3
2    14
Name: timestamp, dtype: int32
```

</div>

Also `.dt.month`, `.dt.day_of_year`, ...

</DmColumn>
<DmColumn header="Converting to date with .dt.normalize()" tone="violet" divider>

```py
df["timestamp"].dt.normalize() == "2023-07-05"
```

<div class="output">

```text
0    False
1     True
2    False
Name: timestamp, dtype: bool
```

</div>

`normalize` sets the time to midnight: 2023-07-05 03:30 becomes 2023-07-05 00:00.

</DmColumn>
</DmColumns>

<!--
Once a column holds real dates and times, you can do much more with it than with text.

On the left: the dt accessor gives you the parts of every date. Here the hour: 14, 3, 14. There is also the
month, the day of the year, the name of the day, and more.

On the right: how to select one day. normalize sets the time of every value to midnight, so 5 July at half
past three becomes 5 July at midnight. Then you can compare it with the date written as text: pandas turns
that text into 5 July at midnight too. It gives True or False per row, so you can use it to select rows, as
you did with any other condition.
-->

---
layout: default
label: 4 · Data types and missing values
---

# Plotting with <span class="dm-accent">dates on the x-axis</span>

<DmColumns class="mt-2">
<DmColumn header="Reading without parse_dates" tone="navy">

```py
daily = pd.read_csv(
    "kmi_daily_2023.csv",
)


zeebrugge = daily[daily["name"] == "ZEEBRUGGE"]
zeebrugge.plot(x="timestamp", y="temp_max")
```

<img src="/img/plot-text-x.png" alt="The highest temperature in Zeebrugge, with the timestamps as text on the x-axis, written over each other" style="width: 100%; margin-top: 12px" />

⚠️ These dates are strings, i.e., labels.

</DmColumn>
<DmColumn header="Reading with parse_dates" tone="violet" divider class="hl-bg">

```py {3}
daily = pd.read_csv(
    "kmi_daily_2023.csv",
    parse_dates=["timestamp"],
    date_format="%Y-%m-%d",
)
zeebrugge = daily[daily["name"] == "ZEEBRUGGE"]
zeebrugge.plot(x="timestamp", y="temp_max")
```

<img src="/img/plot-x-y.png" alt="The highest temperature in Zeebrugge over the year, with the months on the x-axis" style="width: 100%; margin-top: 12px" />

</DmColumn>
</DmColumns>

<!--
One more reason to read dates as dates: plots. On the left, the timestamp is still text. pandas puts the texts
on the x-axis as labels, and they are written over each other.

On the right, the same file read with parse_dates. Now pandas knows it is time, and the x-axis shows the months.
-->

---
layout: statement
title: Exercise - data types and missing values
---

# Exercise time: data types and missing values

<p class="mt-6 text-lg opacity-80"><code>exercises/04-data-types/</code></p>
<p class="mt-4 opacity-80">Read the hourly export of HS01 with the right types, and convert its times from UTC to Belgian time.</p>
<p class="mt-1 opacity-60">About 20 minutes</p>

<!--
Your turn: read the hourly export of one hobby station so that every column gets the right type, dates
included, and convert its times from UTC to Belgian time. About 20 minutes.
-->

---
layout: section
---

# Grouping and aggregating

<!--
The data is clean now. Time to ask questions of it. Almost every question in data analysis is a question
per group: per station, per month, per day. In this part: groupby, and its big brother, the pivot table.
-->

---
layout: default
label: 5 · Grouping and aggregating
---

# Statistics per group with <span class="dm-accent">groupby</span>

<div class="csv-file"><pre class="slidev-code input">  station  temperature
0    HS01         16.0
1    HS01         15.8
2    HS02         14.6
3    HS02         15.0</pre><span class="csv-name">df</span></div>

<DmColumns class="mt-2">
<DmColumn header="Calculating the mean per station" tone="navy">

```py
df.groupby("station")["temperature"].mean()
```

<div class="output">

```text
station
HS01    15.9
HS02    14.8
Name: temperature, dtype: float64
```

<span class="output-type">output, type: Series</span>
</div>

</DmColumn>
<DmColumn header="Turning the station back into a column" tone="violet" divider>

⚠️ Note how the station became the (named) index. To avoid that, use `.reset_index()`:

```py
means = df.groupby("station")["temperature"].mean()
means.reset_index()
```

<div class="output">

```text
  station  temperature
0    HS01         15.9
1    HS02         14.8
```

<span class="output-type">output, type: DataFrame</span>
</div>

</DmColumn>
</DmColumns>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/user_guide/groupby.html" target="_blank">https://pandas.pydata.org/docs/user_guide/groupby.html</a></p>

<!--
This morning we computed one number for a whole column: the mean temperature. But the question is almost
never "what is the mean of everything". It is: the mean per station, per month, per day. That is groupby.

Three steps. Split the rows into groups, one per station. Apply something to each group: here the mean of
the temperature. Combine the results into one table: one row per station.

Look at the result: the station codes are on the left, in the index, with the name station above them. They
are no longer a normal column. On the right, reset_index turns them back into a column, and you have an
ordinary DataFrame again, with row numbers 0 and 1.

If you know SQL: this is GROUP BY. If you know Excel: it is what a pivot table does, and we get to those in
a minute.
-->

---
layout: default
label: 5 · Grouping and aggregating
---

# Several statistics at once with <span class="dm-accent">agg</span>

<DmColumns>
<DmColumn header="Calculating one column per statistic" tone="navy">

```py
df.groupby("station").agg(
    mean_temp=("temperature", "mean"),
    max_temp=("temperature", "max"),
    readings=("temperature", "count"),
)
```

<div class="output">

```text
         mean_temp  max_temp  readings
station
HS01          15.9      16.0         2
HS02          14.8      15.0         2
```

</div>

</DmColumn>
<DmColumn header="How to read it" tone="violet" divider>

`new_name=(column, statistic)`

Statistics: `"mean"`, `"median"`, `"min"`, `"max"`, `"sum"`, `"std"`, `"count"`, `"nunique"`, ...

`"count"` counts the values that are not missing.<br>
`"size"` counts the rows.

</DmColumn>
</DmColumns>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/user_guide/groupby.html#named-aggregation" target="_blank">https://pandas.pydata.org/docs/user_guide/groupby.html#named-aggregation</a></p>

<!--
One statistic per group is often not enough. agg computes several at once, and here you also choose the names
of the result columns.

Every argument reads as: the new column name, equals, which column, and which statistic. So mean_temp is the
mean of the temperature, max_temp its maximum, and readings the number of temperatures.

You can mix columns: the mean of the temperature and the maximum of the humidity in one go.

A detail that matters on real data: count counts the values that are not missing. size counts the rows. If a
station has many missing values, those two differ, and that difference is itself worth knowing.
-->

---
layout: default
label: 5 · Grouping and aggregating
---

# Grouping by <span class="dm-accent">two columns</span>

<DmColumns>
<DmColumn header="Input: one row per measurement" tone="navy">

<div class="csv-file"><pre class="slidev-code input">  station  month  temperature
0    HS01      1          4.0
1    HS01      1          5.0
2    HS01      2          6.0
3    HS02      1          3.0
4    HS02      2          5.5</pre><span class="csv-name">df</span></div>

</DmColumn>
<DmColumn header="Calculating one row per station and month" tone="violet" divider>

```py
df.groupby(["station", "month"])["temperature"].mean()
```

<div class="output">

```text
station  month
HS01     1        4.5
         2        6.0
HS02     1        3.0
         2        5.5
Name: temperature, dtype: float64
```

</div>

</DmColumn>
</DmColumns>

<p class="note">A list of columns makes a group for every combination.<br>The result has a MultiIndex, with two levels. <code>reset_index()</code> turns both back into columns.</p>

<!--
You can group by more than one column: give a list. Now every combination of station and month is a group,
and you get one mean per combination.

The month column comes from the timestamp, with dt.month, as you saw this morning.

The result is long: one row per combination, with two levels in the index. That is fine for a computer, but
to read it, or to compare stations, a table with the stations side by side is easier. That is the next slide.
-->

---
layout: default
label: 5 · Grouping and aggregating
---

# Two groupings at once: <span class="dm-accent">pivot_table</span>

<DmColumns>
<DmColumn header="Input: one row per measurement" tone="navy">

<div class="csv-file"><pre class="slidev-code input">  station  month  temperature
0    HS01      1          4.0
1    HS01      1          5.0
2    HS01      2          6.0
3    HS02      1          3.0
4    HS02      2          5.5</pre><span class="csv-name">df</span></div>

</DmColumn>
<DmColumn header="Calculating the mean per month and station" tone="violet" divider>

```py
df.pivot_table(
    index="month",
    columns="station",
    values="temperature",
    aggfunc="mean",
)
```

<div class="output">

```text
station  HS01  HS02
month
1         4.5   3.0
2         6.0   5.5
```

</div>

</DmColumn>
</DmColumns>

<p class="note">The same numbers as on the previous slide, as a table. Like a pivot table in Excel: rows, columns, and a value with how to combine it. <code>.plot()</code> on it draws one line per station.</p>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot_table.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot_table.html</a></p>

<!--
These are the same numbers as on the previous slide, but laid out as a table. pivot_table puts one grouping
in the rows and the other in the columns. Here: a row per month, a column per station, and the mean
temperature in every cell.

If you have made a pivot table in Excel, this is exactly that: what goes in the rows, what in the columns,
which value, and how to combine it.

A table like this is often where problems jump out: one station that is fine in winter and way off in summer.
And because the months are the index and every station is a column, .plot() on it gives you one line per
station, with a legend.
-->

---
layout: default
label: 5 · Grouping and aggregating
---

# <span class="dm-accent">Windowing</span> operations

<DmColumns class="mt-2">
<DmColumn header="Calculating the change with .diff(1)" tone="navy">

```py
df.assign(
    change=df["temperature"].diff(1)
)
```

<div class="output">

```text
   day  temperature  change
0    1         10.0     NaN
1    2         12.0     2.0
2    3         14.0     2.0
3    4         13.0    -1.0
4    5          9.0    -4.0
```

</div>

Every value minus the value one row earlier.

</DmColumn>
<DmColumn header="Calculating a rolling mean with .rolling(3)" tone="violet" divider>

```py
df.assign(
    rolling_mean=df["temperature"].rolling(3).mean()
)
```

<div class="output">

```text
   day  temperature  rolling_mean
0    1         10.0           NaN
1    2         12.0           NaN
2    3         14.0          12.0
3    4         13.0          13.0
4    5          9.0          12.0
```

</div>

The mean of every value and the two before it.<br>
Also `.sum()`, `.min()`, `.max()`, `.median()`, `.std()`, ...

</DmColumn>
</DmColumns>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/user_guide/window.html" target="_blank">https://pandas.pydata.org/docs/user_guide/window.html</a></p>

<!--
Unlike groupby, these give a value for every row: they look at the rows around it.

On the left: diff(1), every value minus the value one row earlier. Day 2 is 12 minus 10: 2. The first day has
nothing before it, so it is missing.

On the right: a rolling mean. rolling(3) is a window of three rows: the row itself and the two before it. Day 3
is the mean of days 1, 2 and 3: 12. Instead of mean, you can also take the sum, the minimum, the maximum and
more. A 7-day rolling mean of daily temperatures shows the trend without the day-to-day noise.
-->

---
layout: statement
title: Exercise - grouping and aggregating
---

# Exercise time: grouping and aggregating

<p class="mt-6 text-lg opacity-80"><code>exercises/05-aggregations/</code></p>
<p class="mt-4 opacity-80">Compare the KMI stations per station, and per station and month.</p>
<p class="mt-1 opacity-60">About 20 minutes</p>

<!--
Compare the KMI stations: per station, and per station and month. Is the coast really milder? About 20
minutes, then a break.
-->

---
layout: section
---

# File formats

<!--
Data does not only come as CSV. In this part: an Excel file somebody keeps by hand, with a sheet per station,
and Parquet, a better format to save your cleaned data in.
-->

---
layout: default
label: 6 · File formats
---

# Reading <span class="dm-accent">Excel</span> files

<div class="xlsx">
<table>
<thead><tr><th></th><th>A</th><th>B</th><th>C</th></tr></thead>
<tbody>
<tr><th>1</th><td colspan="3" style="font-weight: 700; font-size: 1.15em">Rain gauge logbook - Brugge</td></tr>
<tr><th>2</th><td></td><td></td><td></td></tr>
<tr><th>3</th><td>Date</td><td>Rain</td><td>Remarks</td></tr>
<tr><th>4</th><td></td><td>mm</td><td></td></tr>
<tr><th>5</th><td class="num">02/01/2023</td><td class="num">1.7</td><td>includes the weekend</td></tr>
<tr><th>6</th><td class="num">03/01/2023</td><td class="num">2.1</td><td></td></tr>
<tr><th>7</th><td class="num">04/01/2023</td><td class="num">0.7</td><td></td></tr>
</tbody>
</table>
<div class="tabs"><span>Stations</span><span>HS01</span><span>HS02</span><span class="active">HS03</span><span>HS04</span><span>HS05</span></div>
<span class="csv-name">rain_logbook.xlsx</span>
</div>

<div class="grid grid-cols-2 gap-6 mt-3 tight">
<div>

```py
pd.read_excel(
    "rain_logbook.xlsx", sheet_name="HS03"
)
```

<div class="output no-label" style="--slidev-code-font-size: 10.5px; --slidev-code-line-height: 15px">

```text
  Rain gauge logbook - Brugge Unnamed: 1            Unnamed: 2
0                         NaN        NaN                   NaN
1                        Date       Rain               Remarks
2                         NaN         mm                   NaN
3         2023-01-02 00:00:00        1.7  includes the weekend
4         2023-01-03 00:00:00        2.1                   NaN
5         2023-01-04 00:00:00        0.7                   NaN
```

</div>

</div>
<div>

```py
pd.read_excel(
    "rain_logbook.xlsx", sheet_name="HS03", skiprows=[0, 1, 3]
)
```

<div class="output no-label" style="--slidev-code-font-size: 10.5px; --slidev-code-line-height: 15px">

```text
        Date  Rain               Remarks
0 2023-01-02   1.7  includes the weekend
1 2023-01-03   2.1                   NaN
2 2023-01-04   0.7                   NaN
```

</div>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html</a></p>

</div>
</div>

<!--
The volunteers also keep a rain logbook in Excel. One sheet per station, plus a sheet with the list of
stations.

Excel files made by people have a title, empty rows, a row with units. read_excel needs the sheet name, and
then on the left you see what happens if you read it as it is: the title becomes a column name, and the real
column names end up as a data row.

On the right: skiprows, with the row numbers to skip, counting from zero. Row 0 is the title, row 1 is empty,
row 3 has the units. Now Date, Rain and Remarks are the column names, and the data starts where it should.
-->

---
layout: default
label: 6 · File formats
---

# Stacking DataFrames with <span class="dm-accent">pd.concat</span>

```py
hs01 = pd.read_excel(..., sheet_name="HS01").assign(station="HS01")
hs02 = pd.read_excel(..., sheet_name="HS02").assign(station="HS02")
```

<div class="grid grid-cols-2 gap-6 items-start">
<div class="csv-file"><pre class="slidev-code input">        Date  Rain station
0 2023-01-01   0.0    HS01
1 2023-01-02   4.2    HS01</pre><span class="csv-name">hs01</span></div>
<div class="csv-file"><pre class="slidev-code input">        Date  Rain station
0 2023-01-01   0.3    HS02
1 2023-01-02   4.6    HS02</pre><span class="csv-name">hs02</span></div>
</div>

<DmColumns class="mt-2">
<DmColumn header="Stacking with pd.concat" tone="navy">

```py
pd.concat([hs01, hs02])
```

<div class="output"><pre class="marked-code">        Date  Rain station
<span class="mark-index">0</span> 2023-01-01   0.0    HS01
<span class="mark-index">1</span> 2023-01-02   4.2    HS01
<span class="mark-index">0</span> 2023-01-01   0.3    HS02
<span class="mark-index">1</span> 2023-01-02   4.6    HS02</pre></div>

⚠️ The row numbers 0 and 1 now occur twice.

</DmColumn>
<DmColumn header="Numbering the rows again with ignore_index" tone="violet" divider>

```py
pd.concat([hs01, hs02], ignore_index=True)
```

<div class="output"><pre class="marked-code">        Date  Rain station
<span class="mark-index">0</span> 2023-01-01   0.0    HS01
<span class="mark-index">1</span> 2023-01-02   4.2    HS01
<span class="mark-index">2</span> 2023-01-01   0.3    HS02
<span class="mark-index">3</span> 2023-01-02   4.6    HS02</pre></div>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.concat.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.concat.html</a></p>

</DmColumn>
</DmColumns>

<!--
The logbook has one sheet per station. To compare the stations, you want them in one DataFrame.

Read every sheet, and add a column with the station, with assign: otherwise you no longer know where a row came
from. Then pd.concat puts the DataFrames under each other. You give it a list.

On the left: every DataFrame keeps its own row numbers, so 0 and 1 occur twice. Usually harmless, but some
operations match rows by those numbers, and then it goes wrong without an error. On the right: ignore_index
numbers the rows again, 0 to 3. Use that by default.
-->

---
layout: default
label: 6 · File formats
---

# Saving to <span class="dm-accent">Parquet</span>

<DmColumns>
<DmColumn header="CSV" tone="navy">

- **Text**: you can open it directly in any text or code editor
- Stores no types: every read has to guess again
- 3.0 MB for our measurements

</DmColumn>
<DmColumn header="Parquet" tone="violet" divider>

- **Binary**: you need a library like pandas to read it
- Stores the types with the data
- 0.5 MB, compressed

</DmColumn>
</DmColumns>

```py
df.to_parquet("hobby_measurements.parquet")
df = pd.read_parquet("hobby_measurements.parquet")
```

<p class="note">Clean the data once, save it as Parquet, and start the next step from that file.</p>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html</a></p>

<!--
Once your data is clean, save it. Not as CSV, but as Parquet.

A CSV is text: you can open it in any editor, which is nice. But it stores no types: every time you read it,
pandas guesses again, and you need sep, decimal, na_values and to_datetime again.

Parquet is binary. You cannot open it in a text editor, but it stores the types along with the data. The
dates are dates, Int64 stays Int64. And it is compressed: our measurements go from 3 megabytes to half a
megabyte.

So: clean the data once, save it as Parquet, and start the next step from that file. That is what we will do
for the rest of the day.
-->

---
layout: default
label: 6 · File formats
---

# Open table formats

<div class="logo-row">
  <img src="/img/logo-delta-lake.svg" alt="Delta Lake" />
  <img src="/img/logo-iceberg.svg" alt="Apache Iceberg" />
  <img src="/img/logo-hudi.png" alt="Apache Hudi" />
</div>

<p>Parquet files, with more:</p>

- A log of every change to the table
- History: read the table as it was last week
- Safe concurrent writes to the same table

<p class="note">Today we don't need these features: Parquet is enough.</p>

<!--
You may hear these names: Delta Lake, Iceberg, Hudi. They are table formats built on top of Parquet: a folder
of Parquet files, plus a log of every change.

That log gives you history, so you can read the table as it was last week, and it makes it safe for several
programs to write to the same table at once. That is why data platforms are built on them.

For an analysis on one machine, you don't need any of that. Parquet is enough. But when someone says
"it's in a Delta table": it's Parquet underneath, and pandas can read it.
-->

---
layout: statement
title: Exercise - file formats
---

# Exercise time: file formats

<p class="mt-6 text-lg opacity-80"><code>exercises/06-file-formats/</code></p>
<p class="mt-4 opacity-80">Read the rain logbook, combine the sheets of all stations, and save the result as Parquet.</p>
<p class="mt-1 opacity-60">About 15 minutes</p>

<!--
Read the rain logbook of the hobby stations, combine the sheets of all stations, and save the result as
Parquet. About 15 minutes.
-->

---
layout: section
---

# Joins

<!--
Data is often spread over several tables: the measurements in one, the names of the stations in another.
Combining two tables is a join. In this part: merge, inner and left joins, and joining on time.
-->

---
layout: default
label: 7 · Joins
---

# Combining DataFrames with a <span class="dm-accent">join</span> ("merge")

<div class="grid grid-cols-2 gap-6 items-start">
<div class="csv-file"><pre class="slidev-code input">  station  temperature
0    HS01         16.0
1    HS01         15.8
2    HS02         14.6</pre><span class="csv-name">measurements</span></div>
<div class="csv-file"><pre class="slidev-code input">  station             name
0    HS01  Mechelen garden
1    HS02     Gent rooftop</pre><span class="csv-name">stations</span></div>
</div>

```py
measurements.merge(stations, on="station")
```

<div class="output">

```text
  station  temperature             name
0    HS01         16.0  Mechelen garden
1    HS01         15.8  Mechelen garden
2    HS02         14.6     Gent rooftop
```

</div>

<p class="note">The column you join on is the <b>key</b>.</p>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html</a></p>

<!--
We have measurements, with a station code, and a separate table with the station names. To put the name next
to every measurement, we join: merge.

merge looks up, for every row on the left, the row on the right with the same station code, and adds its
columns. The column you join on is the key. HS01 appears twice in the measurements, so it gets the name twice.

If you know VLOOKUP in Excel: this is the same idea, for a whole table at once.
-->

---
layout: default
label: 7 · Joins
---

# <span class="dm-accent">Inner</span> and <span class="dm-accent">left</span> joins

<div class="grid grid-cols-2 gap-6 items-start">
<div class="csv-file"><pre class="slidev-code input">  station  temperature
0    HS01         16.0
1    HS02         14.6
2    HS06         15.2</pre><span class="csv-name">measurements</span></div>
<div class="csv-file"><pre class="slidev-code input">  station             name
0    HS01  Mechelen garden
1    HS02     Gent rooftop</pre><span class="csv-name">stations</span></div>
</div>

<DmColumns class="mt-2">
<DmColumn header="Inner join (the default): keys in both" tone="navy">

```py
measurements.merge(stations, on="station")
```

<div class="output">

```text
  station  temperature             name
0    HS01         16.0  Mechelen garden
1    HS02         14.6     Gent rooftop
```

</div>

HS06 is not in `stations`: dropped.

</DmColumn>
<DmColumn header="Left join: every row of the left table" tone="violet" divider>

```py
measurements.merge(stations, on="station", how="left")
```

<div class="output">

```text
  station  temperature             name
0    HS01         16.0  Mechelen garden
1    HS02         14.6     Gent rooftop
2    HS06         15.2              NaN
```

</div>

HS06 stays, with a missing `name`.

</DmColumn>
</DmColumns>

<p class="note">⚠️ A key that is not unique on the right duplicates rows on the left.</p>

<!--
What if a key has no partner? Here a new station, HS06, has measurements, but it is not in the station list
yet.

An inner join, the default, keeps only keys found in both tables: HS06 disappears, without any warning. A left
join keeps every row of the left table, and fills in NaN where there is no partner.

Two checks after every join. Compare the number of rows before and after: did you lose rows you expected to
keep? And: is the key unique on the right? If the same key appears twice on the right, every matching row on
the left is duplicated. That is the most common join bug.
-->

---
layout: default
label: 7 · Joins
---

# Joining on time with <span class="dm-accent">merge_asof</span>

<div class="grid grid-cols-2 gap-6 items-start">
<div class="csv-file"><pre class="slidev-code input">            timestamp  temp
0 2023-07-01 10:00:03  16.0
1 2023-07-01 10:30:02  16.2
2 2023-07-01 10:59:58  16.6</pre><span class="csv-name">hobby</span></div>
<div class="csv-file"><pre class="slidev-code input">            timestamp  kmi_temp
0 2023-07-01 10:00:00      16.4
1 2023-07-01 11:00:00      16.9</pre><span class="csv-name">kmi</span></div>
</div>

<DmColumns class="mt-2">
<DmColumn header="Joining exactly on the timestamp" tone="navy">

```py
hobby.merge(kmi, on="timestamp")
```

<div class="output">

```text
Empty DataFrame
Columns: [timestamp, temp, kmi_temp]
Index: []
```

</div>

The clocks are a few seconds off: no timestamp matches exactly.

</DmColumn>
<DmColumn header="Joining the nearest one, within 15 minutes" tone="violet" divider>

```py
pd.merge_asof(hobby, kmi, on="timestamp",
              direction="nearest",
              tolerance=pd.Timedelta(minutes=15))
```

<div class="output">

```text
            timestamp  temp  kmi_temp
0 2023-07-01 10:00:03  16.0      16.4
1 2023-07-01 10:30:02  16.2       NaN
2 2023-07-01 10:59:58  16.6      16.9
```

</div>

</DmColumn>
</DmColumns>

<p class="note">⚠️ Both tables must be sorted on the <code>on</code> column, or pandas raises an error.<br>💡 If you want to consider each station separately, use <code>by="station"</code> (needs a column <code>station</code>, of course).</p>

<!--
Joining on a time is a special case. Real clocks are never exactly on the hour: this hobby station sends its
readings a few seconds early or late. Join on the timestamp, and nothing matches. You get an empty DataFrame,
or worse, in real data, a few rows that happened to match and all the others silently gone.

merge_asof joins on the nearest value instead of the exact one. Here: the nearest KMI observation, at most 15
minutes away. 10:00:03 gets the KMI value of 10:00, 10:59:58 the one of 11:00. 10:30 is half an hour from both,
so it gets nothing: a missing value.

The other directions: backward takes the last observation at or before, which is the default; forward the
first one after. Two practical things: both tables must be sorted on the column you join on, otherwise pandas
gives an error, and with by you match within a group, for example per station.
-->

---
layout: statement
title: Exercise - joins
---

# Exercise time: joins

<p class="mt-6 text-lg opacity-80"><code>exercises/07-joins/</code></p>
<p class="mt-4 opacity-80">Join the KMI data with the list of stations, and find out how much colder it gets higher up.</p>
<p class="mt-1 opacity-60">About 10 minutes</p>

<!--
Join the KMI data with the list of stations, and find out how much colder it gets higher up. About 10
minutes.
-->

---
layout: section
---

# Regression

<!--
The last big part. Remember the two missing days in exercise 1: the KMI station in Sint-Katelijne-Waver
measured nothing on 11 and 12 June. Can we estimate them from the stations around it? That is a regression
model.
-->

---
layout: default
label: 8 · Regression
---

# Linear <span class="dm-accent">regression</span>

<DmColumns>
<DmColumn>

<img src="/img/regression-line.png" alt="The daily mean temperature in Sint-Katelijne-Waver against the one in Uccle in 2023, with a fitted line" style="width: 100%" />

</DmColumn>
<DmColumn divider>

The KMI station in Sint-Katelijne-Waver (SKW) missed 11 and 12 June 2023. Its neighbours: Uccle (Brussels) and Stabroek (Antwerp).

A linear regression finds the straight line closest to all points:

`skw = a × uccle + b`

With more inputs, the same idea:

`skw = a × uccle + b × stabroek + c`

</DmColumn>
</DmColumns>

<!--
Every point is one day of 2023: the mean temperature in Uccle against the one in Sint-Katelijne-Waver, which
lies between Brussels and Antwerp. They follow each other closely.

A linear regression finds the straight line that is closest to all points: SKW equals a times Uccle plus b.
With that line, you can estimate SKW on a day it did not measure. And you can give the model more inputs, for
example Stabroek, near Antwerp, as well. Then each input gets its own coefficient.

And the model stays useful: if the station fails again, we fill in the gap the same way.
-->

---
layout: default
label: 8 · Regression
---

# Every scikit-learn model: <span class="dm-accent">fit</span>, then <span class="dm-accent">predict</span>

<div class="grid gap-4 items-start" style="grid-template-columns: minmax(0, 0.95fr) minmax(0, 1fr)">
<div>

<div class="xy">
  <div class="xy-cols"><span></span><span class="xy-x">X: the inputs</span><span class="xy-y">y: to predict</span><span class="xy-arrow">⟶</span></div>
  <table class="xy-header">
    <colgroup><col class="c-date"><col class="c-u"><col class="c-z"><col class="c-m"></colgroup>
    <tbody>
    <tr><th>date</th><th class="xy-xc">temp_uccle</th><th class="xy-xc">temp_stabroek</th><th class="xy-yc">temp_skw</th></tr>
    </tbody>
  </table>
  <div class="xy-group">
    <span class="xy-tag">known: 363 days</span>
    <table>
      <colgroup><col class="c-date"><col class="c-u"><col class="c-z"><col class="c-m"></colgroup>
      <tbody>
      <tr><td>2023-01-01</td><td class="xy-xc">12.8</td><td class="xy-xc">12.7</td><td class="xy-yc">13.3</td></tr>
      <tr><td>2023-01-02</td><td class="xy-xc">9.2</td><td class="xy-xc">9.8</td><td class="xy-yc">9.8</td></tr>
      <tr><td>...</td><td class="xy-xc">...</td><td class="xy-xc">...</td><td class="xy-yc">...</td></tr>
      </tbody>
    </table>
  </div>
  <div class="xy-group">
    <span class="xy-tag">missing: 2 days (for now)</span>
    <table>
      <colgroup><col class="c-date"><col class="c-u"><col class="c-z"><col class="c-m"></colgroup>
      <tbody>
      <tr><td>2023-06-11</td><td class="xy-xc">24.4</td><td class="xy-xc">25.2</td><td class="xy-yc">???</td></tr>
      <tr><td>2023-06-12</td><td class="xy-xc">24.1</td><td class="xy-xc">25.0</td><td class="xy-yc">???</td></tr>
      </tbody>
    </table>
  </div>
</div>

```py
known = df[df["temp_skw"].notna()]
missing = df[df["temp_skw"].isna()]
X = known[["temp_uccle", "temp_stabroek"]]
y = known["temp_skw"]
X_missing = missing[["temp_uccle", "temp_stabroek"]]
```

</div>
<div>

<DmSteps dir="vertical" class="steps-code-sm">
<DmStep n="1" label="Create a model">

```py
model = sklearn.linear_model.LinearRegression()
```

or any other model, for example:

```py
model = sklearn.ensemble.RandomForestRegressor()
```

</DmStep>
<DmStep n="2" label="Fit it on the known days">

```py
model.fit(X, y)
```

</DmStep>
<DmStep n="3" label="Predict the missing days">

```py
model.predict(X_missing)
```

<div class="output small">

```text
array([25.11743099, 24.87904092])
```

<span class="output-type">output, type: NumPy array</span>
</div>

Use `pd.Series(...)` to turn it into a pandas Series.

</DmStep>
</DmSteps>

</div>
</div>

<p class="note">Every scikit-learn model has <code>fit</code> and <code>predict</code>: to try another model, you change only step 1.</p>

<!--
A model learns to go from inputs to what you want to predict. The inputs are called X: a table, one row per
day, here the temperature in Uccle and in Stabroek. What you want to predict is called y: one column, here the
temperature in Sint-Katelijne-Waver. We fit on the 363 days where we know it.

Then three steps. Create a model. Fit it on the known days. Predict the missing days: about 25.1 and 24.9
degrees.

And this is the point: every model in scikit-learn works like this. To try a random forest instead of a
straight line, you change only step one.
-->

---
layout: default
label: 8 · Regression
---

# How good is the estimate? Keep <span class="dm-accent">test data</span> apart

<table class="split-table">
  <thead>
    <tr><th>date</th><th class="xy-xc">temp_uccle</th><th class="xy-xc">temp_stabroek</th><th class="xy-yc">temp_skw</th><th></th><th class="split-pred">predicted</th></tr>
  </thead>
  <tbody>
    <tr><td>...</td><td class="xy-xc">...</td><td class="xy-xc">...</td><td class="xy-yc">...</td><td></td><td class="split-pred"></td></tr>
    <tr class="split-test"><td>2023-02-19</td><td class="xy-xc">8.5</td><td class="xy-xc">8.7</td><td class="xy-yc">9.1</td><td><span class="split-pill">test</span></td><td class="split-pred">8.8</td></tr>
    <tr class="split-train"><td>2023-02-20</td><td class="xy-xc">7.0</td><td class="xy-xc">8.3</td><td class="xy-yc">8.0</td><td><span class="split-pill">train</span></td><td class="split-pred"></td></tr>
    <tr class="split-train"><td>2023-02-21</td><td class="xy-xc">5.3</td><td class="xy-xc">7.3</td><td class="xy-yc">6.4</td><td><span class="split-pill">train</span></td><td class="split-pred"></td></tr>
    <tr class="split-test"><td>2023-02-22</td><td class="xy-xc">6.8</td><td class="xy-xc">7.0</td><td class="xy-yc">7.0</td><td><span class="split-pill">test</span></td><td class="split-pred">7.0</td></tr>
    <tr class="split-train"><td>2023-02-23</td><td class="xy-xc">7.8</td><td class="xy-xc">7.6</td><td class="xy-yc">7.9</td><td><span class="split-pill">train</span></td><td class="split-pred"></td></tr>
    <tr class="split-test"><td>2023-02-24</td><td class="xy-xc">4.8</td><td class="xy-xc">5.3</td><td class="xy-yc">5.2</td><td><span class="split-pill">test</span></td><td class="split-pred">5.2</td></tr>
    <tr class="split-test"><td>2023-02-25</td><td class="xy-xc">3.9</td><td class="xy-xc">4.2</td><td class="xy-yc">4.3</td><td><span class="split-pill">test</span></td><td class="split-pred">4.1</td></tr>
    <tr><td>...</td><td class="xy-xc">...</td><td class="xy-xc">...</td><td class="xy-yc">...</td><td></td><td class="split-pred"></td></tr>
  </tbody>
</table>

```py
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

<p class="note">The model never sees the test days, so we can compare its prediction with what was measured.<br>To predict the future, split by time instead: train on the past, test on what comes after.</p>

<!--
How good are those two estimates? We cannot check them: the station did not measure on those days. So we do
the next best thing. We set a quarter of the days we do know apart, the test data, fit the model on the rest,
the training data, and predict the test data. For those days we know the answer, so we can compare.

train_test_split picks the test days at random. random_state makes that the same every time, so your results
do not change each time you run the notebook. The four results are always in this order: X_train, X_test,
y_train, y_test.

One warning: if you want to predict the future, a random split is too optimistic. Then you split by time:
train on the past, test on what comes after.
-->

---
layout: default
label: 8 · Regression
---

# How good is the model? The <span class="dm-accent">mean absolute error</span>

<div class="grid gap-8 items-center" style="grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)">
<div>

<img src="/img/mae-errors.png" alt="Measured against predicted temperature for test days, with a red line from each point to the prediction line: the error of that day" style="width: 100%" />

</div>
<div>

The mean absolute error (MAE) is the average distance between prediction and measurement.

```py
from sklearn.metrics import mean_absolute_error

mean_absolute_error(y_test, y_pred)
```

<div class="output">

```text
0.2165123541224739
```

<span class="output-type">output, type: float</span>
</div>

</div>
</div>

<p class="docs">📖 <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html" target="_blank">https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html</a></p>

<!--
How good is the model? Here the test days: what the model predicted against what was measured. On the
diagonal, the prediction is exactly right. The red line is the error of each day: the distance to the
diagonal.

The mean absolute error is the average length of those red lines: too high and too low both count. For our
model: 0.22 degrees, on days it has never seen.
-->

---
layout: statement
title: Exercise - regression
---

# Exercise time: regression

<p class="mt-6 text-lg opacity-80"><code>exercises/08-regression/</code></p>
<p class="mt-4 opacity-80">Estimate the temperature in the Ardennes from the one in Brussels, and check it on October to December.</p>
<p class="mt-1 opacity-60">About 15 minutes</p>

<!--
Estimate the temperature in the Ardennes from the one in Brussels, and check it on the test data. About 15
minutes.
-->

---
layout: section
---

# Fetching data from an API

<!--
Our files only cover 2023, and only the columns we chose. The KMI publishes much more as open data, through
an API. In this part we fetch data from it ourselves.
-->

---
layout: default
label: 9 · Fetching data from an API
---

# What is a <span class="dm-accent">web API</span>?

<DmSteps dir="horizontal" class="mt-4">
  <DmStep n="1" label="You build a URL">with parameters that say what you want</DmStep>
  <DmStep n="2" label="The server parses the URL">and looks up the data you asked for</DmStep>
  <DmStep n="3" label="It responds">with a status code and the data, as JSON or CSV</DmStep>
</DmSteps>

<div class="grid gap-6 items-start mt-2" style="grid-template-columns: minmax(0, 2fr) minmax(0, 1fr)">
<div>

For KMI, to get the data about stations as JSON:

<p class="api-url"><a href="https://opendata.meteo.be/service/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=aws:aws_station&outputFormat=json" target="_blank">https://opendata.meteo.be/service/ows?<wbr>service=WFS&<wbr>version=2.0.0&<wbr>request=GetFeature&<wbr>typeNames=aws:aws_station&<wbr>outputFormat=json</a></p>

<table class="url-parts">
  <tbody>
    <tr><td>service=WFS</td><td>Web Feature Service: a standard for geographic data</td></tr>
    <tr><td>version=2.0.0</td><td>the version of that standard</td></tr>
    <tr><td>request=GetFeature</td><td>fetch the records, called features in WFS: here one per station</td></tr>
    <tr><td>typeNames=aws:aws_station</td><td>the dataset: the list of automatic weather stations (AWS)</td></tr>
    <tr><td>outputFormat=json</td><td>the format of the answer: JSON or CSV</td></tr>
  </tbody>
</table>

<p class="docs" style="margin-top: 6px">📖 All parameters (GeoServer): <a href="https://docs.geoserver.org/latest/en/user/services/wfs/reference/" target="_blank">https://docs.geoserver.org/latest/en/user/services/wfs/reference/</a></p>

</div>
<div>

<table class="status-codes">
  <thead><tr><th>Code</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td>200</td><td>OK</td></tr>
    <tr><td>400</td><td>Bad Request: something is wrong in your URL</td></tr>
    <tr><td>404</td><td>Not Found</td></tr>
    <tr><td>429</td><td>Too Many Requests: slow down</td></tr>
    <tr><td>500</td><td>Internal Server Error</td></tr>
    <tr><td>...</td><td>...</td></tr>
  </tbody>
</table>

</div>
</div>

<!--
A web API is an interface for programs, over the internet. Your code builds a URL, with parameters that say
what you want. The server parses it and looks up the data. It responds with a status code, 200 if all went
well, and the data in a fixed format: JSON or CSV.

This is a real URL. Everything after the question mark are parameters, separated by ampersands. This one asks
for the list of KMI weather stations, as JSON.
-->

---
layout: default
label: 9 · Fetching data from an API
---

# Fetching data with <span class="dm-accent">requests</span>

```py
import requests

params = {
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeNames": "aws:aws_station",
    "outputFormat": "json",
}
url = "https://opendata.meteo.be/service/ows"
response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
answer = response.json()
```

<div class="note">

- `params`: the parameters as a dictionary, `requests` builds the URL
- `timeout`: give up after 30 seconds instead of waiting forever
- `raise_for_status()`: stop with an error if the server answered with one
- `response.json()`: turn the JSON text into Python dictionaries and lists

</div>

<p class="docs">📖 <a href="https://requests.readthedocs.io/en/latest/user/quickstart/" target="_blank">https://requests.readthedocs.io/en/latest/user/quickstart/</a></p>

<!--
In Python, you fetch a URL with the requests library.

You put the parameters in a dictionary, and requests builds the URL with the question mark and the
ampersands for you. Then requests.get.

Two habits worth having. timeout: if the server does not answer, give up after 30 seconds instead of waiting
forever. And raise_for_status: if the server answers with an error, stop here with a clear error message,
instead of trying to read an error page as data three lines later.

response.json turns the JSON text into Python dictionaries and lists.
-->

---
layout: default
label: 9 · Fetching data from an API
---

# From <span class="dm-accent">JSON</span> to a DataFrame

<DmColumns>
<DmColumn header="Input: the features in the answer (shortened)" tone="navy">

```json
[
  {
    "id": "aws_station.6414",
    "properties": {
      "name": "BEITEM",
      "altitude": 24.8
    }
  },
  {
    "id": "aws_station.6418",
    "properties": {
      "name": "ZEEBRUGGE",
      "altitude": 12.1
    }
  }
]
```

</DmColumn>
<DmColumn header="Flattening with pd.json_normalize" tone="violet" divider>

```py
pd.json_normalize(answer["features"])
```

<div class="output small no-label">

```text
                 id properties.name  properties.altitude
0  aws_station.6414          BEITEM                 24.8
1  aws_station.6418       ZEEBRUGGE                 12.1
```

</div>

A key at the top level keeps its name. Nested keys become column names joined by a dot.

</DmColumn>
</DmColumns>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html" target="_blank">https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html</a></p>

<!--
JSON is nested: dictionaries inside dictionaries. Here, every station is a dictionary with an id, and a
dictionary of properties inside it, with the name and the altitude.

json_normalize flattens that into a table. A key at the top level, like id, becomes a column. A nested key
becomes a column whose name is the path, joined with dots: properties.name, properties.altitude. Then you
rename the columns to something shorter.
-->

---
layout: default
label: 9 · Fetching data from an API
---

# Filtering on the server

```py
params = {
    ...
    "typeNames": "aws:aws_1hour",
    "outputFormat": "json",
    # only Melle, only 2023
    "CQL_FILTER": "code = 6434 AND timestamp DURING 2023-01-01T00:00:00Z/2023-12-31T23:00:00Z",
    # only these columns
    "propertyName": "code,timestamp,sun_duration",
}
```

<DmColumns class="mt-1">
<DmColumn header="Size of a year of hourly data, as JSON" tone="navy">

<table class="size-table">
  <thead><tr><th></th><th>All columns</th><th>3 columns</th></tr></thead>
  <tbody>
    <tr><th>All stations</th><td>110.2 MB</td><td>19.8 MB</td></tr>
    <tr><th>Only Melle</th><td>9.6 MB</td><td class="size-best">1.7 MB</td></tr>
  </tbody>
</table>

</DmColumn>
<DmColumn header="Filtering rows and columns" tone="violet" divider>

`CQL_FILTER` chooses the rows, in a language much like the `WHERE` of SQL.

`propertyName` chooses the columns.

<p class="docs" style="margin-top: 8px">📖 <a href="https://docs.geoserver.org/latest/en/user/filter/ecql_reference/" target="_blank">https://docs.geoserver.org/latest/en/user/filter/ecql_reference/</a></p>

</DmColumn>
</DmColumns>

<p class="note">A public service is shared by everyone who uses it. Filter on the server, and save the result.</p>

<!--
Don't download everything and filter afterwards. Ask the server for only what you need.

This API lets you filter rows with CQL_FILTER, here on the station and the date, in a language that looks a
lot like the WHERE of SQL. And you choose the columns with propertyName. Here: the hourly sunshine of Melle,
for 2023. For all stations with all columns, that is 110 megabytes. Only Melle: almost 10.
Only Melle and only the columns we need: 1.7.

A public service is shared by everyone who uses it. Filter on the server, and save the result to a file, so
you do not fetch it again every time you run your notebook.
-->

---
layout: statement
title: Exercise - fetching data from an API
---

# Exercise time: fetching data from an API

<p class="mt-6 text-lg opacity-80"><code>exercises/09-fetching-from-an-api/</code></p>
<p class="mt-4 opacity-80">Fetch the KMI station list and the data of 2024 straight from the API.</p>
<p class="mt-1 opacity-60">About 20 minutes</p>

<!--
Fetch the KMI station list and a year of data that is not in our files, 2024, straight from the API. About
20 minutes.
-->

---
layout: section
---

# NumPy and SciPy

<!--
pandas is built on NumPy. In this part: why calculations on whole columns are fast, and fitting a curve with
SciPy, the scientific library.
-->

---
layout: default
label: 10 · NumPy and SciPy
---

# <span class="dm-accent">NumPy</span>: the engine underneath pandas

pandas uses NumPy for its calculations.<br>You can use some of its math functions on pandas columns:

```py
import numpy as np

np.log(df["rain"])
np.sqrt(df["area"])
np.cos(df["angle"])
```

And `np.nan` for a missing value.

<p class="docs">📖 <a href="https://numpy.org/doc/stable/user/absolute_beginners.html" target="_blank">https://numpy.org/doc/stable/user/absolute_beginners.html</a></p>

<!--
NumPy is the library for calculating on arrays of numbers. You have been using it all day without noticing:
the number and date columns of a DataFrame are stored as NumPy arrays, and when you calculate on a whole
column, NumPy does the work, in compiled code.

You rarely need to call NumPy yourself for data analysis. pandas has mean, sum and the rest built in. What
you do use are its math functions: logarithms, square roots, sines and cosines. They work directly on a
column. And np.nan, when you need to write a missing value yourself.
-->

---
layout: default
label: 10 · NumPy and SciPy
---

# User-defined functions <span class="dm-accent" style="font-size: 0.6em">(and why to avoid them if you can)</span>

<p>Converting 86 000 temperatures to Fahrenheit, two ways that give the same Series:</p>

<DmColumns class="mt-4">
<DmColumn header="Applying your own function" tone="navy">

```py
def to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

df["temperature"].apply(to_fahrenheit)
```

**19 ms**

</DmColumn>
<DmColumn header="Calculating on the whole column" tone="violet" divider>

```py
df["temperature"] * 9 / 5 + 32
```

**0.3 ms: more than 50 times faster**

</DmColumn>
</DmColumns>

<div class="calc-row">
  <p class="calc-in">Calculated in <span class="calc-slow">Python, one value at a time</span></p>
  <p class="calc-in">Calculated in <span class="calc-fast">the NumPy engine, vectorized</span></p>
</div>

<p class="note">A user-defined function works for anything, so it is the fallback: use it only when pandas has no built-in way.</p>

<p class="docs">📖 <a href="https://pandas.pydata.org/docs/user_guide/user_defined_functions.html" target="_blank">https://pandas.pydata.org/docs/user_guide/user_defined_functions.html</a></p>

<!--
A user-defined function is a function you write yourself, and let pandas run on your data. On the left: a
function that converts one temperature to Fahrenheit, and apply runs it for every value in the column.

It works, and you will see it a lot. But look at the time: 19 milliseconds. On the right, the same formula on
the whole column: 0.3 milliseconds, more than 50 times faster. apply runs a line of Python for every
value; the calculation on the whole column runs in NumPy, in a loop of compiled code, without Python in
between. That is what "vectorized" means.

Milliseconds sound harmless, but on ten million rows the difference is seconds against nothing. So: a
user-defined function is the fallback, for when pandas has no built-in way. If you know Spark, it is the same
lesson as user-defined functions there.
-->

---
layout: default
label: 10 · NumPy and SciPy
---

# SciPy: a pocket knife of maths tools

<div class="knife-wrap">
<svg viewBox="-130 -15 1260 330" class="knife" role="img" aria-label="A pocket knife with six tools folded out, labelled curve fitting, signal processing, statistics, interpolation, numerical integration and linear algebra">
<g transform="translate(350 260) rotate(-60)"><path d="M -11 0 L -11 -165 Q 12 -160 13 -128 L 13 0 Z" fill="#d4d8de" stroke="#7d8794" stroke-width="2" stroke-linejoin="round"/></g>
<g transform="translate(350 260) rotate(-30)"><path d="M -9 0 L -9 -150 L 9 -150 L 15 -144 L 9 -138 L 15 -132 L 9 -126 L 15 -120 L 9 -114 L 15 -108 L 9 -102 L 15 -96 L 9 -90 L 15 -84 L 9 -78 L 15 -72 L 9 -66 L 15 -60 L 9 -54 L 15 -48 L 9 -42 L 15 -36 L 9 -30 L 15 -24 L 9 -18 L 15 -12 L 9 -6 L 9 0 Z" fill="#d4d8de" stroke="#7d8794" stroke-width="2" stroke-linejoin="round"/></g>
<g transform="translate(350 260) rotate(0)"><path d="M -7 0 L 0 -140 L 7 0 Z" fill="#d4d8de" stroke="#7d8794" stroke-width="2" stroke-linejoin="round"/></g>
<g transform="translate(650 260) rotate(0)"><polyline points="0,0 0,-25 11,-34 -11,-43 11,-52 -11,-61 11,-70 -11,-79 11,-88 -11,-97 11,-106 -11,-115" fill="none" stroke="#7d8794" stroke-width="5" stroke-linejoin="round"/></g>
<g transform="translate(650 260) rotate(30)"><path d="M -6 0 L -6 -125 L -9 -140 L 9 -140 L 6 -125 L 6 0 Z" fill="#d4d8de" stroke="#7d8794" stroke-width="2" stroke-linejoin="round"/></g>
<g transform="translate(650 260) rotate(60)"><path d="M -3 0 L -13 -130 L 3 -55 Z" fill="#d4d8de" stroke="#7d8794" stroke-width="2" stroke-linejoin="round"/><path d="M 3 0 L 13 -130 L -3 -55 Z" fill="#d4d8de" stroke="#7d8794" stroke-width="2" stroke-linejoin="round"/></g>
<rect x="315" y="228" width="370" height="64" rx="32" fill="#d52b1e" stroke="#9e1b12" stroke-width="3"/>
<circle cx="350" cy="260" r="9" fill="#e9ecef" stroke="#7d8794" stroke-width="2"/>
<circle cx="650" cy="260" r="9" fill="#e9ecef" stroke="#7d8794" stroke-width="2"/>
<line x1="203" y1="175" x2="160" y2="192" stroke="#5b4be1" stroke-width="2"/>
<text x="150" y="190" text-anchor="end" class="knife-term">curve fitting</text>
<text x="150" y="211" text-anchor="end" class="knife-detail">finding a minimum</text>
<text x="150" y="232" text-anchor="end" class="knife-module">optimize</text>
<line x1="275" y1="130" x2="160" y2="94" stroke="#5b4be1" stroke-width="2"/>
<text x="150" y="92" text-anchor="end" class="knife-term">signal processing</text>
<text x="150" y="113" text-anchor="end" class="knife-detail">filtering, smoothing</text>
<text x="150" y="134" text-anchor="end" class="knife-module">signal</text>
<line x1="350" y1="120" x2="350" y2="64" stroke="#5b4be1" stroke-width="2"/>
<text x="350" y="10" text-anchor="middle" class="knife-term">statistics</text>
<text x="350" y="31" text-anchor="middle" class="knife-detail">distributions, statistical tests</text>
<text x="350" y="52" text-anchor="middle" class="knife-module">stats</text>
<line x1="650" y1="145" x2="650" y2="64" stroke="#5b4be1" stroke-width="2"/>
<text x="650" y="10" text-anchor="middle" class="knife-term">interpolation</text>
<text x="650" y="31" text-anchor="middle" class="knife-detail">filling gaps, resampling</text>
<text x="650" y="52" text-anchor="middle" class="knife-module">interpolate</text>
<line x1="720" y1="139" x2="840" y2="94" stroke="#5b4be1" stroke-width="2"/>
<text x="850" y="92" text-anchor="start" class="knife-term">numerical integration</text>
<text x="850" y="113" text-anchor="start" class="knife-detail">integrals, differential equations</text>
<text x="850" y="134" text-anchor="start" class="knife-module">integrate</text>
<line x1="763" y1="195" x2="840" y2="192" stroke="#5b4be1" stroke-width="2"/>
<text x="850" y="190" text-anchor="start" class="knife-term">linear algebra</text>
<text x="850" y="211" text-anchor="start" class="knife-detail">matrices, systems of equations</text>
<text x="850" y="232" text-anchor="start" class="knife-module">linalg</text>
</svg>
</div>

<p class="docs">📖 <a href="https://docs.scipy.org/doc/scipy/tutorial/" target="_blank">https://docs.scipy.org/doc/scipy/tutorial/</a></p>

<!--
SciPy is the scientific library, built on NumPy. Think of it as a pocket knife of maths tools: curve fitting,
signal processing, statistics, interpolation, numerical integration, linear algebra. Each tool has its own
part of SciPy, the name under it. You take out the one you need.

Today we use one of them: curve fitting, with optimize. The link is there for when you need the rest.
-->

---
layout: default
label: 10 · NumPy and SciPy
---

# Fitting a curve

<DmColumns>
<DmColumn class="hl-bg">

```py {11}
from scipy import optimize

def annual_cycle(day, mean, amplitude, peak):
    angle = 2 * np.pi * (day - peak) / 365
    return mean + amplitude * np.cos(angle)

daily = pd.read_csv(
    "kmi_daily_2023.csv", parse_dates=["timestamp"]
)
uccle = daily[daily["name"] == "UCCLE"]
params, _ = optimize.curve_fit(
    annual_cycle,
    uccle["timestamp"].dt.day_of_year,
    uccle["temp_avg"],
    p0=[10, 8, 200],
)
params
```

<div class="output small">

```text
array([ 12.14413699,   7.5689495 , 208.18547004])
```

</div>

<p class="docs">📖 <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html" target="_blank">https://docs.scipy.org/doc/scipy/reference/generated/<wbr>scipy.optimize.curve_fit.html</a></p>

</DmColumn>
<DmColumn divider>

<img src="/img/annual-cycle.png" alt="Daily mean temperature in Uccle in 2023 with a fitted cosine curve" style="width: 100%; max-height: 150px; object-fit: contain" />

$$
\text{temperature} = a + b \cos\left(2\pi \, \frac{\text{day} - d}{365}\right)
$$

Results:

- $a$, the mean: 12.1 °C
- $b$, the amplitude: 7.6 °C
- $d$, the peak: the 208th day (July 27)

`p0` is a first guess for the parameters, so that `curve_fit` starts in the right place.

</DmColumn>
</DmColumns>

<!--
Temperature follows a yearly cycle: cold in winter, warm in summer. You can describe that with a cosine,
with three parameters: the mean, the amplitude, how far it swings up and down, and the day of the peak.

You write that formula as a Python function. We take the days of Uccle: the day of the year as input, and
the mean temperature of that day as what the curve must follow. curve_fit then tries values for the three
parameters until the curve is as close to the measured points as possible. p0 is your first guess, to help it
start in the right place.

The result: a mean of 12.1 degrees, and the warmest day of the year on average is 27 July. This works for any
formula you can write as a function.
-->

---
layout: statement
title: Exercise - SciPy
---

# Exercise time: SciPy

<p class="mt-6 text-lg opacity-80"><code>exercises/10-scipy/</code></p>
<p class="mt-4 opacity-80">Fit the yearly cycle for the coast and the Ardennes.</p>
<p class="mt-1 opacity-60">About 15 minutes</p>

<!--
Fit the yearly cycle for the coast and the Ardennes. About 15
minutes.
-->

---
layout: section
---

# Best practices

<!--
To finish: a few best practices for keeping an analysis like this in Git, because data and notebooks need
some special care.
-->

---
layout: default
label: 11 · Best practices
---

# Best practices

<div class="grid grid-cols-2 gap-5 mt-4">
<DmInfoCard title="Don't put data in Git">

Git keeps every version of every file, forever. Put `data/` in `.gitignore`, and commit the code that fetches or generates the data.

</DmInfoCard>
<DmInfoCard title="Strip the outputs of notebooks">

Outputs change every time you run a cell, and fill your history with changes nobody can read. `uv run nbstripout --install` makes Git store notebooks without outputs.

</DmInfoCard>
<DmInfoCard title="Make your code idempotent">

Running a cell or a notebook twice must give the same result: never change your input, give every result a new name.

</DmInfoCard>
<DmInfoCard title="Test your data, ideally automatically">

Check what you assume: the number of rows, missing values, ranges, duplicates. Write the checks as code, so they run every time.

</DmInfoCard>
</div>

<!--
Four habits to take home.

Don't put data in Git. Git keeps every version of every file, forever: a large file you commit once stays in
the repository for good. Put the data folder in .gitignore, and commit the code that fetches or generates the
data instead.

Strip the outputs of notebooks. A notebook file also stores the outputs of its cells, and they change every
time you run a cell. nbstripout makes Git store your notebooks without outputs; your own copy keeps them.

Make your code idempotent: running a cell twice must give the same result. Never change your input, and give
every result a new name, as we saw this morning.

And test your data. Check what you assume: how many rows, missing values, ranges, duplicates. Write those
checks as code, so they run every time, not just once when you first looked.
-->

---
layout: default
label: Wrap-up
---

# Four DataFrame libraries

<DmComparison
  class="engine-cmp mt-4"
  :rows="['Born 🐣', 'What it is 📖', 'Runs on 🖥️']"
  :cols="['🐼 pandas', '✨ PySpark', '🧩 Dask', '🐻‍❄️ Polars']"
>
  <template #r0c0>2008</template>
  <template #r0c1>2009 (Spark)</template>
  <template #r0c2>2015</template>
  <template #r0c3>2020</template>

  <template #r1c0>The original Python DataFrame library, and still the most widely used.</template>
  <template #r1c1>The Python interface to Spark, which spreads the work over many machines.</template>
  <template #r1c2>Many pandas DataFrames, processed in parallel as one large table.</template>
  <template #r1c3>A newer DataFrame library, written in Rust and built for speed.</template>

  <template #r2c0>One machine, mostly on one core</template>
  <template #r2c1>A cluster of machines</template>
  <template #r2c2>One machine or a cluster</template>
  <template #r2c3>One machine, on all its cores</template>
</DmComparison>

<p class="engine-punch">All four give you a DataFrame. Today we used <b>pandas</b>.</p>

<!--
pandas is not the only DataFrame library. You will meet these names.

PySpark is for data that does not fit on one machine: it spreads the work over a cluster. Dask splits a big
table into many pandas DataFrames and processes them in parallel, so existing pandas code can grow. Polars is
newer, written in Rust, and uses all the cores of your machine; it is usually much faster than pandas.

They all give you a DataFrame. The ideas from today, selecting, filtering, grouping, joining, carry over
directly. Only the syntax differs. We used pandas because it is what you will find in most code, tutorials
and answers.
-->

---
layout: thanks
---

# Thank you

<!--
Thank you. The slides, the exercises and the solutions stay available in the repository. Questions?
-->
