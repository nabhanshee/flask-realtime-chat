from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from config import app, db, socketio, login_manager
from models import User

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# All your routes here: /register, /login, /logout, /chat

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('chat'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', username=current_user.username)



# Socket.IO events
# Socket.IO events
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('send_message')
def handle_send_message(data):
    print(f"Received message from {data['username']}: {data['message']}")  # Debugging line
    socketio.emit('receive_message', {'username': data['username'], 'message': data['message']}, to='*')

@socketio.on('send_message')
def handle_send_message(data):
    username = data['username']
    message = data['message']
    print(f"Received message from {username}: {message}")
    socketio.emit('receive_message', {'username': username, 'message': message})


from flask_cors import CORS

CORS(app)  # Enable CORS for all routes


# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print(User.query.all())  # 👈 THIS LINE shows all users in the DB
    socketio.run(app, debug=True)

