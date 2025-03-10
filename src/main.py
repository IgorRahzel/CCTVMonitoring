from ultralytics import YOLO
import cv2

video_path = 'videos/SuperMarket.mp4'
#model_path = 'models/yolov8s.pt'
model = YOLO('yolov8l.pt')
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    # Criar uma cópia do frame original para desenhar apenas as detecções de pessoas
    frame_plot = frame.copy()

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])  # Obtém a classe da detecção
            if cls == 0:  # Classe 0 corresponde a 'pessoa' no COCO dataset
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas da bounding box
                conf = box.conf[0]  # Confiança da detecção
                label = f'Pessoa {conf:.2f}'
                
                # Desenha a bounding box no frame
                cv2.rectangle(frame_plot, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame_plot, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('frame', frame_plot)
   
    # close if q, esc or close window button is pressed
    if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
        break

cap.release()
cv2.destroyAllWindows()
