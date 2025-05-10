import cv2

def get_video_frame():
    """Capture a single frame from the webcam."""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    return None
