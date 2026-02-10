import cv2
import mediapipe as mp
import math
import time
import matplotlib.pyplot as plt

# Initialize mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

# Function to detect index finger and thumb landmarks
def detect_finger_landmarks(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    thumb_point = None
    index_point = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Index finger (landmark ID: 8)
                if id == 8:
                    index_point = (cx, cy)
                    cv2.circle(image, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

                # Thumb (landmark ID: 4)
                elif id == 4:
                    thumb_point = (cx, cy)
                    cv2.circle(image, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return image, thumb_point, index_point

# Calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    if point1 is not None and point2 is not None:
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    else:
        return -1

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Set the duration for video capture in seconds
capture_duration = 20  # Capture for 60 seconds

# Lists to store time and distance data
times = []
distances = []

start_time = time.time()
end_time = start_time + capture_duration  # Calculate the end time

while cap.isOpened() and time.time() < end_time:  # Capture until end time is reached
    ret, frame = cap.read()
    if not ret:
        break

    # Detect finger landmarks
    frame, thumb, index = detect_finger_landmarks(frame)

    # Calculate distance between thumb and index finger
    distance = calculate_distance(thumb, index)

    # Record current time
    current_time = time.time() - start_time

    # Append time and distance data to lists
    times.append(current_time)
    distances.append(distance)

    # Display the frame
    cv2.putText(frame, f'Distance: {distance:.2f} pixels', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Calculate and display remaining time
    remaining_time = int(end_time - time.time())
    cv2.putText(frame, f'Time Left: {remaining_time} s', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Hand Tracking', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()

# Plotting the graph
plt.plot(times, distances)
plt.title('Change in Distance over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Distance (pixels)')
plt.grid(True)
plt.show()
