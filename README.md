# ClimbTrack: Indoor Climbing Training Logger

ClimbTrack is a comprehensive web-based training log tool for indoor climbers. Record your climbing sessions, track progress, analyze performance, and compete with the climbing community.


## Live Demo
https://climbtrack.onrender.com


## 🎯 Key Features

- **🔐 User Management**: Secure authentication and user profiles
- **🧗 Session Logging**: Record climbs with grades, notes, and photos
- **📊 Progress Tracking**: Automatic personal best detection and statistics
- **🏆 Rankings**: Global leaderboards for bouldering and sport climbing
- **🏢 Gym Management**: Track gym info and crowd levels
- **🔌 RESTful API**: Complete CRUD operations for all data

## 🚀 Quick Start

### 1. Setup Database
```bash
python database/init_database.py
```

### 2. Install & Run
```bash
pip install -r requirements.txt
python app.py
```
Visit [http://localhost:5000](http://localhost:5000)

### 3. Login with Test Accounts
- **Alice**: `alice` / `password123`
- **Bob**: `bob` / `climbhard`  
- **Charlie**: `charlie` / `bouldering`

## 📁 Project Structure

```
ClimbTrack/
├── app.py                    # Main Flask application
├── database/                 # Database layer
│   ├── models.py            # Data models
│   ├── dao.py               # Data access objects
│   ├── services.py          # Business logic
│   └── init_database.py     # Database setup
├── templates/               # HTML templates
├── static/                  # CSS, JS, uploads
└── API_DOCUMENTATION.md     # Complete API docs
```

## 💻 API Examples

### Service Layer
```python
from database.services import AuthService, ClimbingService

# Authenticate user
user = AuthService.authenticate_user("alice", "password123")

# Create climb log
climb_data = {"name": "Crimson Tide", "type": "bouldering", "grade": "V4"}
ClimbingService.create_climb_log(user['id'], "2024-01-15", climb_data)
```

### REST API
```bash
# Get rankings
GET /api/rankings

# Create climb log
POST /api/climb-logs
{"name": "Blue Moon", "type": "bouldering", "grade": "V5", "session_date": "2024-01-15"}
```

## 🧪 Testing

```bash
pytest test/test_session_log.py -v
```

## 📚 Documentation

- **[API Documentation](API_DOCUMENTATION.md)**: Complete API reference
- **[Setup Guide](SETUP_GUIDE.md)**: Detailed setup instructions
- **[Database Docs](database/DATABASE_README.md)**: Database schema and design

## 🛠️ Technology Stack

- **Backend**: Python Flask, SQLite
- **Frontend**: HTML5, CSS3, Bootstrap
- **Architecture**: Three-tier with DAO pattern
- **API**: RESTful JSON with session auth

## 📈 Database Management

```bash
# Update statistics
python database/update_statistics.py

# Backup database
cp database/climbtrack.db database/backup_$(date +%Y%m%d).db
```

## 🎯 Current Status

✅ **Complete**: Database architecture, user auth, climbing logs, rankings, API  
🚧 **Future**: Mobile app, social features, advanced analytics

## 📞 Contact

**Repository**: [ClimbTrack GitHub](https://github.com/FFFfff1FFFfff/ClimbTrack)  
**Developer**: zyx119@uw.edu  
**Client**: yifanli8@uw.edu

---

**Ready to start climbing? Initialize the database and start logging! 🧗‍♀️🧗‍♂️**
