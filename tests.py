from datetime import date

import pytest
from bs4 import BeautifulSoup

from events import extract_event_info
from matches import (
    convert_datestring_to_datetime,
    extract_general_results,
    extract_map_results,
    extract_player_stats,
    extract_veto_map,
)


@pytest.mark.parametrize(
    "html_content, expected_output",
    [
        (
            """
    <table class="table">
        <tbody>
            <tr>
                <td class="col-value event-col">
                    <div class="text-ellipsis">LOOT.BET HotShot Series Season 1</div>
                </td>
                <td class="col-value small-col">16</td>
                <td class="col-value small-col prizePoolEllipsis" title="$15,000">$15,000</td>
                <td class="col-value small-col gtSmartphone-only">Online</td>
            </tr>
            <tr class="eventDetails">
                <td><span class="smallCountry"><img alt="Europe" src="/img/static/flags/30x20/EU.gif" class="flag" title="Europe"><span class="col-desc">Europe (Online) | </span></span><span class="col-desc"><span><span class="" data-time-format="MMM do" data-unix="1549191600000">Feb 3rd</span><span> - <span class="" data-time-format="MMM do" data-unix="1549710000000">Feb 9th</span></span></span></span></td>
                <td class="col-desc">Teams</td>
                <td class="col-desc">Prize</td>
                <td class="col-desc gtSmartphone-only"></td>
            </tr>
        </tbody>
    </table>
    """,
            {
                "Event Name": "LOOT.BET HotShot Series Season 1",
                "Rank": "16",
                "Prize Pool": "$15,000",
                "Event Type": "Online",
                "Location": "Europe",
                "Start Date": "Feb 3rd",
                "End Date": "Feb 9th",
            },
        )
    ],
)
def test_extract_event_info(html_content, expected_output):
    soup = BeautifulSoup(html_content, "html.parser")
    assert extract_event_info(soup) == expected_output


@pytest.fixture
def result_html():
    return """
<div class="result-con" data-zonedgrouping-entry-unix="1696197747000"><a href="/matches/2367032/nexus-vs-mouz-nxt-esea-advanced-season-46-europe" class="a-reset">
                        <div class="result">
                          <table>
                            <tbody><tr>
                              <td class="team-cell">
                                <div class="line-align team1">
                                  <div class="team ">Nexus</div>
<img alt="Nexus" src="https://img-cdn.hltv.org/teamlogo/TsvwZ9z4tVRO9Ry1jYxs_n.png?ixlib=java-2.1.0&amp;w=50&amp;s=ca777e2c0f8a3e0b26d0c90d98d72fbe" class="team-logo" title="Nexus"></div>
                              </td>
                              <td class="result-score"><span class="score-lost">0</span> - <span class="score-won">2</span></td>
                              <td class="team-cell">
                                <div class="line-align team2"><img alt="MOUZ NXT" src="https://img-cdn.hltv.org/teamlogo/RfR1zmFJ0eP08VmFb6UOu3.png?ixlib=java-2.1.0&amp;w=50&amp;s=051cbffad4d1c25468d83abee6f4fe23" class="team-logo" title="MOUZ NXT">
                                  <div class="team team-won">MOUZ NXT</div>
                                </div>
                              </td>
                              <td class="event"><img alt="ESEA Advanced Season 46 Europe" src="https://img-cdn.hltv.org/eventlogo/b75aNG0i4UVPNQHX_Tq-Zq.png?ixlib=java-2.1.0&amp;w=50&amp;s=abd9825a16bb8b751c86d126865a5d9f" class="event-logo" title="ESEA Advanced Season 46 Europe"><span class="event-name">ESEA Advanced Season 46 Europe</span></td>
                              <td class="star-cell">
                                <div class="map-text">bo3</div>
                              </td>
                            </tr>
                          </tbody></table>
                        </div>
                      </a></div>
    """


