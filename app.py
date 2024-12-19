from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# Dicionário para armazenar os usuários conectados
users = {}

# Rota que renderiza o template
@app.route('/chat/connect', methods=['GET'])
def index():
    return render_template('index.html', title="Chat em Tempo Real")

# Evento de conexão
@socketio.on('connect')
def handle_connect():
    print("Um usuário se conectou.")

# Evento de desconexão
@socketio.on('disconnect')
def handle_disconnect():
    username = users.get(request.sid, "Um usuário")
    print(f"{username} se desconectou.")
    emit('message', f"{username} saiu do chat.", broadcast=True)
    users.pop(request.sid, None)

# Evento para registrar um novo usuário
@socketio.on('register')
def handle_register(username):
    users[request.sid] = username
    print(f"{username} se conectou.")
    emit('message', f"{username} entrou no chat.", broadcast=True)

# Evento para mensagens enviadas
@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Anônimo")
    timestamp = datetime.now().strftime('%H:%M:%S')
    formatted_msg = f"[{timestamp}] {username}: {msg}"
    print(f"Mensagem recebida: {formatted_msg}")
    emit('message', formatted_msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
