const int currentPin = 34; // A2 on FireBeetle
float sensitivity = 0.100; // Change to 0.185 if you have the 5A version

void setup() {
  Serial.begin(115200);
  pinMode(currentPin, INPUT);
  delay(2000);
}

void loop() {
  Serial.println("START_WINDOW");
  
  for (int i = 0; i < 500; i++) {
    int rawValue = analogRead(currentPin);
    float voltage = (rawValue / 4095.0) * 3.3;
    float current = (voltage - 2.5) / sensitivity;
    
    Serial.println(current, 3);
    delay(2);
  }
  
  Serial.println("END_WINDOW");
  delay(3000);
}
