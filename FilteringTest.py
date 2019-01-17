import random
import time

# File for testing output of digital filtering systems prior to inclusion in c based software.

nTaps = 32

#buffer = [0] * nTaps
#buffer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
buffer = [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 20, 20, 20, 20]

h = [
  -175,
  -487,
  -500,
  282,
  1504,
  1894,
  740,
  -747,
  -588,
  1129,
  1745,
  -446,
  -2871,
  -857,
  6283,
  13009,
  13009,
  6283,
  -857,
  -2871,
  -446,
  1745,
  1129,
  -588,
  -747,
  740,
  1894,
  1504,
  282,
  -500,
  -487,
  -175
]


def filter(value):
    output = 0

    # Shift the delay line, where i is the number of taps -1

    for i in range(nTaps-1, 0, -1):
        buffer[i] = buffer[i-1];  # Moving data one along sample up in the buffer

    buffer[0] = value

    for x in range(0, nTaps-1):
        output += buffer[x] * h[x];  # h is impulse response values from internet
        print(output)

    return output;


while 1:
    print(buffer)

    temp = random.randint(19, 41)

    print("     " + str(temp))

    filteredValue = filter(22)

    dividedValue = filteredValue / nTaps / 16

    print("         " + str(dividedValue))

    time.sleep(1)

