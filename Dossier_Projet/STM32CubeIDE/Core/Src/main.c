#include "main.h"
#include "adc_sensor.h"
#include "pwm_control.h"
#include "uart_logger.h"

// Les handles restent ici (générés par CubeMX)
ADC_HandleTypeDef hadc1;
TIM_HandleTypeDef htim1;
UART_HandleTypeDef huart2;

int main(void) {
  HAL_Init();
  SystemClock_Config();

  // Initialisation des périphériques (généré par CubeMX)
  MX_GPIO_Init();
  MX_ADC1_Init();
  MX_TIM1_Init();
  MX_USART2_UART_Init();

  // Initialisation de nos modules personnalisés
  PWM_Init();
  UART_Logger_Init();
  UART_Log_Welcome();

  while (1) {
    // 1. Acquisition
    ADC_Data_t sensor = ADC_Read_Values();

    // 2. Actionneur & LEDs
    PWM_Update(sensor.frequency, sensor.duty_cycle);

    // 3. Communication (non-bloquante)
    UART_Log_Status(sensor.frequency, sensor.duty_cycle);

    HAL_Delay(5);
  }
}
