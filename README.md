# Chat App with OTP Authentication

A Streamlit-based chat application with OTP (One-Time Password) authentication that integrates with n8n webhooks.

## Features

✅ **OTP Authentication**: Secure email-based OTP login system
✅ **Chat Interface**: Clean and intuitive chat UI
✅ **n8n Integration**: Backend powered by n8n webhook
✅ **Session Management**: Secure session handling
✅ **Email Notifications**: Automated OTP delivery

## Quick Start

### Prerequisites
- Python 3.9+
- Gmail account with App Password

### Setup

1. **Clone or download this repository**

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure secrets**
   - Create `.streamlit/secrets.toml`:
   ```toml
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = 587
   SENDER_EMAIL = "your.email@gmail.com"
   SENDER_PASSWORD = "your-app-password"
   ```

5. **Run locally**
   ```bash
   streamlit run streamlit_app.py
   ```

## Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create new app from repository
4. Add secrets in Advanced Settings
5. Deploy!

## Getting Gmail App Password

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Go to App passwords
4. Generate password for Mail
5. Copy and use in secrets.toml

## Project Structure

```
.
├── streamlit_app.py      # Main application
├── requirements.txt      # Python dependencies
├── .gitignore           # Git exclusions
└── README.md            # This file
```

## Troubleshooting

**Email not sending**: Check Gmail App Password and 2-Step Verification
**n8n webhook failing**: Verify webhook URL and n8n workflow is active
**Import errors**: Make sure all packages in requirements.txt are installed

## Support

- [Streamlit Docs](https://docs.streamlit.io)
- [n8n Docs](https://docs.n8n.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)

---

Built with ❤️ using Streamlit and n8n
