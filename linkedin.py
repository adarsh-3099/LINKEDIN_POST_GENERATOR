#set GROQ_API_KEY in the secrets
import os
from groq import Groq
import re, requests
from bs4 import BeautifulSoup

def get_page_content(medium_url):
    response = requests.get(medium_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    text = '\n'.join(line.strip() for line in text.split('\n'))
    text = '\n'.join(line for line in text.split('\n') if line)
    return text

def get_title_description(medium_url):
    # def extract_title_and_description(input_text):
    #     title_pattern = r"Title:(.+?)(?=Description:)"
    #     description_pattern = r"Description:(.+)"
    #     title_match = re.search(title_pattern, input_text, re.DOTALL)
    #     description_match = re.search(description_pattern, input_text, re.DOTALL)
    #     if title_match and description_match:
    #         title = title_match.group(1).strip()
    #         description = description_match.group(1).strip()
    #         return title, description
    #     else:
    #         return None, None
    x = get_page_content(medium_url)
    client = Groq(api_key="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")
    DEFAULT_SYSTEM_PROMPT = '''You are a content title and content generator. Your task is to create a captivating title and a concise long content for a given content. Provide one compelling title and a informative long content.
         response should be in this format. for example.
         Title: Title Content
         Content: Content
         Aim for creativity and clarity in your creations, ensuring that both the title and content are attention-grabbing, long and informative.'''
    system_prompt = {
        "role": "system",
        "content": DEFAULT_SYSTEM_PROMPT
    }
    chat_history = [system_prompt]
    chat_history.append({"role": "user", "content": "[" + x + "].Create one title and content of the content"})
    response = client.chat.completions.create(model="llama3-70b-8192",
                                            messages=chat_history,
                                            max_tokens=100,
                                            temperature=1.2)
    
    chat_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    # Print the response
    print("Assistant:", response.choices[0].message.content)

    
get_title_description("https://medium.com/@weidagang/zod-schema-validation-made-easy-195f86d82d44")

