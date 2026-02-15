================================================================================
                    PINOUT CONFIGURATION - STM32F407
                    Projet Génération PWM Variable
================================================================================
			RÉSUMÉ DU PROJET
================================================================================
Ce système embarqué génère un signal PWM variable sur STM32F407 avec:
  • 2 potentiomètres analogiques contrôlant fréquence (1-10 kHz) et duty (0-100%)
  • 1 sortie PWM principale sur PE9 (TIM1_CH1)
  • 3 LEDs indicatrices pour visualiser le niveau duty cycle
  • Communication UART (115200 baud) pour monitoring temps réel
  • Mise à jour dynamique instantanée sans interruptions
  • Gestion non-bloquante via polling ADC et HAL_GetTick()

Caractéristiques Clés:
  ✓ Horloge système: 168 MHz (PLL from 8 MHz HSE)
  ✓ Résolution ADC: 12 bits (4096 niveaux)
  ✓ Mode ADC: Scan Mode (2 canaux séquentiels)
  ✓ Timer PWM: Prescaler = 0 (précision maximale)
  ✓ Affichage UART: Toutes les 2 secondes en non-bloquant
  ✓ LEDs: Progressive indication à 33%, 66%, 100% duty

================================================================================
                         ADC INPUT PINS
================================================================================

Pin          | GPIO Port  | Pin Number | ADC Channel | Function
---------|------------|------------|-------------|----------------------------------
POT_FREQ     | GPIOA      | PIN 0      | ADC_CHANNEL_0   | Contrôle Fréquence PWM (1-10 kHz)
POT_DUTY     | GPIOA      | PIN 1      | ADC_CHANNEL_1   | Contrôle Rapport Cyclique (0-100%)

Mode ADC: Scan Mode (ENABLE) - 2 Canaux
Résolution: 12 bits (0-4095)
Sampling Time: 84 cycles

================================================================================
                         TIMER PWM OUTPUT PINS
================================================================================

Pin          | GPIO Port  | Pin Number | Timer      | Channel | Function
---------|------------|------------|-----------|---------|----------------------------------
PWM_OUT      | GPIOE      | PIN 9      | TIM1       | CH1     | Sortie PWM Principale
                                                              | Fréquence: 1-10 kHz
                                                              | Duty: 0-100%

Timer Config:
  - Prescaler: 0 (Précision maximale)
  - Mode: PWM1
  - OCMode: TIM_OCMODE_PWM1
  - Polarity: TIM_OCPOLARITY_HIGH
  - AutoReload: ENABLED (TIM_AUTORELOAD_PRELOAD_ENABLE)

================================================================================
                         GPIO OUTPUT PINS (LEDs)
================================================================================

Pin          | GPIO Port  | Pin Number | Function                 | Logic
---------|------------|------------|---------------------------|----------
LED1         | GPIOD      | PIN 12     | Indicateur Duty ≥ 33%    | HIGH = ON
LED2         | GPIOD      | PIN 13     | Indicateur Duty ≥ 66%    | HIGH = ON
LED3         | GPIOD      | PIN 14     | Indicateur Duty = 100%    | HIGH = ON

Mode GPIO: Output Push-Pull (GPIO_MODE_OUTPUT_PP)
Pull: No Pull (GPIO_NOPULL)
Speed: Low Speed (GPIO_SPEED_FREQ_LOW)
Initial State: All LOW (GPIO_PIN_RESET)

================================================================================
                       UART COMMUNICATION PINS
================================================================================

Pin          | GPIO Port  | Pin Number | Interface  | Function
---------|------------|------------|-----------|----------------------------------
UART_TX      | GPIOA      | PIN 2      | UART2      | Transmission (115200 baud)
UART_RX      | GPIOA      | PIN 3      | UART2      | Réception (115200 baud)

UART Config:
  - BaudRate: 115200
  - WordLength: 8 bits
  - StopBits: 1
  - Parity: None
  - Mode: TX & RX
  - HardwareFlow: None
  - Oversampling: 16

================================================================================
                      COMPLETE PINOUT SUMMARY
================================================================================

GPIOA (Entrées & Communication):
  PIN 0  → ADC1_CHANNEL_0   → Potentiomètre Fréquence
  PIN 1  → ADC1_CHANNEL_1   → Potentiomètre Duty Cycle
  PIN 2  → UART2 TX         → Transmission UART
  PIN 3  → UART2 RX         → Réception UART

