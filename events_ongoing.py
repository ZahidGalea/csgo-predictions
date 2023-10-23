import json

from bs4 import BeautifulSoup
from datetime import datetime

from common import request

HLTV_BASE_URL = "https://www.hltv.org"


def extract_event_info(soup):
    # Extracting the event name
    event_name = soup.find("h1", class_="event-hub-title").text

    # Extracting the number (assuming it's a rank)
    rank = soup.find("td", class_="teamsNumber").text

    # Extracting the prize pool
    prize_pool = soup.find("td", class_="prizepool").text

    date_range = soup.find_all("span", {"data-time-format": "MMM do"})

    start_date = date_range[0].text
    end_date = (
        date_range[1].text if len(date_range) > 1 else None
    )  # considering the possibility of just one date

    return {
        "Event Name": event_name,
        "Rank": rank,
        "Prize Pool": prize_pool,
        "Event Type": "Reemplazar",
        "Location": "Reemplazar",
        "Start Date": start_date,
        "End Date": end_date if end_date else "N/A",
    }


def get_current_events(soup):
    events = soup.find_all(class_="a-reset ongoing-event")

    # Initialize a list to store the extracted data
    events_data = []

    for event in events:
        if not event:
            continue
        try:
            # Extraer el atributo href
            link = event["href"]
            print("Event Link: ", link)
            url = f"{HLTV_BASE_URL}/{link}"
            response = request(url=url)
            soup = BeautifulSoup(response, "html.parser")
            result = extract_event_info(soup=soup)
            data = events_data.append(result)
            # {"Event Name": "HealthPoint Cup", "Rank": "4+", "Prize Pool": "$1,200", "Event Type": "Local LAN", "Location": "Russia", "Start Date": "Mar 10th", "End Date": "N/A"}
        except Exception as e:
            print(e)
    with open(f"data/events_ongoing/events_ongoing.json", "w") as outfile:
        for event in events_data:
            outfile.write(json.dumps(event) + "\n")
    return events_data


def get_ongoing_events():
    url = f"{HLTV_BASE_URL}/events#tab-ALL"
    response = request(url=url)
    soup = BeautifulSoup(response, "html.parser")
    return get_current_events(soup=soup)


if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d")
    get_ongoing_events()
