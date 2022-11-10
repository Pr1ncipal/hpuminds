#include <Adafruit_NeoPixel.h>

int x;
int NUMPIXELS = 4;
int PIN = 12;

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);

  pixels.begin();
  pixels.clear();
  pixels.show();
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt() - 1;

  pixels.clear();
  pixels.show();

  int i = 0;
  while (i < x) {
    pixels.setPixelColor(i, pixels.Color(255, 0, 0));
    pixels.show();
    i++;
  }
} 
