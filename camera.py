import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Abrir la cámara en /dev/video5
cap = cv2.VideoCapture('/dev/video5')

# Verificar si la cámara se abre correctamente
if not cap.isOpened():
    print("Error: No se puede abrir la cámara en /dev/video5")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Crear una sola ventana
cv2.namedWindow("Detección de Dedos", cv2.WINDOW_NORMAL)

# Bucle principal de captura
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede recibir el frame")
            break

        # Convertir la imagen a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar la imagen con MediaPipe Hands
        results = hands.process(frame_rgb)

        # Dibujar la detección de manos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Mostrar la imagen en UNA SOLA ventana
        cv2.imshow("Detección de Dedos", frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nInterrupción manual detectada. Cerrando...")

# Cerrar todo correctamente
cap.release()
cv2.destroyAllWindows()
