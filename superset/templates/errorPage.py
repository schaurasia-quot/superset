from flask import Flask, render_template

app = Flask(__name__)

@app.route('/errorpage')
def index():
    print('I am here')
    return render_template('errorPage.html')


if __name__ == '__main__':
   app.run(debug = True)
