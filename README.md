 # GitHub Trending Scraper

A small Python project I made to scrape GitHub Trending and see which repositories are getting attention.

## What it does

- Scrapes trending repositories from GitHub
- Lets you filter by programming language
- Sorts repositories by their total stars
- Shows a summary of the results in the terminal
- Saves the results to CSV and TXT files

## How to run it

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the scraper:

```bash
python scraper.py
```

Enter a programming language when prompted, such as `python` or `java`. Leave it blank to get repositories from all languages.

The results are saved in the `data` folder as `trending.csv` and `trending.txt`.

## Built with

Python, Requests, BeautifulSoup and lxml.
