#ifndef MAIN_H_
#define MAIN_H_

void setup(void);
void init_SCH(void);
void updateSensorData_task(void);
void temperature_task(void);
void light_task(void);
void ledKeyUnit_task(void);
void ledKeyUnitButtonReading_task(void);
void rollerShutter_task(void);
void distance_task(void);
int main(void);

#endif
