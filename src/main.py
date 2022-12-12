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
    # q = """
    # select distinct ?club ?ar ?v where {
    #   ?club  a <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#Club> .
    #   ?club  ?r "%s" 
    #   ?club  ?ar ?v
    # }
    # """ % name

    # club = list(default_world.sparql(q))
    # club = toJson(club)
    
        q = """
    select distinct ?club ?ar ?av where {
      ?club  a <http://www.semanticweb.org/miguel/ontologies/2022/10/FootyPedia#Club> .
      ?club  ?r ?v
      ?club  ?ar ?av
      filter contains(?v,"%s") 
    }
    """ % name

    club= [{  "GK": [    [25, "Zaidu Sanusi"], [25, "Zaidu Sanusi"],[25, "Zaidu Sanusi"],[25, "Zaidu Sanusi"],[25, "Zaidu Sanusi"],   [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"]  ],  "DEF": [    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"]  ],  "MID": [    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"]  ],  "ATTACK": [    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"],    [25, "Zaidu Sanusi"]  ]},{  "Liga dos Campe\u00f5es": ["6", "4", "0", "2", "12-7"],  "Liga Portuguesa": ["13", "9", "2", "2", "31-9"],  "Superta\u00e7a": ["1", "1", "0", "0", "3-0"],  "Ta\u00e7a de Portugal": ["2", "2", "0", "0", "9-0"],  "Ta\u00e7a da Liga": ["2", "1", "1", "0", "4-2"],  "": ["24", "17", "3", "4", "59-18"]},{  "Nome": ["Futebol Clube do Porto"],  "Alcunhas": ["Drag\u00f5es, Azuis e Brancos, Portistas"],  "Associa\u00e7\u00e3o": ["AF Porto"],  "Presidente": ["Jorge Nuno de Lima Pinto da Costa"],  "Evolu\u00e7\u00e3o hist\u00f3rica": ["FC Porto"],  "Morada": [    "Est\u00e1dio do Drag\u00e3o, Entrada Nascente, Porta 15, Piso 3 Via Futebol Clube do Porto, 4350-415 Porto"],    "Site Oficial": ["http://www.fcporto.pt"],    "E-mail": ["fcporto@fcporto.pt"],    "Rankings": ["16", "60"],    "Hino Oficial": [""],    "Ano de Funda\u00e7\u00e3o": ["1893-09-28"],    "Cidade": ["Porto"],    "Pa\u00eds": ["Portugal"],    "Marca Equipamento": ["New Balance"],    "Patroc\u00ednio": [      "Betano | New Balance | Revigr\u00e9s | Super Bock | MEO"    ],    "Equipamento": [""],    "Outras Liga\u00e7\u00f5es": ["efgi"],    "Num.FPF": ["529"]  },  {    "Ta\u00e7a Intercontinental": "2",    "Superta\u00e7a Europeia": "1",    "Liga dos Campe\u00f5es": "2",    "Europa League": "2",    "Liga Portuguesa": "30",    "Ta\u00e7a de Portugal": "18",    "Superta\u00e7a C\u00e2ndido de Oliveira": "23",    "Campeonato de Portugal (Extinto)": "4"  },  "https://www.zerozero.pt/img/logos/equipas/9_imgbank.png"]
    club_name="FC Porto"
    return render_template('club.html', club_name=club_name ,club_info=club)
        
@app.route("/league/<id>_<season>")
def league(id, season):

    table= [ ["1", "", "Benfica", "37", "13", "12", "1", "0", "37", "7", "+30"],
    ["2", "", "FC Porto", "29", "13", "9", "2", "2", "31", "9","+22",]]

    games = []

    with open('scraping\\results\\P1.csv', newline='') as f:
        reader = csv.DictReader(f)
        i=0
        for row in reader:
            i+=1
            games.append([row['Date'],row['Time'],row['HomeTeam'],row['AwayTeam'],row['FTHG'],row['FTAG']])
            if i == 25:
                break

    return render_template('league.html', table=table, games=games)


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

def ceiling(nr,div):
    return math.ceil(nr/div)

app.jinja_env.globals.update(ceiling=ceiling)

if __name__ == "__main__":
    app.run(debug=True)
