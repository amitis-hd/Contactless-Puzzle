################################################################################
# Kipchirchir, Rennie and Hamidi, Amitis 
################################################################################

import pygame
import random
import cv2
import pyautogui
import speech_recognition as sr
import time
from multiprocessing import Process, Event, Manager



# Name: recognize_voice_commands
# Description: This function is in charge of detecting user voice commands and 
# acting accordingly. 
#   "this" and "that" => curser clicks
#   "quit" => program quits at any stage
#   "restart" => game restarts
# The function is also in charge of giving audio clues to the user indicating 
# selection, swapping, and invalid voice command
# Input: an Event stop_event, which is shared across the program processes, and
# is used to indicate if all processes should terminate
# An Event restart_event used to indicate when the pygame needs to end and a new
# one to start
# Output: Does not return 
# Notes: uses local files "click.mp3", "swap.mp3", "invalid.mp3"
# uses Google's speech recognition
def recognize_voice_commands(stop_event , restart_event):
    #initialization of audio clues
    pygame.mixer.init()
    click_sound = pygame.mixer.Sound("click.mp3")
    swap_sound = pygame.mixer.Sound("swap.mp3")
    invalid_sound = pygame.mixer.Sound("invalid.mp3")

    #initialization of the recognizer
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        while not stop_event.is_set():
            print("Say something!")

            # The user has 5 seconds to say their command
            audio = r.listen(source, phrase_time_limit=5)
            
            # recognize speech using Google Speech Recognition
            try:
                text = r.recognize_google(audio)
                print("We think you said " + text)

                if("this" in text):
                    click_sound.play()
                    pyautogui.click()
                elif("there" in text):
                    swap_sound.play()
                    pyautogui.click()
                elif("quit" in text):
                    stop_event.set()    #end the entire program
                    break   
                elif("restart" in text):
                    restart_event.set()
                    print("restarting")
                else:
                    invalid_sound.play()
                    print("Please use game commands")
            
            #error handeling
            except sr.UnknownValueError:
                invalid_sound.play()
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                time.sleep(1)
            except sr.ConnectionResetError:
                print("Error connecting to the server")
                time.sleep(1)
            time.sleep(2)


# Name: find_and_move_to_face
# Description: This function is responsible for detecting a face, and moving the
# cuser based on where it detects the center of the face to be
# Input: an Event stop_event, which is shared across the program processes, and
# is used to indicate if all processes should terminate
# Output: Does not return 
# Notes: 
def find_and_move_to_face(stop_event):
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
 
    # Start the video capture
    video_capture = cv2.VideoCapture(0)
 
    while not stop_event.is_set():
        # Read a frame from the video capture
        ret, frame = video_capture.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
 
        # Iterate over the detected faces
        for (x, y, w, h) in faces:
            # Get the center position of the face
            face_center_x = x + w // 2
            face_center_y = y + h // 2
 
            # Move the cursor to the center of the face
            pyautogui.moveTo(face_center_x, face_center_y)
 
    # Release the video capture and close the window
    video_capture.release()
    cv2.destroyAllWindows()


# Name: load_and_scale_image
# Description: This function is responsible for loading and scaling the puzzle 
# image if it is larger than the initial screen. 
# Input: The path to the image, as well as the max hight and width of the screen
# Output: returns the new image
# Notes: 
def load_and_scale_image(image_path, max_width, max_height):
    image = pygame.image.load(image_path)
    image_width, image_height = image.get_size()

    # Scale the image if it's larger than the screen
    if image_width > max_width or image_height > max_height:
        #crops the image so that the proportions of width and height match that
        #of the screen
        if(image_height / image_width > max_height/max_width):
            image_height = (image_width * max_height) / max_width
        elif( image_width / image_height >  max_width / max_height):
            image_width = (image_height * max_width) / max_height
        #scales the image so that it would fit the screen
        scaling_factor = min(max_width / image_width, max_height / image_height)
        new_size = (int(image_width * scaling_factor), int(image_height * scaling_factor))
        image = pygame.transform.scale(image, new_size)

    return image

# Name: slice_image
# Description: This function splits a given image into square pieces
# Input: An image and a the number of pieces it will be broken into 
# (pieces = num_pieces ^2)
# Output: returns an array of pieces
# Notes: 
def slice_image(image, num_pieces):
    #calculate the piece dimentions
    image_width, image_height = image.get_size()
    piece_width = image_width // num_pieces
    piece_height = image_height // num_pieces

    pieces = []
    #populate pieces
    for i in range(num_pieces):
        for j in range(num_pieces):
            rect = pygame.Rect(j * piece_width, i * piece_height, piece_width, piece_height)
            piece = image.subsurface(rect)
            pieces.append(piece)

    return pieces

