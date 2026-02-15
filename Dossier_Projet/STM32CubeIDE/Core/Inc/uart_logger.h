#ifndef UART_LOGGER_H
#define UART_LOGGER_H

#include "main.h"
#include <stdio.h>
#include <string.h>

void UART_Logger_Init(void);
void UART_Log_Welcome(void);
void UART_Log_Status(uint32_t freq, uint32_t duty);

#endif
