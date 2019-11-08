#ifndef ROLLERSHUTTER_H_
#define ROLLERSHUTTER_H_

void setRollerShutterClosed();
void setRollerShutterOpened();
void setRollerShutterAnimating(uint8_t openOrClosed);

void setShutterForceClosed();
void setShutterForceOpened();
void setShutterFreed();
uint8_t getRollerShutterState();

void rollerShutterUpdate(int8_t temperature, int8_t lightIntensity, int8_t prefferedTemperature, int8_t prefferedLightIntensity);

#endif /* ROLLERSHUTTER_H_ */
