# How to send a text from Excel like Kelly Rowland

I can't promise you can recreate this easily. Why would you?

## How to use
1. In `messaging.xlsm`, put a message in A1
2. Update your own phone number in the Python script
3. Probably install `xlwings` etc. as per the instructions below
2. Click the Send message button
3. SMS should send? Maybe? Cell A5 has debug messages.


## Setup instructions (if you want to do this yourself)

1. Install `xlwings` (in a `conda` environment!)
2. Run `xlwings addin install` to install the Excel Add-In
3. Enable Trust access to the VBA project object model under File > Options > Trust Center > Trust Center Settings > Macro Settings. You only need to do this once.
4. Run `xlwings quickstart project_name` to create a new folder with a module and Excel workbook inside it (called `project_name`)
5. The code in `messaging.py` contains the necessary Python functions and the `messaging.xlsm` contains a button to send a message. This calls VBA's "RunPython" function/macro/thing to invoke the Python function in `messaging.py`

## Known issues

1. This is a dumb idea.
2. Use `conda` environments, xlwings doesn't like `poetry`