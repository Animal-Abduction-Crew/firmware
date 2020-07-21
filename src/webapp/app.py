from flask import Flask, render_template
import subprocess

locked = False

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rescue/<animal>')
def resuce(animal):

    global locked

    if not locked:
        if animal in ['elephant', 'tiger', 'star', 'cat', 'frog']:
            locked = True
            print(f"Ok, i'm going to resuce a(n) {animal}")

            subprocess.call(["/home/pi/repos/firmware/src/serious/main.py", animal])
            locked = False
            return 'OK'
        else:
            return f"WTF is a {animal}? I'm not going to do anything!"
    else:
        return "I'm already searching for a stupid animal!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
