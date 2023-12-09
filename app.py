from email_generator import generate_personalized_email
from email_reader import get_latest_email_content,get_gmail_service
import time


gmail_user = 'YOUR_EMAILID'
gmail_password = 'PASSWORD'

def generate_email():

    gmail_service = get_gmail_service()
    summary_conversations = get_latest_email_content(gmail_service)

    time.sleep(60)

    generated_reply = generate_personalized_email(summary_conversations)
    print(generated_reply)

if __name__ == '__main__':
    generate_email()