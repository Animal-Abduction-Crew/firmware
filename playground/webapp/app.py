from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<animal>')
def action(animal):
    if animal=='cat':
        print('Das ist eine Katze.')
        

    if animal=='tiger':
        print('Das ist eine Tiger.')

    if animal=='star':
        print('Das ist ein Stern.')

    if animal=='frog':
        print('Das ist eine Frosch.')

    if animal=='elephant':
        print('Das ist ein Elefant.')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')