GPIOD (LEDs):
  PIN 12 → GPIO Output      → LED1 (Duty ≥ 33%)
  PIN 13 → GPIO Output      → LED2 (Duty ≥ 66%)
  PIN 14 → GPIO Output      → LED3 (Duty ≥ 95%)

GPIOE (PWM Output):
  PIN 9  → TIM1_CH1         → Signal PWM Principal

GPIOH (System):
  Horloge: HSE (8 MHz) → PLL (M=8, N=336, P=2) → 168 MHz

================================================================================
                      SYSTEM CLOCK CONFIGURATION
================================================================================

Clock Source: External HSE (8 MHz)
PLL Parameters:
  - PLLM: 8     (Division factor)
  - PLLN: 336   (Multiplication factor)
  - PLLP: 2     (Main PLL division factor)
  - PLLQ: 7     (USB OTG FS clock division)

System Clock: 168 MHz
APB1 Clock: 42 MHz (UART2, TIM1)
APB2 Clock: 84 MHz

================================================================================
                      CODE VARIABLES MAPPING
================================================================================

ADC Values:
  adc_freq_raw  → Valeur brute ADC Fréquence (0-4095)
  adc_duty_raw  → Valeur brute ADC Duty Cycle (0-4095)

Calculated Values:
  frequency_hz  → Fréquence calculée (1000-10000 Hz)
  duty_percent  → Rapport cyclique calculé (0-100%)

Timer Registers:
  timer_arr     → Auto-Reload Register (Période PWM)
  timer_ccr     → Capture/Compare Register (Duty Cycle PWM)

UART Output:
  uart_buffer   → Buffer pour transmission (300 bytes)
  last_uart_tick→ Timestamp dernière transmission UART

================================================================================
                      PERIPHERAL INITIALIZATION ORDER
================================================================================

1. SystemClock_Config()    → Configure PLL 168 MHz
2. MX_GPIO_Init()          → Initialize GPIO ports (A, D, E, H)
3. MX_ADC1_Init()          → Configure ADC1 (2 channels, scan mode)
4. MX_TIM1_Init()          → Configure TIM1 PWM
5. MX_USART2_UART_Init()   → Configure UART2

Main Loop Operations:
  ├─ Read ADC (2 channels) via polling
  ├─ Calculate frequency & duty cycle
  ├─ Update TIM1 ARR & CCR registers
  ├─ Update LED states
  └─ Send UART status (every 2 seconds)

================================================================================
                      CONVERSION FORMULAS (CODE)
================================================================================

Frequency Conversion:
  frequency_hz = FREQ_MIN + ((uint32_t)adc_freq_raw * (FREQ_MAX - FREQ_MIN)) / 4095
  Where: FREQ_MIN = 1000, FREQ_MAX = 10000

Duty Cycle Conversion:
  duty_percent = ((uint32_t)adc_duty_raw * 100) / 4095

Timer ARR Calculation:
  timer_arr = (SYSCLOCK / frequency_hz) - 1
  Where: SYSCLOCK = 168000000

Timer CCR Calculation:
  timer_ccr = ((timer_arr + 1) * duty_percent) / 100

LED Activation Conditions:
  LED1 (PD12): ON if duty_percent >= 33
  LED2 (PD13): ON if duty_percent >= 66
  LED3 (PD14): ON if duty_percent >= 95 (Note: in code it's >= 100, not >= 95)

================================================================================
                      ELECTRICAL SPECIFICATIONS
================================================================================

Logic Level: 3.3V
ADC Input Range: 0V - 3.3V
GPIO Output Current: Max 25 mA per pin
Total GPIO Current: Max 200 mA
PWM Output (PE9): 3.3V logic level

Timer Clock: 168 MHz (No Prescaler)
ADC Clock: 42 MHz (PCLK2 / 4)
UART Clock: 42 MHz (PCLK1)

================================================================================
                      IMPORTANT CODE NOTES
================================================================================

✓ ADC Mode: Scan enabled for sequential reading of 2 channels
✓ Non-blocking: Polling with 10ms timeout, HAL_ADC_Stop() always called
✓ PWM Update: Real-time update of ARR & CCR without interrupts
✓ LED Control: Update_LEDs() function for progressive LED indication
✓ UART: 2-second non-blocking transmission using HAL_GetTick()
✓ Safety: Bounds checking for frequency and duty cycle values
✓ Visual Feedback: ASCII gauge bar in UART output

================================================================================
                            END OF PINOUT
================================================================================
