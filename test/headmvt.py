import cv2
import pyautogui
 
def find_and_move_to_face():
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
 
    # Start the video capture
    video_capture = cv2.VideoCapture(0)
 
    while True:
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
 
        # Display the frame with face detection
        #cv2.imshow('Face Detection', frame)
 
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    # Release the video capture and close the window
    video_capture.release()
    cv2.destroyAllWindows()
 
# Call the function to start face detection and cursor movement
find_and_move_to_face()