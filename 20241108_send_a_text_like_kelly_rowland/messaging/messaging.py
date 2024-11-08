import xlwings as xw


def main():
    pass

@xw.func
def send_message():

    INPUT_CELL = "A1"
    DEBUG_OUTPUT_CELL = "A5"

    # hard code phone number for now
    number = "123456"

    wb = xw.Book.caller()
    sheet = wb.sheets[0]

    # read the message
    message = sheet[INPUT_CELL].value

    # if sheet is empty, Python registers it as None
    if message:
        # debug output
        sheet[DEBUG_OUTPUT_CELL].value = f"Sending '{message}' to {number}"

        # only use credits if there is a message to send
    else:
        sheet[DEBUG_OUTPUT_CELL].value = "Nothing happened. No message to send!"

if __name__ == "__main__":
    xw.Book("messaging.xlsm").set_mock_caller()
    main()
