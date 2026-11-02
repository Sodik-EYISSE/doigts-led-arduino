import time
import math
import cv2
import serial
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

PORT = "COM3"          # port de ton Arduino
VITESSE = 9600         # doit être identique à Serial.begin(9600)
FRAMES_STABLES = 5     # nombre d'images identiques avant de valider un changement


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def compter_doigts(pts):
    n = 0
    for bout, articulation in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if pts[bout].y < pts[articulation].y:
            n += 1
    if distance(pts[4], pts[17]) > distance(pts[2], pts[17]):
        n += 1
    return n


print("Connexion à l'Arduino...")
arduino = serial.Serial(PORT, VITESSE)
time.sleep(2)  # l'Arduino redémarre à l'ouverture du port : on lui laisse le temps
print("Arduino connecté")

options = vision.HandLandmarkerOptions(
    base_options=mp_python.BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
)
detecteur = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
t0 = time.time()

etat = 0          # valeur validée, celle qui est envoyée
candidat = 0      # valeur vue sur l'image courante
compteur = 0      # depuis combien d'images on voit le même candidat

while True:
    ok, img = cap.read()
    if not ok:
        print("Erreur : impossible de lire la caméra")
        break
    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    horodatage = int((time.time() - t0) * 1000)
    resultat = detecteur.detect_for_video(image_mp, horodatage)

    h, w = img.shape[:2]
    n = 0
    if resultat.hand_landmarks:
        pts = resultat.hand_landmarks[0]
        n = compter_doigts(pts)
        for point in pts:
            cv2.circle(img, (int(point.x * w), int(point.y * h)), 5, (0, 255, 0), -1)

    # Filtre de stabilité : on ne valide n que s'il reste identique plusieurs images
    if n == candidat:
        compteur += 1
    else:
        candidat = n
        compteur = 1

    if compteur >= FRAMES_STABLES and candidat != etat:
        etat = candidat
        arduino.write(str(etat).encode())   # envoie le caractère '0' à '5'
        print("Envoyé :", etat)

    cv2.putText(img, f"Doigts: {n}", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    cv2.putText(img, f"Lampes allumees: {etat}", (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 200, 255), 2)

    cv2.imshow("Detection de la main", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

arduino.write(b"0")   # éteint les LED en quittant
arduino.close()
cap.release()
cv2.destroyAllWindows()
print("Programme terminé")