@pytest.fixture
def veto_map_htlm():
    return """
    <div class="standard-box veto-box">
                    <div class="padding preformatted-text">Best of 3 (Online)

* Lower bracket round 3</div>
                  </div>
    <div class="standard-box veto-box">
                    <div class="padding">
                      <div>1. MOUZ NXT removed Mirage</div>
                      <div>2. Nexus removed Vertigo</div>
                      <div>3. MOUZ NXT picked Ancient</div>
                      <div>4. Nexus picked Nuke</div>
                      <div>5. MOUZ NXT removed Anubis</div>
                      <div>6. Nexus removed Inferno</div>
                      <div>7. Overpass was left over</div>
                    </div>
                  </div>
    """


@pytest.fixture
def map_results():
    return """
    <div class="mapholder">
                      <div class="played">
                        <div class="map-name-holder"><img alt="Ancient" src="/img/static/maps/ancient.png" class="minimap" title="Ancient" height="32px" width="311px">
                          <div class="mapname">Ancient</div>
                        </div>
                      </div>
                      <div class="results played">
                        <div class="results-left lost ">
                          <div class="results-teamlogo-container"><img alt="Nexus" src="https://img-cdn.hltv.org/teamlogo/TsvwZ9z4tVRO9Ry1jYxs_n.png?ixlib=java-2.1.0&amp;w=50&amp;s=ca777e2c0f8a3e0b26d0c90d98d72fbe" class="logo team1Logo" title="Nexus" height="20px" width="20px"></div>
                          <div class="results-teamname-container text-ellipsis">
                            <div class="results-teamname text-ellipsis">Nexus</div>
                            <div class="results-team-score">20</div>
                          </div>
                        </div>
                        <div class="results-center">
                          <div class="results-center-stats"><a href="/stats/matches/mapstatsid/163749/nexus-vs-mouz-nxt" class="results-stats" data-link-tracking-page="Matchpage" data-link-tracking-column="[Main content]" data-link-tracking-destination="Click on Map stats [button]">STATS</a></div>
                          <div class="results-center-half-score"><span> (</span><span class="ct">6</span><span class="">:</span><span class="t">9</span><span>; </span><span class="t">9</span><span class="">:</span><span class="ct">6</span><span></span><span>)</span><span> (</span><span>5</span><span class="">:</span><span>7</span><span>)</span></div>
                        </div>
<span class="results-right won pick">
                          <div class="results-teamlogo-container"><img alt="MOUZ NXT" src="https://img-cdn.hltv.org/teamlogo/RfR1zmFJ0eP08VmFb6UOu3.png?ixlib=java-2.1.0&amp;w=50&amp;s=051cbffad4d1c25468d83abee6f4fe23" class="logo team1Logo" title="MOUZ NXT" height="20px" width="20px"></div>
                          <div class="results-teamname-container text-ellipsis">
                            <div class="results-teamname text-ellipsis">MOUZ NXT</div>
                            <div class="results-team-score">22</div>
                          </div>
                        </span></div>
                    </div>
    <div class="mapholder">
                      <div class="played">
                        <div class="map-name-holder"><img alt="Nuke" src="/img/static/maps/nuke.png" class="minimap" title="Nuke" height="32px" width="311px">
                          <div class="mapname">Nuke</div>
                        </div>
                      </div>
                      <div class="results played">
                        <div class="results-left lost pick">
                          <div class="results-teamlogo-container"><img alt="Nexus" src="https://img-cdn.hltv.org/teamlogo/TsvwZ9z4tVRO9Ry1jYxs_n.png?ixlib=java-2.1.0&amp;w=50&amp;s=ca777e2c0f8a3e0b26d0c90d98d72fbe" class="logo team1Logo" title="Nexus" height="20px" width="20px"></div>
                          <div class="results-teamname-container text-ellipsis">
                            <div class="results-teamname text-ellipsis">Nexus</div>
                            <div class="results-team-score">10</div>
                          </div>
                        </div>
                        <div class="results-center">
                          <div class="results-center-stats"><a href="/stats/matches/mapstatsid/163752/mouz-nxt-vs-nexus" class="results-stats" data-link-tracking-page="Matchpage" data-link-tracking-column="[Main content]" data-link-tracking-destination="Click on Map stats [button]">STATS</a></div>
                          <div class="results-center-half-score"><span> (</span><span class="t">6</span><span class="">:</span><span class="ct">9</span><span>; </span><span class="ct">4</span><span class="">:</span><span class="t">7</span><span></span><span>)</span></div>
                        </div>
<span class="results-right won ">
                          <div class="results-teamlogo-container"><img alt="MOUZ NXT" src="https://img-cdn.hltv.org/teamlogo/RfR1zmFJ0eP08VmFb6UOu3.png?ixlib=java-2.1.0&amp;w=50&amp;s=051cbffad4d1c25468d83abee6f4fe23" class="logo team1Logo" title="MOUZ NXT" height="20px" width="20px"></div>
                          <div class="results-teamname-container text-ellipsis">
                            <div class="results-teamname text-ellipsis">MOUZ NXT</div>
                            <div class="results-team-score">16</div>
                          </div>
                        </span></div>
                    </div>
    <div class="mapholder">
                      <div class="optional">
                        <div class="map-name-holder"><img alt="Overpass" src="/img/static/maps/overpass.png" class="minimap" title="Overpass" height="32px" width="311px">
                          <div class="mapname">Overpass</div>
                        </div>
                      </div>
                      <div class="results optional">
                        <div class="results-left tie ">
                          <div class="results-teamlogo-container"><img alt="Nexus" src="https://img-cdn.hltv.org/teamlogo/TsvwZ9z4tVRO9Ry1jYxs_n.png?ixlib=java-2.1.0&amp;w=50&amp;s=ca777e2c0f8a3e0b26d0c90d98d72fbe" class="logo team1Logo" title="Nexus" height="20px" width="20px"></div>
                          <div class="results-teamname-container text-ellipsis">
                            <div class="results-teamname text-ellipsis">Nexus</div>
                            <div class="results-team-score">-</div>
                          </div>
                        </div>
                        <div class="results-center"></div>
<span class="results-right tie ">
                          <div class="results-teamlogo-container"><img alt="MOUZ NXT" src="https://img-cdn.hltv.org/teamlogo/RfR1zmFJ0eP08VmFb6UOu3.png?ixlib=java-2.1.0&amp;w=50&amp;s=051cbffad4d1c25468d83abee6f4fe23" class="logo team1Logo" title="MOUZ NXT" height="20px" width="20px"></div>
                          <div class="results-teamname-container text-ellipsis">
                            <div class="results-teamname text-ellipsis">MOUZ NXT</div>
                            <div class="results-team-score">-</div>
                          </div>
                        </span></div>
                    </div>
    
    """


