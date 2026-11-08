import serial
import numpy as np
import joblib
import time

# --- 1. Load trained models ---
print("Loading models...")
rf_model = joblib.load('proposed_random_forest.joblib')
label_encoder = joblib.load('label_encoder.joblib')
print("Models loaded successfully.")

# --- 2. Set up Serial ---
SERIAL_PORT = 'COM9'  # CHANGE THIS to your FireBeetle's port (check Arduino IDE Tools > Port)
BAUD_RATE = 115200
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
print(f"Connected to {SERIAL_PORT}")
time.sleep(2)

# --- 3. Feature Extraction (matches Colab) ---
def extract_features(values):
    values = np.array(values)
    return [
        np.mean(values), np.std(values), np.min(values), np.max(values),
        np.sqrt(np.mean(values**2)), np.ptp(values),
        np.median(values), np.percentile(values, 25), np.percentile(values, 75)
    ]

# --- 4. Admission Logic ---
power_estimates = {'0': 1200, '1': 15, '2': 50, '3': 150, '4': 1500, 
                   '5': 1500, '6': 60, '7': 60, '8': 1200, '9': 1000, '10': 500}

def make_decision(predicted_label, current_soc=55):
    predicted_power = power_estimates.get(predicted_label, 400)
    net_available = 490
    if predicted_power <= net_available and current_soc > 40:
        return "ALLOW", predicted_power
    elif predicted_power <= net_available + 400 and current_soc > 30:
        return "DELAY", predicted_power
    else:
        return "REJECT", predicted_power

# --- 5. Main Loop ---
print("Waiting for data from ESP32...")
window_data = []
is_recording = False

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line == "START_WINDOW":
            is_recording = True
            window_data = []
            print("Collecting waveform...", end="")
        elif line == "END_WINDOW":
            is_recording = False
            print(" Done.")
            if len(window_data) == 500:
                features = extract_features(window_data)
                pred_encoded = rf_model.predict([features])[0]
                pred_label = label_encoder.inverse_transform([pred_encoded])[0]
                decision, power = make_decision(pred_label)
                print(f"--> Predicted Class: {pred_label} | Est. Power: {power}W | Decision: {decision}\n")
        elif is_recording:
            try:
                window_data.append(float(line))
            except ValueError:
                pass
except KeyboardInterrupt:
    print("\nExiting.")
    ser.close()