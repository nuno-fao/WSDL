from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "key_super_secreta_não_digam_a_ninguém"


@app.route("/")  # this sets the route to this page
def index():
    args = request.args.to_dict()
    data_filter = "Any"
    if "data-filter" in args:
        data_filter = args["data-filter"]
    return render_template('index.html', data_filter=data_filter)


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
