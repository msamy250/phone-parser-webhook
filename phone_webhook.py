from flask import Flask, request, jsonify
from flask_cors import CORS
import phonenumbers
from phonenumbers import geocoder, carrier
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for Zapier and other services

@app.route('/parse-phone', methods=['POST'])
def parse_phone():
    """
    Webhook endpoint to parse phone number information
    
    Expected JSON input:
    {
        "phone_number": "+1234567890"
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "local_number": "234567890",
            "country_code": "1",
            "country_name": "United States"
        }
    }
    """
    try:
        # Get phone number from request
        data = request.get_json()
        
        if not data or 'phone_number' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'phone_number' in request body"
            }), 400
        
        phone_number_str = data['phone_number']
        
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number_str, None)
        
        # Extract information
        country_code = str(parsed_number.country_code)
        local_number = str(parsed_number.national_number)
        country_name = geocoder.description_for_number(parsed_number, "en")
        
        # Prepare response
        response = {
            "success": True,
            "data": {
                "local_number": local_number,
                "country_code": country_code,
                "country_name": country_name
            }
        }
        
        return jsonify(response), 200
        
    except phonenumbers.NumberParseException as e:
        return jsonify({
            "success": False,
            "error": f"Invalid phone number: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    # Run the server (debug=False for production)
    app.run(host='0.0.0.0', port=port, debug=False)
