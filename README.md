# Video Vector Visualisation

## Overview

This project captures hand movements using a webcam and performs motion analysis by tracking the hand's position, velocity, and acceleration over time. The project uses OpenCV for video capture, MediaPipe for hand landmark detection, and NumPy and Matplotlib for data analysis and visualization.
![Figure_2](https://github.com/user-attachments/assets/ec4601ac-6ebc-4a5b-baa7-22aa2bd16cc1)
![Figure_3](https://github.com/user-attachments/assets/a018bed7-61e2-4f11-be0b-5f413aebaedd)



## Requirements

- Python 3.x
- Required Python libraries: OpenCV, MediaPipe, NumPy, Matplotlib

You can install the required libraries using pip:

```bash
pip install opencv-python mediapipe numpy matplotlib
```

## Code Description

### Video Capture and Hand Tracking

**Initialize Video Capture:**

- `cv2.VideoCapture(0)` opens the default webcam.
- `cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)` and `cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)` set the video frame size.

**MediaPipe Initialization:**

- `mp.solutions.hands.Hands` initializes the MediaPipe hand tracking model with specified parameters for detection and tracking confidence.

**Capture and Process Frames:**

- The script captures video frames in a loop, processes them to detect hand landmarks, and calculates the center of the hand based on the landmarks' positions.
- The center of the hand is calculated as the average of the landmark positions, and the coordinates are displayed on the video feed.

**Display Results:**

- The hand's center is visualized with a circle, and its coordinates are shown on the video frame.

### Motion Analysis

**Calculate Velocity and Acceleration:**

- After capturing the video, the script calculates the velocity and acceleration of the hand's center using NumPy's `np.gradient` function.

**Plot Results:**

- Matplotlib is used to plot the hand's position, velocity, and acceleration over time in three separate subplots.

## How to Run

1. **Execute the Script**:
   Run the script using Python from the command line:

   ```bash
   python hand_tracking_motion_analysis.py
   ```
2. **Interact with the Video**:
   Press any key to stop the video capture.

3. **View Results**:
   After stopping the capture, Matplotlib will display the plots showing the hand's position, velocity, and acceleration over time.

