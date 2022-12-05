from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "key_super_secreta_não_digam_a_ninguém"

@app.route("/")  # this sets the route to this page
def index():
	return render_template('index.html')


@app.route("/results")
def results():
      
      return render_template('results.html')

if __name__ == "__main__":
    app.run(debug=True)
