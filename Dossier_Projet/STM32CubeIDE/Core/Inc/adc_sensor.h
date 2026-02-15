#ifndef ADC_SENSOR_H
#define ADC_SENSOR_H

#include "main.h"

typedef struct {
    uint32_t frequency;
    uint32_t duty_cycle;
} ADC_Data_t;

void ADC_Sensor_Init(void);
ADC_Data_t ADC_Read_Values(void);

#endif
