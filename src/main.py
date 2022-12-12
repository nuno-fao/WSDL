import json
import csv
import math
from flask import Flask, render_template, request
from owlready2 import *

app = Flask(__name__)
app.secret_key = "key_super_secreta_não_digam_a_ninguém"

onto = get_ontology("../rdf/result").load()


@app.route("/")  # this sets the route to this page
def index():
    return render_template('index.html')


@app.route("/results")
def results():
    args = request.args.to_dict()
    query = ""
    if "query" in args:
        query = args["query"]
    results = {}

    club = """
        select distinct ?image ?name ?country ?city ?year_of_foundation ?id where {
          ?ent ?r ?v .
          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubImage> ?image .
          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubFullName> ?name .
          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubCountry> ?country .
          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubCity> ?city .
          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubFoundationYear> ?year_of_foundation .
          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> ?id .
          filter contains(?v,"%s")
        }
        """ % query

    entry_club = list(default_world.sparql(club))
    out_club = treat(entry_club)
    club_results = []
    for club in out_club:
        club_results.append({
            "image": club[0],
            "name": club[1],
            "country": club[2],
            "city": club[3],
            "year_of_foundation": club[4],
            "id": club[5],
        })
    if len(out_club) > 0:
        results["Team"] = club_results

    player = """
            select distinct ?image ?name ?position ?birthdate ?id ?clubName ?clubId where {
              ?ent ?r ?v .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerimage> ?image .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playername> ?name .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerposition> ?position .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerbirthdate> ?birthdate .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> ?id .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerPlayedForSquad> ?squad .
              ?squad <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#squadYear> "22_23" .  
              ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubHasSquad> ?squad .
              ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubFullName> ?clubName .
              ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> ?clubId .
              
              filter (contains(?v,"%s") || contains(?clubName,"%s"))
            }
            """ % (query, query)

    entry_player = list(default_world.sparql(player))
    out_player = treat(entry_player)
    player_results = []
    for player in out_player:
        player_results.append({
            "image": player[0],
            "name": player[1],
            "position": player[2],
            "birthdate": player[3],
            "id": player[4],
            "clubName": player[5],
            "clubId": player[6]
        })
    if len(out_player) > 0:
        results["Player"] = player_results

    if len(results) == 0:
        results = {"Team": [], "Player": [], "League": ["Liga Portugal"]}
        active = "Team"
    else:
        if "category_input" in args and args["category_input"] in results:
            results = {args["category_input"]: results[args["category_input"]]}
            active = args["category_input"]
        else:
            for i in results.keys():
                active = i
                break
    results["League"] = ["Liga Portugal"]

    return render_template('results.html', query=query, results=results, active=active)


def toJson(entitiesList):
    temp = treat(entitiesList)
    # out = json.dumps(out)

    out = {}
    for e in temp:
        if not (e[0] in out.keys()):
            out[e[0]] = {}
        if not (e[1] in out[e[0]].keys()):
            out[e[0]][e[1]] = []
        out[e[0]][e[1]].append(e[2])

    return out


def treat(entitiesList):
    temp = []
    for c in entitiesList:
        line = []
        for e in c:
            if type(e) == type(2):
                line.append(e)
            elif isinstance(e, str):
                line.append(e)
            else:
                try:
                    a = "http://localhost:5000/api/id/"
                    line.append(a + e.name)
                except:
                    line.append("")
        temp.append(line)
    # out = json.dumps(out)

    return temp


@app.route("/api")
def api():
    q = request.args.get("q")
    print(q)
    entry = list(default_world.sparql("""%s""" % q))
    out = treat(entry)

    out = json.dumps(out)
    out = json.loads(out)
    return (out)


@app.route("/api/id/<id>")
def apiID(id):
    q1 = """
    select ?ent ?r ?v where {
      ?ent  <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> "%s" .
      ?ent ?r ?v  
    }
    """ % id

    q2 = """
    select distinct ?ent ?r ?v where {
      ?ent  <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> "%s" .
      ?v ?r ?ent  
    }
    """ % id

    entry1 = list(default_world.sparql(q1))
    entry2 = list(default_world.sparql(q2))
    entry = entry1 + entry2
    out = toJson(entry)

    out = json.dumps(out)
    out = json.loads(out)
    return (out)


