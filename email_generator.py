import openai

openai.api_key = 'YOUR_KEY'

def generate_personalized_email(email_summaries):
    """
    Gets the response based on the summaries of previous conversations using OpenAI.

    Args:
      email_summaries: The summaries of all the conversations as a Dictionary.

    Returns:
      The response to the email.
    """


    prompt = "Here are summaries of all email conversations in the thread:\n\n" + "\n".join(email_summaries) + "\n\nPlease generate a comprehensive response based on these summaries."

    response = openai.completions.create(
        model="text-davinci-003",
        prompt= prompt,
        max_tokens=1024,
        temperature = 0.7
    )
    return response.choices[0].text.strip()

def get_email_summary(email_content):
    """
    Gets the summary of an email using OpenAI.

    Args:
      email_content: The content of the email as a string.

    Returns:
      The summary of the email as a string.
    """
    response = openai.completions.create(
        model="text-davinci-003",
        prompt=f"Summarize the email. Also, specify the names of the individuals involved in the conversation.: {email_content}",
        temperature=0.5,
        max_tokens=512
    )
    return response.choices[0].text.strip()