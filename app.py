import csv
import json
import os
from datetime import datetime

import cv2
import qrcode


ATTENDANCE_FILE = "attendance.csv"
QRCODE_DIR = "qrcodes"


def ensure_directories() -> None:
    """Create required folders and files if they do not exist."""
    if not os.path.isdir(QRCODE_DIR):
        os.makedirs(QRCODE_DIR, exist_ok=True)

    # Ensure CSV file exists with header
    if not os.path.isfile(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "name", "date", "time"])


def generate_qr(user_id: str, name: str) -> str:
    """
    Generate a QR code image for the given user.

    The encoded payload is a small JSON string containing user_id and name.
    Returns the path to the generated image.
    """
    ensure_directories()

    payload = {"user_id": user_id.strip(), "name": name.strip()}
    data = json.dumps(payload, ensure_ascii=False)

    img = qrcode.make(data)

    # Use a safe filename based on the user_id
    safe_id = "".join(c for c in user_id if c.isalnum() or c in ("-", "_"))
    if not safe_id:
        safe_id = "user"

    filename = f"{safe_id}.png"
    path = os.path.join(QRCODE_DIR, filename)
    img.save(path)

    return path


def _has_attendance_today(user_id: str) -> bool:
    """Check if the user already has an attendance entry for today."""
    if not os.path.isfile(ATTENDANCE_FILE):
        return False

    today_str = datetime.now().date().isoformat()

    with open(ATTENDANCE_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("user_id") == user_id and row.get("date") == today_str:
                return True
    return False


def mark_attendance(user_id: str, name: str) -> bool:
    """
    Append attendance for a user if not already marked for today.

    Returns True if a new record was added, False if it was a duplicate.
    """
    ensure_directories()

    if _has_attendance_today(user_id):
        return False

    now = datetime.now()
    date_str = now.date().isoformat()
    time_str = now.strftime("%H:%M:%S")

    with open(ATTENDANCE_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([user_id, name, date_str, time_str])

    return True


def scan_qr_and_mark_attendance() -> None:
    """
    Open the default webcam, scan QR codes, and mark attendance.

    - Press 'q' to quit.
    - When a valid QR code is detected, its user is marked present (if not already marked today).
    """
    ensure_directories()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW helps on Windows
    if not cap.isOpened():
        print("Error: Could not open webcam. Make sure it is connected and not used by another application.")
        return

    detector = cv2.QRCodeDetector()
    print("Scanning for QR codes. Press 'q' in the window to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read from webcam.")
                break

            data, points, _ = detector.detectAndDecode(frame)

            if points is not None:
                # Draw outline around the QR code
                pts = points[0].astype(int)
                for i in range(len(pts)):
                    pt1 = tuple(pts[i])
                    pt2 = tuple(pts[(i + 1) % len(pts)])
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            message = "Show QR code to the camera. Press 'q' to quit."

            if data:
                try:
                    payload = json.loads(data)
                    user_id = str(payload.get("user_id", "")).strip()
                    name = str(payload.get("name", "")).strip()

                    if user_id and name:
                        if mark_attendance(user_id, name):
                            message = f"Attendance marked for {name} ({user_id})."
                            print(message)
                        else:
                            message = f"Duplicate today: {name} ({user_id})."
                            print(message)
                    else:
                        message = "Invalid QR payload (missing user_id or name)."
                except json.JSONDecodeError:
                    message = "Invalid QR content (not JSON)."

            # Put status text on the frame
            cv2.putText(
                frame,
                message,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

            cv2.imshow("QR Attendance - Webcam", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


def main_menu() -> None:
    """Simple text menu for generating QR codes and scanning attendance."""
    ensure_directories()

    while True:
        print("\n=== QR Code Attendance System ===")
        print("1. Generate QR code for a user")
        print("2. Start attendance scanning (webcam)")
        print("3. Exit")

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            user_id = input("Enter user ID (e.g., roll number or employee ID): ").strip()
            name = input("Enter full name: ").strip()

            if not user_id or not name:
                print("User ID and name are required.")
                continue

            path = generate_qr(user_id, name)
            print(f"QR code generated and saved to: {path}")

        elif choice == "2":
            scan_qr_and_mark_attendance()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main_menu()



