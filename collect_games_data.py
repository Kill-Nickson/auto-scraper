import logging
from time import strftime
from urllib.request import urlopen
from urllib.error import URLError

from requests import get
from bs4 import BeautifulSoup


def matches_parse(yesterday):
    matches = []
    try:
        while True:
            base_url = 'https://***'
            link = str(base_url) + str(int(0 * 100))

            results_sublists = get_results_sublists(link)

            for sublist in results_sublists:

                date = get_date_from_sublist(sublist)

                if date == [int(yesterday.strftime("%d")),
                            int(yesterday.strftime("%m")),
                            int(yesterday.strftime("%Y"))]:
                    game_results = add_stars_amount_to_game_result(sublist)

                    matches = process_each_match(game_results, matches)
            break
    except Exception:
        logging.getLogger(__name__)
        logging.error(strftime('%Y-%m-%d %H:%M:%S') + ' - Occurred an error in a collect_games_data module')
        exit()
    finally:
        return matches


def get_results_sublists(link):
    request = get(link).content
    matches_page = BeautifulSoup(str(request), 'html.parser')

    results_holder = matches_page.findAll('***', {'class': '***'})
    results_all = None

    for i in results_holder:
        if 'Results for' in i.text:
            results_all = i.find('***', {'class': '***'})
    results_sublists = results_all.findAll('***', {'class': '***'})

    return results_sublists


def get_date_from_sublist(sublist):
    sublist_date = sublist.text.split('\\n')[0].split('for ')[1].split(' ')

    day = int(sublist_date[1][::-1][2:][::-1])

    month = 0
    if sublist_date[0] == 'January':
        month = 1
    elif sublist_date[0] == 'February':
        month = 2
    elif sublist_date[0] == 'March':
        month = 3
    elif sublist_date[0] == 'April':
        month = 4
    elif sublist_date[0] == 'May':
        month = 5
    elif sublist_date[0] == 'June':
        month = 6
    elif sublist_date[0] == 'July':
        month = 7
    elif sublist_date[0] == 'August':
        month = 8
    elif sublist_date[0] == 'September':
        month = 9
    elif sublist_date[0] == 'October':
        month = 10
    elif sublist_date[0] == 'November':
        month = 11
    elif sublist_date[0] == 'December':
        month = 12

    year = int(sublist_date[2])

    return [day, month, year]


def add_stars_amount_to_game_result(sublist):
    game_results = sublist.findAll('***', {'class': '***'})

    for j in range(len(game_results)):
        if len(game_results[j].findAll('***', {'class': '***'})) < 1:
            i_of_stars = 0
        else:
            i_of_stars = len(game_results[j].find('***', {'class': '***'}).
                             findAll('***'))

        game_results[j] = [game_results[j].find('a').get('href'),
                           i_of_stars]
    return game_results


