# app.py
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_cors import CORS
import pandas as pd
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session and flash messages
CORS(app)

# Initialize DataFrame with sample videos
sample_videos = [
    {
        "video_id": "dQw4w9WgXcQ",
        "title": "Test Video 1",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "ratings_list": "[]",  # Store as string representation of list
        "average_rating": 0.0
    }
]

# Create or load the DataFrame
try:
    profile=pd.read_csv('profile.csv')
    value = profile['stage'].iloc[0]
    points=profile['score'].iloc[0]
    df = pd.read_csv('video_dataset.csv')
    df=df[df['stage'] == 1]
    
    if 'ratings_list' not in df.columns:
        df['ratings_list'] = '[]'
    if 'average_rating' not in df.columns:
        df['average_rating'] = 0.0
except FileNotFoundError:
    df = pd.DataFrame(sample_videos)
    df.to_csv('video_ratings.csv', index=False)

# Path to Excel file to store login data
LOGIN_DATA_FILE = os.path.join(os.path.expanduser("~"), "login_data.xlsx")

def save_login_data(username, method):
    try:
        if os.path.exists(LOGIN_DATA_FILE):
            login_df = pd.read_excel(LOGIN_DATA_FILE)
        else:
            login_df = pd.DataFrame(columns=["username", "method"])
        new_entry = {"username": username, "method": method}
        login_df = login_df.append(new_entry, ignore_index=True)
        login_df.to_excel(LOGIN_DATA_FILE, index=False)
    except Exception as e:
        print(f"Error saving login data: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # For demonstration, accept any username/password
        if username and password:
            session['username'] = username
            save_login_data(username, "password")
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'error')
    return render_template('login.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/login/google')
def login_google():
    # Placeholder for Google OAuth login start
    username = "google_user"
    session['username'] = username
    save_login_data(username, "google")
    flash('Logged in with Google.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/login/microsoft')
def login_microsoft():
    # Placeholder for Microsoft OAuth login start
    username = "microsoft_user"
    session['username'] = username
    save_login_data(username, "microsoft")
    flash('Logged in with Microsoft.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')  # This must match the name in url_for()
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/descri')  # This must match the name in url_for()
def descri():
    return render_template('descri.html')

@app.route('/quiz')  # This must match the name in url_for()
def quiz():
    return render_template('quiz.html')

@app.route('/path')  # This must match the name in url_for()
def path():
    return render_template('path.html')

@app.route('/videos')  # This must match the name in url_for()
def videos():
    return render_template('videos.html')

@app.route('/api/videos', methods=['GET'])
def get_videos():
    videos = df.copy()
    # Convert string ratings to list for each video
    videos['ratings'] = videos['ratings_list'].apply(json.loads)
    videos_list = videos.to_dict('records')
    return jsonify(videos_list)

@app.route('/api/rate', methods=['POST'])
def rate_video():
    try:
        data = request.json
        video_id = data['video_id']
        rating = int(data['rating'])
        
        if rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Find the video index
        matching_rows = df[df['video_id'] == video_id]
        if matching_rows.empty:
            return jsonify({'error': 'Video not found'}), 404

        video_idx = matching_rows.index[0]  # ✅ Get the first matching index

        # Get current ratings, add new rating
        current_ratings = json.loads(df.at[video_idx, 'ratings_list'])
        current_ratings.append(rating)
        
        # Update ratings list and average
        df.at[video_idx, 'ratings_list'] = json.dumps(current_ratings)
        df.at[video_idx, 'average_rating'] = sum(current_ratings) / len(current_ratings)
        
        # Save to CSV
        df.to_csv('video_ratings.csv', index=False)
        
        return jsonify({
            'success': True,
            'average_rating': float(df.at[video_idx, 'average_rating']),
            'total_ratings': len(current_ratings)
        })
        
    except Exception as e:
        print(f"Error in rate_video: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)