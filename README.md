# Simple Chatbot Project

This is a Django-based chatbot application that provides FAQ responses and a simple web interface.

## Features
- FAQ-based chatbot using a JSON knowledge base
- Web interface for user interaction
- Admin panel for managing FAQs
- Static styling for a clean UI

## Project Structure
```
chatbot_project/
├── chatbot/
│   ├── admin.py
│   ├── apps.py
│   ├── faq.json
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/commands/build_faq_index.py
│   ├── migrations/
│   ├── static/chatbot/style.css
│   └── templates/chatbot/index.html
├── chatbot_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## Setup Instructions
1. **Clone the repository:**
   ```powershell
   git clone https://github.com/<your-username>/simple_chatbot.git
   cd simple_chatbot
   ```
2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```powershell
   python manage.py migrate
   ```
5. **Run the development server:**
   ```powershell
   python manage.py runserver
   ```
6. **Access the app:**
   Open your browser and go to `http://127.0.0.1:8000/`

## How to Push to GitHub
1. **Initialize git (if not already):**
   ```powershell
   git init
   ```
2. **Add remote origin:**
   ```powershell
   git remote add origin https://github.com/<your-username>/simple_chatbot.git
   ```
3. **Add and commit changes:**
   ```powershell
   git add .
   git commit -m "Initial commit"
   ```
4. **Push to GitHub:**
   ```powershell
   git push -u origin main
   ```

## License
This project is licensed under the MIT License.
