from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins (for development)

# Your API key for Anthropic
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

@app.route('/track', methods=['POST'])
def track():

    # Get the legal_description from the POST request
    # legal_description = request.get_json('legal_description')

    data = request.get_json()
    
    # Access the specific field 'legal_description'
    legal_description = data.get('legal_description')
    
    # For demonstration, you might want to print it
    print("Legal Description:", legal_description)

    if not legal_description:
        return jsonify({"error": "No legal description provided"}), 400

    prompt = Please convert the following legal description into a simplified format of deed calls (directions and distances). 

    **Important:** The exact format must be strictly followed. Each deed call should be presented on a new line with no additional text or explanation. The format is as follows:

    DirectionDistance Space Distance followed by "f"
    Each deed call should end with a single newline (\\n).
    Example:
    S89.12E 683.22f\n
    S89.12W 289.76f\n
    S89.12W 324.33f\n

    Legal Description:
    {legal_description}

    Please ensure the output matches this format exactly.
    """

#     prompt = f"""
# Please convert the following legal description into a simplified format of deed calls, specifying directions and distances. 
# Ensure that no words or lines from the legal description are skipped, and strictly adhere to the following format:

# Format:
# S89.12E 683.22f
# S89.12W 289.76f
# S89.12W 324.33f
# ...

# Legal Description:
# {legal_description}
# """

    # Make the request to the Claude API using a different model, like claude-2
    response = requests.post(
        "https://api.anthropic.com/v1/complete",
        headers={
            "x-api-key": anthropic_api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",  # Change to the appropriate valid version
        },
        json={
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "model": "claude-2",  # Use a different, valid model name
            "max_tokens_to_sample": 500,
        }
    )

    # Extract and return the deed calls from Claude's response
    response_json = response.json()

    if 'completion' in response_json:
        deed_calls = response_json['completion'].strip()
        return jsonify({"deed_calls": deed_calls}), 200
    else:
        return jsonify({"error": "Failed to generate deed calls"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
