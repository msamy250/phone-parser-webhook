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

def detect_country_from_local_number(phone_number_str):
    """
    Detect country from local phone number patterns
    Returns country code (e.g., 'EG', 'US', 'AE') or None
    """
    # Remove spaces, dashes, parentheses
    clean_number = ''.join(filter(str.isdigit, phone_number_str))
    length = len(clean_number)
    
    # ===== EGYPT (EG) =====
    # Mobile: 11 digits starting with 010, 011, 012, 015
    if length == 11 and clean_number.startswith(('010', '011', '012', '015')):
        return 'EG'
    
    # ===== SAUDI ARABIA (SA) =====
    # Mobile: 10 digits starting with 05 (must come before Egypt landline check)
    if length == 10 and clean_number.startswith('05'):
        return 'SA'
    
    # ===== JORDAN (JO) =====
    # Mobile: 10 digits starting with 07 (must come before Egypt landline check)
    if length == 10 and clean_number.startswith('07'):
        return 'JO'
    
    # ===== PHILIPPINES (PH) =====
    # With country code already included: 12 digits starting with 63
    if length == 12 and clean_number.startswith('63'):
        return None  # Already has country code
    # Mobile: 10 digits starting with 09 (must come before Egypt landline check)
    if length == 10 and clean_number.startswith('09'):
        return 'PH'
    
    # EGYPT (continued)
    # Landline: 9-10 digits starting with 02-04, 06-08 (exclude 05, 07, 09)
    if 9 <= length <= 10 and clean_number.startswith('0'):
        if clean_number[1:2] in '234678':  # Exclude 0, 1, 5, 7, 9
            return 'EG'
    
    # ===== UAE (AE) =====
    # Mobile: 9 digits starting with 5 (50, 52, 54, 55, 56, 58)
    if length == 9 and clean_number.startswith(('50', '52', '54', '55', '56', '58')):
        return 'AE'
    
    # ===== KUWAIT (KW) =====
    # Mobile: 8 digits starting with 5, 6, or 9
    if length == 8 and clean_number[0] in ('5', '6', '9'):
        return 'KW'
    
    # ===== BAHRAIN (BH) =====
    # Mobile: 8 digits starting with 3
    if length == 8 and clean_number.startswith('3'):
        return 'BH'
    
    # ===== QATAR (QA) =====
    # Mobile: 8 digits starting with 3, 5, 6, or 7
    if length == 8 and clean_number[0] in ('3', '5', '6', '7'):
        # Conflict with Kuwait and Bahrain, prioritize Qatar if starts with 3 or 7
        if clean_number[0] in ('3', '7'):
            return 'QA'
        # For 5 and 6, default to Kuwait
        return 'KW'
    
    # ===== TURKEY (TR) =====
    # Mobile: 11 digits starting with 05
    if length == 11 and clean_number.startswith('05'):
        return 'TR'
    
    # ===== NEPAL (NP) =====
    # With country code already included: 13 digits starting with 977
    if length == 13 and clean_number.startswith('977'):
        return None  # Already has country code, let phonenumbers handle it
    # Mobile: 10 digits starting with 984, 985, 986 (more specific)
    if length == 10 and clean_number.startswith(('984', '985', '986', '980', '981', '982')):
        return 'NP'
    
    # ===== INDIA (IN) =====
    # Mobile: 10 digits starting with 6, 7, 8, 9
    if length == 10 and clean_number[0] in ('6', '7', '8', '9'):
        return 'IN'
    
    # ===== PAKISTAN (PK) =====
    # Mobile: 10 digits starting with 3
    if length == 10 and clean_number.startswith('3'):
        return 'PK'
    
    # ===== UNITED KINGDOM (GB) =====
    # Mobile: 11 digits starting with 07
    if length == 11 and clean_number.startswith('07'):
        return 'GB'
    # Mobile/Landline: 11 digits starting with 0 (general UK pattern)
    if length == 11 and clean_number.startswith('0'):
        return 'GB'
    
    # ===== UNITED STATES (US) / CANADA (CA) =====
    # Mobile/Landline: 10 digits starting with 2-5
    if length == 10 and clean_number[0] in ('2', '3', '4', '5'):
        return 'US'  # Could also be Canada (same country code)
    
    # ===== UKRAINE (UA) =====
    # With country code: 12 digits starting with 380
    if length == 12 and clean_number.startswith('380'):
        return None  # Already has country code
    
    # ===== UGANDA (UG) =====
    # With country code: 12 digits starting with 256
    if length == 12 and clean_number.startswith('256'):
        return None  # Already has country code
    
    # ===== SUDAN (SD) =====
    # With country code: 12 digits starting with 249
    if length == 12 and clean_number.startswith('249'):
        return None  # Already has country code
    
    # ===== SOMALIA (SO) =====
    # With country code: 12 digits starting with 252
    if length == 12 and clean_number.startswith('252'):
        return None  # Already has country code
    
    # ===== SWEDEN (SE) =====
    # With country code: 11 digits starting with 46
    if length == 11 and clean_number.startswith('46'):
        return None  # Already has country code
    
    return None

