"""
IoT Absensi Biometrik — VERSI LITE (Demo Lokal)

Eksperimen konsep "2-Layer Anti-Spoofing Attendance" dengan OpenCV murni:

  1. Face Detection   -> memastikan ada ORANG di depan kamera.
  2. Gesture Liveness -> memastikan itu ORANG HIDUP (bukan foto diam), lewat
     gerakan mengangkat tangan di atas posisi wajah.

Versi ini berjalan PENUH LOKAL (tanpa server, tanpa database) sehingga mudah
untuk dicoba, dipelajari, dan dimodifikasi.

Cara pakai:
    pip install -r requirements.txt
    python lite_attendance_demo.py

Tekan Q untuk keluar dari jendela kamera.
"""

import argparse

import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_faces(frame):
    """Deteksi wajah memakai Haar cascade bawaan OpenCV."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.05, minNeighbors=4, minSize=(40, 40)
    )
    return [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in faces]


def build_skin_mask(frame):
    """Segmentasi warna kulit menjadi mask biner (kandidat tangan/badan)."""
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    lower = np.array([0, 135, 85], dtype=np.uint8)
    upper = np.array([255, 180, 135], dtype=np.uint8)
    mask = cv2.inRange(ycrcb, lower, upper)
    mask = cv2.medianBlur(mask, 5)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=1)
    return mask


def hand_raised(frame, face_boxes):
    """True jika ada kontur kulit (tangan) berada DI ATAS wajah."""
    h, w = frame.shape[:2]
    mask = build_skin_mask(frame)

    # Kecualikan area wajah agar wajah tidak salah dikira tangan.
    for (x, y, bw, bh) in face_boxes:
        y0 = max(0, y - int(0.3 * bh))
        y1 = min(h, y + int(1.4 * bh))
        x0 = max(0, x - int(0.3 * bw))
        x1 = min(w, x + int(1.3 * bw))
        mask[y0:y1, x0:x1] = 0

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return False

    face_top = min((y for (x, y, w, h) in face_boxes), default=h)

    for c in sorted(contours, key=cv2.contourArea, reverse=True)[:3]:
        area = cv2.contourArea(c)
        if area < 0.008 * (h * w) or area > 0.5 * (h * w):
            continue
        bottom_y = max(pt[0][1] for pt in c)
        if bottom_y < face_top - 10:
            return True
    return False


def main():
    p = argparse.ArgumentParser(description="Demo lokal absensi biometrik (lite)")
    p.add_argument("--camera", type=int, default=0)
    args = p.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("Error: kamera tidak dapat dibuka.")
        return

    print("Demo Lite — hadapkan wajah, lalu ANGKAT TANGAN sebagai bukti hidup.")
    print("Tekan Q untuk keluar.")
    print("=" * 60)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # Layer 1: deteksi wajah.
        faces = detect_faces(frame)
        face_found = len(faces) > 0
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Layer 2: gestur liveness (angkat tangan).
        raised = hand_raised(frame, faces)

        status = []
        if face_found:
            status.append("WAJAH TERDETEKSI")
        else:
            status.append("WAJAH TIDAK ADA - hadapkan muka")
        if raised:
            status.append("TANGAN TERANGKAT - LIVENESS OK")
        else:
            status.append("ANGKAT TANGAN...")
        if face_found and raised:
            status.append(">>> VERIFIED OK <<<")

        yy = 30
        for line in status:
            cv2.putText(
                frame, line, (20, yy), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 0) if face_found else (0, 0, 255), 2,
            )
            yy += 30

        cv2.imshow("Lite - Face + Hand Liveness", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
