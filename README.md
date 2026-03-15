## QR Code Attendance System (Python, Windows-Friendly)

This is a **simple QR code–based attendance system** implemented in pure Python.

It lets you:

- **Generate QR codes for users**
- **Scan QR codes using a webcam**
- **Mark attendance with date and time**
- **Prevent duplicate entries for the same user on the same day**
- **Store attendance in a CSV file**

The code is kept small and readable, and it works on **Windows**.

---

### 1. Project Structure

- **`app.py`** – main script with all logic:
  - QR code generation
  - Webcam QR scanning
  - Attendance CSV handling
- **`requirements.txt`** – Python dependencies
- **`attendance.csv`** – created automatically on first run
- **`qrcodes/`** – folder where generated QR image files are stored

---

### 2. Requirements

- **OS**: Windows 10 or later
- **Python**: 3.8+ (64-bit recommended)
- **Webcam**: any basic USB/webcam supported by OpenCV

Python packages (also listed in `requirements.txt`):

- `qrcode`
- `Pillow`
- `opencv-python`

---

### 3. Installation

1. **Open PowerShell** and go to the project folder:

```bash
cd D:\.thumbnails\Desktop\web
```

2. (Optional but recommended) **Create and activate a virtual environment**:

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

If `pip` is not recognized, try:

```bash
python -m pip install -r requirements.txt
```

---

### 4. Running the Application

From the project directory:

```bash
python app.py
```

You will see a simple **text menu**:

1. Generate QR code for a user  
2. Start attendance scanning (webcam)  
3. Exit

---

### 5. Generating QR Codes

Choose **option 1** from the menu.

- Enter:
  - **User ID** (e.g., roll number, employee ID)
  - **Full Name**
- The script will:
  - Create a JSON payload `{"user_id": "...", "name": "..."}`.
  - Generate a QR code image.
  - Save it into the `qrcodes/` folder as `<user_id>.png` (sanitized).

You can then:

- Print this QR code, or
- Display it on a phone screen to scan later.

---

### 6. Taking Attendance via Webcam

Choose **option 2** from the menu.

The script will:

- Open the **default webcam**.
- Continuously look for QR codes in the camera view.
- Decode QR data and expect JSON with `user_id` and `name`.
- **Mark attendance** by appending a row to `attendance.csv`:
  - `user_id, name, date, time`
- **Prevent duplicates per day**:
  - If the same `user_id` was already recorded for today, it will show a
    *"Duplicate today"* message and **not** add a new row.

On-screen:

- A window titled **“QR Attendance - Webcam”** appears.
- Instructions and messages are overlaid on the video.
- **Press `q`** in that window to quit scanning.

If you see:

- `Error: Could not open webcam`  
  Ensure no other app (Teams, Zoom, browser, etc.) is using the camera.

---

### 7. Attendance CSV Format

The file `attendance.csv` is created automatically on first run with header:

```text
user_id,name,date,time
```

Every successful scan adds one row (unless already marked today), for example:

```text
S001,John Doe,2025-12-23,09:15:30
S002,Jane Smith,2025-12-23,09:16:10
```

You can open this file in:

- Excel
- LibreOffice Calc
- Any text editor

---

### 8. Notes and Tips

- **Lighting**: Good lighting helps the camera detect QR codes reliably.
- **QR size**: Print QR codes in a reasonable size (not too small).
- **Distance**: Move the QR closer or farther until the green box appears around it.
- **Performance**: For small teams/classes, this design (simple CSV + in-memory check) is sufficient.

---

### 9. How It Works (Short Technical Overview)

- **QR generation**:
  - Uses `qrcode` and `Pillow` to generate PNG images.
  - Stores user information as a compact JSON string.
- **QR scanning**:
  - Uses `opencv-python`'s built-in `QRCodeDetector`.
  - Detects and decodes QR data from each video frame.
- **Duplicate prevention**:
  - Reads `attendance.csv` and checks if the same `user_id` already has an entry with **today’s date**.
  - If found, it skips adding a new row.

The code is intentionally straightforward so you can modify it easily for:

- Different CSV columns
- Additional user metadata
- Integration with databases or web UIs later



