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
        name = request.form.get('name', '')
        climb_type = request.form.get('type', '')
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
            'note': note,
            'name': name,
            'type': climb_type
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

@app.route('/profile')
def profile():
    # Mock data for demonstration
    stats = {
        'bouldering_max': 'V8',
        'sport_max': '7b+',
        'sessions_this_month': 12,
        'bouldering_rank': '3rd',
        'sport_rank': '5th',
        'attendance_rank': '2nd',
        'total_sessions': 86,
        'total_tops': 150,
        'shoe_size': '38',
        'wall_pref': 'Overhang',
    }
    username = session.get('user', 'Demo User')
    return render_template('profile.html', stats=stats, username=username)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required.')
        elif username in users:
            flash('Username already exists.')
        else:
            users[username] = password
            flash('Account created! Please log in.')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        if not username or not new_password:
            flash('Username and new password are required.')
        elif username not in users:
            flash('Username does not exist.')
        else:
            users[username] = new_password
            flash('Password updated! Please log in.')
            return redirect(url_for('login'))
    return render_template('reset_password.html')

def v_grade_key(grade):
    if not grade or not grade.startswith('V'):
        return -1
    try:
        return int(grade[1:])
    except:
        return -1

def french_grade_key(grade):
    # 6a, 6a+, 6b, 6b+, ..., 9b+
    order = ['a', 'a+', 'b', 'b+', 'c', 'c+']
    if not grade:
        return -1
    try:
        num = int(grade[0])
        rest = grade[1:]
        idx = order.index(rest)
        return num * 10 + idx
    except:
        return -1

def get_bouldering_ranks(logs):
    best = {}
    for log in logs:
        name = log.get('name')
        grade = log.get('grade')
        date = log.get('date')
        if not name:
            continue
        if name not in best or (
            v_grade_key(grade) > v_grade_key(best[name]['grade']) or
            (v_grade_key(grade) == v_grade_key(best[name]['grade']) and date < best[name]['date'])
        ):
            best[name] = {'grade': grade, 'date': date}
    result = sorted(
        [{'name': k, 'grade': v['grade'], 'date': v['date']} for k, v in best.items()],
        key=lambda x: (-v_grade_key(x['grade']), x['date'])
    )
    return result

def get_sport_ranks(logs):
    best = {}
    for log in logs:
        name = log.get('name')
        grade = log.get('grade')
        date = log.get('date')
        if not name:
            continue
        if name not in best or (
            french_grade_key(grade) > french_grade_key(best[name]['grade']) or
            (french_grade_key(grade) == french_grade_key(best[name]['grade']) and date < best[name]['date'])
        ):
            best[name] = {'grade': grade, 'date': date}
    result = sorted(
        [{'name': k, 'grade': v['grade'], 'date': v['date']} for k, v in best.items()],
        key=lambda x: (-french_grade_key(x['grade']), x['date'])
    )
    return result

@app.route('/rank')
def rank():
    bouldering_logs = [log for log in session_logs if log.get('type') == 'bouldering']
    sport_logs = [log for log in session_logs if log.get('type') == 'sport']
    bouldering_ranks = get_bouldering_ranks(bouldering_logs)
    sport_ranks = get_sport_ranks(sport_logs)
    return render_template('rank.html', bouldering_ranks=bouldering_ranks, sport_ranks=sport_ranks)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

