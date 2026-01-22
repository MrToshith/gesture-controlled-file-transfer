import cv2
import mediapipe as mp
import requests
import time

# API Endpoint
SERVER_URL = "http://localhost:8000/transfer"

# MediaPipe Setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Logic Variables
last_action = "none" # "grab", "release", "none"
last_action_time = 0
COOLDOWN = 1.0 # Seconds between actions to prevent spamming

def send_action(action):
    try:
        print(f"Sending action '{action}' to {SERVER_URL}...")
        resp = requests.post(SERVER_URL, json={"action": action})
        print(f"Sent action: {action}. Server replied: {resp.status_code} {resp.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send action: {e}")

def main():
    global last_action, last_action_time

    cap = cv2.VideoCapture(0)
    
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Flip for selfie view
            image = cv2.flip(image, 1)
            
            # Convert to RGB
            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            # Draw
            image.flags.writeable = True
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            current_gesture = "none"

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS)
                    
                    # Simple Gesture Recognition
                    # Landmark 0 is wrist
                    # Landmark 8 is index finger tip
                    # Landmark 12 is middle finger tip
                    # Landmark 16 is ring finger tip
                    # Landmark 20 is pinky tip
                    # Landmark 9 is middle finger mcp (knuckle)
                    
                    # Check if fingers are curled (tip below middle knuckle) is a rough approximation of a fist
                    # Adjust logic for robustness as needed.
                    # A simple heuristic: 
                    # Open hand: Tips are far from wrist.
                    # Fist: Tips are close to palm/wrist.

                    # Let's use specific landmarks to determine open/closed
                    # Index (8), Middle (12), Ring (16), Pinky (20)
                    # PIP joints (knuckles in middle of finger): 6, 10, 14, 18
                    # MCP joints (base knuckles): 5, 9, 13, 17
                    
                    # Logic: If finger tip is below (y-value higher) than the PIP joint, it's curled.
                    # Note: Y coordinates increase downwards in image.
                    
                    # Create a list of (Tip, PIP) pairs
                    fingers = [
                        (8, 6), (12, 10), (16, 14), (20, 18)
                    ]
                    
                    curled_count = 0
                    for tip_idx, pip_idx in fingers:
                        # Compare Y coordinates. Tip > PIP means curled (downwards)
                        # However, hand orientation matters. 
                        # A better check involves distance to wrist (0).
                        
                        # Distance specific check
                        tip = hand_landmarks.landmark[tip_idx]
                        wrist = hand_landmarks.landmark[0]
                        mcp = hand_landmarks.landmark[pip_idx - 1] # 5, 9, 13, 17

                        # Calculate distance between tip and wrist
                        dist_tip_wrist = ((tip.x - wrist.x)**2 + (tip.y - wrist.y)**2)**0.5
                        dist_mcp_wrist = ((mcp.x - wrist.x)**2 + (mcp.y - wrist.y)**2)**0.5
                        
                        # If tip is closer to wrist than mcp is to wrist, it is closed
                        # This is a robust-ish heuristic for general "grabbing" pose relative to hand size
                        if dist_tip_wrist < dist_mcp_wrist * 1.2: # Add tolerance
                            curled_count += 1

                    if curled_count >= 3:
                        current_gesture = "grab"
                    elif curled_count <= 1:
                        current_gesture = "release"
                    
                    # Visualize
                    cv2.putText(image, f"Gesture: {current_gesture}", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # State Machine for Actions
            # Only trigger on change, with cooldown
            current_time = time.time()
            if current_time - last_action_time > COOLDOWN:
                # Capture "Grab"
                if current_gesture == "grab" and last_action != "grab":
                    send_action("grab")
                    last_action = "grab"
                    last_action_time = current_time
                
                # Reset local state if hand is opened, but DO NOT send release to server
                # The phone handles the release.
                elif current_gesture == "release" and last_action == "grab":
                    last_action = "none" 
                    # send_action("release") <--- Removed
                    
            # Visual Feedback
            if last_action == "grab":
                 cv2.putText(image, "STATUS: GRABBED!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                 cv2.putText(image, "STATUS: READY", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if cv2.waitKey(5) & 0xFF == 27:
                break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
