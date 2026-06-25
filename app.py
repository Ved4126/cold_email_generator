from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import anthropic
import smtplib
from email.mime.text import MIMEText
import os

load_dotenv()
app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

import fitz

def load_resume():
    doc = fitz.open("Resume_Ved_Dabhi.pdf")  
    text = ""
    for page in doc:              
        text += page.get_text()  
    return text

RESUME = load_resume() 


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name')
    role = request.form.get('role')
    company = request.form.get('company')
    extra = request.form.get('extra', '')

    # Read their LinkedIn PDF
    linkedin_file = request.files.get('linkedin_pdf')
    linkedin_text = ""
    if linkedin_file:
        doc = fitz.open(stream=linkedin_file.read(), filetype="pdf")
        for page in doc:
            linkedin_text += page.get_text()

    prompt = f"""You are a cold email expert helping a student find a summer internship.

Write a short, personalized cold email to {name}, who is a {role} at {company}.

Their LinkedIn profile:
{linkedin_text}

The sender's background (from their resume):
{RESUME}

Guidelines:
- The goal is to land a summer internship at their company
- Keep the email under 150 words
- Reference something specific from their LinkedIn profile
- Highlight 1-2 relevant skills or projects from the resume
- End with one clear ask — a 15 minute call or reply
- Friendly, human tone, not salesy

Return your response in this exact format:
Subject: <subject line here>
Body: <email body here>
"""
    
    message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}]
)

    email_body = message.content[0].text

    # Split subject and body
    lines = email_body.strip().split('\n')
    subject_line = ""
    body_lines = []
    for line in lines:
        if line.startswith("Subject:"):
            subject_line = line.replace("Subject:", "").strip()
        elif line.startswith("Body:"):
            continue
        else:
            body_lines.append(line)

    body_text = "\n".join(body_lines).strip()

    return jsonify({"email": body_text, "subject": subject_line})


@app.route('/send', methods=['POST'])
def send():
    data = request.json
    to_email = data.get('to_email')
    subject = data.get('subject')
    body = data.get('body')

    gmail = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = gmail
        msg['To'] = to_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail, password)
            server.sendmail(gmail, to_email, msg.as_string())

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    

if __name__ == '__main__':
        app.run(debug=True)