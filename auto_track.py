import argparse
import cv2
import time
from yolo import YOLO
import serial
import uuid
import os



ser = serial.Serial('COM4', 9600) 

isMotorFree = True


time.sleep(2)

cv2.ocl.setUseOpenCL(True)
print("OpenCL Enabled:", cv2.ocl.useOpenCL())  # Should return True

step_distance = 0.07  # The stepper motor moves 1 mm per step (adjust based on your motor)
pixel_to_mm = 0.03  # Each pixel in the image corresponds to 0.1mm in the real world

ap = argparse.ArgumentParser()
ap.add_argument('-n', '--network', default="normal", choices=["normal", "tiny", "prn", "v4-tiny"],
                help='Network Type')
ap.add_argument('-d', '--device', type=int, default=0, help='Device to use')
ap.add_argument('-s', '--size', default=256, help='Size for yolo')
ap.add_argument('-c', '--confidence', default=0.2, help='Confidence for yolo')
ap.add_argument('-nh', '--hands', default=-1, help='Total number of hands to be detected per frame (-1 for all)')
args = ap.parse_args()

if args.network == "normal":
    print("loading yolo...")
    yolo = YOLO("models/cross-hands.cfg", "models/cross-hands.weights", ["hand"])
elif args.network == "prn":
    print("loading yolo-tiny-prn...")
    yolo = YOLO("models/cross-hands-tiny-prn.cfg", "models/cross-hands-tiny-prn.weights", ["hand"])
elif args.network == "v4-tiny":
    print("loading yolov4-tiny-prn...")
    yolo = YOLO("models/cross-hands-yolov4-tiny.cfg", "models/cross-hands-yolov4-tiny.weights", ["hand"])
else:
    print("loading yolo-tiny...")
    yolo = YOLO("models/cross-hands-tiny.cfg", "models/cross-hands-tiny.weights", ["hand"])

yolo.size = int(args.size)
yolo.confidence = float(args.confidence)

print("starting webcam...")
cv2.namedWindow("preview")

vc = cv2.VideoCapture(2)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
vc.set(cv2.CAP_PROP_FPS, 30)

width  = int(vc.get(3))
height = int(vc.get(4))

output_directory = "./videos/"
filename = uuid.uuid4().hex+".avi"

output_file = os.path.join(output_directory, filename)  # Output file name
fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
frame_rate = 15
frame_size = (1920, 1080)  # Frame size (width, height)
# Initialize VideoWriter
out = cv2.VideoWriter(output_file, fourcc, frame_rate, frame_size)

def send_data(data):
    ser.write(f"{data}\n".encode())  # Send data with newline character
    print(f"Sent: {data}")

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

last_frame_time = time.time()
# Function to convert pixel distance to stepper motor steps
def pixels_to_steps(pixel_distance):
    pixel_distance = abs(pixel_distance)
    # Calculate the real-world distance moved (in mm)
    real_distance = pixel_distance * pixel_to_mm  # in mm
    
    # Calculate the number of steps needed
    steps = real_distance / step_distance  # In motor steps
    return int(steps)


def checkSerial():
    if ser.in_waiting > 0:  # Check if data is available
        line = ser.readline().decode('utf-8').strip()  # Read & decode
        if line == "motor free":
            print("motor free")
            print("Received:", line)
            global isMotorFree
            isMotorFree = True
       

while rval:
    
    width, height, inference_time, results = yolo.inference(frame)

    # sort by confidence
    results.sort(key=lambda x: x[2])

    # how many hands should be shown
    hand_count = len(results)
    if args.hands != -1:
        hand_count = int(args.hands)
    
    gpu_frame = cv2.UMat(frame)
    
    # display hands

    checkSerial()
    
    for detection in results[:hand_count]:
        id, name, confidence, x, y, w, h = detection
        
        cx = x + (w / 2)
        cy = y + (h / 2)

        distanceFromCenterX = abs(cx) - width/2
        distanceFromCenterY = abs(cy) - height/2

        if (cx <= (width/2)):
            frameXPos = "left"
            distanceFromCenterX = -abs(distanceFromCenterX)
        else:
            frameXPos = "right"
            distanceFromCenterX = abs(distanceFromCenterX)
        if (cy >= (height/2)):
            frameYPos = "top"
            distanceFromCenterY = -abs(distanceFromCenterY)
        else:
            frameYPos = "bottom"
            distanceFromCenterY = abs(distanceFromCenterY)
        
        
        if isMotorFree == True:
            if round(confidence) >= 0.4:
                if frameXPos == "right":
                    send_data(-1*pixels_to_steps(distanceFromCenterX))
                else:
                    send_data(pixels_to_steps(distanceFromCenterX))
                if frameYPos == "top":
                    send_data(-1*pixels_to_steps(distanceFromCenterY))
                else:
                    send_data(pixels_to_steps(distanceFromCenterY))
                
                isMotorFree = False
            else:
                print("confidence is too low")
                
        
        text2 = str(distanceFromCenterX)+","+str(distanceFromCenterY)
        cv2.circle(frame, (int(width/2), int(height/2)), radius=5, color=(0, 255, 0), thickness=-1)
        # draw a bounding box rectangle and label on the image
        color = (0, 255, 255)
        cv2.circle(frame, (int(cx), int(cy)), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        text = "%s (%s)" % (name, round(confidence, 2))
        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
        cv2.putText(frame, text2, (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
        cv2.line(frame, (int(cx),int(cy)), (int(width/2),int(height/2)), color, 2)
    
    out.write(gpu_frame)
    cv2.imshow("preview", frame)
    rval, frame = vc.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Exit if 'q' is pressed

def endLoop():
    cv2.destroyWindow("preview")
    vc.release()