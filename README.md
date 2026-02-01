# Phone Number Parser Webhook - Cloud Deployment

A Flask webhook application that parses phone numbers and returns local number, country code, and country name. **Optimized for Zapier integration with Meta Lead Ads.**

## 🚀 Quick Deploy to Cloud (FREE)

**Important:** Make sure to upload the `countries_reference.csv` file along with the other files when deploying!

### Option 1: Deploy to Render (Recommended - Free Tier)

1. **Create a GitHub repository:**
   - Go to GitHub and create a new repository
   - Upload all the files from this project

2. **Deploy on Render:**
   - Go to [Render.com](https://render.com) and sign up (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the configuration
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Copy your webhook URL: `https://your-app-name.onrender.com`

### Option 2: Deploy to Railway (Alternative - Free Tier)

1. **Create a GitHub repository** (same as above)

2. **Deploy on Railway:**
   - Go to [Railway.app](https://railway.app) and sign up
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-deploy
   - Copy your webhook URL from the deployment

### Option 3: Deploy to Heroku

1. Install Heroku CLI and login
2. Run these commands:
```bash
heroku create your-app-name
git push heroku main
```

## 📱 Zapier Integration Setup

### Step 1: Set Up Your Zap

1. **Trigger:** Meta Lead Ads (or any trigger that captures phone numbers)
   - Connect your Facebook account
   - Select your Lead Ad form
   - Test the trigger to get sample data

2. **Action:** Webhooks by Zapier
   - Choose "POST" request
   - URL: `https://your-app-name.onrender.com/parse-phone`
   - Payload Type: JSON
   - Data:
     ```json
     {
       "phone_number": "{{phone_number_field}}"
     }
     ```
   - Headers:
     - `Content-Type`: `application/json`

3. **Map the Response:**
   - Zapier will automatically parse the JSON response
   - You can access:
     - `data__local_number`
     - `data__country_code`
     - `data__country_name`
     - `data__country_reference` (Emersys reference ID)

### Step 2: Use Parsed Data in Next Steps

After the webhook action, you can use the parsed phone data in:
- Google Sheets (add to spreadsheet)
- CRM (Salesforce, HubSpot, etc.)
- Email notifications
- SMS services
- Any other Zapier action

### Example Zapier Flow

```
Meta Lead Ads (Trigger)
    ↓
Webhooks - POST to Phone Parser
    ↓
Google Sheets - Add Row
    - Name: {{Lead Name}}
    - Phone: {{data__local_number}}
    - Country Code: {{data__country_code}}
    - Country: {{data__country_name}}
    - Country Ref: {{data__country_reference}}
```

## 🧪 Testing Your Webhook

### Test with cURL:
```bash
curl -X POST https://your-app-name.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+14155552671"}'
```

### Test in Zapier:
1. In your Zap, click "Test action"
2. Use a sample phone number from your Meta Lead
3. Verify the response shows correct data

### Expected Response:
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

## 📋 API Endpoints

### POST /parse-phone

Parse a phone number and get its details.

**Request:**
```json
{
    "phone_number": "+14155552671"
}
```

**Response (Success):**
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

**Response (Error):**
```json
{
    "success": false,
    "error": "Invalid phone number: ..."
}
```

### GET /health

Health check endpoint to verify your service is running.

**Response:**
```json
{
    "status": "healthy"
}
```

## 🌍 Supported Phone Number Formats

- International format with +: `+14155552671` ✅ (Recommended)
- International format without +: `14155552671` ✅
- Any valid international phone number with country code

**Note:** For best results, ensure Meta Lead Ads collects phone numbers with country codes.

## 🔧 Local Development

If you want to test locally before deploying:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python phone_webhook.py
```

3. Test with ngrok (to expose local server to Zapier):
```bash
ngrok http 5000
```
Use the ngrok URL in Zapier for testing.

## 📝 Common Phone Number Examples

| Country | Example | Output Country Name |
|---------|---------|-------------------|
| USA | +14155552671 | United States |
| Egypt | +201234567890 | Egypt |
| UK | +442071838750 | United Kingdom |
| UAE | +971501234567 | United Arab Emirates |
| Saudi Arabia | +966501234567 | Saudi Arabia |

## ⚠️ Troubleshooting

### Issue: "Missing phone_number in request body"
- Make sure you're sending JSON data
- Check that the field is named exactly `phone_number`
- In Zapier, verify you've mapped the correct field from Meta Lead Ads

### Issue: "Invalid phone number"
- Ensure the phone number includes the country code
- Check the phone number format in Meta Lead Ads
- Test with a known valid number first

### Issue: Webhook times out
- Check if your deployment is still running (free tiers may sleep)
- Visit the `/health` endpoint to wake it up
- Consider upgrading to a paid tier for always-on service

## 💡 Pro Tips for Zapier

1. **Add a Filter:** Filter out invalid phone numbers before calling the webhook
2. **Error Handling:** Add a "Paths by Zapier" step to handle failed parses
3. **Formatter:** Use Zapier's Formatter to clean phone numbers before parsing
4. **Test Mode:** Always test your Zap thoroughly before turning it on

## 🆓 Free Tier Limitations

- **Render:** 750 hours/month (always-on), sleeps after 15 min inactivity
- **Railway:** 500 hours/month, $5 free credit monthly
- **Heroku:** No longer offers free tier

**Recommendation:** Use Render for the most generous free tier.

## 📞 Support

If you encounter issues:
1. Check the deployment logs in your hosting platform
2. Test the `/health` endpoint
3. Verify the phone number format
4. Check Zapier's error logs in the Zap history

## 🔒 Security Notes

- This webhook is open and doesn't require authentication
- For production use with sensitive data, consider adding API key authentication
- Monitor your usage to stay within free tier limits
