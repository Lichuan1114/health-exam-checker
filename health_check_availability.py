from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import subprocess
import requests

def access_data(location, state):
    """
    Launches a headless Chrome browser, navigates to the health exam booking website,
    searches for availability based on location and state, and evaluates the results.
    """
    # Set Chrome options for headless execution
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the Chrome WebDriver and open the health exam booking website
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()
    driver.get("https://bmvs.onlineappointmentscheduling.net.au/oasis/Default.aspx")
    # time.sleep(2) # Allow time for the page to load
    
    # Click the 'New Individual booking' button - wait until method
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'New Individual booking')]"))
    ).click()
    
    # Click the 'New Individual booking' button
    # button = driver.find_element(By.XPATH, "//button[contains(., 'New Individual booking')]")
    # button.click()
    # time.sleep(2) # Allow time for the page to load
    
    # Find the input field for location and enter the provided location - wait until method
    location_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//label[contains(., 'City, town, suburb or postcode:')]/following-sibling::input"))
    )
    location_input.clear()
    location_input.send_keys(location)
    
    # Find the input field for location and enter the provided location
    # location_input = driver.find_element(By.XPATH, "//label[contains(., 'City, town, suburb or postcode:')]/following-sibling::input")
    # location_input.clear()
    # location_input.send_keys(location)
    
    # Find the state dropdown and select the provided state
    state_dropdown = driver.find_element(By.XPATH, "//label[contains(., 'State:')]/following-sibling::select")
    state_select = Select(state_dropdown)
    state_select.select_by_value(state)
    
    # Click the 'Search' button
    search_button = driver.find_element(By.XPATH, "//input[@value='Search']")
    search_button.click()
    # time.sleep(3) # Allow time for the page to load
    
    tbody = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.tbl-location[role='presentation'] > tbody"))
    )
    
    # Locate the results table containing locations and availability
    # tbody = driver.find_element(By.CSS_SELECTOR, "table.tbl-location[role='presentation'] > tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    location_lst = []  # Stores location names
    availability_lst = []  # Stores availability status

    # Loop through each row in the results table
    for row in rows:
        title_address = row.find_element(By.XPATH, ".//td[@class='tdloc_name']")
        area = title_address.find_element(By.XPATH, ".//label[@class='tdlocNameTitle']").text.strip()
        address = title_address.find_element(By.XPATH, ".//span").text.strip().split("\n")
        
        # Format area and clinic name, address[0] is clinic name
        location = area + " - " + address[0]
        
        # Extract availability information
        availability = row.find_element(By.CSS_SELECTOR, "td.tdloc_availability > span").text.lower().strip().replace("\n", " ")
        
        location_lst.append(location)
        availability_lst.append(availability)
        
    driver.quit()
    evaluate_slot(location_lst, availability_lst)
    

def send_macOS_notification(message, title="Notification"):
    """
    Sends a macOS system notification using AppleScript.
    """
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])
    
def send_telegram_notification(TOKEN, CHAT_ID, MESSAGE):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": MESSAGE}
    
    response = requests.post(url, data=data)

    # Check result
    if response.status_code == 200:
        print("✅ Message sent!")
    else:
        print(f"❌ Failed! {response.text}")
    
def evaluate_slot(location_lst, availability_lst):
    """
    Evaluates the scraped availability data and sends a notification.
    """
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    slot_available = False
    current_time = time.strftime("%m-%d %H:%M")
    message = ""
    
    # Loop through availability data
    for i, msg in enumerate(availability_lst):
        # If an available slot is found
        if (msg != "no available slot"):
            slot_available = True
            temp = msg.capitalize()
            message += f"{location_lst[i]}\n{temp}\n"
    
    # Format final message with timestamp
    message = message.strip()
    message = current_time + "\n" + message
    
    # Send notification based on availability status
    if slot_available:
        # send_macOS_notification(message, "Health Exam slot detected!")
        send_telegram_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "Health Exam slot detected!\n" + message)
    else:
        # send_macOS_notification(message, "No Health Exam slot")
        send_telegram_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "No Health Exam slot\n" + message)

if __name__ == '__main__':
    location = "Adelaide"
    state = "SA"
    access_data(location, state)