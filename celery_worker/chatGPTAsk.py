from openai import OpenAI
import os
import sys



from config import client, config

from celery import Celery


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task()
def ask_gpt_for_image_description(images, max_tokens):
    content = [ {"type": "text", "text": "What are in these images? Please describe them succinctly."} ]

    for image in images:
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}})
    
    response = client.chat.completions.create(
        model='gpt-4-vision-preview',
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()
    
# Function to generate the background information
@celery.task()
def generate_background_info(content_list, max_tokens, images_enabled=False):
    background = []
    images = []
    for item in content_list:
        if item['type'] == 'text' or item['type'] == 'ocr_text':
            background.append(item['data'])
        elif item['type'] == 'image':
            images.append(item['image_data'])
    
    if images_enabled and images:
        background.append(ask_gpt_for_image_description(images, max_tokens))

    return '\n'.join(background)

# Function to generate the prompt
@celery.task()
def generate_prompt(prompt_config, background_information):
    background_information = background_information.strip()
    task = prompt_config.get("task", "Answer the questions in the order the questions are presented using supplied background.")
    detail = prompt_config.get("detail", "high")
    format_instructions = prompt_config.get("format", "listed")
    
    system_prompt = f"Background Information: {background_information}\n\nTask: {task}\nDetail Level: {detail}\nFormat: {format_instructions}"
    return system_prompt

# Function to interact with ChatGPT
@celery.task()
def chat_with_gpt(client, model_name, max_tokens, questions, prompt_config, background_information=""):
    system_prompt = generate_prompt(prompt_config, background_information)
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": questions},
        ],
        max_tokens=max_tokens,  # Adjust as needed
    )
    return response.choices[0].message.content.strip()

# Reads the config and interact with ChatGPT
@celery.task()
def ask_questions(model_name, content_list, images_enabled):
    questions = '\n'.join(map(lambda item: item, config.get("questions", []))) # Joins the questions into a single string
    max_tokens = config.get("max_tokens", 100) # Max tokens to generate
    
    background_information = generate_background_info(content_list, max_tokens, True)

    prompt_config = config.get("prompt", {})

    if not prompt_config or not questions:
        print("No prompt or questions found in the config.")
        return
    
    answer = chat_with_gpt(client, model_name, max_tokens, questions, prompt_config, background_information)
    return answer
