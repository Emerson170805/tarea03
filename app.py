import cv2
import mediapipe as mp
import subprocess

# Iniciar la transmisión desde la Canon
ffmpeg_command = [
    "gphoto2", "--stdout", "--capture-movie",
    "|", "ffmpeg", "-i", "-", "-vcodec", "rawvideo",
    "-pix_fmt", "bgr24", "-f", "v4l2", "/dev/video2"
]

# Ejecutar ffmpeg en segundo plano
ffmpeg_process = subprocess.Popen(" ".join(ffmpeg_command), shell=True)

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Capturar el video desde OpenCV
cap = cv2.VideoCapture("/dev/video2")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir imagen a RGB (MediaPipe usa RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    results = hands.process(rgb_frame)

    # Dibujar las manos detectadas
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Mostrar el video
    cv2.imshow("Detección de Manos", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar todo al salir
cap.release()
cv2.destroyAllWindows()
ffmpeg_process.terminate()
    