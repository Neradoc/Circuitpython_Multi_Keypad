import board
import keypad
import time
import asyncio
from adafruit_ticks import ticks_ms, ticks_less
from multi_macropad import MultiKeypad

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
		event = mkp.next_event()
		if event:
			print(event)
		await asyncio.sleep(1)

asyncio.run(main())
