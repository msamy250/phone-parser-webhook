from flask import Flask, request, jsonify
from flask_cors import CORS
import phonenumbers
from phonenumbers import geocoder, carrier
import os
import csv
import pycountry

app = Flask(__name__)
CORS(app)  # Enable CORS for Zapier and other services

# Load country reference mapping from CSV
COUNTRY_REFERENCE_MAP = {}

def load_country_references():
    """Load country references from CSV file"""
    global COUNTRY_REFERENCE_MAP
    csv_path = os.path.join(os.path.dirname(__file__), 'countries_reference.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                country_name = row.get('Country or region', '').strip()
                reference_value = row.get('correct_country_value', '').strip()
                if country_name and reference_value:
                    COUNTRY_REFERENCE_MAP[country_name] = reference_value
    except FileNotFoundError:
        print("Warning: countries_reference.csv not found. Country references will not be available.")
    except Exception as e:
        print(f"Error loading country references: {e}")

# Load the country references when the app starts
load_country_references()

def get_country_reference(country_name):
    """
    Get country reference value from the mapping.
    Tries multiple matching strategies to find the reference.
    """
    if not country_name:
        return None
    
    # Direct match
    if country_name in COUNTRY_REFERENCE_MAP:
        return COUNTRY_REFERENCE_MAP[country_name]
    
    # Try common variations
    variations = [
        country_name,
        country_name.replace("United States", "United States of America"),
        country_name.replace("United Kingdom", "United Kingdom"),
        country_name.replace("UAE", "United Arab Emirates"),
        country_name.replace("U.A.E.", "United Arab Emirates"),
        country_name.replace("Netherlands", "The Netherlands"),
        country_name.replace("Korea, Republic of", "Korea, South"),
        country_name.replace("Korea, Democratic People's Republic of", "Korea, North"),
        country_name.replace("Congo, The Democratic Republic of the", "Congo, Democratic Republic of the"),
        country_name.replace("Gambia", "Gambia, The"),
    ]
    
    for variation in variations:
        if variation in COUNTRY_REFERENCE_MAP:
            return COUNTRY_REFERENCE_MAP[variation]
    
    # Case-insensitive search
    country_lower = country_name.lower()
    for key, value in COUNTRY_REFERENCE_MAP.items():
        if key.lower() == country_lower:
            return value
    
    return None

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
        
        # Get country name from region code (e.g., 'US' -> 'United States')
        import pycountry
        region_code = phonenumbers.region_code_for_number(parsed_number)
        try:
            country_name = pycountry.countries.get(alpha_2=region_code).name
        except:
            # Fallback to geocoder if pycountry fails
            country_name = geocoder.description_for_number(parsed_number, "en")
        
        # Get country reference from the mapping
        country_reference = get_country_reference(country_name)
        
        # Prepare response
        response = {
            "success": True,
            "data": {
                "local_number": local_number,
                "country_code": country_code,
                "country_name": country_name,
                "country_reference": country_reference
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
