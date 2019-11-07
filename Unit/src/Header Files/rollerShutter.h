#ifndef ROLLERSHUTTER_H_
#define ROLLERSHUTTER_H_

void setRollerShutterClosed();
void setRollerShutterOpened();
void setRollerShutterAnimating();
void rollerShutterUpdate(int8_t temperature, int8_t lightIntensity, int8_t prefferedTemperature, int8_t prefferedLightIntensity);

#endif /* ROLLERSHUTTER_H_ */
