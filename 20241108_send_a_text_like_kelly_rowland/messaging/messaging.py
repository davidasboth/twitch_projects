import xlwings as xw
import http.client
import json

def send_message():

    # read data from Excel sheet
    INPUT_CELL = "A1"
    DEBUG_OUTPUT_CELL = "A5"
    SMS_OUTPUT_CELL = "A6"
    
    # setup
    SENDER = "KellyR"

    JWT = ""
    with open("C:\\git\\twitch_projects\\20241108_send_a_text_like_kelly_rowland\\JWT.txt", "r") as f:
        JWT = f.read()

    NUMBER = ""
    with open("C:\\git\\twitch_projects\\20241108_send_a_text_like_kelly_rowland\\phone_number.txt", "r") as f:
        NUMBER = f.read()

    # read the message
    wb = xw.Book.caller()
    sheet = wb.sheets[0]

    message = sheet[INPUT_CELL].value

    # if sheet is empty, Python registers it as None
    if message:
        # debug output
        sheet[DEBUG_OUTPUT_CELL].value = f"Sending '{message}'..."

        # message sending bit
        conn = http.client.HTTPSConnection("api.thesmsworks.co.uk")

        payload = json.dumps({
            "sender": SENDER,
            "destination": NUMBER,
            "content": message
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': JWT
        }

        conn.request("POST", "/v1/message/send", payload, headers)

        res = conn.getresponse()

        data = res.read()

        response_string = data.decode("utf-8")

        sheet[SMS_OUTPUT_CELL].value = response_string

    # only use credits if there is a message to send
    else:
        sheet[DEBUG_OUTPUT_CELL].value = "Nothing happened. No message to send!"
        sheet[SMS_OUTPUT_CELL].value = ""
