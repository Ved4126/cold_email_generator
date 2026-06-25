# Cold Email Generator

An AI-powered tool that helps students and job seekers write and send personalized cold emails for internship outreach.

## What it does

- You enter the person's name, role, and company
- You upload their LinkedIn profile as a PDF
- AI reads your resume + their LinkedIn profile
- Generates a short, personalized cold email
- Sends it directly from your Gmail with one click

## Tech Stack

- Python + Flask (backend)
- Claude AI by Anthropic (email generation)
- Gmail SMTP (email sending)
- PyMuPDF (PDF reading)
- HTML + CSS + JavaScript (frontend)

## Setup

1. Clone the repo
   
   git clone https://github.com/Ved4126/cold_email_generator.git
   cd cold_email_generator

2. Create a virtual environment and install dependencies
   
   python -m venv .venv
   source .venv/bin/activate
   pip install flask anthropic python-dotenv pymupdf

3. Add your resume PDF to the project folder and name it exactly as referenced in app.py

4. Create a .env file in the root folder
   
   ANTHROPIC_API_KEY=your-api-key-here
   GMAIL_ADDRESS=your-gmail@gmail.com
   GMAIL_APP_PASSWORD=your-app-password-here

5. Run the app
   
   python app.py

6. Open your browser and go to http://127.0.0.1:5000

## Getting your credentials

**Anthropic API key** — sign up at console.anthropic.com and create an API key

**Gmail App Password** — go to myaccount.google.com, search App Passwords, create one and paste it in .env

## How to download a LinkedIn profile as PDF

1. Go to the person's LinkedIn profile
2. Click More
3. Click Save to PDF
4. Upload that PDF in the app

## Project Structure

cold_email_generator/
├── app.py              — Flask backend + Claude API + Gmail
├── templates/
│   └── index.html      — Frontend UI
├── .env                — Secret keys (never uploaded to GitHub)
├── .gitignore          — Ignores .env and PDF files
└── README.md

## Note

This project is for personal use and learning purposes. Be respectful when cold emailing — always personalize and keep it genuine.