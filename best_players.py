import json

from bs4 import BeautifulSoup
from datetime import datetime

from common import request

HLTV_BASE_URL = "https://www.hltv.org"


def get_players_data(soup, classification):
    table = soup.find("table", class_="stats-table player-ratings-table")
    # Get the rows in the table body
    rows = table.tbody.find_all("tr")

    # Initialize a list to store the extracted data
    players_data = []

    for row in rows:
        player = {}

        # Extracting player name
        player_name = row.find("td", {"class": "playerCol"}).a.text
        player["Name"] = player_name.strip()

        # Extracting player team
        player_team = row.find("td", {"class": "teamCol"}).a["href"].split("/")[-2]
        player["Team"] = player_team.strip()

        # Extracting the other stats for the player
        stats = row.findAll("td", {"class": "statsDetail"})
        player["Maps"] = stats[0].text.strip()
        player["Rounds"] = stats[1].text.strip()
        player["K/D"] = stats[2].text.strip()

        # Extracting K-D Diff
        kd_diff = row.find("td", {"class": "kdDiffCol"}).text.strip()
        player["K-D Diff"] = kd_diff

        # Extracting Rating
        rating = row.find("td", {"class": "ratingCol"}).text.strip()
        player["Rating"] = rating
        player["Classification"] = classification

        players_data.append(player)
    return players_data


def get_players(classification, date):
    url = f"https://www.hltv.org/stats/players?startDate=2021-01-01&endDate={date}&matchType={classification}"
    print(f"Querying date {date} - classification {classification}")
    response = request(url=url)
    soup = BeautifulSoup(response, "html.parser")
    return get_players_data(soup=soup, classification=classification)


if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d")
    classifications = ["Majors", "BigEvents", "Lan", "Online"]
    # Define a file to save the data
    with open(f"data/best_players/best_players_{now}.json", "w") as outfile:
        for classification in classifications:
            teams = get_players(classification=classification, date=now)

            # Write each team's data as a newline-delimited JSON entry
            for team in teams:
                outfile.write(json.dumps(team) + "\n")
