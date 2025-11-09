import streamlit as st
import requests
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Configuration
N8N_WEBHOOK_URL = "https://cleen8n.app.n8n.cloud/webhook/11301772-8470-440f-9e1f-0c4838f77ec9/chat"

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "otp" not in st.session_state:
    st.session_state.otp = None
if "otp_email" not in st.session_state:
    st.session_state.otp_email = None
if "otp_timestamp" not in st.session_state:
    st.session_state.otp_timestamp = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# OTP Configuration
OTP_VALIDITY_MINUTES = 10

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    """
    Send OTP via email using SMTP
    Note: You need to configure your SMTP settings in Streamlit secrets
    """
    try:
        # Get email configuration from secrets
        smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = st.secrets.get("SMTP_PORT", 587)
        sender_email = st.secrets.get("SENDER_EMAIL")
        sender_password = st.secrets.get("SENDER_PASSWORD")

        if not sender_email or not sender_password:
            st.error("Email configuration not found. Please add SMTP settings to secrets.")
            return False

        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your OTP Code"
        message["From"] = sender_email
        message["To"] = email

        # Email body
        text = f"""
        Your OTP code is: {otp}

        This code will expire in {OTP_VALIDITY_MINUTES} minutes.

        If you didn't request this code, please ignore this email.
        """

        html = f"""
        <html>
          <body>
            <h2>Your OTP Code</h2>
            <p>Your OTP code is: <strong style="font-size: 24px; color: #4CAF50;">{otp}</strong></p>
            <p>This code will expire in {OTP_VALIDITY_MINUTES} minutes.</p>
            <p>If you didn't request this code, please ignore this email.</p>
          </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())

        return True
    except Exception as e:
        st.error(f"Failed to send OTP: {str(e)}")
        return False

def verify_otp(entered_otp):
    """Verify the entered OTP"""
    if st.session_state.otp is None:
        return False

    # Check if OTP has expired
    if st.session_state.otp_timestamp:
        elapsed_time = time.time() - st.session_state.otp_timestamp
        if elapsed_time > (OTP_VALIDITY_MINUTES * 60):
            st.error("OTP has expired. Please request a new one.")
            return False

    return entered_otp == st.session_state.otp

def send_message_to_n8n(message):
    """Send message to n8n webhook and get response"""
    try:
        payload = {
            "message": message,
            "user_email": st.session_state.otp_email
        }

        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)

        if response.status_code == 200:
            response_data = response.json()
            # Try different possible response formats from n8n
            if isinstance(response_data, dict):
                return response_data.get("response") or response_data.get("output") or response_data.get("message") or str(response_data)
            else:
                return str(response_data)
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"

def login_page():
    """Display the login page with OTP authentication"""
    st.title("🔐 Login with OTP")
    st.write("Enter your email to receive a One-Time Password (OTP)")

    # Email input
    email = st.text_input("Email Address", placeholder="your.email@example.com")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Send OTP", type="primary", use_container_width=True):
            if email:
                if "@" in email and "." in email:
                    # Generate and store OTP
                    otp = generate_otp()
                    st.session_state.otp = otp
                    st.session_state.otp_email = email
                    st.session_state.otp_timestamp = time.time()

                    # Send OTP via email
                    with st.spinner("Sending OTP..."):
                        if send_otp_email(email, otp):
                            st.success(f"OTP sent to {email}! Check your inbox.")
                        else:
                            # Fallback: display OTP on screen (for testing)
                            st.warning("Email sending failed. For testing, your OTP is:")
                            st.code(otp)
                else:
                    st.error("Please enter a valid email address")
            else:
                st.error("Please enter your email address")

    # OTP verification section
    if st.session_state.otp is not None:
        st.markdown("---")
        st.subheader("Enter OTP")

        otp_input = st.text_input(
            "6-digit OTP", 
            max_chars=6, 
            placeholder="Enter the OTP sent to your email",
            type="password"
        )

        with col2:
            if st.button("Verify OTP", type="primary", use_container_width=True):
                if otp_input:
                    if verify_otp(otp_input):
                        st.session_state.authenticated = True
                        st.success("✅ Authentication successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid or expired OTP. Please try again.")
                else:
                    st.error("Please enter the OTP")

def chat_page():
    """Display the chat interface"""
    st.title("💬 Chat Interface")
    st.write(f"Logged in as: {st.session_state.otp_email}")

    # Logout button
    if st.button("Logout", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.otp = None
        st.session_state.otp_email = None
        st.session_state.otp_timestamp = None
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from n8n
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message_to_n8n(prompt)
                st.markdown(response)

        # Add assistant message to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    """Main application logic"""
    st.set_page_config(
        page_title="Chat App with OTP",
        page_icon="💬",
        layout="centered"
    )

    # Add custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Route to appropriate page based on authentication
    if st.session_state.authenticated:
        chat_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
