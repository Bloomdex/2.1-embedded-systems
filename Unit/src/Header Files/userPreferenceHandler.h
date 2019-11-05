#ifndef USERPREFERENCEHANDLER_H_
#define USERPREFERENCEHANDLER_H_

#include <avr/io.h>

void initUserPreferenceHandler();

void setUserTempPreference(int8_t newPrefferedTemperature);
int8_t getUserTempPreference();

void setUserLightPreference(int8_t newPrefferedLightIntensity);
int8_t getUserLightPreference();

#endif /* USERPREFERENCEHANDLER_H_ */
