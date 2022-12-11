import json

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

    results = {
        "Team": [
            {
                "image": "https://www.zerozero.pt/img/logos/equipas/16_imgbank.png",
                "name": "Sporting Clube de Portugal",
                "country": "Portugal",
                "city": "Lisboa",
                "year_of_foundation": "1906-07-01"
            },
            {
                "image": "https://www.zerozero.pt/img/logos/equipas/16_imgbank.png",
                "name": "Sporting Clube de Portugal",
                "country": "Portugal",
                "city": "Lisboa",
                "year_of_foundation": "1906-07-01"
            },
            {
                "image": "https://www.zerozero.pt/img/logos/equipas/16_imgbank.png",
                "name": "Sporting Clube de Portugal",
                "country": "Portugal",
                "city": "Lisboa",
                "year_of_foundation": "1906-07-01"
            },
            {
                "image": "https://www.zerozero.pt/img/logos/equipas/16_imgbank.png",
                "name": "Sporting Clube de Portugal",
                "country": "Portugal",
                "city": "Lisboa",
                "year_of_foundation": "1906-07-01"
            },
            {
                "image": "https://www.zerozero.pt/img/logos/equipas/16_imgbank.png",
                "name": "Sporting Clube de Portugal",
                "country": "Portugal",
                "city": "Lisboa",
                "year_of_foundation": "1906-07-01"
            },
        ],
        "Player": [
            {
                "image": "https://static-img.zz.pt/jogadores/31/28531_20210919193151_rui_patricio.png",
                "name": "Ruí Patricio",
                "position": "GK",
                "birthdate": "1988-02-15"
            }
        ],
        "League": []
    }

    if "category_input" in args and args["category_input"] in results:
        results = {args["category_input"]: results[args["category_input"]]}
        active = args["category_input"]
    else:
        active = "Team"

    return render_template('results.html', query=query, results=results, active=active)


def toJson(entitiesList):
    out = []
    for c in entitiesList:
        line = []
        for e in c:
            if type(e) == type(2):
                line.append(e)
            elif type(e) == type("s"):
                line.append(e)
            else:
                a = "http://localhost:5000/api/"
                line.append(a + e.name)
        out.append(line)
    # out = json.dumps(out)

    return out


@app.route("/api/<id>")
def api(id):
    q1 = """
    select distinct ?ent ?r ?v where {
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
    entry1 = toJson(entry1)
    entry2 = toJson(entry2)
    entry = entry1 + entry2

    out = {}
    for e in entry:
        if not (e[0] in out.keys()):
            out[e[0]] = {}
        if not (e[1] in out[e[0]].keys()):
            out[e[0]][e[1]] = []
        out[e[0]][e[1]].append(e[2])

    print(out)
    out = json.dumps(out)
    out = json.loads(out)
    return (out)


@app.route("/club/<name>")
def club(name):
    name = unquote_plus(name)

    q = """
    select distinct ?club ?ar ?av where {
      ?club  a <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#Club> .
      ?club  ?r ?v
      ?club  ?ar ?av
      filter contains(?v,"%s") 
    }
    """ % name

    club = list(default_world.sparql(q))
    club = toJson(club)
    return render_template('club.html', id=id, club=club)


@app.route("/league/<id>_<season>")
def league(id, season):
    return render_template('league.html', id=id, season=season)


@app.route("/player/<id>")
def player(id):
    return render_template('player.html', id=id)


if __name__ == "__main__":
    app.run(debug=True)
