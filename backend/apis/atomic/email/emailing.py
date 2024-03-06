from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

import logging
from logging.handlers import RotatingFileHandler
import os

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


load_dotenv()

# Load SendinBlue API key from environment variables
sendinblue_api_key = os.getenv("SENDINBLUE_API_KEY")

# Create a SendinBlue API configuration
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = sendinblue_api_key

# Initialize the SendinBlue API instance
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

app = Flask(__name__)
CORS(app)

# Configure logging
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
log_handler = RotatingFileHandler('email_service.log', maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# Define the email sender function
def send_email(subject, html_content, to_address, receiver_name="User"):
    sender = {"name": "ESD-Twitter", "email": "ESD-Twitter@gmail.com"}
    to = [{"email": to_address, "name": receiver_name}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

    app.logger.info(f"Attempting to send email to {to_address} with subject '{subject}'")
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        app.logger.info(f"Email sent successfully: {api_response}")
        return True
    except ApiException as e:
        app.logger.error(f"Exception when calling SMTPApi->send_transac_email: {e}")
        return False

# Route for sending a welcome email to a new user
@app.route('/send_welcome_email', methods=['POST'])
def send_welcome_email():
    data = request.json
    if not data or 'email' not in data or 'username' not in data:
        app.logger.error("send_welcome_email: Missing email or username in the request data")
        return jsonify({"error": "Missing email or username in the request data"}), 400

    to_address = data.get('email')
    user_name = data.get('username')

    app.logger.info(f"Processing welcome email for {user_name} at {to_address}")

    subject = "Welcome to ESD-Twitter!"
    html_content = f"""
        <html>
            <body>
                <h1>Welcome to ESD-Twitter!</h1>
            <p>Thank you for joining our community. We're excited to have you on board.</p>
            <p>ESD-Twitter is a platform where you can share updates, connect with friends, and explore what's happening around the world in real-time.</p>
            <h2>Getting Started</h2>
            <p>Here are some steps to get you started:</p>
            <ul>
                <li>Complete your profile: Add a profile picture and a short bio about yourself.</li>
                <li>Find friends: Search for your friends and start following them to see their updates.</li>
                <li>Post your first tweet: Share what's on your mind or what's happening around you.</li>
            </ul>
            <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>
            <p>We're glad you're here!</p>
            <p>Best regards,</p>
            <p>The ESD-Twitter Team</p>
            </body>
        </html>
    """

    if send_email(subject, html_content, to_address, user_name):
        app.logger.info(f"Welcome email sent to {to_address}")
        return jsonify({"message": "Welcome email sent successfully!"}), 200
    else:
        app.logger.error(f"Failed to send welcome email to {to_address}")
        return jsonify({"error": "Failed to send email."}), 500

# Route for sending an account deletion confirmation email
@app.route('/send_account_deletion_email', methods=['POST'])
def send_account_deletion_email():
    data = request.get_json()
    to_address = data.get('email')
    user_name = data.get('username')
    subject = "Your ESD-Twitter Account Has Been Deleted"
    html_content = f"""
        <html>
            <body>
                <h1>Goodbye, {user_name}.</h1>
                <p>We're sorry to see you go. Your account has been successfully deleted.</p>
                <p>If this was a mistake or you have any questions, please contact our support team.</p>
                <p>Best regards,</p>
                <p>The ESD-Twitter Team</p>
            </body>
        </html>
    """

    if send_email(subject, html_content, to_address, user_name):
        return jsonify({"message": "Account deletion email sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send email."}), 500

# Route for sending a password reset email
@app.route('/send_password_reset_email', methods=['POST'])
def send_password_reset_email():
    data = request.get_json()
    to_address = data.get('email')
    user_name = data.get('username')
    # reset_link = data.get('reset_link')  # Assuming reset_link is provided in the request
    # <p>Please follow this link to reset your password: <a href="{reset_link}">{reset_link}</a></p> # Add this line to the email content if needed
    subject = "Reset Your ESD-Twitter Password"
    html_content = f"""
        <html>
            <body>
                <h1>Password Reset Request</h1>
                <p>Hi, {user_name}. You've requested to reset your password.</p>
                
                <p>If you did not request a password reset, please ignore this email or contact support.</p>
                <p>Best regards,</p>
                <p>The ESD-Twitter Team</p>
            </body>
        </html>
    """

    if send_email(subject, html_content, to_address, user_name):
        return jsonify({"message": "Password reset email sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send email."}), 500

# Route for notifying a user when they have successfully changed their password
@app.route('/send_password_changed_email', methods=['POST'])
def send_password_change_success_email():
    data = request.get_json()
    to_address = data.get('email')
    user_name = data.get('username')
    subject = "Your Password Has Been Changed Successfully"
    html_content = f"""
        <html>
            <body>
                <h1>Password Change Successful</h1>
                <p>Hi {user_name},</p>
                <p>We're confirming that you've successfully changed your password. If you did not initiate this change, please contact our support team immediately.</p>
                <p>Best regards,</p>
                <p>The ESD-Twitter Team</p>
            </body>
        </html>
    """

    if send_email(subject, html_content, to_address, user_name):
        return jsonify({"message": "Password change success email sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send email."}), 500

# Route for sending a content removal warning email
@app.route('/send_content_removal_warning_email', methods=['POST'])
def send_content_removal_warning_email():
    data = request.get_json()
    to_address = data.get('email')
    user_name = data.get('username')
    subject = "Notice: Content Removal and Warning"
    html_content = f"""
        <html>
            <body>
                <h1>Content Removal Notification</h1>
                <p>Dear {user_name},</p>
                <p>We regret to inform you that your recent post has been removed from our platform due to its violation of our community standards. We understand this may be disappointing, but it's important to us to maintain a safe and respectful environment for all users.</p>
                <p>We encourage you to review our content guidelines and terms of service. Repeat violations may lead to further actions, including account suspension. We value your participation in our community and hope you understand the importance of these policies.</p>
                <p>If you believe this was a mistake or if you have any questions, please don't hesitate to contact our support team.</p>
                <p>Best regards,</p>
                <p>The ESD-Twitter Team</p>
            </body>
        </html>
    """

    if send_email(subject, html_content, to_address, user_name):
        return jsonify({"message": "Content removal warning email sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send email."}), 500


# Additional routes for other notifications or email triggers can be added here

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5107, debug=True)