# Name: get_image
# Description: This function returns a random image from an array of images
# Input: none
# Output: retuns the selected image path
def get_image():
    images = ["Images/car.jpeg", "Images/castle.jpeg", "Images/dog.jpeg", 
              "Images/eiffel_tower.jpeg", "Images/italy.jpeg", "Images/landscape.jpeg", 
              "Images/panda.jpeg", "Images/plane.jpeg", "Images/rjacob.jpeg"
              "Images/train.jpeg", "Images/vacation.jpeg"]
    
    index = random.randint(0, len(images) - 1) #index between 0 and length - 1

    return images[index]

# Name: game_setup
# Description: This function initiates a pygame, shuffles and displays the
# pieces, checks for game complition, mouse picking and swaping pieces
# Input: an Event stop_event, which is shared across the program processes, and
# is used to indicate if all processes should terminate
# An Event restart_event used to indicate when the pygame needs to end and a new
# one to start
# Output: returns nothing
# Notes: 
def game_setup(stop_event , restart_event):

    while not stop_event.is_set():
        image_path = get_image()
        num_pieces = 2
        pygame.init()
        screen_width, screen_height = 800, 600

        # Set up the font, text, render, and set position
        font = pygame.font.Font(None, 36) 
        text = "You did it!! Do you want to play again? Say quit or restart."
        text_surface = font.render(text, True, (255, 255, 255))  # White color
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))

        #set up the display
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Puzzle Game")

        # set up the image
        image = load_and_scale_image(image_path, screen_width, screen_height)
        pieces = slice_image(image, num_pieces)

        #original copy saved for complition checks
        orig = pieces.copy()

        # Shuffle the pieces
        random.shuffle(pieces)

        # Display the pieces
        piece_width, piece_height = pieces[0].get_size()
        for i, piece in enumerate(pieces):
            x = (i % num_pieces) * piece_width
            y = (i // num_pieces) * piece_height
            screen.blit(piece, (x, y))

        pygame.display.flip()

        indecies = []  #to store indices for images too be swapped
        count = 0  #keeping track of the number of pieces selected
        complete = False
        
        while not stop_event.is_set() and not complete:
            if(restart_event.is_set()):
                restart_event.clear() #checks to see if the game should restart
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_event.set()  #checks to see if the game should end
                    break
                complete = True
                for i in range (len(pieces)):
                    if pieces[i] != orig[i]: #if a missmatched piece is found
                        complete = False
                if complete:
                    # Blit the text surface onto the screen, asking for replay
                    screen.blit(text_surface, text_rect)
                    pygame.display.flip()
                    while(not restart_event.is_set() or not stop_event.is_set()):
                        time.sleep(1)  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get current mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Calculate the index of the puzzle piece the mouse is over
                    column = mouse_x // piece_width
                    row = mouse_y // piece_height
                    piece_index = row * num_pieces + column
                    indecies.append(piece_index)
                    count += 1 

                    if count == 2: #two pieces have been selected to be swapped
                        pieces[indecies[0]], pieces[indecies[1]] = pieces[indecies[1]], pieces[indecies[0]]
                        count = 0 
                        #redraw the screen
                        for i, piece in enumerate(pieces):
                            x = (i % num_pieces) * piece_width
                            y = (i // num_pieces) * piece_height
                            screen.blit(piece, (x, y))
                            
                        pygame.display.flip()
                        indecies = []

        pygame.quit()

# Name: main
# Description: This is the main fucntion that starts 3 processes
#   1.Voice recognition
#   2.Facial reconition
#   3.Main game
# Input: N/A
# Output: returns nothing
# Notes: 
if __name__ == "__main__":
    
    #used to tell all processes when to terminate
    stop_event = Event()
    restart_event = Event()
    cursor_process = Process(target=find_and_move_to_face, args=(stop_event, ))
    image_process = Process(target=game_setup, args=(stop_event, restart_event))
    voice_process = Process(target=recognize_voice_commands, args=(stop_event, restart_event ))

    #start process
    image_process.start()
    cursor_process.start()
    voice_process.start()

    image_process.join()
    cursor_process.join()
    voice_process.join()
