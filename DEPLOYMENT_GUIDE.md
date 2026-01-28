# Quick Start Guide: Deploy & Connect to Zapier

## 🎯 Goal
Deploy your phone parser webhook to the cloud and connect it to Zapier to process Meta Lead Ads phone numbers.

---

## Step 1: Deploy to Render (5 minutes)

### A. Prepare Your Files
1. Create a new folder on your computer
2. Save all the project files in this folder:
   - `phone_webhook.py`
   - `requirements.txt`
   - `Procfile`
   - `render.yaml`
   - `runtime.txt`

### B. Upload to GitHub
1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon → "New repository"
3. Name it: `phone-parser-webhook`
4. Click "Create repository"
5. Follow the instructions to upload your files:
   - Click "uploading an existing file"
   - Drag and drop all your files
   - Click "Commit changes"

### C. Deploy on Render
1. Go to [Render.com](https://render.com)
2. Sign up with your GitHub account (free)
3. Click "New +" → "Web Service"
4. Click "Connect" next to your `phone-parser-webhook` repository
5. Fill in:
   - **Name:** `phone-parser` (or any name you like)
   - **Environment:** Python
   - Leave everything else as default
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment
8. **Copy your URL:** It will look like `https://phone-parser-xxxx.onrender.com`

✅ **Your webhook is now live!**

---

## Step 2: Test Your Webhook (2 minutes)

Open your terminal or command prompt and run:

```bash
curl -X POST https://your-app-name.onrender.com/parse-phone \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+14155552671"}'
```

Replace `your-app-name` with your actual Render URL.

**Expected Response:**
```json
{
    "success": true,
    "data": {
        "local_number": "4155552671",
        "country_code": "1",
        "country_name": "United States"
    }
}
```

✅ **If you see this, your webhook is working!**

---

## Step 3: Connect to Zapier (5 minutes)

### A. Create Your Zap
1. Go to [Zapier.com](https://zapier.com) and log in
2. Click "Create Zap"

### B. Set Up Trigger
1. **Choose App:** Facebook Lead Ads
2. **Event:** New Lead
3. Click "Continue"
4. **Connect your Facebook account**
5. Select your **Ad Account** and **Form**
6. Click "Test trigger" to get sample data
7. Click "Continue"

### C. Add Webhook Action
1. Click "+" to add an action
2. **Choose App:** Webhooks by Zapier
3. **Event:** POST
4. Click "Continue"
5. Fill in the details:

   **URL:** `https://your-app-name.onrender.com/parse-phone`
   
   **Payload Type:** json
   
   **Data:**
   - Click "+" to add a field
   - Key: `phone_number`
   - Value: Click the field and select the phone number field from your Meta Lead (e.g., "Phone Number")

   **Headers:**
   - Click "Show Options"
   - Add header:
     - Key: `Content-Type`
     - Value: `application/json`

6. Click "Continue"
7. Click "Test action"

**You should see a successful response with:**
- `data__local_number`
- `data__country_code`
- `data__country_name`

✅ **Your webhook is connected to Zapier!**

### D. Use the Parsed Data
1. Click "+" to add another action
2. Choose where to send the data (examples):
   - **Google Sheets:** Add row with parsed phone data
   - **CRM:** Create/update contact
   - **Email:** Send notification with formatted data

3. Map the fields:
   - Use `data__local_number` for the phone number
   - Use `data__country_code` for country code
   - Use `data__country_name` for country name

4. Click "Test action"
5. Click "Publish" to turn on your Zap

---

## 🎉 You're Done!

Now every time someone submits a Meta Lead Ad:
1. Zapier captures the lead
2. Sends the phone number to your webhook
3. Gets back the parsed data (local number, country code, country name)
4. Sends it to your destination (Google Sheets, CRM, etc.)

---

## Example Zapier Flow

```
📱 Meta Lead Ads
    ↓ (Phone: +14155552671)
    
🔗 Webhooks - POST to your webhook
    ↓ 
    Response:
    - Local: 4155552671
    - Code: 1
    - Country: United States
    
📊 Google Sheets - Add New Row
    | Name | Phone | Country Code | Country |
    | John | 4155552671 | 1 | United States |
```

---

## ⚠️ Important Notes

### Free Tier Sleep Mode
Render free tier services sleep after 15 minutes of inactivity. First request may take 30-60 seconds to wake up.

**Solutions:**
1. Use a service like [Uptime Robot](https://uptimerobot.com) to ping your webhook every 5 minutes
2. In Zapier, add a slight delay (1-2 minutes) if the first attempt fails
3. Upgrade to Render's paid plan ($7/month) for always-on service

### Phone Number Format
Make sure your Meta Lead Ads form collects phone numbers with country codes. You can:
1. Add instructions in your form: "Please include country code (e.g., +1 for US)"
2. Use Zapier's Formatter to add a default country code before sending to webhook
3. Add validation in your Meta form

---

## 🆘 Troubleshooting

**Issue:** "Could not connect to webhook"
- Check that your Render service is running (visit the dashboard)
- Visit your webhook URL in a browser to wake it up
- Check the Render logs for errors

**Issue:** "Invalid phone number"
- Test with a valid phone number including country code
- Check the phone field mapping in Zapier
- Use Zapier's Formatter to clean the phone number first

**Issue:** Webhook is slow
- Free tier sleeps after inactivity (first request takes longer)
- Consider using Uptime Robot to keep it awake
- Or upgrade to paid tier

---

## 📞 Need Help?

1. Check Render logs: Go to your service dashboard → Logs
2. Check Zapier task history: Zap → History → View details
3. Test your webhook directly with cURL (see Step 2)
4. Verify your phone number includes country code

---

## 🚀 Next Steps

Once everything is working:
1. Monitor your Zap runs in Zapier dashboard
2. Add filters to handle specific countries differently
3. Add error handling paths in Zapier
4. Consider adding authentication to your webhook for security
