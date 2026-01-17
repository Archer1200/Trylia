# 📧 Quick Email Setup for Trylia Contact Form

## 🎉 **Good News: Your Form is Working!**

The message "Email notification temporarily unavailable" means your contact form is working perfectly, but email notifications aren't configured yet.

## 🚀 **Quick Setup (5 minutes)**

### **Option A: Use Gmail (Recommended)**

#### Step 1: Enable 2-Factor Authentication
1. Go to: https://myaccount.google.com/security
2. Turn on **2-Step Verification**

#### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select **"Mail"** and click **Generate**
3. Copy the **16-character password** (like: `abcd efgh ijkl mnop`)

#### Step 3: Update Email Configuration
Edit `backend/.env` file:
```env
# Replace with your actual details
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-actual-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
FROM_EMAIL=noreply@trylia.com
TO_EMAIL=your-business-email@gmail.com
```

#### Step 4: Restart Backend
```bash
cd backend
# Stop current server (Ctrl+C)
start_server_safe.bat
```

### **Option B: Use Other Email Providers**

#### Outlook/Hotmail:
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
```

#### Yahoo Mail:
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

## 🧪 **Test Email Setup**

After configuration:
```bash
cd backend
python test_contact_form.py
```

**Success looks like:**
```
✅ Contact form submitted successfully!
📧 Email sent: True
📬 Confirmation sent: True
💬 Message: Thank you for your inquiry! We will get back to you within 24 hours.
```

## 🚨 **Troubleshooting**

### "Username and Password not accepted"
- ✅ Use **App Password**, not regular password
- ✅ Enable **2-factor authentication** first
- ✅ Check email address is complete

### "Connection refused"
- ✅ Check firewall settings
- ✅ Try different email provider
- ✅ Verify SMTP server and port

## 💡 **Pro Tips**

1. **Create dedicated email** for Trylia notifications
2. **Test with personal email first** before using business email
3. **Keep App Password secure** - treat it like a password
4. **Monitor server logs** for email status

## 🎯 **What Happens After Setup**

Once configured, when someone submits the contact form:

1. **Form submission** ✅ (already working)
2. **Email to you** with all form details 📧
3. **Confirmation email** to the customer 📬
4. **Success message** changes to: "Thank you for your inquiry! We will get back to you within 24 hours."

## 🔧 **Need Help?**

Run the setup wizard:
```bash
cd backend
setup_email.bat
```

This will guide you through the process step by step.

---

**Remember:** Your contact form is already working perfectly! Email is just an enhancement for notifications. You can see all form submissions in the server console logs.