@app.route('/parse-phone', methods=['POST'])
def parse_phone():
    """
    Webhook endpoint to parse phone number information
    
    Expected JSON input:
    {
        "phone_number": "505237982",
        "country_hint": "AE"   ← Optional: pass Facebook's country field to resolve conflicts
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
        
        phone_number_str = str(data['phone_number']).strip()
        
        # Optional country hint to resolve ambiguous numbers (e.g. UAE vs Saudi)
        # Meta sends country in various formats: 'AE', 'UAE', 'United Arab Emirates', 'SA', 'Saudi Arabia', etc.
        # This is completely optional - detection still works without it
        country_hint_raw = str(data.get('country_hint', '') or '').strip()
        
        # Normalize ALL Meta country name variations to ISO 2-letter codes
        COUNTRY_HINT_MAP = {
            # ── ISO 2-letter codes (Meta sometimes sends these directly) ──
            'AE': 'AE', 'SA': 'SA', 'EG': 'EG', 'IN': 'IN', 'PK': 'PK',
            'PH': 'PH', 'TR': 'TR', 'KW': 'KW', 'BH': 'BH', 'QA': 'QA',
            'JO': 'JO', 'NP': 'NP', 'GB': 'GB', 'US': 'US', 'CA': 'CA',
            'DE': 'DE', 'FR': 'FR', 'IT': 'IT', 'ES': 'ES', 'AU': 'AU',
            'OM': 'OM', 'LB': 'LB', 'IQ': 'IQ', 'SY': 'SY', 'YE': 'YE',
            'MA': 'MA', 'DZ': 'DZ', 'TN': 'TN', 'LY': 'LY', 'SD': 'SD',
            'NG': 'NG', 'KE': 'KE', 'ZA': 'ZA', 'GH': 'GH', 'ET': 'ET',

            # ── UAE variations ──
            'UNITED ARAB EMIRATES': 'AE',
            'UAE': 'AE',
            'U.A.E': 'AE',
            'U.A.E.': 'AE',
            'EMIRATES': 'AE',
            'DUBAI': 'AE',
            'ABU DHABI': 'AE',
            'SHARJAH': 'AE',

            # ── Saudi Arabia variations ──
            'SAUDI ARABIA': 'SA',
            'SAUDI': 'SA',
            'KSA': 'SA',
            'K.S.A': 'SA',
            'K.S.A.': 'SA',
            'KINGDOM OF SAUDI ARABIA': 'SA',
            'RIYADH': 'SA',
            'JEDDAH': 'SA',

            # ── Egypt variations ──
            'EGYPT': 'EG',
            'MISR': 'EG',
            'CAIRO': 'EG',
            'ALEXANDRIA': 'EG',

            # ── India variations ──
            'INDIA': 'IN',
            'IND': 'IN',
            'BHARAT': 'IN',
            'MUMBAI': 'IN',
            'DELHI': 'IN',
            'BANGALORE': 'IN',

            # ── Pakistan variations ──
            'PAKISTAN': 'PK',
            'PAK': 'PK',
            'KARACHI': 'PK',
            'LAHORE': 'PK',

            # ── Philippines variations ──
            'PHILIPPINES': 'PH',
            'FILIPINAS': 'PH',
            'PHL': 'PH',
            'MANILA': 'PH',

            # ── Turkey variations ──
            'TURKEY': 'TR',
            'TURKIYE': 'TR',
            'TUR': 'TR',
            'ISTANBUL': 'TR',

            # ── Kuwait variations ──
            'KUWAIT': 'KW',
            'KWT': 'KW',
            'KUWAIT CITY': 'KW',

            # ── Bahrain variations ──
            'BAHRAIN': 'BH',
            'BHR': 'BH',
            'MANAMA': 'BH',

            # ── Qatar variations ──
            'QATAR': 'QA',
            'QAT': 'QA',
            'DOHA': 'QA',

            # ── Jordan variations ──
            'JORDAN': 'JO',
            'JOR': 'JO',
            'AMMAN': 'JO',

            # ── Nepal variations ──
            'NEPAL': 'NP',
            'NPL': 'NP',
            'KATHMANDU': 'NP',

            # ── UK variations ──
            'UNITED KINGDOM': 'GB',
            'UK': 'GB',
            'GBR': 'GB',
            'GREAT BRITAIN': 'GB',
            'ENGLAND': 'GB',
            'BRITAIN': 'GB',
            'LONDON': 'GB',

            # ── USA variations ──
            'UNITED STATES': 'US',
            'UNITED STATES OF AMERICA': 'US',
            'USA': 'US',
            'U.S.A': 'US',
            'U.S.A.': 'US',
            'AMERICA': 'US',

            # ── Canada variations ──
            'CANADA': 'CA',
            'CAN': 'CA',
            'TORONTO': 'CA',
            'VANCOUVER': 'CA',

            # ── Oman variations ──
            'OMAN': 'OM',
            'MUSCAT': 'OM',

            # ── Lebanon variations ──
            'LEBANON': 'LB',
            'BEIRUT': 'LB',

            # ── Iraq variations ──
            'IRAQ': 'IQ',
            'BAGHDAD': 'IQ',

            # ── Morocco variations ──
            'MOROCCO': 'MA',
            'MAROC': 'MA',
            'CASABLANCA': 'MA',
        }

        # Normalize the hint (uppercase, trimmed) and look up
        country_hint = COUNTRY_HINT_MAP.get(country_hint_raw.upper()) if country_hint_raw else None
        
        # Try to detect country from local number patterns
        detected_country = None
        if not phone_number_str.startswith('+'):
            detected_country = detect_country_from_local_number(phone_number_str)
        
        # Apply country_hint to resolve ambiguous cases
        # Only override pattern detection when there's genuine ambiguity
        if country_hint and not phone_number_str.startswith('+'):
            clean = ''.join(filter(str.isdigit, phone_number_str))
            length = len(clean)
            valid_hints = {'AE','SA','EG','IN','PK','PH','TR','KW','BH','QA',
                           'JO','NP','GB','US','CA','OM','LB','IQ','SY','YE',
                           'MA','DZ','TN','LY','SD','NG','KE','ZA','GH','ET'}
            
            if country_hint in valid_hints:
                # Case 1: No detection at all → trust the hint
                if detected_country is None:
                    detected_country = country_hint
                
                # Case 2: UAE vs Saudi ambiguity
                # 9-digit numbers starting with 5 could be UAE or Saudi (without leading 0)
                elif length == 9 and clean[0] == '5' and country_hint in ('AE', 'SA'):
                    detected_country = country_hint
                
                # Case 3: Pattern detected a country but hint disagrees
                # Only override if hint is plausible for this number length/prefix
                elif detected_country != country_hint:
                    # Trust hint over pattern for ambiguous Gulf numbers (5x, 9 digits)
                    if length == 9 and clean[0] in ('5', '6') and country_hint in ('AE', 'KW', 'QA', 'BH', 'OM'):
                        detected_country = country_hint
                    # Trust hint for 8-digit Gulf numbers (KW, BH, QA overlap)
                    elif length == 8 and country_hint in ('KW', 'BH', 'QA'):
                        detected_country = country_hint
                    # Trust hint for 10-digit numbers (SA, IN, PK, JO overlap)
                    elif length == 10 and country_hint in ('SA', 'IN', 'PK', 'JO'):
                        detected_country = country_hint
        
        # Parse the phone number
        try:
            parsed_number = phonenumbers.parse(phone_number_str, detected_country)
        except phonenumbers.NumberParseException:
            # If parsing fails and we haven't tried country detection, try it
            if detected_country is None:
                detected_country = detect_country_from_local_number(phone_number_str)
                if detected_country:
                    parsed_number = phonenumbers.parse(phone_number_str, detected_country)
                else:
                    raise
        
        # Extract information
        country_code = str(parsed_number.country_code)
        local_number = str(parsed_number.national_number)
        region_code = phonenumbers.region_code_for_number(parsed_number)
        
        # For Egyptian numbers, preserve the leading 0 in local format
        if region_code == 'EG' and not local_number.startswith('0'):
            local_number = '0' + local_number
        
        # Get country name from region code (e.g., 'US' -> 'United States')
        country_name = ""
        
        # Try pycountry first
        try:
            import pycountry
            country_obj = pycountry.countries.get(alpha_2=region_code)
            if country_obj:
                country_name = country_obj.name
        except:
            pass
        
        # Fallback to geocoder if pycountry fails
        if not country_name:
            try:
                country_name = geocoder.description_for_number(parsed_number, "en")
            except:
                pass
        
        # Final fallback - use region code mapping
        if not country_name and region_code:
            region_to_country = {
                'US': 'United States',
                'GB': 'United Kingdom', 
                'CA': 'Canada',
                'IN': 'India',
                'PK': 'Pakistan',
                'PH': 'Philippines',
                'NP': 'Nepal',
                'EG': 'Egypt',
                'AE': 'United Arab Emirates',
                'SA': 'Saudi Arabia',
                'KW': 'Kuwait',
                'BH': 'Bahrain',
                'QA': 'Qatar',
                'JO': 'Jordan',
                'TR': 'Turkey',
            }
            country_name = region_to_country.get(region_code, region_code)
        
        # Get country reference from the mapping
        country_reference = get_country_reference(country_name)
        
        # Validate that all fields have values
        if not local_number or not country_code or not country_name:
            return jsonify({
                "success": False,
                "error": "Unable to parse phone number completely",
                "data": {
                    "local_number": local_number or None,
                    "country_code": country_code or None,
                    "country_name": country_name or None,
                    "country_reference": country_reference
                }
            }), 400
        
        # Prepare response
        response = {
            "success": True,
            "data": {
                "local_number": local_number,
                "country_code": country_code,
                "country_name": country_name,
                "country_reference": country_reference,
                "country_hint_used": country_hint if country_hint else None
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
    