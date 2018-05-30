from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('home.html')

if __name__ == '__main__':
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
