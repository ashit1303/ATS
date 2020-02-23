import cv2 as cv
import numpy as np
import socket
#python3 rcwl.py & python3 pir.py & python3 laser.py & python3 s360.py& python3 s180.py
host = "192.168.43.136" # set to IP address of target computer
#send_rcwl = 8085
#send_pir =8086
send_s360 =8087
send_s180 =8088
send_laser =8089
#send_addr_r = (host, send_rcwl)
#send_addr_p = (host, send_pir)
send_addr_s360 = (host, send_s360)
send_addr_s180 = (host, send_s180)
send_addr_l = (host, send_laser)
UDPSock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize the parameters
confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4   #Non-maximum suppression threshold
inpWidth = 640       #Width of network's input image
inpHeight = 480      #Height of network's input image


# Load names of classes
classesFile = "./data/coco.names";


# Process inputs
winName = 'Detection in OpenCV'
cv.namedWindow(winName, cv.WINDOW_NORMAL)

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.

#acurate version but slow
#modelConfiguration = "./cfg/yolov3.cfg";
#modelWeights = "./weights/yolov3.weights";

#modelConfiguration = "./cfg/tiny-yolo.cfg";
#modelWeights = "./weights/tiny-yolo.weights";

#fast version


modelConfiguration = "./cfg/yolov2-tiny.cfg";
modelWeights = "./weights/yolov2-tiny.weights";



net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

global pers_now 
pers_now = 0
global count 
count = 0
def cal_center(left,top,l,h):
    pct=top+(h/2) #person frame center top
    pcl=left+(l/2) #person frame center left
    #pc=(pct,pcl) #center of person frame
    pl=pcl-(l/4)
    pr=pcl+(l/4)
    pt=pct-(h/4)
    pb=pct+(h/4)
    fcl=320
    fct=240
    if(fcl>pl and fcl<pr and fct<pb and fct>pt):
        global pers_now
        global count
        print("all condn satisfied turn on laser")
        
        data1="laserTrue"
        UDPSock_send.sendto(data1.encode(), send_addr_l)
            
        pers_now=pers_now+1        
    elif (fct<pb and fct>pt):
        print("Height satisfied and stop servo 180")
        #code for moving along the y axis vertically
        if(pcl<fcl):
            if(count==2):
                print("move left")
                data="move_left"
                UDPSock_send.sendto(data.encode(), send_addr_s360)
            count=(count+1)%3    
        else:
            if(count==2):
                print("move right")
                data="move_right"
                UDPSock_send.sendto(data.encode(), send_addr_s360)
            count=(count+1)%3   
    elif(fcl>pl and fcl<pr):
        print("length satisfied and stop servo movement 360")
        #code for moving along the x axis horizontally
        if(pct<fct):
            if(count==2):
                print("move top")
                data="move_top"
                UDPSock_send.sendto(data.encode(), send_addr_s180)
            count=(count+1)%3   
        else:
            if(count==2):
                print("move bottom")
                data="move_bottom"
                UDPSock_send.sendto(data.encode(), send_addr_s180)
            count=(count+1)%3   
    else:
        if(pcl<fcl):
            if(count==2):
                print("move left")
                data="move_left"
                UDPSock_send.sendto(data.encode(), send_addr_s360)
            count=(count+1)%3   
        else:
            if(count==2):
                print("move right")
                data="move_right"
                UDPSock_send.sendto(data.encode(), send_addr_s360)
            count=(count+1)%3   
        if(pct<fct):
            if(count==2):
                print("move top")
                data="move_top"
                UDPSock_send.sendto(data.encode(), send_addr_s180)
            count=(count+1)%5   
        else:
            if(count==4):
                print("move bottom")
                data="move_bottom"
                UDPSock_send.sendto(data.encode(), send_addr_s180)
            count=(count+1)%5   
# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Draw the predicted bounding box
def drawPred(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 135, 161), 3)
    cv.rectangle(frame, (318, 238), (322, 242), (255, 135, 161), 3)
    #cv.rectangle(frame, (0, 50), (323, 244), (255, 135, 161), 3)
    label = '%.2f' % conf
        
    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    #Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
    #cv.rectangle(frame, (left, top )), (left , top), (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)

# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
                #cal_center(left,top,width,height)
                #print(boxes,classIds)
                data=[classIds,boxes]
                data=str(data)
    mul_person(boxes,classIds)
                #UDPSock.sendto(data.encode(), addr)
    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
        #print(box)
def mul_person(boxes,classIds):
    global pers_now   
    no=len(classIds) 
    if( pers_now >= no):
        pers_now=no
    print(pers_now,"current person",no)
    if(pers_now<no and classIds[pers_now]==0):
        print(boxes[pers_now],"boxes[no]")
        lt=boxes[pers_now][0]
        tp=boxes[pers_now][1]
        l=boxes[pers_now][2]
        h=boxes[pers_now][3]
        cal_center(lt,tp,l,h)
    else:
        #send regular rotation
        data="none"
        UDPSock_send.sendto(data.encode(), send_addr_s360)
        
# Webcam input
cap = cv.VideoCapture("http://192.168.43.136:8082/")
#cap = cv.VideoCapture(0)

while cv.waitKey(1) < 0:
    
    # get frame from the video
    hasFrame, frame = cap.read(0)
    frame = cv.flip(frame,1)
    
    # Stop the program if reached end of video
    if not hasFrame:
        print("Done processing !!!")
        cv.waitKey(3000)
        # Release device
        cap.release()
        break

    # Create a 4D blob from a frame.
    blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

    # Sets the input to the network
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers
    outs = net.forward(getOutputsNames(net))
    # Remove the bounding boxes with low confidence
    postprocess(frame, outs)

    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    # Write the frame with the detection boxes
   
    cv.imshow(winName, frame)

UDPSock_send.close()