@pytest.fixture
def players_stats():
    return """
    <table class="table totalstats">
                      <tbody><tr class="header-row">
                        <td class="players">
                          <div class="align-logo"><img alt="Nexus" src="https://img-cdn.hltv.org/teamlogo/TsvwZ9z4tVRO9Ry1jYxs_n.png?ixlib=java-2.1.0&amp;w=50&amp;s=ca777e2c0f8a3e0b26d0c90d98d72fbe" class="logo" title="Nexus" height="25px" width="25px"><a href="/team/7187/nexus" class="teamName team">Nexus</a></div>
                        </td>
                        <td class="kd text-center">K-D</td>
                        <td class="plus-minus text-center gtSmartphone-only">plus-minus</td>
                        <td class="adr text-center">ADR</td>
                        <td class="kast text-center" title="Percentage of rounds in which the player either had a kill, assist, survived or was traded">KAST</td>
                        <td class="rating text-center">Rating<span class="ratingDesc">2.0</span></td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/17116/ragga" class="flagAlign no-maps-indicator-offset"><img alt="Romania" src="/img/static/flags/30x20/RO.gif" class="flag flag" title="Romania">
                              <div class="gtSmartphone-only statsPlayerName">Cosmin '<span class="player-nick">ragga</span>' Teodorescu</div>
                              <div class="smartphone-only statsPlayerName">ragga</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">53-46</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="won">+7</span></td>
                        <td class="adr text-center ">89.8</td>
                        <td class="kast text-center">73.5%</td>
                        <td class="rating text-center">1.25</td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/9626/xellow" class="flagAlign no-maps-indicator-offset"><img alt="Romania" src="/img/static/flags/30x20/RO.gif" class="flag flag" title="Romania">
                              <div class="gtSmartphone-only statsPlayerName">Adrian '<span class="player-nick">XELLOW</span>' Guță</div>
                              <div class="smartphone-only statsPlayerName">XELLOW</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">44-43</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="won">+1</span></td>
                        <td class="adr text-center ">62.6</td>
                        <td class="kast text-center">76.5%</td>
                        <td class="rating text-center">1.02</td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/19167/smekk" class="flagAlign no-maps-indicator-offset"><img alt="Romania" src="/img/static/flags/30x20/RO.gif" class="flag flag" title="Romania">
                              <div class="gtSmartphone-only statsPlayerName">Cristi '<span class="player-nick">smekk-</span>' Flutur</div>
                              <div class="smartphone-only statsPlayerName">smekk-</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">49-56</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="lost">-7</span></td>
                        <td class="adr text-center ">77.5</td>
                        <td class="kast text-center">67.6%</td>
                        <td class="rating text-center">0.96</td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/1206/btn" class="flagAlign no-maps-indicator-offset"><img alt="Romania" src="/img/static/flags/30x20/RO.gif" class="flag flag" title="Romania">
                              <div class="gtSmartphone-only statsPlayerName">Cătălin-Ionuț '<span class="player-nick">BTN</span>' Stănescu</div>
                              <div class="smartphone-only statsPlayerName">BTN</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">42-49</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="lost">-7</span></td>
                        <td class="adr text-center ">71.9</td>
                        <td class="kast text-center">69.1%</td>
                        <td class="rating text-center">0.88</td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/19817/s0und" class="flagAlign no-maps-indicator-offset"><img alt="Romania" src="/img/static/flags/30x20/RO.gif" class="flag flag" title="Romania">
                              <div class="gtSmartphone-only statsPlayerName">Alexandru '<span class="player-nick">s0und</span>' Ștefan</div>
                              <div class="smartphone-only statsPlayerName">s0und</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">34-49</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="lost">-15</span></td>
                        <td class="adr text-center ">57.1</td>
                        <td class="kast text-center">66.2%</td>
                        <td class="rating text-center">0.78</td>
                      </tr>
                    </tbody></table>
    <table class="table totalstats">
                      <tbody><tr class="header-row">
                        <td class="players">
                          <div class="align-logo"><img alt="MOUZ NXT" src="https://img-cdn.hltv.org/teamlogo/RfR1zmFJ0eP08VmFb6UOu3.png?ixlib=java-2.1.0&amp;w=50&amp;s=051cbffad4d1c25468d83abee6f4fe23" class="logo" title="MOUZ NXT" height="25px" width="25px"><a href="/team/11176/mouz-nxt" class="teamName team">MOUZ NXT</a></div>
                        </td>
                        <td class="kd text-center">K-D</td>
                        <td class="plus-minus text-center gtSmartphone-only">plus-minus</td>
                        <td class="adr text-center">ADR</td>
                        <td class="kast text-center" title="Percentage of rounds in which the player either had a kill, assist, survived or was traded">KAST</td>
                        <td class="rating text-center">Rating<span class="ratingDesc">2.0</span></td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/21972/neityu" class="flagAlign no-maps-indicator-offset"><img alt="France" src="/img/static/flags/30x20/FR.gif" class="flag flag" title="France">
                              <div class="gtSmartphone-only statsPlayerName">Ryan '<span class="player-nick">Neityu</span>' Aubry</div>
                              <div class="smartphone-only statsPlayerName">Neityu</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">57-40</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="won">+17</span></td>
                        <td class="adr text-center ">84.8</td>
                        <td class="kast text-center">75.0%</td>
                        <td class="rating text-center">1.28</td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/22695/sirah" class="flagAlign no-maps-indicator-offset"><img alt="Denmark" src="/img/static/flags/30x20/DK.gif" class="flag flag" title="Denmark">
                              <div class="gtSmartphone-only statsPlayerName">William '<span class="player-nick">sirah</span>' Kjærsgaard </div>
                              <div class="smartphone-only statsPlayerName">sirah</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">59-43</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="won">+16</span></td>
                        <td class="adr text-center ">89.0</td>
                        <td class="kast text-center">77.9%</td>
                        <td class="rating text-center">1.27</td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/20872/nexius" class="flagAlign no-maps-indicator-offset"><img alt="Belgium" src="/img/static/flags/30x20/BE.gif" class="flag flag" title="Belgium">
                              <div class="gtSmartphone-only statsPlayerName">Bram '<span class="player-nick">Nexius</span>' Campana</div>
                              <div class="smartphone-only statsPlayerName">Nexius</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">49-52</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="lost">-3</span></td>
                        <td class="adr text-center ">82.8</td>
                        <td class="kast text-center">61.8%</td>
                        <td class="rating text-center">1.10</td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/22279/pr" class="flagAlign no-maps-indicator-offset"><img alt="Czech Republic" src="/img/static/flags/30x20/CZ.gif" class="flag flag" title="Czech Republic">
                              <div class="gtSmartphone-only statsPlayerName">Oldřich '<span class="player-nick">PR</span>' Nový</div>
                              <div class="smartphone-only statsPlayerName">PR</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">45-46</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="lost">-1</span></td>
                        <td class="adr text-center ">75.1</td>
                        <td class="kast text-center">69.1%</td>
                        <td class="rating text-center">1.02</td>
                      </tr>
                      <tr class="">
                        <td class="players">
                          <div class="flagAlign"><a href="/player/21983/chr1zn" class="flagAlign no-maps-indicator-offset"><img alt="Denmark" src="/img/static/flags/30x20/DK.gif" class="flag flag" title="Denmark">
                              <div class="gtSmartphone-only statsPlayerName">Christoffer '<span class="player-nick">Chr1zN</span>' Storgaard</div>
                              <div class="smartphone-only statsPlayerName">Chr1zN</div>
                            </a></div>
                        </td>
                        <td class="kd text-center">31-43</td>
                        <td class="plus-minus text-center gtSmartphone-only"><span class="lost">-12</span></td>
                        <td class="adr text-center ">54.0</td>
                        <td class="kast text-center">70.6%</td>
                        <td class="rating text-center">0.85</td>
                      </tr>
                    </tbody></table>
    """


