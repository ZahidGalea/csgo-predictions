import json

from bs4 import BeautifulSoup
from datetime import datetime

from common import request

HLTV_BASE_URL = "https://www.hltv.org"


def get_teams_data(soup, classification):
    table = soup.find("table", class_="stats-table player-ratings-table")
    # Get the rows in the table body
    rows = table.tbody.find_all("tr")

    # Initialize a list to store the extracted data
    teams_data = []

    for row in rows:
        team_name = row.find("td", class_="teamCol-teams-overview").a.text
        maps = row.find("td", class_="statsDetail").text
        kd_diff = row.find("td", class_="kdDiffCol").text
        kd = row.findAll("td", class_="statsDetail")[1].text
        rating = row.find("td", class_="ratingCol").text

        team_info = {
            "Team Name": team_name,
            "Maps": maps,
            "K-D Diff": kd_diff,
            "KD": kd,
            "Rating": rating,
            "Class": classification,
        }
        teams_data.append(team_info)
    return teams_data


def get_teams(classification, date):
    url = f"https://www.hltv.org/stats/teams?startDate=2021-01-01&endDate={date}&matchType={classification}"
    print(f"Querying date {date} - classification {classification}")
    response = request(url=url)
    soup = BeautifulSoup(response, "html.parser")
    return get_teams_data(soup=soup, classification=classification)


if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d")
    classifications = ["Majors", "BigEvents", "Lan", "Online"]
    # Define a file to save the data
    with open(f"data/best_teams/teams_data_{now}.json", "w") as outfile:
        for classification in classifications:
            teams = get_teams(classification=classification, date=now)

            # Write each team's data as a newline-delimited JSON entry
            for team in teams:
                outfile.write(json.dumps(team) + "\n")
