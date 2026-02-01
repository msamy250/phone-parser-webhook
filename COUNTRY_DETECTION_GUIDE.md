# Multi-Country Phone Number Detection

This webhook automatically detects phone numbers from **20+ countries** even without country codes!

## 🌍 Supported Countries

### Middle East & North Africa

#### 🇪🇬 Egypt (EG)
- **Mobile:** 11 digits starting with `010`, `011`, `012`, `015`
- **Landline:** 9-10 digits starting with `02-09`
- **Examples:** `01234567890`, `0221234567`
- **Country Code:** `+20`
- **Reference:** `53`

#### 🇦🇪 United Arab Emirates (AE)
- **Mobile:** 9 digits starting with `50`, `52`, `54`, `55`, `56`, `58`
- **Examples:** `505237982`, `522438846`, `565900369`
- **Country Code:** `+971`
- **Reference:** `183`

#### 🇸🇦 Saudi Arabia (SA)
- **Mobile:** 10 digits starting with `05`
- **Examples:** `0501234567`, `0551234567`
- **Country Code:** `+966`
- **Reference:** `151`

#### 🇰🇼 Kuwait (KW)
- **Mobile:** 8 digits starting with `5`, `6`, `9`
- **Examples:** `51234567`, `66123456`, `99123456`
- **Country Code:** `+965`
- **Reference:** `92`

#### 🇧🇭 Bahrain (BH)
- **Mobile:** 8 digits starting with `3`
- **Examples:** `33123456`, `36123456`
- **Country Code:** `+973`
- **Reference:** `13`

#### 🇶🇦 Qatar (QA)
- **Mobile:** 8 digits starting with `3`, `5`, `6`, `7`
- **Examples:** `33123456`, `55123456`, `77123456`
- **Country Code:** `+974`
- **Reference:** `141`

#### 🇯🇴 Jordan (JO)
- **Mobile:** 10 digits starting with `07`
- **Examples:** `0791234567`, `0781234567`
- **Country Code:** `+962`
- **Reference:** `86`

#### 🇹🇷 Turkey (TR)
- **Mobile:** 11 digits starting with `05`
- **Examples:** `05312345678`, `05551234567`
- **Country Code:** `+90`
- **Reference:** `178`

---

### Asia & Pacific

#### 🇮🇳 India (IN)
- **Mobile:** 10 digits starting with `6`, `7`, `8`, `9`
- **Examples:** `9876543210`, `8123456789`, `7012345678`
- **Country Code:** `+91`
- **Reference:** `77`

#### 🇵🇰 Pakistan (PK)
- **Mobile:** 10 digits starting with `3`
- **Examples:** `3001234567`, `3331234567`
- **Country Code:** `+92`
- **Reference:** `131`

#### 🇵🇭 Philippines (PH)
- **Mobile:** 10 digits starting with `9`
- **Examples:** `9171234567`, `9051234567`
- **Country Code:** `+63`
- **Reference:** `138`

#### 🇳🇵 Nepal (NP)
- **Mobile:** 10 digits starting with `98` or `97`
- **Examples:** `9841234567`, `9801234567`
- **Country Code:** `+977`
- **Reference:** `123`

---

### Europe & Americas

#### 🇬🇧 United Kingdom (GB)
- **Mobile:** 10-11 digits starting with `07` (with leading 0)
- **Landline:** 10-11 digits starting with `01`, `02`
- **Examples:** `07123456789`, `02012345678`
- **Country Code:** `+44`
- **Reference:** `184`

#### 🇺🇸 United States (US)
- **Mobile/Landline:** 10 digits
- **Examples:** `4155552671`, `2125551234`
- **Country Code:** `+1`
- **Reference:** `185`

#### 🇨🇦 Canada (CA)
- **Mobile/Landline:** 10 digits
- **Examples:** `4165551234`, `6135551234`
- **Country Code:** `+1` (same as US)
- **Reference:** `32`

---

### Auto-Detected (Already Have Country Code)

These numbers include country codes and are detected automatically:
- 🇺🇦 Ukraine: `380XXXXXXXXX` (12 digits)
- 🇺🇬 Uganda: `256XXXXXXXXX` (12 digits)
- 🇸🇩 Sudan: `249XXXXXXXXX` (12 digits)
- 🇸🇴 Somalia: `252XXXXXXXXX` (12 digits)
- 🇸🇪 Sweden: `46XXXXXXXXXX` (11 digits)

---

## 📊 Detection Priority

When numbers could match multiple countries, the webhook uses this priority:

1. **Exact pattern match** (most specific)
2. **Length + prefix combination**
3. **Regional defaults**

### Conflict Resolution:
- **8 digits starting with 3:** Bahrain (not Qatar)
- **8 digits starting with 5, 6:** Kuwait (not Qatar)
- **10 digits starting with 9:** India (not Philippines)
- **10 digits (no prefix):** United States

---

## 🧪 Testing Examples

### Middle East Tests

