# 🏥 Health Exam Availability Checker in Australia  
This project is a Python script that automatically checks for health exam appointment for individual availability and notifies you via Telegram, whether or not slots are available. It can be run manually or scheduled to run at specified intervals using GitHub Actions.

## 🚀 Features  
✅ Automates the booking availability check for health exams  
✅ Uses Selenium to scrape the booking website  
✅ Allows users to enter location and state via command-line arguments or prompt, and save for future use.  
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
You can run the script in different ways:
1. Using Saved Location and State
If you've previously run the script and entered a location, it will use that:
```bash
python health_check_availability.py
```
2. Providing Location and State via Command Line
```bash
python health_check_availability.py [location] [State Abbreviation]
```
3. Entering Location and State Manually
If no saved location is found and no arguments are provided, the script will prompt you:
```bash
Enter Location or Postcode (e.g., Adelaide):
Enter State Abbr. (e.g., SA):
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



