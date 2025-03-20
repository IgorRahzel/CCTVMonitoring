import cv2
import numpy as np
'''
cap = cv2.VideoCapture('videos/superMarket.mp4')

fps = cap.get(cv2.CAP_PROP_FPS)  # Obtém o FPS do vídeo
delay = int(1000 / fps)  # Calcula o delay adequado

corridor = np.array([[360,0],[540,326],[580,326],[580,0]],np.int32)
corridor = corridor.reshape((-1,1,2))

exit = np.array([[267,326],[268,0],[0,0],[0,326]],np.int32)
exit = exit.reshape((-1,1,2))


register1 = np.array([[269,290],[515,290],[520,326],[269,326]],np.int32)
register1 = register1.reshape(-1,1,2)

register2 = np.array([[270,154],[435,154],[504,282],[270,282]],np.int32)
register2 = register2.reshape(-1,1,2)

register3 = np.array([[270,80],[400,80],[427,143],[270,143]],np.int32)
register3 = register3.reshape(-1,1,2)


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.polylines(frame,[corridor],True,(0,255,255),2)
    cv2.polylines(frame,[exit],True,(255,0,255),2)
    cv2.polylines(frame,[register1],True,(255,255,0),2)
    cv2.polylines(frame,[register2],True,(0,255,0),2)
    cv2.polylines(frame,[register3],True,(0,0,255),2)
    cv2.imshow('frame', frame)
    print(f'frame.shape: {frame.shape}, FPS: {fps}')

    if cv2.waitKey(delay) & 0xFF in [ord('q'), 27]:
        break

cap.release()
cv2.destroyAllWindows()
'''

NumberToArea = {0: 'corridor', 1: 'exit', 2: 'register1', 3: 'register2', 4: 'register3'}
for i in range(len(NumberToArea)):
    print(f'Area: {NumberToArea[i]}')