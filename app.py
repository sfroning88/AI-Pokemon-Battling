import os, sys
from flask import Flask, render_template, request, jsonify
from ngrok import connect

# create a Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# get the Ngrok token
ngrok_token = os.environ.get('NGROK_API_TOKEN')

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/UPDATE_GLOBALS', methods=['POST'])
def UPDATE_GLOBALS():
    import support.config
    from flask import request
    
    data = request.get_json()

    if data is None:
        return jsonify({'success': False, 'message': ''})
    
    boom_user = data.get('boom_user')
        
    if not boom_user:
        return jsonify({'success': False, 'message': 'Missing required parameters.'}), 400
        
    # Update global variables
    support.config.boom_user = boom_user

    print(f"CHECKPOINT: Boom user identified as  {support.config.boom_user}")
        
    return jsonify({'success': True, 'message': 'Global variables updated successfully.'}), 200

# generic button function
@app.route('/UPLOAD_FILE', methods=['POST'])
def UPLOAD_FILE():
    from support.extension import ALLOWED_EXTENSIONS, retrieve_extension
    from support.generate import generate_code

    file = request.files.get('file')
    if not file:
            return jsonify({'success': False, 'message': 'No file detected.'}), 400

    file_extension = retrieve_extension(file.filename)
    if file_extension not in ALLOWED_EXTENSIONS:
        print(f"WARNING: Invalid file of type {file_extension}")
        return jsonify({'success': False, 'message': "Invalid file extension detected."}), 400

    import support.config
    code = generate_code(file.filename)
    support.config.files[code] = {'name': file.filename, 'content': file}
    
    print(f"CHECKPOINT: File {file.filename} with code {code} processed successfully")
    return jsonify({'success': True, 'message': f'File {file.filename} with code {code} processed successfully'}), 200


# generic button function
@app.route('/BUTTON_FUNCTION_TWO', methods=['POST'])
def BUTTON_FUNCTION_TWO():
    return jsonify({'success': True, 'message': 'Button Function Two success.'}), 200

@app.route('/BUTTON_FUNCTION_THREE', methods=['POST'])
def BUTTON_FUNCTION_THREE():
    return jsonify({'success': True, 'message': 'Button Function Three success.'}), 200

@app.route('/BUTTON_FUNCTION_FOUR', methods=['POST'])
def BUTTON_FUNCTION_FOUR():
    return jsonify({'success': True, 'message': 'Button Function Four success.'}), 200

@app.route('/BUTTON_FUNCTION_FIVE', methods=['POST'])
def BUTTON_FUNCTION_FIVE():
    return jsonify({'success': True, 'message': 'Button Function Five success.'}), 200

@app.route('/BUTTON_FUNCTION_SIX', methods=['POST'])
def BUTTON_FUNCTION_SIX():
    return jsonify({'success': True, 'message': 'Button Function Six success.'}), 200

@app.route('/BUTTON_FUNCTION_SEVEN', methods=['POST'])
def BUTTON_FUNCTION_SEVEN():
    return jsonify({'success': True, 'message': 'Button Function Seven success.'}), 200

@app.route('/BUTTON_FUNCTION_EIGHT', methods=['POST'])
def BUTTON_FUNCTION_EIGHT():
    return jsonify({'success': True, 'message': 'Button Function Eight success.'}), 200
    
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
    tunnel = connect(5000, domain="guiding-needlessly-mallard.ngrok-free.app")

    if tunnel is None:
        print("ERROR: Failed to connect to ngrok tunnel, check active instances")
        sys.exit(1)

    print("##############################_APP_BEGIN_##############################")

    # Static domain is configured in api/connect.py
    print(f"CHECKPOINT: Using static domain: https://guiding-needlessly-mallard.ngrok-free.app/oauth/callback")

    import support.config
    support.config.files = {}
    support.config.boom_user = "Sean"

    print("##############################_APP_END_##############################")

    # run the app
    app.run(debug=False, port=5000)
