import os, sys

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# create a Flask app
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Google OAuth imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# get the Ngrok token
from ngrok import connect
ngrok_token = os.environ.get('NGROK_TOKEN')

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

# OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']

@app.route('/')
def login():
    return render_template('user_login.html')

@app.route('/auth/google')
def google_auth():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    session['state'] = state
    return redirect(authorization_url)

@app.route('/auth/callback')
def auth_callback():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    
    user_email = user_info.get('email')
    user_name = user_info.get('name')
    user_picture = user_info.get('picture')
    
    session['user_email'] = user_email
    session['user_name'] = user_name
    session['user_picture'] = user_picture
    
    # Check if user already has an account with us
    from api.supabase import fetch_existing_users
    existing_users = fetch_existing_users()
    
    if existing_users:
        user_emails = [user['user_email'] for user in existing_users]
        if user_email in user_emails:
            return redirect(url_for('home'))
    
    return redirect(url_for('new_user'))
    

@app.route('/new_user')
def new_user():
    # Check if user is authenticated
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('user_new.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    user_display = request.form.get('user_display')
    user_logo = request.files.get('user_logo')
    
    # Handle logo upload to S3 bucket
    logo_filename = None
    if user_logo and user_logo.filename:
        # Upload to Supabase S3 bucket
        from api.supabase import post_user_avatar
        logo_filename = post_user_avatar(session['user_email'], user_logo)
    
    # Create user in Supabase using the post_new_user function
    from api.supabase import post_new_user
    response = post_new_user(session['user_email'], user_display, logo_filename)
    
    if response:
        # Store user info in session
        session['user_display'] = user_display
        session['user_logo'] = logo_filename
        return redirect(url_for('home'))
    else:
        return "Error creating account", 500

@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    # Handle file upload for user logo
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    user_logo = request.files.get('user_logo')
    
    if user_logo and user_logo.filename:
        # Upload to Supabase S3 bucket
        from api.supabase import post_user_avatar
        logo_filename = post_user_avatar(session['user_email'], user_logo)
        
        # Update user record with logo
        from api.supabase import post_new_user
        # For upload route, we might want to update existing user or create new one
        # This depends on the specific use case
        return jsonify({"success": True, "logo_filename": logo_filename})
    
    return jsonify({"success": False, "error": "No file uploaded"}), 400

@app.route('/home')
def home():
    # Check if user is authenticated
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    # Get user data from session
    user_data = {
        'user_display': session.get('user_display', session.get('user_name', 'User')),
        'user_email': session.get('user_email'),
        'user_logo': session.get('user_logo')
    }
    
    # Get avatar URL from S3 bucket if user has a logo
    if user_data['user_logo']:
        from api.supabase import fetch_avatar_url
        avatar_url = fetch_avatar_url(user_data['user_logo'])
        user_data['avatar_url'] = avatar_url
    else:
        user_data['avatar_url'] = None
    
    return render_template('user_home.html', **user_data)
    
if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage: python3 app.py")
        sys.exit(1)

    # ngrok tunnel URL (will be set when tunnel is created)
    ngrok_url = None

    # Check if ngrok is available and create tunnel
    import importlib.util
    ngrok_spec = importlib.util.find_spec("ngrok")
    
    if ngrok_spec is None:
        print("ERROR: ngrok package not available")
        sys.exit(1)

    # Authenticate with ngrok using environment token
    if ngrok_token is None:
        print("ERROR: Please set your ngrok token")
        sys.exit(1)
    
    from ngrok import set_auth_token
    set_auth_token(ngrok_token)

    from ngrok import connect
    ngrok_domain = os.environ.get('NGROK_DOMAIN')
    tunnel = connect(5000, domain=ngrok_domain)

    if tunnel is None:
        print("ERROR: Failed to connect to ngrok tunnel, check active instances")
        sys.exit(1)

    print(f"CHECKPOINT: Using static domain: {ngrok_domain}")

    # run the app with HTTPS
    app.run(debug=False, port=5000, ssl_context=('cert.pem', 'key.pem'))
