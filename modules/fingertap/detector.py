import cv2
import mediapipe as mp
import math
import time
import matplotlib.pyplot as plt

# Initialize mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)


def detect_finger_landmarks(image):
    """Detects index finger and thumb landmarks exactly as in the prototype."""
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


def calculate_distance(point1, point2):
    """Calculates Euclidean distance exactly as in the prototype."""
    if point1 is not None and point2 is not None:
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    else:
        return -1


def run_assessment(capture_duration=20):
    """
    Generator that processes the webcam feed, collects data,
    and yields frames back to the UI to avoid cv2.imshow().
    """
    cap = cv2.VideoCapture(0)

    times = []
    distances = []

    start_time = time.time()
    end_time = start_time + capture_duration

    while cap.isOpened() and time.time() < end_time:
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

        # Display information on the frame exactly as before
        cv2.putText(
            frame,
            f"Distance: {distance:.2f} pixels",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )

        remaining_time = int(end_time - time.time())
        cv2.putText(
            frame,
            f"Time Left: {remaining_time} s",
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )

        # Convert frame from BGR to RGB for Streamlit rendering
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Yield the current state to the UI instead of blocking
        yield frame_rgb, remaining_time, times, distances

    cap.release()


def generate_graph(times, distances):
    """Generates the matplotlib figure to be passed to st.pyplot() instead of plt.show()."""
    fig, ax = plt.subplots()
    ax.plot(times, distances)
    ax.set_title("Change in Distance over Time")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Distance (pixels)")
    ax.grid(True)
    return fig
