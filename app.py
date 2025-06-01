from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, session
import os
from werkzeug.utils import secure_filename
from datetime import datetime

# 导入数据库服务
from database.services import AuthService, UserService, ClimbingService, StatisticsService, GymService, NoteService

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['DATABASE'] = 'database/climbtrack.db'
app.secret_key = 'climbtrack_secret'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/session-log', methods=['GET', 'POST'])
def session_log():
    if not session.get('user'):
        flash('Please login first.')
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    if not user_id:
        flash('User not found.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        file = request.files.get('image')
        note = request.form.get('note', '')
        grade = request.form.get('grade', '')
        date_input = request.form.get('date')
        name = request.form.get('name', '')
        climb_type = request.form.get('type', '')
        
        if not all([grade, name, climb_type]):
            flash('Grade, name, and type are required.')
            return redirect(url_for('session_log'))
        
        # 处理图片上传
        filename = None
        if file and allowed_file(file.filename):
            filename = datetime.now().strftime('%Y%m%d%H%M%S_') + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # 确定日期
        session_date = date_input if date_input else datetime.now().strftime('%Y-%m-%d')
        
        # 准备攀登数据
        climb_data = {
            'name': name,
            'type': climb_type,
            'grade': grade,
            'notes': note,
            'image_filename': filename or ''
        }
        
        # 创建攀登记录
        climb_log_id = ClimbingService.create_climb_log(user_id, session_date, climb_data)
        
        if climb_log_id:
            flash('Session uploaded!')
        else:
            flash('Failed to upload session.')
        
        return redirect(url_for('session_log'))
    
    # 获取用户的攀登记录
    grouped_logs, session_logs = ClimbingService.get_user_climb_logs_grouped(user_id)
    
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
        
        if not username or not password:
            flash('Username and password are required.')
            return render_template('login.html')
        
        user = AuthService.authenticate_user(username, password)
        if user:
            session['user'] = username
            session['user_id'] = user['id']
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if not session.get('user'):
        flash('Please login first.')
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    if not user_id:
        flash('User not found.')
        return redirect(url_for('login'))
    
    # 获取用户资料统计数据
    stats = StatisticsService.get_user_profile_stats(user_id)
    username = session.get('user', 'Demo User')
    
    return render_template('profile.html', stats=stats, username=username)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email', '')
        
        if not username or not password:
            flash('Username and password are required.')
            return render_template('signup.html')
        
        # 创建新用户
        user_id = AuthService.create_user(username, password, email)
        if user_id:
            flash('Account created! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists or creation failed.')
    
    return render_template('signup.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        
        if not username or not new_password:
            flash('Username and new password are required.')
            return render_template('reset_password.html')
        
        # 更新密码
        if AuthService.update_password(username, new_password):
            flash('Password updated! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username does not exist.')
    
    return render_template('reset_password.html')

@app.route('/rank')
def rank():
    # 获取排名数据
    rankings = ClimbingService.get_climbing_rankings()
    
    return render_template('rank.html', 
                         bouldering_ranks=rankings['bouldering'], 
                         sport_ranks=rankings['sport'])

# API路由 - 用户管理
@app.route('/api/users', methods=['GET'])
def api_get_users():
    """获取所有用户列表"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    from database.dao import user_dao
    users = user_dao.get_all()
    return {'users': users}

@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    """获取指定用户信息"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    user_info = UserService.get_user_info(user_id)
    if user_info:
        return user_info
    return {'error': 'User not found'}, 404

@app.route('/api/users/<int:user_id>/profile', methods=['PUT'])
def api_update_user_profile(user_id):
    """更新用户资料"""
    if not session.get('user') or session.get('user_id') != user_id:
        return {'error': 'Not authorized'}, 403
    
    profile_data = request.get_json()
    if UserService.update_user_profile(user_id, profile_data):
        return {'message': 'Profile updated successfully'}
    return {'error': 'Failed to update profile'}, 400

# API路由 - 攀登记录管理
@app.route('/api/climb-logs', methods=['POST'])
def api_create_climb_log():
    """创建攀登记录"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    user_id = session.get('user_id')
    data = request.get_json()
    
    required_fields = ['name', 'type', 'grade', 'session_date']
    if not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    climb_log_id = ClimbingService.create_climb_log(user_id, data['session_date'], data)
    if climb_log_id:
        return {'climb_log_id': climb_log_id, 'message': 'Climb log created successfully'}
    return {'error': 'Failed to create climb log'}, 400

@app.route('/api/climb-logs/<int:user_id>', methods=['GET'])
def api_get_user_climb_logs(user_id):
    """获取用户攀登记录"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    grouped_logs, all_logs = ClimbingService.get_user_climb_logs_grouped(user_id)
    return {
        'grouped_logs': grouped_logs,
        'all_logs': all_logs
    }

@app.route('/api/climb-logs/<int:log_id>', methods=['DELETE'])
def api_delete_climb_log(log_id):
    """删除攀登记录"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    user_id = session.get('user_id')
    if ClimbingService.delete_climb_log(log_id, user_id):
        return {'message': 'Climb log deleted successfully'}
    return {'error': 'Failed to delete climb log'}, 400

# API路由 - 统计数据
@app.route('/api/statistics/update/<int:user_id>', methods=['POST'])
def api_update_user_statistics(user_id):
    """更新用户统计数据"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    StatisticsService.update_user_statistics(user_id)
    return {'message': 'Statistics updated successfully'}

@app.route('/api/statistics/update-all', methods=['POST'])
def api_update_all_statistics():
    """更新所有用户统计数据"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    StatisticsService.update_all_user_statistics()
    return {'message': 'All statistics updated successfully'}

# API路由 - 场馆管理
@app.route('/api/gyms', methods=['GET'])
def api_get_gyms():
    """获取所有场馆"""
    from database.dao import climbing_gym_dao
    gyms = climbing_gym_dao.get_all()
    return {'gyms': gyms}

@app.route('/api/gyms', methods=['POST'])
def api_create_gym():
    """创建场馆"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    gym_data = request.get_json()
    if 'name' not in gym_data:
        return {'error': 'Gym name is required'}, 400
    
    gym_id = GymService.create_gym(gym_data)
    if gym_id:
        return {'gym_id': gym_id, 'message': 'Gym created successfully'}
    return {'error': 'Failed to create gym'}, 400

@app.route('/api/gyms/<int:gym_id>', methods=['PUT'])
def api_update_gym(gym_id):
    """更新场馆"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    gym_data = request.get_json()
    if GymService.update_gym(gym_id, gym_data):
        return {'message': 'Gym updated successfully'}
    return {'error': 'Failed to update gym'}, 400

# API路由 - 笔记管理
@app.route('/api/movement-notes', methods=['POST'])
def api_create_movement_note():
    """创建动作笔记"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    user_id = session.get('user_id')
    data = request.get_json()
    
    required_fields = ['climb_log_id', 'title', 'content']
    if not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    note_id = NoteService.create_movement_note(user_id, data['climb_log_id'], data)
    if note_id:
        return {'note_id': note_id, 'message': 'Note created successfully'}
    return {'error': 'Failed to create note'}, 400

@app.route('/api/movement-notes/<int:user_id>', methods=['GET'])
def api_get_user_movement_notes(user_id):
    """获取用户动作笔记"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    from database.dao import movement_note_dao
    notes = movement_note_dao.get_by_user_id(user_id)
    return {'notes': notes}

@app.route('/api/movement-notes/<int:note_id>', methods=['PUT'])
def api_update_movement_note(note_id):
    """更新动作笔记"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    note_data = request.get_json()
    if NoteService.update_movement_note(note_id, note_data):
        return {'message': 'Note updated successfully'}
    return {'error': 'Failed to update note'}, 400

@app.route('/api/movement-notes/<int:note_id>', methods=['DELETE'])
def api_delete_movement_note(note_id):
    """删除动作笔记"""
    if not session.get('user'):
        return {'error': 'Not authenticated'}, 401
    
    from database.dao import movement_note_dao
    if movement_note_dao.delete_by_id(note_id):
        return {'message': 'Note deleted successfully'}
    return {'error': 'Failed to delete note'}, 400

# API路由 - 排名数据
@app.route('/api/rankings', methods=['GET'])
def api_get_rankings():
    """获取排名数据"""
    rankings = ClimbingService.get_climbing_rankings()
    return rankings

@app.route('/delete-session/<int:log_id>', methods=['POST'])
def delete_session(log_id):
    """Web form route to delete climb log"""
    if not session.get('user'):
        flash('Please login first.')
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    if ClimbingService.delete_climb_log(log_id, user_id):
        flash('Session deleted successfully!')
    else:
        flash('Failed to delete session.')
    
    return redirect(url_for('session_log'))

@app.route('/edit-session/<int:log_id>', methods=['POST'])
def edit_session(log_id):
    """Web form route to edit climb log"""
    if not session.get('user'):
        flash('Please login first.')
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    if not user_id:
        flash('User not found.')
        return redirect(url_for('login'))
    
    # Get form data
    name = request.form.get('name', '')
    climb_type = request.form.get('type', '')
    grade = request.form.get('grade', '')
    note = request.form.get('note', '')
    date_input = request.form.get('date')
    
    print(f"🔍 Edit session {log_id}: name={name}, type={climb_type}, grade={grade}, date={date_input}")  # Debug
    
    if not all([name, climb_type, grade]):
        flash('Name, type, and grade are required.')
        return redirect(url_for('session_log'))
    
    # Handle image upload
    file = request.files.get('image')
    new_image_filename = None
    if file and file.filename and allowed_file(file.filename):
        new_image_filename = datetime.now().strftime('%Y%m%d%H%M%S_') + secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_image_filename))
        print(f"🖼️ New image uploaded: {new_image_filename}")  # Debug
    
    # Prepare climb data
    climb_data = {
        'name': name,
        'type': climb_type,
        'grade': grade,
        'notes': note
    }
    
    print(f"📝 Calling update_climb_log with: log_id={log_id}, user_id={user_id}, climb_data={climb_data}, new_image={new_image_filename}")  # Debug
    
    # Update the climb log
    if ClimbingService.update_climb_log(log_id, user_id, climb_data, new_image_filename):
        flash('Session updated successfully!')
        print(f"✅ Session {log_id} updated successfully")  # Debug
    else:
        flash('Failed to update session.')
        print(f"❌ Failed to update session {log_id}")  # Debug
    
    return redirect(url_for('session_log'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 检查数据库是否存在
    if not os.path.exists(app.config['DATABASE']):
        print("❌ 数据库文件不存在！请先运行 database/init_database.py 初始化数据库")
        print("💡 运行命令: python database/init_database.py")
    
    app.run(debug=True)

