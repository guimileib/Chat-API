from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# Rota que renderiza o template
@app.route('/chat/connect', methods=['GET'])
def index():
    return render_template('index.html', title="Chat em Tempo Real")

# Evento para mensagens enviadas
@socketio.on('message')
def handle_message(msg):
    print(f"Mensagem recebida: {msg}")
    emit('message', msg, broadcast=True)

@socketio.on('message')
def handle_message(msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    formatted_msg = f"[{timestamp}] {msg}"
    print(f"Mensagem recebida: {formatted_msg}")
    emit('message', formatted_msg, broadcast=True)
    
if __name__ == '__main__':
    socketio.run(app, debug=True)