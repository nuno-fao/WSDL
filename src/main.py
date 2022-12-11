import json

from flask import Flask, render_template, request
from owlready2 import *
from urllib.parse import unquote_plus

app = Flask(__name__)
app.secret_key = "key_super_secreta_não_digam_a_ninguém"


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
            try:
                line.append(e.iri)
            except:
                line.append(e)
        out.append(line)
    out = json.dumps(out)
    return out


@app.route("/club/<name>")
def clup(name):
    name = unquote_plus(name)

    get_ontology("../rdf/result").load()
    q = """
    select distinct ?club ?ar ?v where {
      ?club  a <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#Club> .
      ?club  ?r "%s" 
      ?club  ?ar ?v
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

    player_example = ["12",
                "Zaidu Sanusi",
                "25 anos",
                "1997-06-13",
                "",
                "Nig\u00e9ria",
                "",
                "Lagos",
                "Defesa (Defesa Esquerdo)",
                "Esquerdo",
                "182 cm",
                "76 kg",
                "https://static-img.zz.pt/jogadores/53/526053_20220817115014_zaidu_sanusi.png",
                {
                    "Liga dos Campe\u00f5es": [
                        "6",
                        "412",
                        "1",
                        "0"
                    ],
                    "Liga Portuguesa": [
                        "9",
                        "620",
                        "0",
                        "0"
                    ],
                    "Superta\u00e7a": [
                        "1",
                        "90",
                        "0",
                        "0"
                    ],
                    "Total": [
                        "16",
                        "1122",
                        "1",
                        "0"
                    ]
                },
                {
                    "Liga Portuguesa": "1",
                    "Ta\u00e7a de Portugal": "1",
                    "Superta\u00e7a C\u00e2ndido de Oliveira": "2"
                },
                {
                    "2022/23": [
                        "FC Porto",
                        "16",
                        "1",
                        "0"
                    ],
                    "2021/22": [
                        "FC Porto",
                        "40",
                        "3",
                        "0"
                    ],
                    "2020/21": [
                        "FC Porto",
                        "41",
                        "2",
                        "1"
                    ]
                }
            ]

    return render_template('player.html', player=player_example)



if __name__ == "__main__":
    app.run(debug=True)
