# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Neradoc
# SPDX-License-Identifier: MIT
#
# pylint: disable=unsubscriptable-object
"""
`multi_keypad`
================================================================================

A library to manage multiple keypad instances (and compatible) as a single event queue.


* Author(s): Neradoc

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit Ticks Library: https://github.com/adafruit/Adafruit_CircuitPython_Ticks
"""

from adafruit_ticks import ticks_less

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/Neradoc/CircuitPython_multi_keypad.git"


class Event:
    """
    Event class, adds the keypad ID to the keypad event.

    :param int keypad: The ID number of the keypad that generated that event.
    :param obj event: The original keypad event.
    :param int offset: The offset added to the key_number (default 0).
    """

    def __init__(self, keypad, event, offset=0):
        self.pad_number = keypad
        self.timestamp = event.timestamp
        self.pressed = event.pressed
        self.released = event.released
        self.key_number = event.key_number + offset
        self.original_event = event

    def __eq__(self, other: object) -> bool:
        """Two Event objects are equal by comparing their key_number,
        pressed value, timestamp, and keypad number."""
        return (
            self.pad_number == other.pad_number
            and self.key_number == other.key_number
            and self.pressed == other.pressed
            and self.timestamp == other.timestamp
        )

    def __hash__(self) -> int:
        """Returns a hash for the Event, so it can be used in dictionaries, etc.
        Assumes less than 8192 keys on the keyboard"""
        return (
            self.pad_number
            << 14 + self.original_event.key_number
            << 1 + int(self.pressed)
        )

    def __repr__(self):
        status = "pressed" if self.pressed else "released"
        return f"<Event: pad_number {self.pad_number} key_number {self.key_number} {status}>"


class EventMultiQueue:
    """
    A queue of Event objects.
    """

    def __init__(self, keypads):  # , max_events=64):
        self.keypads = keypads
        self.offsets = [0] + [pad.key_count for pad in keypads]
        # The next event from each keypad queue
        self.next_events = [None] * len(keypads)

    def get(self) -> Event:
        """
        Return the next key transition event.
        Return None if no events are pending.
        """
        next_event = None
        # collate one event per keypad if none already
        for padnum, keypad in enumerate(self.keypads):
            if self.next_events[padnum] is None:
                new_event = keypad.events.get()
                if new_event is not None:
                    # record that event
                    new_event = (new_event.timestamp, padnum, new_event)
                    self.next_events[padnum] = new_event
            else:
                new_event = self.next_events[padnum]
            # keep it if it's the oldest
            if new_event is not None:
                if next_event is None or ticks_less(new_event[0], next_event[0]):
                    next_event = new_event
        # return (and remove) the event
        if next_event is not None:
            self.next_events[next_event[1]] = None
            padnum = next_event[1]
            return Event(padnum, next_event[2], self.offsets[padnum])
        return None

    def get_into(self, event: Event) -> bool:
        """
        Puts the next event into the passed object. This does not avoid
        allocating storage because we have to cache events from the underlying
        keypads anyway. Only there for compatibility.
        """
        if not isinstance(event, Event):
            raise ValueError("Event must be of class multi_keypad.Event")
        new_event = self.get()
        if not new_event:
            return False

        event.pad_number = new_event.pad_number
        event.timestamp = new_event.timestamp
        event.pressed = new_event.pressed
        event.released = new_event.released
        event.key_number = new_event.key_number
        event.original_event = new_event.original_event
        return True

    def clear(self) -> None:
        """
        Clear any queued key transition events.
        Also sets ``overflowed`` to ``False``.
        """
        for keypad in self.keypads:
            keypad.clear()

    def overflowed(self) -> bool:
        """
        ``True`` if an event could not be added to the event queue because
        it was full. (read-only) Set to ``False`` by ``clear()``.
        """
        return any(kp.overflowed for kp in self.keypads)

    def __bool__(self) -> bool:
        """
        ``True`` if ``len()`` is greater than zero.
        This is an easy way to check if the queue is empty.
        """
        return any(self.keypads.events)

    def __len__(self) -> int:
        """
        Return the number of events currently in the queue.
        Used to implement ``len()``.
        """
        return sum(len(x) for x in self.keypads.events)


class MultiKeypad:
    """Multi Keypad. Read events from multiple keypads as a single queue.

    :param obj keypads: Instances of keypad scanenrs or compatible objects.
    """

    def __init__(self, *keypads):
        self.events = EventMultiQueue(keypads)
        self.key_count = sum(pad.key_count for pad in keypads)

    def next_event(self):
        """Deprecated method to get the next event"""
        return self.events.get()
