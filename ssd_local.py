# Import the necessary library 
from functions import *

# frames counter
cnt = 0
fps = 0

# Open the webcam
cap = cv2.VideoCapture(0)

if len(sys.argv) < 2:
    mode = 'w'
else:
    mode = sys.argv[1]

lst = (cv2.__version__).split('.')
major_name = int(lst[0])
if major_name > 2:
    #define the codec
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
else:
    #define the codec
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
filename = check_filename()
out = cv2.VideoWriter(filename, fourcc, 9.5, (640, 480))

net, transformer, labelmap = load_model()

while (True):
    _, frame = cap.read()
    cnt = cnt + 1
    
    if cnt == 1:
        start = datetime.datetime.now()

    # count 10 frames and calculated the frames per seconds(fps) 
    if cnt == 10:
        end = datetime.datetime.now()
        period = end - start
        fps = 10 / (period.total_seconds())
        cnt = 0
    cv2.putText(frame,
                    "fps : " + str(fps),
                    (0, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (150,0,255),
                    2)

    image = frame.astype(np.float32)/255
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = image[...,::-1]
    transformed_image = transformer.preprocess('data', image)
    net.blobs['data'].data[...] = transformed_image

    # Forward pass.
    detections = net.forward()['detection_out']

    # Parse the outputs.
    det_label = detections[0,0,:,1]
    det_conf = detections[0,0,:,2]
    det_xmin = detections[0,0,:,3]
    det_ymin = detections[0,0,:,4]
    det_xmax = detections[0,0,:,5]
    det_ymax = detections[0,0,:,6]

    # Get detections with confidence higher than 0.6.
    top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.6]

    top_conf = det_conf[top_indices]
    top_label_indices = det_label[top_indices].tolist()
    top_labels = get_labelname(labelmap, top_label_indices)
    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]

    for i in xrange(top_conf.shape[0]):
        xmin = int(round(top_xmin[i] * image.shape[1]))
        ymin = int(round(top_ymin[i] * image.shape[0]))
        xmax = int(round(top_xmax[i] * image.shape[1]))
        ymax = int(round(top_ymax[i] * image.shape[0]))
        score = top_conf[i]
        label = int(top_label_indices[i])
        label_name = top_labels[i]

        if mode =='w':
            if label_name == 'car':
                show_object(frame, label_name, car_width, xmax, xmin, ymax, ymin)
            if label_name == 'person':
                show_object(frame, label_name, person_width, xmax, xmin, ymax, ymin)

            if label_name == 'motorbike':
                show_object(frame, label_name, motorbike_width, xmax, xmin, ymax, ymin)         

            if label_name == 'bus':
                show_object(frame, label_name, bus_width, xmax, xmin, ymax, ymin)

            else :
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (150,0,255), 2)
                cv2.putText(frame,
                            label_name,
                            (xmin, ymin-5),
                            font,
                            1,
                            
                            (150,0,255),
                            2)
        elif mode =='p':
                    C = 94
                    y = 480-ymax
                    theta_i = math.degrees(math.atan((ymax-240)/focal_length))
                    D = C * math.tan(math.radians(90-theta_i))
                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (150,0,255), 2)
                    cv2.putText(frame,
                        "%.2fcm" % D,
                        (xmax, ymax),
                        font,
                        1,
                        (150,0,255),
                        2)
                    cv2.putText(frame,
                        label_name,
                        (xmin, ymin),
                        font,
                        1,
                        (150,0,255),
                        2)

    cv2.imshow('frame', frame)
    
    # Save the images as a video file
    out.write(np.uint8(frame))

    # Press 'q' to stop the program
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        print("quit")
        break

# Clear the buffer
cap.release()
out.release()
cv2.destroyAllWindows()