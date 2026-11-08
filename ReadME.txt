WSN Capstone Project - D2: Edge-ML Predictive Load Admission
Overview
This repository contains the source code, trained models, and artifacts for Deliverable 2 (D2) of the Wireless Sensor Networks Capstone Project.

The goal of this project is to build an Edge-ML load-admission controller for small solar-battery systems. The system reads the turn-on current signature of an appliance, classifies it using machine learning, and makes a decision to ALLOW, DELAY, or REJECT the load to protect the battery.

Because of the memory constraints of the ESP32, this prototype uses a Gateway Architecture:

The ESP32 senses the current and streams raw data over USB Serial.

A Python script on a laptop (the Gateway) extracts features, runs the Random Forest model, and makes the admission decision.

Repository Contents
sensor_node.ino: The Arduino code for the ESP32 (DFRobot FireBeetle). It reads the ACS712 current sensor and streams 500-sample waveforms over Serial at 115200 baud.

gateway.py: The Python script that runs on the laptop. It reads the Serial data, calculates 9 statistical features, loads the trained Random Forest model, and prints the final ALLOW/DELAY/REJECT decision.

proposed_random_forest.joblib: The trained Random Forest model (89.59% accuracy on the PLAID dataset).

baseline_decision_tree.joblib: The baseline Decision Tree model (76.95% accuracy on the PLAID dataset).

label_encoder.joblib: The Label Encoder used to map predictions back to appliance classes.

Copy_of_Untitled14.ipynb: The Colab notebook used for dataset preprocessing, feature extraction, model training, and evaluation.

images/: Contains the breadboard prototype photo and the terminal output screenshot.

Hardware Requirements
DFRobot FireBeetle ESP32 (DFR0478)

ACS712 Current Sensor (5A or 20A version)

5V Relay Module

9V Battery and DC Motor (representing the load)

Breadboard and Jumper Wires

How to Run the Prototype
Step 1: Upload the ESP32 Code
Open sensor_node.ino in the Arduino IDE.

Select ESP32 Dev Module as the board and the correct COM port.

Upload the code to the FireBeetle.

Step 2: Run the Python Gateway
Ensure you have Python installed on your laptop.

Install the required libraries:

bash
pip install pyserial numpy scikit-learn joblib
Open gateway.py and change the SERIAL_PORT variable to match your ESP32's port (e.g., COM9 or /dev/ttyUSB0).

Run the script:

bash
python gateway.py
Step 3: Observe the Output
When the ESP32 sends a waveform, the Python script will print the predicted appliance class and the admission decision:

text
Collecting waveform... Done.
--> Predicted Class: 1 | Est. Power: 15W | Decision: ALLOW
Results & Limitations
Accuracy: The Random Forest model achieves 89.59% accuracy on the PLAID dataset (AC appliances).

Domain Mismatch: The model was tested live on a DC motor. Because it was trained on AC appliances, it consistently misclassified the DC motor as class '1' (CFL). This highlights the need for domain-specific training data in future work.

Virtual PV/SOC: The battery and solar values are simulated in the Python script to demonstrate the admission logic.

Team
Joseph Walusimbi (2401600068)

Ritah Kobusingye (2401600224)

Patience Clare Esaete (2401600415)

Course: Wireless Sensor Networks Capstone, Year 3 Semester 2, 2026/27
Institution: Soroti University

