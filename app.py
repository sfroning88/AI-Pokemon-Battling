import os, sys

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# create a Flask app
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# get the Ngrok token
from ngrok import connect
ngrok_token = os.environ.get('NGROK_TOKEN')

# create Supabase client
from supabase import create_client
supabase_key = os.environ.get('SUPABASE_KEY')
supabase_url = os.environ.get('SUPABASE_URL')
supabase = create_client(supabase_url, supabase_key)

@app.route('/')
def login():
    return render_template('user_login.html')

@app.route('/auth/callback')
def auth_callback():
    # Handle Google OAuth callback
    # Extract session and redirect to user_home.html
    pass

@app.route('/home')
def home():
    # Check if user is authenticated
    # Render user_home.html
    return render_template('user_home.html')
    
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

    # run the app
    app.run(debug=False, port=5000)
