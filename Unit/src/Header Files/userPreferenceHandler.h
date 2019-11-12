#ifndef USERPREFERENCEHANDLER_H_
#define USERPREFERENCEHANDLER_H_

#include <avr/io.h>

void initUserPreferenceHandler();

void setUserTempPreference(int8_t newPrefferedTemperature);
int8_t getUserTempPreference();

void setUserLightPreference(int8_t newPrefferedLightIntensity);
int8_t getUserLightPreference();

void setUserShutterMaxPreference(int8_t newPreferedMaxShutter);
void setUserShutterMinPreference(int8_t newPreferedMinShutter);
int8_t getUserMaxShutterPreference();
int8_t getUserMinShutterPreference();

extern int8_t preferedMinShutter;
extern int8_t preferedMaxShutter;

#endif /* USERPREFERENCEHANDLER_H_ */
