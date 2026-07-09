#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;

const int SERVO1_PIN = 8;
const int SERVO2_PIN = 9;
const int SERVO3_PIN = 11;

const int SERVO_CENTER = 130;
const int SERVO_MIN = 90;
const int SERVO_MAX = 160;

int target1 = SERVO_CENTER;
int target2 = SERVO_CENTER;
int target3 = SERVO_CENTER;

void setup()
{
    Serial.begin(115200);
    Serial.setTimeout(5);

    servo1.attach(SERVO1_PIN);
    servo2.attach(SERVO2_PIN);
    servo3.attach(SERVO3_PIN);

    servo1.write(SERVO_CENTER);
    servo2.write(SERVO_CENTER);
    servo3.write(SERVO_CENTER);
}

void loop()
{
    if (Serial.available())
    {
        String data = Serial.readStringUntil('\n');

        int c1 = data.indexOf(',');
        int c2 = data.lastIndexOf(',');

        if (c1 != -1 && c2 != -1)
        {
            target1 = data.substring(0, c1).toInt();
            target2 = data.substring(c1 + 1, c2).toInt();
            target3 = data.substring(c2 + 1).toInt();

            target1 = constrain(target1, SERVO_MIN, SERVO_MAX);
            target2 = constrain(target2, SERVO_MIN, SERVO_MAX);
            target3 = constrain(target3, SERVO_MIN, SERVO_MAX);

            servo1.write(target1);
            servo2.write(target2);
            servo3.write(target3);
        }
    }
}