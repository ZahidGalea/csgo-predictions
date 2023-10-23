import concurrent.futures
import json
import re
from bs4 import BeautifulSoup, Tag
from datetime import datetime, timedelta
from common import request, HLTV_BASE_URL


def convert_datestring_to_datetime(soup_dayline: str):
    splitted = soup_dayline.split()[2:5]
    splitted[1] = (
        splitted[1]
        .replace("th", "")
        .replace("st", "")
        .replace("nd", "")
        .replace("rd", "")
    )
    cleaned_date_string = " ".join(splitted)
    date = (
        datetime.strptime(cleaned_date_string, "%B %d %Y").date().strftime("%Y-%m-%d")
    )
    return date


def extract_general_results(html_tags):
    team1_name = html_tags.select_one(".team1 .team").text
    html_tags_score = html_tags.select_one(".result-score").text.split("-")
    team1_html_tags = html_tags_score[0].strip()

    team2_name = html_tags.select_one(".team2 .team").text
    team2_html_tags = html_tags_score[1].strip()

    event_name = html_tags.select_one(".event .event-name").text

    event_type = html_tags.select_one(".map-text").text
    match_data = {
        "left_team": {
            "name": team1_name,
            "score": team1_html_tags,
        },
        "right_team": {
            "name": team2_name,
            "score": team2_html_tags,
        },
        "event": event_name,
        "event_type": event_type,
    }

    return match_data


def extract_country_results(html_tags):
    team1_country = html_tags.find("img", class_="team1")["title"]
    team2_country = html_tags.find("img", class_="team2")["title"]
    data = {
        "team_left_country": team1_country,
        "team_right_country": team2_country,
    }
    return data


def extract_veto_map(detail_soup):
    html_tags = detail_soup.select(".veto-box .padding")
    result = [str(x.string) for x in html_tags[1] if isinstance(x, Tag)]
    return result


def extract_scores(s):
    # Usa una expresión regular para encontrar todos los grupos de '(score1:score2)'
    matches = re.findall(r"(\d+):(\d+)", s)
    dict_result = {
        "half_{}".format(i + 1): {"left_team": tup[0], "right_team": tup[1]}
        for i, tup in enumerate(matches)
    }
    return dict_result


def extract_map_results(detail_soup):
    matches = []

    # Encontrar todos los 'mapholder' divs
    mapholders = detail_soup.find_all("div", class_="mapholder")

    for mapholder in mapholders:
        match_data_dict = {}

        # Obtener el nombre del mapa
        map_name = mapholder.find("div", class_="mapname").text
        match_data_dict["map_name"] = map_name

        # Obtener el logo, nombre y puntuación del equipo de la izquierda
        left_team_name = (
            mapholder.find("div", class_="results-left")
            .find("div", class_="results-teamname")
            .text
        )
        left_team_score = (
            mapholder.find("div", class_="results-left")
            .find("div", class_="results-team-score")
            .text
        )

        match_data_dict["left_team"] = {
            "name": left_team_name,
            "score": left_team_score,
        }

        # Obtener el logo, nombre y puntuación del equipo de la derecha
        right_team_name = (
            mapholder.find("span", class_="results-right")
            .find("div", class_="results-teamname")
            .text
        )
        right_team_score = (
            mapholder.find("span", class_="results-right")
            .find("div", class_="results-team-score")
            .text
        )
        match_data_dict["right_team"] = {
            "name": right_team_name,
            "score": right_team_score,
        }
        if right_team_score != "-" or left_team_score != "-":
            try:
                scores_half = extract_scores(
                    mapholder.find("div", class_="results-center-half-score").text
                )
                match_data_dict["score_per_half"] = scores_half
            except Exception as e:
                print("Scores per half failed")

        matches.append(match_data_dict)

    return matches


