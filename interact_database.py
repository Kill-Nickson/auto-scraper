import logging
from time import strftime
import sqlite3


def table_init(directory, parsing_date):
    try:
        conn = sqlite3.connect(directory + '/databases/' + parsing_date + '.db')
        cursor = conn.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS matches (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                       team1 TEXT NOT NULL,
                                                                       team1world_rank REAL NOT NULL,
                                                                       team1in_top REAL NOT NULL,
                                                                       team1average_age REAL NOT NULL,
                                                                       team1players_stats_1 REAL NOT NULL,
                                                                       team1players_stats_2 REAL NOT NULL,
                                                                       team2 TEXT NOT NULL,
                                                                       team2world_rank REAL NOT NULL,
                                                                       team2in_top REAL NOT NULL,
                                                                       team2average_age REAL NOT NULL,
                                                                       team2players_stats_1 REAL NOT NULL,
                                                                       team2players_stats_2 REAL NOT NULL,
                                                                       map_name TEXT NOT NULL,
                                                                       team1_score REAL NOT NULL,
                                                                       team1_rates REAL NOT NULL,
                                                                       team2_score REAL NOT NULL,
                                                                       team2_rates REAL NOT NULL,
                                                                       stars REAL NOT NULL)""")
        conn.commit()
        conn.close()
    except Exception:
        logging.getLogger(__name__)
        logging.error(strftime('%Y-%m-%d %H:%M:%S') + '- Occurred an error in a table_init func of an '
                                                      'interact_database module')
        exit()


def table_update(directory, parsing_date, matches):
    try:
        conn = sqlite3.connect(directory + '\\databases\\' + parsing_date + '.db')
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO matches(team1,team1world_rank,team1in_top,team1average_age,"
                           "                    team1players_stats_1,team1players_stats_2,"
                           "                    team2,team2world_rank,team2in_top,team2average_age,"
                           "                    team2players_stats_1, team2players_stats_2,"
                           "                    map_name, "
                           "                    team1_score, team1_rates,"
                           "                    team2_score, team2_rates,"
                           "                    stars) "
                           "            VALUES (?,?,?,?,?,?"
                           "                    ?,?,?,?,?,?"
                           "                    ?,?,?,?,?,?,)", matches)
        conn.commit()
        conn.close()
    except Exception:
        logging.getLogger(__name__)
        logging.error(strftime('%Y-%m-%d %H:%M:%S') + '- Occurred an error in a table_update func of an '
                                                      'interact_database module')
        exit()
