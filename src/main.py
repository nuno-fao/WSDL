from flask import Flask, render_template, request

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

    results = {"Team": {}, "Player": {}, "League": {}}

    if "category_input" in args and args["category_input"] in results:
        results = {args["category_input"]: results[args["category_input"]]}
        active = args["category_input"]
    else:
        active = "Team"

    return render_template('results.html', query=query, results=results, active=active)

@app.route("/club/<id>")
def clup(id):

    return render_template('club.html', id=id)

@app.route("/league/<id>")
def clup_page(id):

    return render_template('league.html', id=id)

if __name__ == "__main__":
    app.run(debug=True)
