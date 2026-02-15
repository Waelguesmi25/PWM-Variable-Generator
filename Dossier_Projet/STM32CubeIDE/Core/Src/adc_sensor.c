#include "adc_sensor.h"

extern ADC_HandleTypeDef hadc1;

void ADC_Sensor_Init(void) {
    // L'initialisation MX_ADC1_Init est appelée ici si déplacée
}

ADC_Data_t ADC_Read_Values(void) {
    ADC_Data_t data = {0};
    uint16_t raw_f = 0, raw_d = 0;

    HAL_ADC_Start(&hadc1);
    if (HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK) {
        raw_f = HAL_ADC_GetValue(&hadc1);
        if (HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK) {
            raw_d = HAL_ADC_GetValue(&hadc1);
        }
    }
    HAL_ADC_Stop(&hadc1);

    data.frequency = 1000 + ((uint32_t)raw_f * 9000) / 4095;
    data.duty_cycle = ((uint32_t)raw_d * 100) / 4095;

    if (data.duty_cycle > 100) data.duty_cycle = 100;
    return data;
}
