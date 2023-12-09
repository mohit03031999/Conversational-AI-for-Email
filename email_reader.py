from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import re
import os
import base64
from email_generator import get_email_summary


email_summaries = {}


def remove_links(text):
    """
    Gets the content of the email after removing any hyperlinks.

    Args:
      text: The content of the email as a string.

    Returns:
      The text without any links into it.
    """
    return re.sub(r'<[^>]*>', '', text)


def remove_extra_spaces(text):
    """
    Gets the content of the email after removing extra spaces.

    Args:
      text: The content of the email as a string.

    Returns:
      The text after removing extra spaces.
    """
    return ' '.join(text.split())


def get_gmail_service():

    """
   Use for the authentication of Gmail API.

   Returns:
     The authenticated Gmail Service.
   """

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def get_subject(thread_messages):
    """
    Gets the subject of email.

    Args:
      text: The content of the email.

    Returns:
      The Subject of the email.
    """

    for email in thread_messages:
        for header in email["payload"]["headers"]:
            if header["name"] == "Subject":
                subject = header["value"]
                return subject


def get_latest_email_content(service):
    """
    Gets the summary of all the conversations as a Dictionary with key as Subject.

    Args:
      service: The authenticated Gmail service.

    Returns:
      The dictionary with key as "Subject" and value as summary of all the conversation under the subject.
    """

    user_id = 'me'
    response = service.users().messages().list(userId=user_id,
                                               q='in:inbox -category:{social promotions updates forums}',
                                               maxResults=1).execute()

    if 'messages' in response:
        message = response['messages'][0]
        thread_id = message['threadId']

        thread_messages = service.users().threads().get(userId=user_id, id=thread_id).execute()['messages']

        subject = get_subject(thread_messages)

        for email in thread_messages:
            for p in email["payload"]["parts"]:
                if p["mimeType"] in ["text/plain"]:
                    data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
                    text_only = remove_links(data)
                    final_string = remove_extra_spaces(text_only)

                    summary = get_email_summary(final_string)

                    if subject in email_summaries:
                        email_summaries[subject] += summary
                    else:
                        email_summaries[subject] = summary

    return email_summaries
