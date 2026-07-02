import cv2
import mediapipe as mp
import math
import time
import av
import traceback
from matplotlib.figure import Figure


def detect_finger_landmarks(image, hands):
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
    WebRTC Video Processor.

    IMPORTANT: mediapipe's Hands() is NOT thread-safe. Each processor
    instance (i.e. each WebRTC track/session) must own its own Hands
    object rather than sharing one cached instance across sessions —
    concurrent calls into a shared instance can silently hang instead
    of raising, which freezes the video with no error shown.
    """

    def __init__(self):
        self.times = []
        self.distances = []
        self.start_time = None
        self.capture_duration = 20
        self.finished = False

        # State tracking for frame skipping optimization
        self.frame_count = 0
        self.last_thumb = None
        self.last_index = None
        self.last_distance = -1

        # Per-instance MediaPipe Hands object — NOT shared/cached globally.
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def recv(self, frame):
        try:
            # Convert incoming WebRTC frame to OpenCV BGR format
            img = frame.to_ndarray(format="bgr24")
            self.frame_count += 1

            # Initialize start time on the very first frame
            if self.start_time is None:
                self.start_time = time.time()

            current_time = time.time() - self.start_time

            # Process frame and record data ONLY within the capture duration
            if current_time <= self.capture_duration:

                # OPTIMIZATION: Run heavy MediaPipe detection every second frame
                if self.frame_count % 2 != 0:
                    img, thumb, index = detect_finger_landmarks(img, self.hands)
                    distance = calculate_distance(thumb, index)

                    self.last_thumb = thumb
                    self.last_index = index
                    self.last_distance = distance

                    self.times.append(current_time)
                    self.distances.append(distance)
                else:
                    # On skipped frames, draw the last known dots so the UI doesn't flicker
                    if self.last_index:
                        cv2.circle(img, self.last_index, 10, (255, 0, 0), cv2.FILLED)
                    if self.last_thumb:
                        cv2.circle(img, self.last_thumb, 10, (0, 255, 0), cv2.FILLED)

                # Display information on the frame exactly as before
                remaining_time = max(0, int(self.capture_duration - current_time))
                cv2.putText(
                    img,
                    f"Distance: {self.last_distance:.2f} pixels",
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
                # Set the flag to true so the Streamlit UI can poll it instantly
                self.finished = True
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

        except Exception:
            # Never let recv() throw silently — that's what causes the
            # video to hang with no visible error. Log it and pass the
            # original frame through so the stream stays alive.
            traceback.print_exc()
            return frame


def generate_graph(times, distances):
    """
    Generates a thread-safe matplotlib figure using the Object-Oriented API.
    Prevents Streamlit "Invalid image width: 0" frontend crashes.
    """
    fig = Figure()
    ax = fig.subplots()

    # Failsafe: if the camera didn't record data, prevent plotting a 0x0 empty bounding box
    if not times or not distances:
        ax.text(
            0.5,
            0.5,
            "No tracking data recorded.",
            horizontalalignment="center",
            verticalalignment="center",
        )
    else:
        ax.plot(times, distances)

    ax.set_title("Change in Distance over Time")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Distance (pixels)")
    ax.grid(True)
    return fig
