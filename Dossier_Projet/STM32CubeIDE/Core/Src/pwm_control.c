#include "pwm_control.h"

extern TIM_HandleTypeDef htim1;

void PWM_Init(void) {
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
}

void PWM_Update(uint32_t freq, uint32_t duty) {
    uint32_t arr = (168000000 / freq) - 1;
    uint32_t ccr = ((arr + 1) * duty) / 100;

    __HAL_TIM_SET_AUTORELOAD(&htim1, arr);
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, ccr);

    // Mise à jour des LEDs (PD12, PD13, PD14)
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12, (duty >= 33) ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13, (duty >= 66) ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, (duty >= 95) ? GPIO_PIN_SET : GPIO_PIN_RESET);
}
