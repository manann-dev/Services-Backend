# PDF-LLM-Contract

This project offers a robust solution for extracting insights from PDF documents by integrating the power of ChatGPT with a PDF parsing Flask application. Designed to automate and enrich the analysis of PDF content, it facilitates text and image extraction and leverages OpenAI's GPT model for intelligent text completion and question-answering capabilities. Ideal for researchers, developers, and content analysts, this guide walks you through setting up a Python project that bridges cutting-edge AI with practical PDF parsing functionality.

## Features

- **ChatGPT Integration:** Utilize OpenAI's GPT model to generate accurate and context-aware text completions. This feature allows for dynamic question-answering sessions based on the content extracted from PDF documents, enabling a deeper interaction with the material.

- **PDF Parser API:** Our Flask application acts as a powerful PDF parser, capable of extracting both text and images from documents. This API is designed for ease of use and integration, offering a straightforward way for applications to process and analyze PDF content programmatically.

## Prerequisites

Before diving into the setup, make sure you have the following:

- **Python 3.6 or higher:** The project is developed with Python's modern features and syntax in mind. Ensure you have a compatible version installed on your system. You can check your Python version by running `python --version` in your terminal.
- **An active OpenAI API key:** Essential for integrating ChatGPT's capabilities into the project. If you don't have one, visit [OpenAI's API documentation](https://openai.com/api/) to sign up and obtain your key.

## Installation

Setting up the project environment is straightforward. Follow these steps:

1. **Get the Project:** Clone this repository to your local machine or download the project files directly. If you're using Git, you can clone the repository with `git clone <repository-url>`.

2. **Navigate to Project Directory:** Open a terminal or command prompt, and change into the project directory using `cd path/to/project`.

3. **Create a Virtual Environment:** Isolate your project dependencies by creating a virtual environment. Run `python -m venv venv` to create an environment named `venv`.

4. **Activate the Virtual Environment:**
   - For **Windows**, use `.\\venv\\Scripts\\activate`.
   - For **Unix or MacOS**, use `source venv/bin/activate`.

5. **Install Dependencies:** Install all required packages with `pip install -r requirements.txt`. This ensures your project has all the necessary Python libraries.

## Configuration

Properly configuring your project is crucial for its functionality. Follow these steps:

1. **OpenAI API Key:** Your OpenAI API key enables communication with ChatGPT. Set it as an environment variable for secure access:
   - For **Windows**, run `set OPENAI_API_KEY=your_openai_api_key` in your terminal.
   - For **Unix or MacOS**, use `export OPENAI_API_KEY=your_openai_api_key`.
   Replace `your_openai_api_key` with the actual key you obtained from OpenAI.

export OPENAI_API_KEY=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
export CONFIG_FILE=./config.yml

2. **Edit `config.yml`:** This file contains settings for the ChatGPT model, including which model to use, the maximum number of tokens for responses, and the questions you wish to ask. Customize it to fit your project's needs. Here's an example with comments for guidance:
   ```yaml
   max_tokens: 50              # Set the maximum response length
   prompt:                     # Customize the prompt settings
      task: "Answer the following questions..."
      detail: Low
      format: Listed with bullets
   questions:                  # List your questions here
     - "What is the meaning of life?"
     - "Tell me about artificial intelligence."
   ```

Note: `model` is no longer defined in config.

3. **Set the `CONFIG_FILE` environment variable:**
   Similar to step 1.
 
## Running the Application

To run the Flask application for PDF parsing:

```bash
python pdfParse.py
```

This will start the development server on `http://127.0.0.1:5000/`.

### API Docks
You can visit the localhost on port 5000 (or 8000 with docker) to see the documentation.

### Using the PDF Parser API

- **Parse a PDF:**
  Send a POST request to `http://127.0.0.1:5000/pdf_parse/parsePDF` with the PDF file under the key `file`.
- **Example `curl` Command:**
  ```bash
  curl -F "file=@path_to_your_pdf_file.pdf" http://127.0.0.1:5000/pdf_parse/parsePDF
  ```
  Replace `path_to_your_pdf_file.pdf` with the actual path to your PDF file.

### Using ChatGPT to Answer Questions Using a PDF

To use ChatGPT with background information, supply a PDF similar to parsing it with this endpoint
  ```bash
  curl -F "file=@path_to_your_pdf_file.pdf" http://127.0.0.1:5000/pdf_parse/askQuestionsAboutPDF
  ```

ChatGPT will answer your questions and use the background knowledge.

TODO: Use Images for background knowledge as well. Currently, ChatGPT-4 requires you to spend $1 on the account.


## Fine-Tuning a model

https://platform.openai.com/docs/guides/fine-tuning

### Generating your Dataset

To fine-tune a model, first you need a dataset. In scripts folder, there are three ways to generate a dataset.
The datasets look like
```
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already."}]}
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who wrote 'Romeo and Juliet'?"}, {"role": "assistant", "content": "Oh, just some guy named William Shakespeare. Ever heard of him?"}]}
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "How far is the Moon from Earth?"}, {"role": "assistant", "content": "Around 384,400 kilometers. Give or take a few, like that really matters."}]}
```

We add an extra message called system which tells the bot how to behave. That is always asked first.

Firstly, you can generate a simple one to teach your model how to be sarcastic or answer things a certain way.
This can be accomplished with
```python3 generate_finetuning_file.py -S/--split validation-split-percentage```

You can either pipe in a conversation from stdin or run the program and be given prompts. You can make as many prompts as you'd like. OpenAI recommends 50-100 to finetune a model. 10 is the minimum.
NOTE: if using stdin, the first message will be the system message.

You can also specif percentage to go into validation set to see if your model is getting better. 
We recommend this for any type of training to do arouns 20%.

Secondly, you can help your model learn how to read pitches or other PDFs based on questions in `config/config.yml`. 
```python3 generate_finetuning_background.py -t/--target file-to-save-to -e/--endpoint http://localhost:8000 -f folder-with-pdfs -S/--split validation-split-percentage```
will read PDFs, provide you the background information and then ask the questions to you for you to provide answers for.
This will help the model learn how to write and answer questions about the PDF.

Similarly, you can use 
```python3 generate_finetuning_from_app.py```
and it will take a folder with pairs of slides and apps.
Ensure the slides and apps follow the following pattern:
```text company-slides.pdf company-app.pdf```
otherwise the script will ignore them.
You will recieve a large training set based on the question and the answers in the application you can then use to train.

To use the model you finetuned, you can use the endpoint `/training/retrieveJob/<job_id>` to get the job. If the job finished, the model will be displayed.
You can then query it like normal. It will not appear if it is not finished.

## Docker

### Docker Setup

Ensure you have installed docker and have a docker daemon running.

1. **Build the Docker Image:**
   Navigate to the project root directory where the `Dockerfile` is located and run:
   ```bash
   docker build -t pdf-llm-contract .
   ```
   This command builds a Docker image named `pdf-llm-contract` based on the instructions in your `Dockerfile`.

2. **Run the Application with Docker Compose:**
   Once the image is built, you can use `docker-compose` to run your application. Make sure you have `docker-compose.yml` configured with the necessary services.
   ```bash
   docker-compose up
   ```
   This command starts all services defined in your `docker-compose.yml`. It includes your Flask application and any other services you've defined (like databases or cache services).

NOTE: In the docker-compose file, the new port to communicate with the flask app is 8000.
Make sure you put your envrionment variables.

## Configuration

Ensure you configure your application properly by setting environment variables and adjusting settings in the `config.yml` file as detailed in the local environment setup section.

## Running the Application

- **With Docker:** If you've set up your application with Docker, simply use `docker-compose up` to start your application. The services will be accessible based on the configuration in your `docker-compose.yml` file.
- **Locally:** To run the Flask application locally, execute `python pdfParse.py` as mentioned previously.

