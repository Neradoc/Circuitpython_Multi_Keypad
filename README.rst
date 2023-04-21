Introduction
============


.. image:: https://readthedocs.org/projects/multi-keypad-for-circuitpython/badge/?version=latest
    :target: https://multi-keypad-for-circuitpython.readthedocs.io/
    :alt: Documentation Status



.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/Neradoc/Circuitpython_Multi_Keypad/workflows/Build%20CI/badge.svg
    :target: https://github.com/Neradoc/Circuitpython_Multi_Keypad/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A library to manage multiple keypad instances (and compatible) as a single event queue.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.


Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install multi_macropad

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    import board
    from multi_macropad import MultiKeypad
    keys1 = keypad.Keys((board.GP3, board.GP7), value_when_pressed=False, pull=True)
    keys2 = keypad.Keys((board.GP11,), value_when_pressed=False, pull=True)

    mkp = MultiKeypad(keys1, keys2)
    while True:
        event = mkp.next_event()
        if event:
            print(event)


Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-multi-macropad.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/Neradoc/CircuitPython_multi_macropad/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
