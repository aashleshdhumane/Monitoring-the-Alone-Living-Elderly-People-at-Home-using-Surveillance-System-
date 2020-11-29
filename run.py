import flask
from main import Check

app = flask.Flask(__name__, template_folder='Template')
@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/' , methods=['POST'])
def getdata():
    v = flask.request.form['v']

    Check(v)
    return v
if __name__ == '__main__':
    app.run(debug=True)
