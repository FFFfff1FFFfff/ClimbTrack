# ClimbTrack: Indoor Climbing Training Logger
## Project Scope

ClimbTrack is a web-based training log tool for indoor climbers. It helps users record their climbing sessions, upload media, write movement notes, detect crowd, and track progress over time in an organized, intuitive format.

## Target Users

- Indoor climbers of all levels seeking structured training feedback  
- Climbers preparing for competitions or training cycles  

Users want to:
- Log training sessions with details like route difficulty and location  
- Upload and review videos/photos  
- Note down beta, crux moves, or style observations  
- Track personal goals and progress visually  

## Features

### Core Features:
- Log climb sessions (date, location, grade/difficulty)  
- Add movement notes (beta, style, crux descriptions)  
- Upload and store media files (photos and videos)
- Detect the number of people in the climbing gym (number and activities)

### Additional Features:
- **User Login**: Simple username/password login (default: testuser / password123).
- **Session Log**: Upload climbing session records with photo, grade, notes, and date. All records are grouped by day in a timeline (like social media moments).
- **Crowd Detection**: (Stub page) For future crowd detection features.
- **Rank**: (Stub page) For future ranking features.
- **Modern UI**: Responsive, modern design with Bootstrap and custom styles.
- **Unit Tests**: Pytest-based tests for session log upload and grouping.

## Project Progress
- **Session Log**: Record each climbing session with date, grade, notes, photo, type, and name.
- **Rank Page**: View bouldering and sport climbing leaderboards, ranked by highest grade and completion time.
- **Crowd Detection**: Visualize historical, current, and predicted gym crowd levels with interactive charts.
- **Profile Page**: See your climbing stats, ability radar, wall preference pie chart, grade progression, 30-day activity heatmap, and manage your training notes.
- **User System**: Login, sign up for a new account, and reset your password if forgotten.
- **Unified Navigation**: All pages have a consistent, homepage-style navigation bar for easy access.

## Project Structure

```
climbing_gym_app/
│
├── app.py        
├── pages/
│   └── profile.py     
├── requirements.txt   
└── README.md           
```

## Next Week's Plan
- [ ] Database integration for persistent user and session storage
- [ ] Email verification and password reset via email
- [ ] More advanced analytics and visualizations

## Timeline
| Week | Tasks |
|------|-------|
| 1–2  | Setup environment and Develop basic page structure |
| 3–4  | Implement personal profile and history screens |
| 5–6  | Develop media upload/storage system |
| 7    | Integrate media upload and backend storage |
| 8-9  | Refine and implement crowd detection and activity monitory |


## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   python app.py
   ```
   Visit [http://localhost:5000](http://localhost:5000)

3. **Login**
   - Username: `testuser`
   - Password: `password123`

4. **Session Log**
   - Click "Session Log" on the homepage.
   - Click the big "+" button to upload a new session (photo, grade, notes, date).
   - All sessions are grouped by day in a timeline.

5. **Run Tests**
   ```bash
   pytest test_session_log.py
   ```

## Contact Information

**Project GitHub:** [https://github.com/FFFfff1FFFfff/TECHIN510](https://github.com/FFFfff1FFFfff/ClimbTrack)  
**Client Email:** yifanli8@uw.edu |
**Developer Email:** zyx119@uw.edu