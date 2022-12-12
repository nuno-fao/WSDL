import json
import csv
import math
from flask import Flask, render_template, request
from owlready2 import *
from urllib.parse import unquote_plus

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
        results = {"Team": [], "Player": []}
    else:
        if "category_input" in args and args["category_input"] in results:
            results = {args["category_input"]: results[args["category_input"]]}
            active = args["category_input"]
        else:
            for i in results.keys():
                active = i
                break

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
    name = unquote_plus(name)

    # get_ontology("../rdf/result").load()
    #
    #     q = """
    # select distinct ?club ?ar ?av where {
    #   ?club  a <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#Club> .
    #   ?club  ?r ?v
    #   ?club  ?ar ?av
    #   filter contains(?v,"%s")
    # }
    # """ % name

    # club = list(default_world.sparql(q))
    # club = toJson(club)

    club = [{"GK": [[25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"],
                    [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"]],
             "DEF": [[25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"]],
             "MID": [[25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"]],
             "ATTACK": [[25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"]]},
            {"Liga dos Campe\u00f5es": ["6", "4", "0", "2", "12-7"], "Liga Portuguesa": ["13", "9", "2", "2", "31-9"],
             "Superta\u00e7a": ["1", "1", "0", "0", "3-0"], "Ta\u00e7a de Portugal": ["2", "2", "0", "0", "9-0"],
             "Ta\u00e7a da Liga": ["2", "1", "1", "0", "4-2"], "": ["24", "17", "3", "4", "59-18"]},
            {"Nome": ["Futebol Clube do Porto"], "Alcunhas": ["Drag\u00f5es, Azuis e Brancos, Portistas"],
             "Associa\u00e7\u00e3o": ["AF Porto"], "Presidente": ["Jorge Nuno de Lima Pinto da Costa"],
             "Evolu\u00e7\u00e3o hist\u00f3rica": ["FC Porto"], "Morada": [
                "Est\u00e1dio do Drag\u00e3o, Entrada Nascente, Porta 15, Piso 3 Via Futebol Clube do Porto, 4350-415 Porto"],
             "Site Oficial": ["http://www.fcporto.pt"], "E-mail": ["fcporto@fcporto.pt"], "Rankings": ["16", "60"],
             "Hino Oficial": [""], "Ano de Funda\u00e7\u00e3o": ["1893-09-28"], "Cidade": ["Porto"],
             "Pa\u00eds": ["Portugal"], "Marca Equipamento": ["New Balance"],
             "Patroc\u00ednio": ["Betano | New Balance | Revigr\u00e9s | Super Bock | MEO"], "Equipamento": [""],
             "Outras Liga\u00e7\u00f5es": ["efgi"], "Num.FPF": ["529"]},
            {"Ta\u00e7a Intercontinental": "2", "Superta\u00e7a Europeia": "1", "Liga dos Campe\u00f5es": "2",
             "Europa League": "2", "Liga Portuguesa": "30", "Ta\u00e7a de Portugal": "18",
             "Superta\u00e7a C\u00e2ndido de Oliveira": "23", "Campeonato de Portugal (Extinto)": "4"},
            "https://www.zerozero.pt/img/logos/equipas/9_imgbank.png"]
    club_name = "FC Porto"
    return render_template('club.html', club_name=club_name, club_info=club)


@app.route("/league/<id>_<season>")
def league(id, season):
    table = [["1", "", "Benfica", "37", "13", "12", "1", "0", "37", "7", "+30"],
             ["2", "", "FC Porto", "29", "13", "9", "2", "2", "31", "9", "+22", ]]

    games = []

    with open('scraping\\results\\P1.csv', newline='') as f:
        reader = csv.DictReader(f)
        i = 0
        for row in reader:
            i += 1
            games.append([row['Date'], row['Time'], row['HomeTeam'], row['AwayTeam'], row['FTHG'], row['FTAG']])
            if i == 25:
                break

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
                        select ?clubFullName ?assists ?games ?goals ?minutes ?competition where {
                          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#iden> "%s" .
                          ?ent <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#playerPlayedForSquad> ?squad .
                          ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubHasSquad> ?squad .
                          ?club <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#clubFullName> ?clubFullName .
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

    out_player += [{
        "Liga Portuguesa": ["1"],
        "Ta\u00e7a de Portugal": "1",
        "Superta\u00e7a C\u00e2ndido de Oliveira": "2"
    }, ]

    out_player += [competition]

    out_player += [clubs_map]

    return render_template('player.html', player=out_player)


def ceiling(nr, div):
    return math.ceil(nr / div)


app.jinja_env.globals.update(ceiling=ceiling)

if __name__ == "__main__":
    app.run(debug=True)
