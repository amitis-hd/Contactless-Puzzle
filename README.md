# Contactless Puzzle

## Project Overview
The **Contactless Puzzle** is an interactive puzzle game that uses facial recognition and voice commands to create a hands-free gaming experience. This project was developed by **Amitis Hamidi**, **Kipchirchir**, and **Rennie**. The game allows users to solve puzzles by simply moving their face and issuing voice commands, making it a unique and accessible way to play.

## Features
- **Voice Command Integration:** Players can control the game using simple voice commands such as "this," "that," "quit," and "restart."
- **Facial Recognition:** The game tracks the player's face and moves the cursor to the detected face position.
- **Puzzle Mechanics:** The game includes several puzzles with images that are sliced into pieces. Players can select and swap pieces to solve the puzzle.

## Dependencies
This project requires the following Python libraries:
- `pygame`
- `random`
- `cv2` (OpenCV)
- `pyautogui`
- `speech_recognition`
- `multiprocessing`

To install the necessary dependencies, run:
```bash
pip install pygame opencv-python pyautogui SpeechRecognition

## Game Instructions
Starting the Game: The game begins by selecting a random image from the provided images. The image is then split into square pieces, which are shuffled on the screen.
##Voice Commands:
- "this" or "that": Click to select puzzle pieces.
- "quit": Quit the game at any time.
- "restart": Restart the game with a new puzzle.
## Facial Recognition:
The cursor moves to the center of the detected face, allowing you to select puzzle pieces without using a mouse.