#### Egypt
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "01234567890"}'
```
Response: `EG, +20, ref: 53`

#### UAE
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "505237982"}'
```
Response: `AE, +971, ref: 183`

#### Saudi Arabia
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "0501234567"}'
```
Response: `SA, +966, ref: 151`

#### Kuwait
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "51234567"}'
```
Response: `KW, +965, ref: 92`

#### Bahrain
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "33123456"}'
```
Response: `BH, +973, ref: 13`

#### Qatar
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "77123456"}'
```
Response: `QA, +974, ref: 141`

#### Jordan
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "0791234567"}'
```
Response: `JO, +962, ref: 86`

#### Turkey
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "05312345678"}'
```
Response: `TR, +90, ref: 178`

---

### Asia Tests

#### India
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9876543210"}'
```
Response: `IN, +91, ref: 77`

#### Pakistan
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "3001234567"}'
```
Response: `PK, +92, ref: 131`

#### Philippines
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9171234567"}'
```
Response: `PH, +63, ref: 138`

#### Nepal
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9841234567"}'
```
Response: `NP, +977, ref: 123`

---

### Europe & Americas Tests

#### United Kingdom
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "07123456789"}'
```
Response: `GB, +44, ref: 184`

#### United States
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "4155552671"}'
```
Response: `US, +1, ref: 185`

---

## 📱 Real Examples from Your Facebook Leads

Based on actual data from your CSV:

#### Turkey - "0531 349 46 25"
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "05313494625"}'
```

#### UAE - "585524744"
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "585524744"}'
```

#### Nepal - "9779807436843" (includes country code)
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9779807436843"}'
```

#### Philippines - "639260423673" (includes country code)
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "639260423673"}'
```

#### Pakistan - "509814894"
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "509814894"}'
```

#### India - "585356369"
```bash
curl -X POST https://phone-parser-webhook.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "585356369"}'
```

---

## 🔧 Response Format

All responses follow this format:

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

---

## 📊 Complete Country Reference Table

| Country | Code | Local Format | Reference |
|---------|------|--------------|-----------|
| 🇪🇬 Egypt | +20 | 010XXXXXXXX | 53 |
| 🇦🇪 UAE | +971 | 5XXXXXXXX | 183 |
| 🇸🇦 Saudi Arabia | +966 | 05XXXXXXXX | 151 |
| 🇰🇼 Kuwait | +965 | 5XXXXXXX | 92 |
| 🇧🇭 Bahrain | +973 | 3XXXXXXX | 13 |
| 🇶🇦 Qatar | +974 | 7XXXXXXX | 141 |
| 🇯🇴 Jordan | +962 | 07XXXXXXXX | 86 |
| 🇹🇷 Turkey | +90 | 05XXXXXXXXX | 178 |
| 🇮🇳 India | +91 | 9XXXXXXXXX | 77 |
| 🇵🇰 Pakistan | +92 | 3XXXXXXXXX | 131 |
| 🇵🇭 Philippines | +63 | 9XXXXXXXXX | 138 |
| 🇳🇵 Nepal | +977 | 98XXXXXXXX | 123 |
| 🇬🇧 UK | +44 | 07XXXXXXXXX | 184 |
| 🇺🇸 USA | +1 | 10 digits | 185 |
| 🇨🇦 Canada | +1 | 10 digits | 32 |

---

## 💡 Facebook Lead Ads Integration

The webhook automatically handles all these formats from Facebook:

✅ **With country code:** `+971505237982`, `639260423673`
✅ **Without country code:** `505237982`, `9260423673`
✅ **With spaces:** `0531 349 46 25`
✅ **With dashes:** `050-123-4567`

**No configuration needed in Zapier!** Just map the phone field:

```json
{
  "phone_number": "{{phone}}"
}
```

The webhook handles the rest automatically!

---

## ⚠️ Important Notes

1. **Leading Zeros:** Egyptian and some other countries preserve leading zeros
2. **US vs Canada:** Both use +1, distinguished by area codes (if needed)
3. **Auto-Detection:** Only works for numbers WITHOUT `+` prefix
4. **Fallback:** Numbers with country codes are parsed directly

---

## 🎯 Common Use Cases

### Zapier → Google Sheets
```
Meta Lead → Webhook → Google Sheets

Result in Sheet:
| Name | Phone | Country | Code | Reference |
| John | 505237982 | UAE | 971 | 183 |
```

### Zapier → CRM (Salesforce, HubSpot)
```
Meta Lead → Webhook → CRM

Automatically populate:
- Phone: local_number
- Country: country_name
- Country Code: country_code
- Emersys ID: country_reference
```

---

## 🚀 Adding More Countries

To add a new country, edit the `detect_country_from_local_number` function in `phone_webhook.py`.

Example for Morocco (10 digits, starts with 06 or 07):

```python
# Morocco (MA)
if length == 10 and clean_number.startswith(('06', '07')):
    return 'MA'
```

Then deploy and test!
