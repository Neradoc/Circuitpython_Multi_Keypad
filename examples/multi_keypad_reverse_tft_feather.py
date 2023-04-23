# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Neradoc
#
# SPDX-License-Identifier: Unlicense

import board
import keypad
import time
from multi_keypad import MultiKeypad

################################################################
# The keypad part
################################################################

# buttons D1 and D2 are pulled down (for wake up purposes)
keys1 = keypad.Keys((board.D1, board.D2), value_when_pressed=True, pull=True)
# button D0 is pulled down (because it's the BOOT button)
keys2 = keypad.Keys((board.BUTTON,), value_when_pressed=False, pull=True)

################################################################
# Multi Keypad
################################################################

mkp = MultiKeypad(keys1, keys2)

while True:
    event = mkp.events.get()
    if event:
        print(event)
    time.sleep(0.1)
