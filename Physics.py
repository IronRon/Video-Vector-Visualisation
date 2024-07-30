import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.4, min_tracking_confidence=0.1)

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:  # If FPS is not determined, set a default value
    fps = 30

hand_centers = []

while True:
    success, frame = cap.read()
    if not success:
        break
    
    RGB_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hand.process(RGB_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Calculate the center of the hand (average of landmarks)
            x_coords = [landmark.x for landmark in hand_landmarks.landmark]
            y_coords = [landmark.y for landmark in hand_landmarks.landmark]
            z_coords = [landmark.z for landmark in hand_landmarks.landmark]

            center_x = np.mean(x_coords) * frame.shape[1]
            center_y = np.mean(y_coords) * frame.shape[0]
            center_z = np.mean(z_coords)  # Z-coordinate is already normalized

            hand_centers.append((center_x, center_y, center_z))

            cv2.circle(frame, (int(center_x), int(center_y)), 5, (0, 255, 0), -1)

            coord_text = f"X: {center_x:.2f}, Y: {center_y:.2f}, Z: {center_z:.4f}"
            cv2.putText(frame, coord_text, (int(center_x) - 20, int(center_y) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) != -1:
        break

cap.release()
cv2.destroyAllWindows()
hand.close()


# Calculate velocity and acceleration from the center points
hand_centers = np.array(hand_centers)
hand_centers_length = len(hand_centers)
if hand_centers_length > 1:
    velocities = np.gradient(hand_centers, axis=0)
    accelerations = np.gradient(velocities, axis=0)    

    times = np.linspace(0, hand_centers_length / fps, hand_centers_length)

    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(times, hand_centers[:, 0], label='X Position')
    plt.plot(times, hand_centers[:, 1], label='Y Position')
    plt.plot(times, hand_centers[:, 2], label='Z Position')
    plt.legend()
    plt.title('Hand Position over Time')

    plt.subplot(3, 1, 2)
    plt.plot(times, velocities[:, 0], label='X Velocity')
    plt.plot(times, velocities[:, 1], label='Y Velocity')
    plt.plot(times, velocities[:, 2], label='Z Velocity')
    plt.legend()
    plt.title('Hand Velocity over Time')

    plt.subplot(3, 1, 3)
    plt.plot(times, accelerations[:, 0], label='X Acceleration')
    plt.plot(times, accelerations[:, 1], label='Y Acceleration')
    plt.plot(times, accelerations[:, 2], label='Z Acceleration')
    plt.legend()
    plt.title('Hand Acceleration over Time')

    plt.tight_layout()
    plt.show()

    plt.ion()

    # Calculate vectors
    vectors = np.diff(hand_centers, axis=0)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    quiver = None

    def update(frame):
        global quiver
        if quiver:
            quiver.remove()  # Remove the existing quiver object
        quiver = ax.quiver(0, 0, 0, velocities[frame, 0], velocities[frame, 1], velocities[frame, 2], color='r', length=1, normalize=True)
        #print(f"Updated Frame {frame}: {velocities[frame, 0]}, {velocities[frame, 1]}, {velocities[frame, 2]}")
        plt.pause(.001) # added pause made the vectors visible
        return quiver,

    # Creating animation
    ani = FuncAnimation(fig, update, frames=len(vectors), interval=100, blit=True)

    plt.show()