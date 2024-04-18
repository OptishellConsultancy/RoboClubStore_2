

#define LED_1 23

#define soundSensor 15 // Analog input pin that the Sensor is attached to

/* boolean variables to hold the status of the pins*/

bool ledPin1Status;

void setup() {

  pinMode(LED_1, OUTPUT);

  pinMode(soundSensor, INPUT);

  Serial.begin(9600);// initialize serial communications at 9600 bps:

}

void loop() {

  int sensorValue = analogRead(soundSensor);

  Serial.println(sensorValue);

  if (sensorValue < 3500)
{
    ledPin1Status = 1;
}

  if (ledPin1Status == 1)
  {

    if (sensorValue > 555 || sensorValue < 537  )
    {
      digitalWrite(LED_1, HIGH);
    }


    delay(200);

    ledPin1Status = 0;

  }

  digitalWrite(LED_1, LOW);



}
