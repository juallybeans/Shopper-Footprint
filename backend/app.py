from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io
import json

# Load environment variables from .env file
load_dotenv()

# --- Initialize Supabase ---
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- Initialize Google Gemini ---
gemini_api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
# Use the updated model name: gemini-1.5-flash-latest
model = genai.GenerativeModel('gemini-1.5-flash-latest')


# --- Initialize Flask App ---
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# --- API Endpoints ---

@app.route('/purchases', methods=['GET'])
def get_purchases():
    """Fetches all purchases from the database."""
    try:
        response = supabase.table('purchases').select("*").order('created_at', desc=True).execute()
        return jsonify(response.data)
    except Exception as e:
        # Log the detailed error to the console for debugging
        print(f"Error fetching purchases: {e}")
        return jsonify({"error": "Failed to fetch purchases from the database."}), 500


@app.route('/purchases', methods=['POST'])
def add_purchase():
    """Adds a new purchase to the database."""
    data = request.get_json()
    try:
        new_purchase = {
            'item_name': data.get('item_name'),
            'package_size': data.get('package_size'),
            'carbon_footprint': data.get('carbon_footprint')
        }
        response = supabase.table('purchases').insert(new_purchase).execute()
        return jsonify(response.data), 201
    except Exception as e:
        # Log the detailed error to the console for debugging
        print(f"Error adding purchase: {e}")
        return jsonify({"error": "Failed to add purchase. Ensure all fields are correct."}), 500


@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    """Analyzes an uploaded image using Gemini to identify the object and its carbon footprint."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        img = Image.open(io.BytesIO(file.read()))
        
        prompt = """
        Analyze the object in this image. 
        1. Identify the primary object (e.g., "black t-shirt", "running shoes", "wireless headphones").
        2. Provide a reasonable, estimated carbon footprint for the production of this single item in kg CO2e.
        Return the response ONLY as a valid JSON object with two keys: "object_name" and "carbon_footprint".
        For example: {"object_name": "cotton t-shirt", "carbon_footprint": 5.5}
        The value for carbon_footprint must be a number, not a string.
        """
        
        response = model.generate_content([prompt, img])
        
        # Extract and clean the JSON string from the response
        json_string = response.text.strip().replace('```json', '').replace('```', '')
        
        # Parse the string to a Python dictionary to ensure it's valid JSON before sending
        json_data = json.loads(json_string)
        
        # --- ADDED VALIDATION ---
        # Check if the response from the AI has the required keys and types
        if 'carbon_footprint' not in json_data or not isinstance(json_data['carbon_footprint'], (int, float)):
            raise ValueError("AI response did not contain a valid 'carbon_footprint' number.")

        return jsonify(json_data), 200

    except Exception as e:
        # This will now catch our custom ValueError as well
        print(f"Error during AI analysis or data validation: {e}")
        return jsonify({"error": "AI model returned an invalid data format."}), 500

# --- Main execution ---
if __name__ == '__main__':
    app.run(debug=True)

