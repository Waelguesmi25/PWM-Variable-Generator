#include "uart_logger.h"

extern UART_HandleTypeDef huart2;
static uint32_t last_uart_tick = 0;

void UART_Logger_Init(void) {
    last_uart_tick = HAL_GetTick();
}

void UART_Log_Welcome(void) {
    char *msg = "\r\n=== PROJET STM32 - ENIT 2AGE3 ===\r\n"
                "  > Wael GUESMI & Maha ROMDHANI  \r\n"
                "=================================\r\n";
    HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 1000);
}

void UART_Log_Status(uint32_t freq, uint32_t duty) {
    if (HAL_GetTick() - last_uart_tick >= 2000) {
        char buffer[200];
        char jauge[11] = "..........";
        for(int i=0; i < (duty/10) && i < 10; i++) jauge[i] = '|';

        sprintf(buffer, "\r\n[ ETAT ] Freq: %lu Hz | Duty: %lu%% [%s]\r\n",
                freq, duty, jauge);

        HAL_UART_Transmit(&huart2, (uint8_t*)buffer, strlen(buffer), 100);
        last_uart_tick = HAL_GetTick();
    }
}
