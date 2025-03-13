# 🏥 Health Exam Availability Checker in Australia  
This project is a Python script that automatically checks for health exam appointment availability and notifies you via Telegram when slots open up in Australia for visa purposes as an individual.

## 🚀 Features  
✅ Automates the booking availability check for health exams  
✅ Uses Selenium to scrape the booking website  
✅ Sends notifications via Telegram  
✅ Runs on GitHub Actions every 2 hours if enabled  

## 📌 Setup  
### Prerequisites
1️⃣ Make sure you have:
- Python 3.x installed
- Google Chrome installed
- ChromeDriver installed  

2️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/health-exam-checker.git
cd health-exam-checker
```

3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

4️⃣ Set Up Environment Variables
Create a .env file in the project directory and add:
```sh
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

5️⃣ Run the Script
```bash
python health_check_availability.py
```

## ⚙️ GitHub Actions Workflow
This project includes a GitHub Actions workflow that runs the script automatically every 2 hours.  
To enable it, push the repository to GitHub and add your Telegram API credentials as GitHub Secrets:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

Activate it by enabling the following lines in run_script.yml:
```bash
  schedule:
    - cron: "0 */2 * * *"  # Runs every 2 hours
```

## 🛠 How It Works  
1. Opens the health exam booking website using Selenium
2. Searches for availability in the specified location & state
3. Extracts available slots and formats them
4. Sends a Telegram notification with the results

## 📜 License  
This project is open-source under the MIT License.



