"""mailer microservice"""
import os
import pika
import json
from typing import TypedDict
from enum import Enum


import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


# Load SendinBlue API key from environment variables
SENDINBLUE_API_KEY = os.environ["SENDINBLUE_API_KEY"]
try:
    RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
    RABBITMQ_PORT = int(os.environ["RABBITMQ_PORT"])
except KeyError:
    RABBITMQ_HOST = "localhost"
    RABBITMQ_PORT = 5672


# AMQP connection to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
# Create a SendinBlue API configuration
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = SENDINBLUE_API_KEY

# Initialize the SendinBlue API instance
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration))


# Define the email sender function
class MessageEnum (Enum):
    """enum for message type"""
    WELCOME_EMAIL = "WELCOME_EMAIL"
    CONTENT_WARNING = "CONTENT_WARNING"


class MessageBody(TypedDict):
    """typed dictionary for rabbitmq message body"""
    message_type: MessageEnum
    email: str
    username: str


def send_email(subject, html_content, to_address, receiver_name="User"):
    """Sends email to user"""
    sender = {"name": "ESD-Twitter", "email": "ESD-Twitter@gmail.com"}
    to = [{"email": to_address, "name": receiver_name}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content, sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        return True
    except ApiException as e:
        print(e)
        return False


def send_welcome_email(email: str, username: str) -> None:
    """sends welcome email to new user"""
    subject = "Welcome to Yapper!"
    html_content = """
        <html>
            <body>
                <h1>Welcome to Yapper!</h1>
            <p>Thank you for joining our community. We're excited to have you on board.</p>
            <p>Yapper is a platform where you can share updates, connect with friends, and explore what's happening around the world in real-time.</p>
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
            <p>The Yapper Team</p>
            </body>
        </html>
    """
    try:
        send_email(subject, html_content, email, username)
    except Exception as e:
        print(e)


def send_content_removal_warning_email(email: str, username: str):
    """sends email to inform of content removal"""
    subject = "Notice: Content Removal and Warning"
    html_content = f"""
        <html>
            <body>
                <h1>Content Removal Notification</h1>
                <p>Dear {username},</p>
                <p>We regret to inform you that your recent post has been removed from our platform due to its violation of our community standards. We understand this may be disappointing, but it's important to us to maintain a safe and respectful environment for all users.</p>
                <p>We encourage you to review our content guidelines and terms of service. Repeat violations may lead to further actions, including account suspension. We value your participation in our community and hope you understand the importance of these policies.</p>
                <p>If you believe this was a mistake or if you have any questions, please don't hesitate to contact our support team.</p>
                <p>Best regards,</p>
                <p>The Yapper Team</p>
            </body>
        </html>
    """
    try:
        send_email(subject, html_content, email, username)
    except Exception as e:
        print(e)


def message_callback(ch, method, properties, body) -> None:
    """callback function message"""
    message_body: MessageBody = json.loads(body)
    email, username, message_type = message_body["email"], message_body["username"], message_body["message_type"]
    if message_type == MessageEnum.WELCOME_EMAIL.value:
        send_welcome_email(email, username)
    elif message_type == MessageEnum.CONTENT_WARNING.value:
        send_content_removal_warning_email(email, username)
    return None


if __name__ == "__main__":
    NOTIFICATION_QUEUE = "notification-queue"
    channel = connection.channel()
    channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)
    channel.basic_consume(queue=NOTIFICATION_QUEUE,
                          on_message_callback=message_callback, auto_ack=True)
    channel.start_consuming()
