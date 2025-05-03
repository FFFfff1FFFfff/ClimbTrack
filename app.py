from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, session
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'climbtrack_secret'

# In-memory log storage (for demo, use DB in production)
session_logs = []

# Simple user store (for demo)
users = {'testuser': 'password123'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/session-log', methods=['GET', 'POST'])
def session_log():
    global session_logs
    if request.method == 'POST':
        file = request.files.get('image')
        note = request.form.get('note', '')
        grade = request.form.get('grade', '')
        date_input = request.form.get('date')
        if date_input:
            date = date_input + ' ' + datetime.now().strftime('%H:%M')
        else:
            date = datetime.now().strftime('%Y-%m-%d %H:%M')
        filename = None
        if file and allowed_file(file.filename):
            filename = datetime.now().strftime('%Y%m%d%H%M%S_') + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        session_logs.insert(0, {
            'date': date,
            'image': filename,
            'grade': grade,
            'note': note
        })
        flash('Session uploaded!')
        return redirect(url_for('session_log'))
    # 分组：同一天的记录放一起
    grouped_logs = defaultdict(list)
    for log in session_logs:
        log_day = log['date'].split(' ')[0]
        grouped_logs[log_day].append(log)
    return render_template('session_log.html', session_logs=session_logs, grouped_logs=grouped_logs)

@app.route('/crowd-detection')
def crowd_detection():
    return render_template('crowd_detection.html')

@app.route('/movement-notes')
def movement_notes():
    return render_template('movement_notes.html')

@app.route('/media-upload')
def media_upload():
    return render_template('media_upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['user'] = username
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