@app.route("/club/<name>")
def club(name):
    club_q = """
            select distinct ?image ?name ?nickname ?assoc ?president ?address ?site ?email ?year ?city ?country where {
              ?ent ?r ?v .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubImage> ?image .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubFullName> ?name .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubNickname> ?nickname .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubAssociation> ?assoc .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubPresident> ?president .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubAddress> ?address .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubWebsite> ?site .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubEmail> ?email .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubFoundationYear> ?year .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubCity> ?city .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubCountry> ?country .
              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> "%s" .
            }
            """ % name

    club_tmp = list(default_world.sparql(club_q))[0]

    club_q = {
        "Nome": club_tmp[1],
        "Alcunhas": club_tmp[2],
        "Associa\u00e7\u00e3o": club_tmp[3],
        "Presidente": club_tmp[4],
        "Morada": club_tmp[5],
        "Site Oficial": club_tmp[6],
        "E-mail": club_tmp[7],
        "Ano de Funda\u00e7\u00e3o": club_tmp[8],
        "Cidade": club_tmp[9],
        "Pa\u00eds": club_tmp[10],
    }

    squad_q = """
                select distinct ?playerName ?playerImage ?playerPosition ?iden where {
                  ?ent ?r ?v .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerimage> ?playerImage .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playername> ?playerName .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerposition> ?playerPosition .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerbirthdate> ?birthdate .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerPlayedForSquad> ?squad .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> ?iden .
                  ?squad <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#squadYear> "22_23" .  
                  ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubHasSquad> ?squad .
                  ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> "%s" .
                }
                """ % name

    squad_tmp = list(default_world.sparql(squad_q))
    squad_q = {"GK": [], "DEF": [], "MID": [], "ATTACK": []}
    for p in squad_tmp:
        if "Guarda Redes" in p[2]:
            squad_q["GK"].append([p[1], p[0], p[3]])
        elif "Defesa" in p[2]:
            squad_q["DEF"].append([p[1], p[0], p[3]])
        elif "Médio" in p[2]:
            squad_q["MID"].append([p[1], p[0], p[3]])
        else:
            squad_q["ATTACK"].append([p[1], p[0], p[3]])

    competition_q = """
                    select ?name where {
                      ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubWonCompetition> ?competition .
                      ?competition <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#competitionName> ?name .
                      ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> "%s" .
                    }
                    """ % name

    competition_tmp = list(default_world.sparql(competition_q))

    current_season = """
                            select ?competition ?games ?minutes ?goals ?assists   where {
                              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> "%s" .
                              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerPlayedForSquad> ?squad .
                              ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubHasSquad> ?squad .
                              ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordForSquad> ?squad .
                              ?squad <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#squadYear> "22_23" .
                              ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerHasRecord> ?record .
                              ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordassists> ?assists .
                              ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordgames> ?games .
                              ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordgoals> ?goals .
                              ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordminutes> ?minutes .
                              ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordcompetitionname> ?competition .

                            }
                            """ % id
    current_season = list(default_world.sparql(current_season))

    print(current_season)

    current_season_map = {}
    for entry in current_season:
        current_season_map[entry[0]] = [entry[1], entry[2], entry[3], entry[4]]

    club = [squad_q,
            current_season_map,
            club_q,
            competition_tmp,
            club_tmp[0]]
    club_name = club_tmp[1]
    return render_template('club.html', club_name=club_name, club_info=club)


