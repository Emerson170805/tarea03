import cv2
import mediapipe as mp
import numpy as np
import pickle

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Inicializar FaceMesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Archivo para guardar puntos clave
DATASET_FILE = "face_data.pkl"
data_points = []

cap = cv2.VideoCapture(2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convertir imagen a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Dibujar la malla facial
            mp_drawing.draw_landmarks(
                frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            
            # Guardar puntos clave en lista
            face_points = [(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark]
            data_points.append(face_points)
    
    cv2.imshow("Face Mesh", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
face_mesh.close()

# Guardar datos en un archivo para entrenamiento
with open(DATASET_FILE, "wb") as f:
    pickle.dump(data_points, f)

print(f"Datos guardados en {DATASET_FILE}")
