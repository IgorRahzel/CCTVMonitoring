from flask import Flask, Response
import cv2
import numpy as np
from ultralytics import YOLO
from area import area
from videoAnalyzer import videoAnalyzer
from utils import clear_stats_folder
import threading
import time

app = Flask(__name__)

# Global variables
current_frame = None
current_heatmap = None
current_spaghetti = None
frame_lock = threading.Lock()
cap = None
model = None
video_analyzer = None

# Clear stats folder
clear_stats_folder('backend/stats')

# Initialize processing
def initialize_processing():
    global cap, model, video_analyzer, current_frame, current_heatmap, current_spaghetti
    
    # Path to video and model
    video_path = 'backend/videos/SuperMarket.mp4'
    model_path = 'backend/models/best.pt'
    
    # Loading model and video
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    
    # Define áreas
    corridor_vertices = np.array([[267,326],[268,0],[0,0],[0,326]],np.int32)
    exit_vertices = np.array([[360,0],[540,326],[580,326],[580,0]],np.int32)
    register1_vertices = np.array([[269,290],[515,290],[520,326],[269,326]],np.int32)
    register2_vertices = np.array([[270,154],[435,154],[504,282],[270,282]],np.int32)
    register3_vertices = np.array([[270,80],[400,80],[427,143],[270,143]],np.int32)
    
    areasList = [
    area('corridor', color=(0,255,255), vertices=corridor_vertices, actionNames=model.names),
    area('exit', color=(255,0,255), vertices=exit_vertices, actionNames=model.names),
    area('register1', color=(255,255,0), vertices=register1_vertices, actionNames=model.names),
    area('register2', color=(0,255,0), vertices=register2_vertices, actionNames=model.names),
    area('register3', color=(0,0,255), vertices=register3_vertices, actionNames=model.names)
    ]
    
    # Inicializar videoAnalyzer
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_analyzer = videoAnalyzer(areasList, height, width, model.names)


def process_frames():
    global current_frame, current_heatmap, current_spaghetti, cap, model, video_analyzer
    
    frameNumber = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Processar frame com YOLO
        results = model(frame)
        
        # Processar análises
        processed_frame = video_analyzer.processVideo(results, frameNumber, frame)
        heatmap = video_analyzer.createHeatMap(frame.copy())
        spaghetti = video_analyzer.createSpaghetiDiagram(frame.copy())
        
        # Converter para JPEG
        _, frame_buffer = cv2.imencode('.jpg', processed_frame)
        _, heatmap_buffer = cv2.imencode('.jpg', heatmap)
        _, spaghetti_buffer = cv2.imencode('.jpg', spaghetti)
        
        # Atualizar frames globais
        with frame_lock:
            current_frame = frame_buffer.tobytes()
            current_heatmap = heatmap_buffer.tobytes()
            current_spaghetti = spaghetti_buffer.tobytes()
        
        frameNumber += 1
        
    cap.release()

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            with frame_lock:
                if current_frame is None:
                    continue
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')
            time.sleep(0.03)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/heatmap')
def heatmap():
    def generate():
        while True:
            with frame_lock:
                if current_heatmap is None:
                    continue
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + current_heatmap + b'\r\n')
            time.sleep(0.03)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/spaghetti_diagram')
def spaghetti_diagram():
    def generate():
        while True:
            with frame_lock:
                if current_spaghetti is None:
                    continue
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + current_spaghetti + b'\r\n')
            time.sleep(0.03)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    initialize_processing()
    # Iniciar processamento em thread separada
    threading.Thread(target=process_frames, daemon=True).start()
    app.run(debug=True)