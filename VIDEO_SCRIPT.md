# 4–5 Minute Video: Demo + Code Walkthrough

**Recording requirement:** Your face must be visible, your microphone must be working, and you must demonstrate **the program actually running** and explain the code. The previous Hello World feedback showed that a silent screen recording is not enough.

Before recording, run the program with the complete `vgsales.csv` and replace any sample-only facts below with the results you actually see. The narration is a suggested script; explain the project in your own words.

## 0:00–0:35 — Introduction (camera visible)

"Hello everyone. My name is Anibal. In this video, I will demonstrate my Python project called Video Game Sales Analyzer. My goal was to learn how to work with a real dataset and use programming to answer questions about video game sales. I used Python, Pandas, Matplotlib, and Visual Studio Code. I will show the CSV data, run the program, explain the code, and present the results."

## 0:35–1:15 — Show the data and explain both questions

**On screen:** Open `data/vgsales.csv` in VS Code; point to `Genre`, `Platform`, `Global_Sales`, `NA_Sales`, and `EU_Sales`.

"The CSV contains information about video games, their platforms, genres, and sales in different regions. The sales numbers represent millions of copies. I wanted to answer two questions. First, which five genres have the highest total global sales? Second, which five platforms have the highest combined sales in North America and Europe, and which region sells more for each platform? I used the complete dataset for this demonstration." 

## 1:15–2:20 — Code walkthrough (explain what each part does)

**On screen:** `analyze_sales.py`.

"Here is the main Python file. The `load_and_clean_data` function reads the CSV with Pandas. It checks that the necessary columns exist. Next, it converts sales values into numbers and removes rows that cannot be used. This helps prevent incorrect calculations. The `analyze_genres` function uses `groupby` to combine games in the same genre. It uses `sum` to calculate global sales and sorts the result to find the top five. The `analyze_platform_regions` function does a similar calculation for gaming platforms. It adds the North American and European sales and checks which region has a larger total. I divided these tasks into functions so the code is organized and easier to test."

## 2:20–3:10 — Demonstrate the program running LIVE

**On screen:** Open the VS Code terminal and run `python analyze_sales.py`. Make sure the terminal is readable.

"Now I will run the program. I open the terminal and type `python analyze_sales.py`. The application loads the full CSV file, analyzes the records, and prints both result tables. Here I can see which genre ranks first and the total sales for the top five. Below, I can see which five platforms have the highest combined North American and European sales. I can also see which region contributes more. The values I am showing come from the data and are not guesses."

## 3:10–4:05 — Show charts and output files

**On screen:** Open `output/top_genres.png` and `output/top_platforms.png`, then show one CSV result file.

"The program also generates charts. The first chart is a bar chart comparing the top five genres. The second chart uses stacked bars to compare North American and European sales by platform. The program saves these images automatically, so I can use them in a report. It also saves the numerical results as CSV files and creates a text report with short conclusions. Data visualization makes these comparisons easier to understand."

## 4:05–4:40 — Tests, limitations, conclusion

**On screen:** Run `python -m unittest discover -s tests -v` and show that all tests pass.

"I added automated tests to check that the program groups values correctly, ranks the results, and handles invalid data. One important limitation is that the dataset is historical, so I cannot use it to describe today's game sales. During this project I learned more about Pandas, data cleaning, grouping data, and making charts with Matplotlib. I also practiced organizing Python functions and testing my code. Thank you for watching."

## Final Video Checklist

- [ ] Face visible while explaining.
- [ ] Voice clearly audible for the entire walkthrough.
- [ ] Show a CSV dataset and explain both questions.
- [ ] Run `python analyze_sales.py` and show the output.
- [ ] Explain loading, cleaning, grouping, sorting, and chart functions.
- [ ] Show two charts and the CSV/text report.
- [ ] Show automated tests running.
- [ ] Publish 4–5 minute video and verify its link works.
- [ ] Paste the link in Module Submit form and the Data Analysis Teams channel.