def test_extract_general_result(result_html):
    result = BeautifulSoup(result_html, "html.parser")
    data = extract_general_results(result)

    assert data["team1"]["name"] == "Nexus"
    assert data["team1"]["score"] == "0"
    assert data["team2"]["name"] == "MOUZ NXT"
    assert data["team2"]["score"] == "2"
    assert data["event"] == "ESEA Advanced Season 46 Europe"
    assert data["map_q"] == "bo3"


def test_veto_map(veto_map_htlm):
    result = BeautifulSoup(veto_map_htlm, "html.parser")
    data = extract_veto_map(result)
    assert data == [
        "1. MOUZ NXT removed Mirage",
        "2. Nexus removed Vertigo",
        "3. MOUZ NXT picked Ancient",
        "4. Nexus picked Nuke",
        "5. MOUZ NXT removed Anubis",
        "6. Nexus removed Inferno",
        "7. Overpass was left over",
    ]


def test_map_results(map_results):
    result = BeautifulSoup(map_results, "html.parser")
    data = extract_map_results(result)
    # Verificar que devuelve una lista
    assert isinstance(data, list)

    # Verificar que cada item de la lista es un diccionario
    for match in data:
        assert isinstance(match, dict)

        # Verificar las llaves principales en el diccionario
        assert "map_name" in match
        assert "left_team" in match
        assert "right_team" in match

        # Verificar estructura del equipo de la izquierda
        assert "name" in match["left_team"]
        assert "score" in match["left_team"]

        # Verificar estructura del equipo de la derecha
        assert "name" in match["right_team"]
        assert "score" in match["right_team"]


