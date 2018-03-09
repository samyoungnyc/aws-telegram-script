from telethon import TelegramClient
from telethon.tl.types import ChannelAdminLogEventsFilter
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import InputUserSelf
from telethon.tl.types import InputUser
from time import sleep
import pyrebase

#FIREBASE SETUP
CONFIG = {
  "apiKey": "AIzaSyBOJiBDZmf2vNvZ01eQ8qqpL9ADRN3Qomo",
  "authDomain": "tbkairdrop.firebaseapp.com",
  "databaseURL": "https://tbkairdrop.firebaseio.com",
  "storageBucket": "tbkairdrop.appspot.com",
  "serviceAccount": "tbkairdrop-b8b59508de14.json"
}

#GLOBALS
ALL_PARTICIPANTS = []
OFFSET = 0
LIMIT = 1000
API_ID = 152336 # Your api_id
API_HASH = '92a6acabaac470daeb953d11f512b787' # Your api_hash
PHONE_NUMBER = '+16469373743' # Your phone number

telegram_username = 'etherkid'
push_id = '-L62tR081IjvRE7wAfDz'

#INITIALIZE FIREBASE APP
firebase = pyrebase.initialize_app(CONFIG)

#CREATE THE USER
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("samuel@sam.com", "yoyoyoyo")

#CREATE A REF TO THE DB
db = firebase.database()

#WHILE client.is_user_authorized() IS TRUE, SET UP THE PARTICIPANTS LIST:

#function for api

def isInTG(push_id, telegramUserStatus):
    # IF TRUE, SEND JSON OBJECT TO UPDATE FIREBASE TO TRUE
     # CLOUD FUNCTION WILL DETECT THE SWITCH AND SEND A VERIFICATION EMAIL
    print('{} is in TG'.format(push_id))    
    db.child("airdrop-form").child(push_id).update({"telegramMember": telegramUserStatus})
    return

def isNotInTG(push_id, telegramUserStatus):
    print('{} not in TG'.format(push_id))
    db.child("airdrop-form").child(push_id).update({"telegramMember": telegramUserStatus})
    return

#ALL_PARTICIPANTS.extend(participants.users)
#OFFSET += len(participants.users)

def openTelegramApiAndCheckForUsername(telegram_username):
    "this connects to telegram and checks username passed to it from firebase"
    client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)
    client.session.report_errors = False
    client.connect()

    if not client.is_user_authorized():
        client.send_code_request(PHONE_NUMBER)
        client.sign_in(PHONE_NUMBER, input('Enter the code: '))

    participants = client(GetParticipantsRequest('tokenbnk', ChannelParticipantsSearch(telegram_username), OFFSET, LIMIT , hash=0))
    if not participants.users:
        checkForTelegramUsername(False)
        return False    
    # inTelegramOrNot = checkForTelegramUsername(telegram_username, push_id)
    checkForTelegramUsername(True)    
    return True

  # IF USERNAME IS PRESENT, WRITE telegramUser: true IN FIREBASE
  # THAT TRIGGERS AN EMAIL FROM FIREBASE

def checkForTelegramUsername(telegramUserStatus):

    if telegramUserStatus:
        print('call isInTG')
        isInTG(push_id, telegramUserStatus)
    elif telegramUserStatus is False:
        print('call isInTG')
        isNotInTG(push_id, telegramUserStatus)
    
    # isInTelegram = openTelegramApiAndCheckForUsername(telegram_username)
    # if isInTelegram:
    #  # IF TRUE, SEND JSON OBJECT TO UPDATE FIREBASE TO TRUE
    #  # CLOUD FUNCTION WILL DETECT THE SWITCH AND SEND A VERIFICATION EMAIL
    #     isInTG(push_id)
    #     return True
    # elif isInTelegram is False:
    #  # IF TRUE, SEND JSON OBJECT TO UPDATE FIREBASE TO TRUE
    #  # CLOUD FUNCTION WILL DETECT THE SWITCH AND SEND A VERIFICATION EMAIL
    #     isNotInTG(push_id)
    #     return False
    # return True if telegramUsername else False
    return

#parameter 1
# telegram_username = 'etherkid'

# #parameter 2
# push_id = "-L62tR081IjvRE7wAfDz"

if __name__ == "__main__":
    # checkForTelegramUsername(telegram_username, push_id)
    openTelegramApiAndCheckForUsername(telegram_username)
