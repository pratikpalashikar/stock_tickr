''' -------------------
   | ticker_tracker.py |
   |   Adam  Denning   |
    -------------------
    This program is designed to get a given stock's current price, and output indicators to an arduino.
    https://www.youtube.com/c/ProjectCentral/
'''
import finnhub  # Stock Price API
import serial  # To send to Arduino
import time  # For Timers

# (Notes for future distribution): Enter your personal Finnhub API key here. You can get a free API key at https://finnhub.io/ by creating account.
fhub = finnhub.Client("yourAPIKey")
# (Notes for future distribution): Enter the serial port assigned to your Arduino here.
ser = serial.Serial('/dev/cu.usbmodem146101',9600)

# Global Variables
# Price Keys
fcurrent = "c"
fchange = "d"
fpchange = "dp"
# Write Codes
clear = "/"
green = "{"
red = "}"
row1 = "["
row2 = "]"


def write(content):
    ser.write(content.encode())


def get_target():
    target_ticker = input(
        "Welcome to the Ticker Tracker program.\nPlease enter your desired stock ticker symbol to begin (SPY): ").upper()

    return target_ticker


def determine_indicators():
    # set indicator arrays
    available_indicators = [1, 2, 3, 4, 5]
    # return chosen indicators
    return available_indicators;


def get_price(target):
    ticker_price = fhub.quote(target)

    return ticker_price


def send_price(name, p, ind):
    # indicator light
    if 4 in ind:
        # green or red
        print(p[fchange])
        write(clear)
        time.sleep(.1)  # allows clear time to execute without interfering with writes
        if (p[fchange] > 0):
            write(green)
        else:
            write(red)

    # display price
    if 1 in ind:
        write(clear)
        time.sleep(.1)  # allows clear time to execute without interfering with writes
        write(row1)
        write(f"{name}: {p[fcurrent]}")

    write(row2)

    # change num
    if 2 in ind:
        write(f"{p[fchange]} ")

    # change per
    if 3 in ind:
        write(f"{p[fpchange]:.2f}% ")


def main():
    # program setup
    indicators = determine_indicators()
    i = 0
    # loop
    while 1 == 1:

        ticker = ['DOW','BAC','TSLA', 'AMC', 'MRTX']

        length = len(ticker)
        if i >= length:
            i = 0

        # gets ticker info
        price = get_price(ticker[i])

        print(i, price, ticker[i])

        # outputs to arduino
        send_price(ticker[i], price, indicators)
        i += 1
        # refresh buffer
        time.sleep(5)



# run program
if __name__ == "__main__":
    main()