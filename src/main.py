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
    return render_template('results.html', query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True)