def extract_player_stats(detail_soup):
    teams_data = []

    # Iteramos sobre cada tabla (en este caso hay dos tablas, una por equipo)
    for table in detail_soup.find_all("table", class_="table totalstats"):
        team_name = table.find("a", class_="teamName team").text.strip()

        players = []
        for row in table.find_all("tr")[
            1:
        ]:  # El primer tr es el encabezado, por eso lo excluimos
            player_info = {}

            player_name = row.find("span", class_="player-nick").text
            kd = row.find("td", class_="kd text-center").text.strip().split("-")
            plus_minus_element = row.find(
                "td", class_="plus-minus text-center gtSmartphone-only"
            ).span
            plus_minus = plus_minus_element.text.strip() if plus_minus_element else None
            adr = row.find("td", class_="adr text-center").text.strip()
            kast = row.find("td", class_="kast text-center").text.strip()
            rating = row.find("td", class_="rating text-center").text.strip()

            player_info["nickname"] = player_name
            player_info["K"] = kd[0]
            player_info["D"] = kd[1]
            player_info["plus-minus"] = plus_minus
            player_info["ADR"] = adr
            player_info["KAST"] = kast
            player_info["Rating"] = rating

            players.append(player_info)

        team_data = {"team_name": team_name, "players": players}
        teams_data.append(team_data)
    return teams_data


def process_date(date):
    data = {}
    date = date.strftime("%Y-%m-%d")
    print(f"Querying date {date}")
    url = f"{HLTV_BASE_URL}/results?startDate={date}&endDate={date}&gameType=CSGO"
    response = request(url=url)
    soup = BeautifulSoup(response, "html.parser")

    day_results = soup.find_all(class_="results-sublist")
    for day in day_results:
        print(f"Querying day {day}")
        day_headline_obj = day.find("span", class_="standard-headline")
        if not day_headline_obj:
            continue
        match_date = convert_datestring_to_datetime(day_headline_obj.text.strip())
        results_soup: Tag = day.find_all(class_="result-con")
        results_parsed = []
        for result_soup in results_soup:
            if not result_soup:
                continue

            match_data = {"general_result": extract_general_results(result_soup)}
            if match_data["general_result"]["event_type"] == "def":
                # Forfeit
                sub_data = match_data
            else:
                endpoint = result_soup.select_one("a")["href"]
                detail_response = request(url=f"{HLTV_BASE_URL}{endpoint}")
                detail_soup = BeautifulSoup(detail_response, "html.parser")
                try:
                    veto_maps = extract_veto_map(detail_soup)
                except Exception as e:
                    print("EXCEPTION OCCURRED in veto maps")
                    print(e)
                    veto_maps = {}
                try:
                    player_stats = extract_player_stats(detail_soup)
                except Exception as e:
                    print("EXCEPTION OCCURRED in player stats")
                    print(e)
                    player_stats = {}
                try:
                    map_results = extract_map_results(detail_soup)
                except Exception as e:
                    print("EXCEPTION OCCURRED in map results")
                    print(e)
                    map_results = {}

                try:
                    countries = extract_country_results(detail_soup)
                except Exception as e:
                    print("EXCEPTION OCCURRED in country results")
                    print(e)
                    countries = {}

                sub_data = (
                    match_data
                    | {"veto_maps": veto_maps}
                    | {"player_stats": player_stats}
                    | {"map_results": map_results}
                    | {"countries": countries}
                )
            results_parsed.append(sub_data)

        if match_date in data:
            data[match_date]["results"] = data[match_date]["results"] + results_parsed
        else:
            data[match_date] = {"results": results_parsed}

    with open(f"data/matches/matches_{date}.json", "w") as file:
        for match_date, entry in data.items():
            entry_with_date = {"date": match_date, "results": entry["results"]}
            file.write(json.dumps(entry_with_date) + "\n")
    return date


def generate_date_range(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Calculate the number of days between start and end dates
    numdays = (start_date - end_date).days + 1

    date_list = [start_date - timedelta(days=x) for x in range(numdays)]

    return date_list


if __name__ == "__main__":
    start_date = "2023-10-06"
    end_date = "2023-10-06"
    dates = generate_date_range(start_date, end_date)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for date in executor.map(process_date, dates):
            print(f"Finished processing date {date}")
