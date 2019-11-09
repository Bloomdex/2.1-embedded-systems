#ifndef DATAHANDLER_H_
#define DATAHANDLER_H_

#define TEMPERATURE_POOL_STORAGE_SIZE 20
#define LIGHTINTENSITY_POOL_STORAGE_SIZE 20

void updateSensorData();

int8_t getTemperatureMod();
int8_t getLightIntensityMod();

int8_t getMode(int8_t array[], uint8_t size) ;

#endif /* DATAHANDLER_H_ */