def test_players_stats(players_stats):
    result = BeautifulSoup(players_stats, "html.parser")
    data = extract_player_stats(result)
    assert data == [
        {
            "team_name": "Nexus",
            "players": [
                {
                    "nickname": "ragga",
                    "K": "53",
                    "D": "46",
                    "plus-minus": "+7",
                    "ADR": "89.8",
                    "KAST": "73.5%",
                    "Rating": "1.25",
                },
                {
                    "nickname": "XELLOW",
                    "K": "44",
                    "D": "43",
                    "plus-minus": "+1",
                    "ADR": "62.6",
                    "KAST": "76.5%",
                    "Rating": "1.02",
                },
                {
                    "nickname": "smekk-",
                    "K": "49",
                    "D": "56",
                    "plus-minus": "-7",
                    "ADR": "77.5",
                    "KAST": "67.6%",
                    "Rating": "0.96",
                },
                {
                    "nickname": "BTN",
                    "K": "42",
                    "D": "49",
                    "plus-minus": "-7",
                    "ADR": "71.9",
                    "KAST": "69.1%",
                    "Rating": "0.88",
                },
                {
                    "nickname": "s0und",
                    "K": "34",
                    "D": "49",
                    "plus-minus": "-15",
                    "ADR": "57.1",
                    "KAST": "66.2%",
                    "Rating": "0.78",
                },
            ],
        },
        {
            "team_name": "MOUZ NXT",
            "players": [
                {
                    "nickname": "Neityu",
                    "K": "57",
                    "D": "40",
                    "plus-minus": "+17",
                    "ADR": "84.8",
                    "KAST": "75.0%",
                    "Rating": "1.28",
                },
                {
                    "nickname": "sirah",
                    "K": "59",
                    "D": "43",
                    "plus-minus": "+16",
                    "ADR": "89.0",
                    "KAST": "77.9%",
                    "Rating": "1.27",
                },
                {
                    "nickname": "Nexius",
                    "K": "49",
                    "D": "52",
                    "plus-minus": "-3",
                    "ADR": "82.8",
                    "KAST": "61.8%",
                    "Rating": "1.10",
                },
                {
                    "nickname": "PR",
                    "K": "45",
                    "D": "46",
                    "plus-minus": "-1",
                    "ADR": "75.1",
                    "KAST": "69.1%",
                    "Rating": "1.02",
                },
                {
                    "nickname": "Chr1zN",
                    "K": "31",
                    "D": "43",
                    "plus-minus": "-12",
                    "ADR": "54.0",
                    "KAST": "70.6%",
                    "Rating": "0.85",
                },
            ],
        },
    ]


