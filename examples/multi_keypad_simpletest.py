# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Neradoc
#
# SPDX-License-Identifier: Unlicense

import asyncio
import board
import keypad
from multi_keypad import MultiKeypad

################################################################
# The keypad part
################################################################

keys1 = keypad.Keys((board.GP3, board.GP7), value_when_pressed=False, pull=True)
keys2 = keypad.Keys((board.GP11,), value_when_pressed=False, pull=True)

################################################################
# Multi Keypad
################################################################


async def main():
    mkp = MultiKeypad(keys1, keys2)
    while True:
        event = mkp.events.get()
        if event:
            print(event)
        await asyncio.sleep(0.1)


asyncio.run(main())
