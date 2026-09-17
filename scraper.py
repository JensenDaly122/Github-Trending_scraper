import requests # lets python take hyml requests ie take the raw html code from the website
from bs4 import BeautifulSoup # raw html - naviagateable tree structure
import csv
from datetime import date


def scrape_trending(language=""):
    url = f"https://github.com/trending/{language}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers) # Sends the get request with those headers, storing the full response status code, HTML body in response.
    soup = BeautifulSoup(response.text, "lxml") # parses raw html using lxml making it a searchable soup object.

    repos = []
    for article in soup.select("article.Box-row"): # loops through every row
        name_tag = article.select_one("h2 a")
        name = name_tag.text.strip().replace("\n", "").replace(" ", "") #removes newlines and spaces between creator and the repo name

        desc_tag = article.select_one("p") #Gets description
        description = desc_tag.text.strip() if desc_tag else "" # (Error Detection) prevents crashing if description is missing

        star_tag = article.select_one('a[href$="/stargazers"]') #finds total star count
        stars = star_tag.text.strip().replace(",", "") if star_tag else "0" #text cleaning for sorting later

        today_tag = article.select_one("span.d-inline-block.float-sm-right")
        stars_today = today_tag.text.strip().split(" ")[0] if today_tag else "0"

        repos.append(
        {
            "name": name,
            "description": description,
            "language": language if language else "All",
            "stars": stars,
            "stars_today": stars_today
        })

        # for searching for the language

    return repos


def sort_by_stars(repos):
    return sorted(repos, key=lambda r: int(r["stars"]), reverse=True)

 
def save_to_csv(repos, filename="data/trending.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "description", "language", "stars", "stars_today"])
        writer.writeheader()
        writer.writerows(repos)
        #saves to trending.csv filename header repo rows and overwrites the file if it already exists


def save_to_txt(repos, filename="data/trending.txt"):
    name_width = 35
    lang_width = 15
    stars_width = 10
    today_width = 10

    with open(filename, "w", encoding="utf-8") as f:
        header = f"{'NAME':<{name_width}}{'LANGUAGE':<{lang_width}}{'STARS':<{stars_width}}{'TODAY':<{today_width}}\n"
        f.write(header)
        f.write("-" * (name_width + lang_width + stars_width + today_width) + "\n")

        for r in repos:
            name = r["name"][:name_width - 1]
            f.write(
                f"{name:<{name_width}}"
                f"{r['language']:<{lang_width}}"
                f"{r['stars']:<{stars_width}}"
                f"{r['stars_today']:<{today_width}}\n"
            )


def print_summary(repos, limit=5):
    print(f"Found {len(repos)} trending repos ({date.today()})")
    for r in repos[:limit]:
        print(f"{r['name']} - {r['stars']} stars ({r['stars_today']} today) - {r['language']}")


if __name__ == "__main__":
    language = input("Enter a language to filter by (or press Enter for all): ").strip().lower()

    repos = scrape_trending(language)
    repos = sort_by_stars(repos)

    print_summary(repos)

    save_to_csv(repos)
    save_to_txt(repos)
    print("Saved to data/trending.csv and data/trending.txt")