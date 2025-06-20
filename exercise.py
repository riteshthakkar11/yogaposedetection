import cv2
import mediapipe as mp
import math

print("1.Push-ups \n2.Sit-Ups \n3.Squats \nEnter Choice : ")
ch = int(input())
#  Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    # angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    # if angle < 0:
    #     angle += 360
    # return angle
    """Calculate the angle between three points (a, b, c)."""
    a = [a[0] - b[0], a[1] - b[1]]
    c = [c[0] - b[0], c[1] - b[1]]
    
    angle = math.atan2(c[1], c[0]) - math.atan2(a[1], a[0])
    angle = abs(angle)
    
    if angle > math.pi:
        angle = 2 * math.pi - angle
    
    return angle * 180.0 / math.pi
            
# Video capture
cap = cv2.VideoCapture(0)

# Variables for Excercise counting
pushup_count = 0
down = False
situp_count = 0
squat_counter = 0
squat_stage = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Pose
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Draw landmarks
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get landmarks for shoulders and hips
        landmarks = results.pose_landmarks.landmark

        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]

        if (ch == 1) :
            # Calculate average shoulder and hip height
            shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
            elbow_y = (left_elbow.y + right_elbow.y) / 2
            hip_y = (left_hip.y + right_hip.y) / 2

            # Down-Up position
            if elbow_y > shoulder_y + 0.08 and hip_y > shoulder_y + 0.12:  # Down position
                down_position = True
            elif down_position and elbow_y <= shoulder_y + 0.03 and hip_y <= shoulder_y + 0.06:  # Up position
                down_position = False
                pushup_count += 1
            
            # Display pushup count
            cv2.putText(frame, f"Pushups: {pushup_count}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif (ch == 2) :
            # Calculate average knee position
            knee_y = (left_knee.y + right_knee.y) / 2

            # Determine the nose position relative to the knees
            if nose.y > knee_y + 0.1:  # Threshold for "down" position
                down = True
            elif down and nose.y <= knee_y + 0.1:  # Threshold for "up" position
                situp_count += 1
                down = False

            # Display sit-up count
            cv2.putText(frame, f"Sit-ups: {situp_count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif (ch == 3) :

            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            # Calculate the angle between the hip, knee, and ankle
            angle = calculate_angle(hip, knee, ankle)

            # Check squat stage and count squats
            if angle > 160:
                squat_stage = "up"
            if angle < 90 and squat_stage == "up":
                squat_stage = "down"
                squat_counter += 1
            
            # Display Squats count
            cv2.putText(frame, f"Squats: {squat_counter}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        else :
            print("Invalid Choice...")

    # Show the frame
    frame = cv2.resize(frame, (1550, 720))
    cv2.imshow('Excercise Counter', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