def test_convert_datestring_to_datetime():
    test_cases = [
        ("Results for January 1st 2020", date(2020, 1, 1)),
        ("Results for February 2nd 2019", date(2019, 2, 2)),
        ("Results for March 3rd 2018", date(2018, 3, 3)),
        ("Results for April 4th 2017", date(2017, 4, 4)),
        ("Results for May 5th 2016", date(2016, 5, 5)),
        ("Results for June 6th 2015", date(2015, 6, 6)),
        ("Results for July 7th 2014", date(2014, 7, 7)),
        ("Results for August 8th 2013", date(2013, 8, 8)),
        ("Results for September 9th 2012", date(2012, 9, 9)),
        ("Results for October 10th 2011", date(2011, 10, 10)),
        ("Results for November 11th 2010", date(2010, 11, 11)),
        ("Results for December 12th 2009", date(2009, 12, 12)),
        ("Results for December 21st 2009", date(2009, 12, 21)),
        ("Results for December 22nd 2009", date(2009, 12, 22)),
        ("Results for December 23rd 2009", date(2009, 12, 23)),
    ]

    for date_str, expected in test_cases:
        assert convert_datestring_to_datetime(date_str) == str(expected)

    # Casos que deberían causar errores:
    with pytest.raises(ValueError):
        convert_datestring_to_datetime(
            "Results for December 32nd 2009"
        )  # Día no válido
    with pytest.raises(ValueError):
        convert_datestring_to_datetime("Results for December 0th 2009")  # Día no válido
    with pytest.raises(ValueError):
        convert_datestring_to_datetime(
            "Results for Decembuary 12th 2009"
        )  # Mes no válido
    with pytest.raises(ValueError):
        convert_datestring_to_datetime("Results for December 12th 200")  # Año no válido
