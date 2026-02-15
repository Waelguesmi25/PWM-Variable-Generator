#ifndef PWM_CONTROL_H
#define PWM_CONTROL_H

#include "main.h"

void PWM_Init(void);
void PWM_Update(uint32_t freq, uint32_t duty);

#endif
