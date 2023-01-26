# Telegram-parser
A python script for parsing information about users and messages from telegram channels and chats.

# How to run
Before running the program you need to create your Telegram Application and get your API credentials.
Follow the link for detailed instructions.
[Follow the link for detailed instructions](https://core.telegram.org/api/obtaining_api_id)

To run this program, you will need to have Python and Git installed on your machine.

1. Clone the repository from GitHub by running the following command in your command prompt:
```
git clone https://github.com/pavlejviki/telegram-parser
```
2. Change into the project directory by running:
```
cd telegram-parser
```
3. Create a virtual environment:
```
python -m venv venv
```
4. Activate the virtual environment:
```
source venv/bin/activate  # on macOS
venv\Scripts\activate  # on Windows 
```
5. Install the required dependencies:
```
pip install -r requirements.txt
```
6. Copy .env.sample -> .env and populate with all required data

7. To parse users from the required channel run:
```
python parse_users.py
```
or to parse messages:
```
python parse_messages.py
```
Upon successful completion an html file will be generated containing an html table with all required data.
