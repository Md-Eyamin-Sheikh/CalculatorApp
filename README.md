# Modern Calculator

A professional and modern desktop calculator built with Python and Tkinter.

## Features

- Dark-themed modern user interface
- Fixed-size centered desktop window
- Large right-aligned display
- Button grid for digits and operators
- Safe expression evaluation using Python `ast`
- Error handling for invalid expressions and division by zero
- Backspace support
- Decimal input support
- Keyboard input support
- Simple calculation history panel

## Requirements

- Python 3.x
- Tkinter

## Run the Application

```bash
python3 modernCalculator.py
```

## Project Structure

- `modernCalculator.py` - Main calculator application
- `README.md` - Project documentation

## Controls

- `0-9` for digits
- `+`, `-`, `*`, `/` for operations
- `.` for decimal values
- `Enter` to calculate
- `Backspace` to delete the last character
- `Escape` to clear the display

## Notes

The calculator uses a safe parser for arithmetic expressions instead of direct `eval`, which makes it more secure for user input.