def process_each_match(game_results, matches):
    for res in game_results:
        stars = res[1]

        if res[0] is None:
            break

        request = get('https://***' + res[0]).content
        matches_page = BeautifulSoup(str(request), 'html.parser')

        # Getting of teams' names
        teams = matches_page.findAll('***', {'class': '***'})

        team1 = teams[0].text
        team2 = teams[1].text

        map_names = []
        score = []
        team1_rates = []
        team2_rates = []
        team1players_stats = []
        team2players_stats = []
        existence_of_the_map = False

        maps = matches_page.findAll('***', {'class': '***'})

        for location in maps:
            if len(location.findAll('***', {'class': '***'})) > 0:
                continue
            if len(location.findAll('***', {'class': '***'})) > 0:
                map_name = location.find('***', {'class': '***'}).text
                if map_name == '***':
                    existence_of_the_map = True
                map_names.append(map_name)

                if len(location.findAll('***', {'class': '***'})) < 1 or \
                        len(location.findAll('***', {'class': '***'})) < 1:
                    continue

                score1 = location.find('***', {'class': '***'}). \
                    find('***', {'class': '***'}).text
                score2 = location.find('***', {'class': '***'}). \
                    find('***', {'class': '***'}).text

                score.append(score1)
                score.append(score2)

        if existence_of_the_map is True:
            continue

        if len(map_names) < 1:
            continue

        team1_link = matches_page.find('***', {'class': '***'})
        team1_link = team1_link.find('a').get('href')

        team2_link = matches_page.find('***', {'class': '***'})
        team2_link = team2_link.find('a').get('href')

        request = get('https://***' + team1_link + '***').content
        matches_page = BeautifulSoup(str(request), 'html.parser')

        all_maps_container = matches_page.findAll('***', {'class': '***'})

        for iterator in range(len(map_names)):
            for map_container in all_maps_container:
                processing_map = map_container.find(
                    '***', {'class': '***'}).text
                map_rate = map_container.find(
                    '***', {'class': '***'}).text

                if map_names[iterator] == processing_map:
                    team1_rates.append(map_rate)
        if len(team1_rates) != len(map_names):
            continue

        # Getting team1world_rank
        team1world_rank = matches_page.findAll('***', {'class': '***'})[0]
        team1world_rank = team1world_rank.findAll('***')
        if len(team1world_rank) < 1:
            continue
        team1world_rank = team1world_rank[0].text
        team1world_rank = int(team1world_rank[1:])

        # Getting team1in_top
        team1in_top = matches_page.findAll('***', {'class': '***'})[1]
        team1in_top = team1in_top.find('***').text
        team1in_top = int(team1in_top)

        # Getting team1average_age
        if len(matches_page.findAll('***', {'class': '***'})) < 3:
            continue

        team1average_age = matches_page.findAll('***', {'class': '***'})[2]
        team1average_age = team1average_age.find('***').text
        team1average_age = float(team1average_age)

        # Getting team1players_stats
        team1players_links = matches_page.find('***', {'class': '***'})
        team1players_links = team1players_links.findAll('***', {'class': '***'})

        links = []
        for link in team1players_links:
            links.append('https://***' + link.get('href'))

        for link in links:
            request = get(link).content
            matches_page = BeautifulSoup(str(request), 'html.parser')

            cols = matches_page.findAll('***', {'class': '***'})
            first_value = float(cols[1].find('***', {'class': '***'}).text)
            second_value = float(cols[4].find('***', {'class': '***'}).text)
            team1players_stats.append([first_value, second_value])

        request = get('https://***' + team2_link + '***').content
        matches_page = BeautifulSoup(str(request), 'html.parser')

        all_maps_container = matches_page.findAll('***', {'class': '***'})

        for iterator in range(len(map_names)):
            for map_container in all_maps_container:
                processing_map = map_container.find(
                    '***', {'class': '***'}).text
                map_rate = map_container.find(
                    '***', {'class': '***'}).text

                if map_names[iterator] == processing_map:
                    team2_rates.append(map_rate)
        if len(team2_rates) != len(map_names):
            continue

        # Getting team2world_rank
        team2world_rank = matches_page.findAll('***', {'class': '***'})[0]
        team2world_rank = team2world_rank.findAll('***')
        if len(team2world_rank) < 1:
            continue
        team2world_rank = team2world_rank[0].text
        team2world_rank = int(team2world_rank[1:])

        # Getting team2in_top
        team2in_top = matches_page.findAll('***', {'class': '***'})[1]
        team2in_top = team2in_top.find('***').text
        team2in_top = int(team2in_top)

        # Getting team2average_age
        if len(matches_page.findAll('***', {'class': '***'})) < 3:
            continue

        team2average_age = matches_page.findAll('***', {'class': '***'})[2]
        team2average_age = team2average_age.find('***').text
        team2average_age = float(team2average_age)

        # Getting team2players_stats
        team2players_links = matches_page.find('***', {'class': '***'})
        team2players_links = team2players_links.findAll('***', {'class': '***'})

        links = []
        for link in team2players_links:
            links.append('https://***' + link.get('href'))

        for link in links:
            request = get(link).content
            matches_page = BeautifulSoup(str(request), 'html.parser')

            cols = matches_page.findAll('***', {'class': '***'})
            first_value = float(cols[1].find('***', {'class': '***'}).text)
            second_value = float(cols[4].find('***', {'class': '***'}).text)
            team2players_stats.append([first_value, second_value])

        score_counter = 0

        for game in range(len(map_names)):
            map_info = [team1, team1world_rank, team1in_top, team1average_age,
                        team1players_stats[0][0], team1players_stats[0][1],
                        team2, team2world_rank, team2in_top, team2average_age,
                        team2players_stats[0][0], team2players_stats[0][1],
                        map_names[game],
                        score[score_counter],
                        team1_rates[game],
                        score[score_counter + 1],
                        team2_rates[game],
                        stars
                        ]
            matches.append(map_info)
            score_counter += 2
    return matches


def check_internet_connection():
    try:
        urlopen("http://google.com")
        return True
    except URLError:
        return False
