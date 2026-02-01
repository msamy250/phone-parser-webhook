# Egyptian Phone Number Handling

This webhook now has special support for Egyptian phone numbers, including those without country codes.

## 🇪🇬 Egyptian Phone Number Support

### Supported Formats

#### Mobile Numbers (with country code):
- `+201234567890` ✅
- `+20 10 1234 5678` ✅
- `00201234567890` ✅

#### Mobile Numbers (WITHOUT country code - auto-detected):
- `01234567890` ✅ (Vodafone - starting with 010)
- `01112345678` ✅ (Etisalat - starting with 011)
- `01012345678` ✅ (Orange - starting with 010)
- `01512345678` ✅ (WE - starting with 015)

#### Landline Numbers (auto-detected):
- `0221234567` ✅ (Cairo - starting with 02)
- `0312345678` ✅ (Alexandria - starting with 03)
- `0451234567` ✅ (Other cities - 04-09)

### How It Works

The webhook automatically detects Egyptian numbers by their patterns:
1. **11-digit numbers starting with 010, 011, 012, 015** → Egypt mobile
2. **9+ digit numbers starting with 02-09** → Egypt landline
3. If country code is provided (+20), uses that directly

### Examples

#### Example 1: Egyptian Mobile (no country code)
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "01234567890"}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "local_number": "01234567890",
    "country_code": "20",
    "country_name": "Egypt",
    "country_reference": "53"
  }
}
```

#### Example 2: Egyptian Mobile (with country code)
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+201234567890"}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "local_number": "01234567890",
    "country_code": "20",
    "country_name": "Egypt",
    "country_reference": "53"
  }
}
```

#### Example 3: Egyptian Landline
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "0221234567"}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "local_number": "0221234567",
    "country_code": "20",
    "country_name": "Egypt",
    "country_reference": "53"
  }
}
```

## 🌍 Other Countries (Without Country Code)

### US Numbers
10-digit numbers without country code are assumed to be US:
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "4155552671"}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "local_number": "4155552671",
    "country_code": "1",
    "country_name": "United States",
    "country_reference": "185"
  }
}
```

## 📱 Facebook Lead Ads Integration

When Facebook Lead Ads collects phone numbers without country codes (common in Egypt), this webhook will:

1. ✅ Automatically detect Egyptian numbers (010, 011, 012, 015)
2. ✅ Parse them correctly as Egyptian numbers
3. ✅ Return the country code (20) and country reference (53)
4. ✅ Preserve the local format with leading zero

### Zapier Setup for Egyptian Leads

No special configuration needed! Just map the phone field:

```
Meta Lead Ads → Webhook
{
  "phone_number": "{{phone}}"  ← Can be with or without country code
}
```

The webhook handles both formats automatically.

## 🔧 Adding More Countries

To add automatic detection for other countries, edit the `detect_country_from_local_number` function in `phone_webhook.py`:

```python
def detect_country_from_local_number(phone_number_str):
    clean_number = ''.join(filter(str.isdigit, phone_number_str))
    
    # Egyptian patterns
    if len(clean_number) == 11 and clean_number.startswith(('010', '011', '012', '015')):
        return 'EG'
    
    # Saudi Arabia patterns (add your own)
    if len(clean_number) == 10 and clean_number.startswith('05'):
        return 'SA'
    
    # UAE patterns (add your own)
    if len(clean_number) == 9 and clean_number.startswith('5'):
        return 'AE'
    
    # Add more countries as needed...
    
    return None
```

## ⚠️ Important Notes

1. **Leading Zero:** Egyptian numbers keep their leading 0 in the `local_number` field
2. **Auto-Detection:** Only works for numbers WITHOUT `+` or country code prefix
3. **Fallback:** If pattern doesn't match any country, returns an error
4. **US Default:** 10-digit numbers default to US if no other pattern matches

## 🧪 Testing Egyptian Numbers

```bash
# Test various Egyptian formats
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "01012345678"}'

curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "01112345678"}'

curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "01234567890"}'

curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "01512345678"}'
```

All should return:
- `country_code: "20"`
- `country_name: "Egypt"`
- `country_reference: "53"`
