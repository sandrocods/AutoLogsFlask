# Importing the Flask, render_template, SocketIO, emit, and datetime modules.
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

# Telling Flask to look for templates in the `template` folder.
app = Flask(__name__, template_folder='template')
# Creating a SocketIO instance.
socketio = SocketIO(app)


#
# The function hello() returns the rendered template index.html
# return: The index.html file is being returned.
#
@app.route("/")
def hello():
    return render_template('index.html')


#
# The function starts by emitting a message to the client to disable the button.
# Then it loops through 100 times, emitting a message to the client with the progress.
# Finally, it emits a message to the client to enable the button
# param message: The message sent by the client
#

@socketio.on('start')
def start(message):
    # disable button
    emit('button_action', {'data': 'disable'})

    # Logs data to the console
    for i in range(100):
        emit('my response',
             {'data': '[ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Progress ' + str(i) + '%'})
        socketio.sleep(0.10)

    emit('my response', {'data': '[ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Progress Done'})

    # enable button
    emit('button_action', {'data': 'enable'})


#
# The function is called when a client connects to the server
#
@socketio.on('connect')
def connect():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Client connected')
    emit('my response', {'data': '[ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Status : Connected'})


#
# The function is called when the client disconnects from the server
#
@socketio.on('disconnect')
def test_disconnect():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Client disconnected')


if __name__ == '__main__':
    print("App Running on http://localhost:5000")
    socketio.run(app, debug=False, log_output=False)
