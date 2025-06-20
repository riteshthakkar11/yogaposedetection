import cv2 
import mediapipe as mp 
import math
import pyttsx3
engine = pyttsx3.init()




"""import pyttsx3
engine = pyttsx3.init()
engine.say("Hello, how are you?")
engine.runAndWait()"""

print("1.Warrior Pose \n2.Tree Pose \n3.Triangle Pose \n4.Downword Dog Pose \n5.Thunderbolt Pose \n6.Plank Pose \nEnter Choice :")
ch = int(input())
# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

def calculate_angle(a, b, c):
    """Calculate the angle between three points (a, b, c)."""
    a = [a[0] - b[0], a[1] - b[1]]
    c = [c[0] - b[0], c[1] - b[1]]
    
    angle = math.atan2(c[1], c[0]) - math.atan2(a[1], a[0])
    angle = abs(angle)
    
    if angle > math.pi:
        angle = 2 * math.pi - angle
    
    return angle * 180.0 / math.pi

def detect_yoga_pose(landmarks):
    """Match detected landmarks to a predefined yoga pose and give feedback."""
    feedback = ""

    # Example: Checking for Warrior pose (right arm and leg alignment)
    try:
        # Get coordinates for key joints involved in Warrior pose
        shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        index_l = [landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]
        index_r = [landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]
        heel_l = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        heel_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
        legindex_l = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
        legindex_r = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
        
        #shoulder-elbow-wrist
        arm_angle_l = calculate_angle(shoulder_l, elbow_l, wrist_l)
        arm_angle_r = calculate_angle(shoulder_r, elbow_r, wrist_r)
        #hip-knee-ankle
        knee_angle_l = calculate_angle(hip_l, knee_l, ankle_l)
        knee_angle_r = calculate_angle(hip_r, knee_r, ankle_r)
        #shoulder1-shoulder2-elbow
        shol_angle_l = calculate_angle(shoulder_r,shoulder_l, elbow_l)
        shol_angle_r = calculate_angle(shoulder_l,shoulder_r, elbow_r)
        #elbow-wrist-index
        wrist_angle_l = calculate_angle(elbow_l,wrist_l,index_l)
        wrist_angle_r = calculate_angle(elbow_r,wrist_r,index_r)
        #shoulder-hip-ankle
        hip_angle_l= calculate_angle(shoulder_l, hip_l, ankle_l)
        hip_angle_r = calculate_angle(shoulder_r, hip_r, ankle_r)
        #hip-shoulder-wrist
        hsw_angle_l = calculate_angle(hip_l, shoulder_l, wrist_l)
        hsw_angle_r = calculate_angle(hip_r, shoulder_r, wrist_r)
        #shoulder-hip-knee
        shk_angle_l = calculate_angle(shoulder_l, hip_l, knee_l)
        shk_angle_r = calculate_angle(shoulder_r, hip_r, knee_r)
        #legindex-heel-ankle
        lak_angle_l = calculate_angle(legindex_l, ankle_l, knee_l)
        lak_angle_r = calculate_angle(legindex_r, ankle_r, knee_r)



        if(ch == 1) : 
            if shol_angle_l < 160 or shol_angle_r < 160 :
                feedback =engine.say("Straighten your shoulder more")
                engine.runAndWait()
            elif arm_angle_l < 160 or arm_angle_r < 160 :
                feedback =engine.say("Straighten your arms more")
                engine.runAndWait()
            elif knee_angle_l > 160 :
                feedback =engine.say("Bend your left side knee more")
                engine.runAndWait()
            elif shk_angle_l > 140 :
                feedback =engine.say("Bend your left hip more")
                engine.runAndWait()
            elif knee_angle_r < 160 :
                feedback =engine.say("Bend only left knee of yours")
                engine.runAndWait()
            else :
                feedback =engine.say("This is a Warrior Pose")
                engine.runAndWait()

        elif(ch == 2) :
            if arm_angle_l > 70 or arm_angle_r > 70 :
                feedback = "bend your arms more"
            elif wrist_angle_l > 160 or wrist_angle_r > 160 :
                feedback = "bend your wrist more"
            elif knee_angle_r > 160 :
                feedback = "Bend right knee"
            elif knee_angle_r > 90 :
                feedback = "lift your leg higher"
            else :
                feedback = "This is a Tree Pose"

        elif(ch == 3) :
            if arm_angle_l < 160 or arm_angle_r < 160 :
                feedback = "Straighten your arms more"
            elif hip_angle_l > 160 and hip_angle_r > 160 :
                feedback = "bend your hip at one side "
            else :
                feedback = "This is a Triangle Pose"

        elif(ch == 4) :
            if hsw_angle_l < 140 and hsw_angle_r < 140 :
                feedback = "band your shoulder more"
            elif hip_angle_l > 160 and hip_angle_r > 160 :
                feedback = "bend your hip "
            elif knee_angle_l < 160 and knee_angle_r < 160:
                feedback = "Straighten your leg more"
            else :
                feedback = "This is a Downword Dog Pose"

        elif(ch == 5) :
            if knee_angle_l > 30 and knee_angle_r > 30 :
                feedback = "band your knee "
            elif lak_angle_l < 160 and lak_angle_r < 160 :
                feedback = "straighten your heel more "
            elif shk_angle_l > 120 and shk_angle_r > 120 :
                feedback = "bend your hip "
            elif arm_angle_l < 160 and arm_angle_r < 160:
                feedback = "Straighten your arms more"
            else :
                feedback = "This is a Thunderbolt Pose"

        elif(ch == 6) :
            if shk_angle_l < 160  and shk_angle_r < 160 :
                feedback = "Straighten your hip "
            elif knee_angle_l < 160 and knee_angle_r < 160 :
                feedback = "Straighten your leg more"
            elif hsw_angle_l > 90  and hsw_angle_r > 90 :
                feedback = "bend your shoulder "
            elif arm_angle_l < 160 and arm_angle_r < 160 :
                feedback = "Straighten your arms more "  
            else :
                feedback = "This is a Plank Pose"
        else :
            print("invalid choice...")
            exit()

    except Exception as e:
        feedback = "Error detecting pose."

    return feedback

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the image to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get pose landmarks
    results = pose.process(rgb_frame)

    # Draw landmarks on the frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get the list of landmarks
        landmarks = results.pose_landmarks.landmark

        # Provide feedback based on the pose
        feedback = detect_yoga_pose(landmarks)

        # Display feedback on the screen
        cv2.putText(frame, feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
    
    frame = cv2.resize(frame,(1550,720))
    # Show the frame with landmarks and feedback
    cv2.imshow('Yoga Pose Detection', frame)


    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
#engine.runAndWait()