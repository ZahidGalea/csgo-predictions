import concurrent.futures
import concurrent.futures
import json
from datetime import datetime

from bs4 import BeautifulSoup
from common import request, HLTV_BASE_URL


def extract_event_info(soup):
    # Extracting the event name
    event_name = soup.find("td", class_="col-value event-col").div.text

    # Extracting the number (assuming it's a rank)
    rank = soup.find("td", class_="col-value small-col").text

    # Extracting the prize pool
    prize_pool = soup.find("td", class_="col-value small-col prizePoolEllipsis").text

    # Extracting event type (e.g., Online)
    event_type = soup.find("td", class_="col-value small-col gtSmartphone-only").text

    # Extracting the location/country of the event and date range
    event_detail_row = soup.find("tr", class_="eventDetails")
    location = event_detail_row.find("span", class_="smallCountry").img["title"]
    date_range = event_detail_row.find_all("span", {"data-time-format": "MMM do"})

    start_date = date_range[0].text
    end_date = (
        date_range[1].text if len(date_range) > 1 else None
    )  # considering the possibility of just one date

    return {
        "Event Name": event_name,
        "Rank": rank,
        "Prize Pool": prize_pool,
        "Event Type": event_type,
        "Location": location,
        "Start Date": start_date,
        "End Date": end_date if end_date else "N/A",
    }


def get_event_data(events):
    data = []
    for event in events:
        if not event:
            continue
        data.append(extract_event_info(event))
    return data


def process_offset(offset):
    print("Working with offset", offset)
    url = f"{HLTV_BASE_URL}/events/archive?offset={offset}"
    response = request(url=url)
    soup = BeautifulSoup(response, "html.parser")
    events = soup.find_all("div", class_="table-holder")
    data = get_event_data(events=events)
    with open(f"data/events/events_{now}_{offset}.json", "w") as outfile:
        for event in data:
            outfile.write(json.dumps(event) + "\n")
    return get_event_data(events=events)


if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d")
    offsets = range(0, 3050, 50)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for offset in executor.map(process_offset, offsets):
            print(f"Finished processing offset {offset}")
