import numpy
import cv2

cap = cv2.VideoCapture("/home/tharun/Videos/vokoscreenNG-2023-07-02_17-46-56.mkv")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter("test.avi",cv2.VideoWriter_fourcc(*'MJPG'),30,(width,height))

### function to get hour::minutes into milliseconds
def GetmSec(time_stamp):
    minute,seconds = tuple(time_stamp.split(":"))
    return ((int(minute)*60)+(int(seconds)))*1000

# print(GetmSec("00:26"))

summary_points = [("0:03","0:10"),
                  ("0:15","0:20")]

summary_milliseconds = [(GetmSec(points[0]),GetmSec(points[1])) for points in summary_points]
sm_start = [i[0] for i in summary_milliseconds]
sm_end = [i[1] for i in summary_milliseconds]

# print("Total Frame Count : ",cap.get(cv2.CAP_PROP_FRAME_COUNT))

# print("FPS : ",cap.get(cv2.CAP_PROP_FPS))

Flag = False

FrameStamp = int(1000/cap.get(cv2.CAP_PROP_FPS))
SkipFrame = 10
SkipStamp = SkipFrame*FrameStamp
# print(SkipStamp)


while(cap.isOpened()):
    ret,frame = cap.read()
    if ret:
        curr_stamp = cap.get(cv2.CAP_PROP_POS_MSEC)
        if curr_stamp in sm_end:
            print("---------- stop ------------",curr_stamp)
            Flag = False
        if curr_stamp in sm_start:
            Flag = True
        if Flag:
            out.write(frame)
            print("---------------writing------------ ",curr_stamp)    
        elif curr_stamp%SkipStamp == 0:
            out.write(frame)
            print("---------------skipping------------")
            
    if not ret:
        cap.release()
        cv2.destroyAllWindows()
        exit()

