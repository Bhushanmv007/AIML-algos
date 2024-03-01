import cv2
import mediapipe as mp
import subprocess
import os

# Set up hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Path to your dataset folders
thumbs_up_folder = r"C:\THUMBS\UP"
thumbs_down_folder = r"C:\THUMBS\DOWN"

# Load dataset images
thumbs_up_images = []
for filename in os.listdir(thumbs_up_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(thumbs_up_folder, filename)
        image = cv2.imread(image_path)
        if image is not None:
            thumbs_up_images.append(image)
        else:
            print(f"Failed to read image: {image_path}")

thumbs_down_images = []
for filename in os.listdir(thumbs_down_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(thumbs_down_folder, filename)
        image = cv2.imread(image_path)
        if image is not None:
            thumbs_down_images.append(image)
        else:
            print(f"Failed to read image: {image_path}")

# Initialize variables for volume control
volume_up_gesture_detected = False
volume_down_gesture_detected = False

# Function to check if hand gesture matches any image in the dataset
def gesture_matches_dataset(gesture, dataset):
    # Process the gesture image and get hand landmarks
    results = hands.process(gesture)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Adjust your gesture detection logic here based on hand landmarks
            # For example, check the position of thumb and index finger landmarks
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Volume control gestures
            if thumb_tip.y < index_tip.y:
                # Thumb is raised (thumbs up)
                return True
            elif thumb_tip.y > index_tip.y:
                # Thumb is lowered (thumbs down)
                return True
    return False

# Set up camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get hand landmarks
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the position of the thumb and index finger tips
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Volume control gestures
            if thumb_tip.y < index_tip.y:
                # Thumb is raised (thumbs up)
                volume_up_gesture_detected = True
                volume_down_gesture_detected = False
            elif thumb_tip.y > index_tip.y:
                # Thumb is lowered (thumbs down)
                volume_down_gesture_detected = True
                volume_up_gesture_detected = False

    # Check if detected gestures match any images in the dataset
    if volume_up_gesture_detected:
        for thumbs_up_image in thumbs_up_images:
            if gesture_matches_dataset(thumbs_up_image, thumbs_up_images):
                subprocess.run(['powershell', '(New-Object -ComObject WScript.Shell).SendKeys([char]175)'])  # Volume Up
                break
        volume_up_gesture_detected = False

    elif volume_down_gesture_detected:
        for thumbs_down_image in thumbs_down_images:
            if gesture_matches_dataset(thumbs_down_image, thumbs_down_images):
                subprocess.run(['powershell', '(New-Object -ComObject WScript.Shell).SendKeys([char]174)'])  # Volume Down
                break
        volume_down_gesture_detected = False

    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()