@app.route("/league/<id>_<season>")
def league(id, season):
    table = [["1", "", "Benfica", "37", "13", "12", "1", "0", "37", "7", "+30"],
             ["2", "", "FC Porto", "29", "13", "9", "2", "2", "31", "9", "+22", ],
             ["3", "", "SC Braga", "28", "13", "9", "1", "3", "29", "12", "+17", ],
             ["4", "", "Sporting", "25", "13", "8", "1", "4", "26", "15", "+11", ],
             ["5", "", "Casa Pia AC", "23", "13", "7", "2", "4", "13", "10", "+3", ],
             ["6", "", "Vitória SC", "23", "13", "7", "2", "4", "14", "13", "+1", ],
             ["7", "", "Portimonense", "19", "13", "6", "1", "6", "12", "14", "-2", ],
             ["8", "", "FC Arouca", "19", "13", "5", "4", "4", "14", "19", "-5", ],
             ["9", "", "GD Chaves", "19", "13", "5", "4", "4", "13", "16", "-3", ],
             ["10", "", "Rio Ave", "18", "13", "5", "3", "5", "16", "18", "-2", ],
             ["11", "", "Boavista", "17", "13", "5", "2", "6", "14", "23", "-9", ],
             ["12", "", "Estoril Praia", "16", "13", "4", "4", "5", "14", "18", "-4", ],
             ["13", "", "FC Vizela", "15", "13", "4", "3", "6", "11", "13", "-2", ],
             ["14", "", "Santa Clara", "13", "13", "3", "4", "6", "11", "13", "-2", ],
             ["15", "", "FC Famalicão", "11", "13", "3", "2", "8", "11", "18", "-7", ],
             ["16", "", "Gil Vicente", "9", "13", "2", "3", "8", "11", "21", "-10", ],
             ["17", "", "Marítimo", "6", "13", "1", "3", "9", "8", "27", "-19", ],
             ["18", "", "Paços de Ferreira", "2", "13", "0", "2", "11", "7", "26", "+-19", ]
             ]

    games = []

    with open('../scraping/results/P1.csv', newline='') as f:
        reader = csv.DictReader(f)
        i = 0
        for row in reader:
            i += 1
            games.append([row['Date'], row['Time'], row['HomeTeam'], row['AwayTeam'], row['FTHG'], row['FTAG']])

    return render_template('league.html', table=table, games=games)


@app.route("/player/<id>")
def player(id):
    player = """
                select distinct ?name ?name ?age ?birthdate ?name ?naturalFrom ?name ?birthplace ?position ?foot ?height ?weight ?image where {
                  ?ent ?r ?v .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playername> ?name .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playername> ?name .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerbirthdate> ?birthdate .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerage> ?age .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playernationality> ?naturalFrom .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerbirthplace> ?birthplace .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerposition> ?position .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerfoot> ?foot .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerheight> ?height .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerweight> ?weight .
                  ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerimage> ?image .

                  filter contains(?v,"%s")
                }
                """ % id

    entry_player = list(default_world.sparql(player))
    out_player = treat(entry_player)[0]

    competition = """
                    select distinct  ?competitionName where {
                      ?ent ?r ?v .
                      ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerWonCompetition> ?competition .
                      ?competition <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#competitionName> ?competitionName .

                      filter contains(?v,"%s")
                    }
                    """ % id

    competition = list(default_world.sparql(competition))

    clubs = """
                    select ?clubFullName ?year ?assists ?games ?goals ?minutes where {
                      ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> "%s" .
                      ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerPlayedForSquad> ?squad .
                      ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubHasSquad> ?squad .
                      ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubFullName> ?clubFullName .
                      ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordForSquad> ?squad .
                      ?squad <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#squadYear> ?year .
                      ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerHasRecord> ?record .
                      ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordassists> ?assists .
                      ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordgames> ?games .
                      ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordgoals> ?goals .
                      ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordminutes> ?minutes .
                      ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordcompetitionname> "Total" .
                    }
                    """ % id

    clubs = list(default_world.sparql(clubs))

    clubs_map = {}
    for entry in clubs:
        clubs_map[entry[1].replace("_", "/")] = [entry[0], entry[3], entry[4], entry[2], entry[5]]

    current_season = """
                        select ?competition ?games ?minutes ?goals ?assists   where {
                          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> "%s" .
                          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerPlayedForSquad> ?squad .
                          ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubHasSquad> ?squad .
                          ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordForSquad> ?squad .
                          ?squad <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#squadYear> "22_23" .
                          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerHasRecord> ?record .
                          ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordassists> ?assists .
                          ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordgames> ?games .
                          ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordgoals> ?goals .
                          ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordminutes> ?minutes .
                          ?record <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#recordcompetitionname> ?competition .
                          
                        }
                        """ % id
    current_season = list(default_world.sparql(current_season))

    print(current_season)

    current_season_map = {}
    for entry in current_season:
        current_season_map[entry[0]] = [entry[1], entry[2], entry[3], entry[4]]

    out_player += [current_season_map]

    out_player += [competition]

    out_player += [clubs_map]

    return render_template('player.html', player=out_player)


def ceiling(nr, div):
    return math.ceil(nr / div)


app.jinja_env.globals.update(ceiling=ceiling)

if __name__ == "__main__":
    app.run(debug=True)
