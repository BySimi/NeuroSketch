import cv2
import mediapipe as mp
import math
import time
import av
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


class FingerTapProcessor:
    """
    WebRTC Video Processor that acts as the callback for incoming browser frames.
    Replaces the cv2.VideoCapture while maintaining the exact data collection logic.
    """

    def __init__(self):
        self.times = []
        self.distances = []
        self.start_time = None
        self.capture_duration = 20

    def recv(self, frame):
        # Convert incoming WebRTC frame to OpenCV BGR format
        img = frame.to_ndarray(format="bgr24")

        # Initialize start time on the very first frame
        if self.start_time is None:
            self.start_time = time.time()

        current_time = time.time() - self.start_time

        # Process frame and record data ONLY within the capture duration
        if current_time <= self.capture_duration:
            img, thumb, index = detect_finger_landmarks(img)
            distance = calculate_distance(thumb, index)

            self.times.append(current_time)
            self.distances.append(distance)

            # Display information on the frame exactly as before
            remaining_time = max(0, int(self.capture_duration - current_time))
            cv2.putText(
                img,
                f"Distance: {distance:.2f} pixels",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                img,
                f"Time Left: {remaining_time} s",
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
        else:
            # Indicate completion on the final frames before shutdown
            cv2.putText(
                img,
                "Assessment Complete.",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

        # Return processed frame back to the browser
        return av.VideoFrame.from_ndarray(img, format="bgr24")


def generate_graph(times, distances):
    """Generates the matplotlib figure."""
    fig, ax = plt.subplots()
    ax.plot(times, distances)
    ax.set_title("Change in Distance over Time")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Distance (pixels)")
    ax.grid(True)
    return fig
