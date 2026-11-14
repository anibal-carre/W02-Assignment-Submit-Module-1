# Overview

**Video Game Sales Analyzer** is a Python application that examines historical video game unit sales by genre, gaming platform, and region. I created it to practice loading real CSV data, checking data quality, using Pandas to calculate grouped statistics, and explaining results through charts and tables. This helps me develop practical data analysis skills for future software projects.

The source is a free historical video game sales dataset based on VGChartz data, available from [Kaggle (GregorUT)](https://www.kaggle.com/datasets/gregorut/videogamesales). A [public CC0 dataset mirror](https://huggingface.co/datasets/haoxianc/thedevastator_global-video-game-sales) provides a convenient download of `vgsales.csv` with 16,598 records. The file contains game names, platform, release year, genre, publisher, and sales in North America, Europe, Japan, other regions, and worldwide. Sales amounts are measured in **millions of copies**, not dollars. Because this is historical data, the results are **not current market rankings**.

The project bundle contains a clearly labeled **50-record sample taken from the top-ranked titles** so that the application can be tested offline. This subset is not representative of the complete dataset. Download the full CSV before creating your final video, and update the results described below to reflect the full-data run.

**Software demonstration:** Record a 4–5 minute video with your face visible, clear voice narration, a live program demo, and a code walkthrough. Include the working link in your Module Submit form. Adding the video link here is optional.

## How to Run

Install Python 3.10+ and VS Code. Open the project folder in the VS Code terminal and run:

```bash
python -m pip install -r requirements.txt
python download_dataset.py
python analyze_sales.py
```

If you use Windows and `python` does not work, try `py` instead. If the download is blocked, get the CSV from the dataset link above, name it `vgsales.csv`, and save it in the `data` folder. Then run `python analyze_sales.py`.

**Offline test using the 50-record sample:**

```bash
python analyze_sales.py --sample
```

**Run the automated tests:**

```bash
python -m unittest discover -s tests -v
```

The program prints the findings and saves these outputs in `output/`:

- `analysis_results.txt` — explanations and ranked results for both questions.
- `top_genres.csv` — global sales grouped by genre.
- `top_platforms.csv` — North America vs. Europe sales grouped by platform.
- `top_genres.png` — bar chart of the top five genres.
- `top_platforms.png` — stacked regional comparison chart.

# Data Analysis Results

**Research question 1: Which five video game genres have the highest total worldwide sales?**

Pandas groups the data by `Genre`, sums `Global_Sales`, and sorts the genre totals from largest to smallest. The five largest groups are displayed in a table and a bar chart.

**Results from the bundled 50-row sample only:** Platform (178.31 million), Sports (160.46 million), Shooter (151.55 million), Role-Playing (144.32 million), and Action (111.72 million). Within this *sample*, Platform ranks first. **These are not the answers for the full dataset.**

**Research question 2: Which five platforms have the highest combined sales in North America and Europe, and which region contributes more for each?**

Pandas groups the data by `Platform`, sums `NA_Sales` and `EU_Sales`, adds both totals, sorts the platforms, and identifies the larger region for each. The comparison is also shown in a stacked chart.

**Results from the bundled 50-row sample only:** Wii (224.45 million), DS (113.90 million), X360 (97.06 million), GB (85.27 million), and NES (73.20 million) combined units. North America has the higher total for all five in this *sample*. **The rankings may change when the full dataset is used.**

**Data preparation:** The program validates the CSV columns, converts the sales columns to numeric values, removes rows with missing genre/platform or invalid sales, and counts removed rows. It does not remove rows just because the release year is missing, since neither research question requires the release year.

**Limitations:** The dataset is a historical collection and may exclude games, contain inconsistent genres or estimates, or record the same game separately for multiple platforms. Results describe entries in the dataset, not all video game sales in the world. The reported results must always be tied to the dataset version used.

# Development Environment

- **Visual Studio Code:** edited and organized the project and used its integrated terminal.
- **Python 3:** programming language used for data preparation and analysis.
- **Pandas:** read the CSV, cleaned values, grouped records, and calculated totals.
- **Matplotlib:** generated two PNG charts to visualize the answers.
- **Git and GitHub:** version control and sharing the project after publication.
- **Python unittest:** checked that cleaning, grouping, ranking, and reporting work correctly.

The main implementation is in `analyze_sales.py`. Functions are documented with comments or docstrings. This is a terminal application, so no web server or database is required.

# Useful Websites

- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [Python argparse Documentation](https://docs.python.org/3/library/argparse.html)
- [Original Video Game Sales Dataset - Kaggle](https://www.kaggle.com/datasets/gregorut/videogamesales)
- [Free CSV Mirror - Hugging Face](https://huggingface.co/datasets/haoxianc/thedevastator_global-video-game-sales)

# Future Work

- Add a third research question comparing genre popularity across different decades.
- Add options for the user to select a specific year range and filter platforms.
- Build an interactive graphical dashboard with searchable charts and tables.
