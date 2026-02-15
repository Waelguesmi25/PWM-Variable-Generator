# 🎛️ Variable PWM Generator (STM32F407)

![Language](https://img.shields.io/badge/Language-C-blue)
![Platform](https://img.shields.io/badge/Platform-STM32F407-green)
![Tools](https://img.shields.io/badge/Tools-MATLAB%20%7C%20Python-orange)

## 📖 Overview
This project is a complete embedded system designed to generate a **Pulse Width Modulation (PWM)** signal with variable **Frequency** and **Duty Cycle**. 

The system allows real-time control via analog potentiometers, visualizes the status via onboard LEDs, and sends telemetry data to a PC via **UART**, where it is displayed on a custom **Python Dashboard**.

---

## 🚀 Key Features

* **Dynamic Frequency Control:** Adjustable from **1 kHz to 10 kHz**.
* **Dynamic Duty Cycle Control:** Adjustable from **0% to 100%**.
* **Real-Time Monitoring:** * **Python Dashboard:** Visualizes frequency and duty cycle on a PC.
    * **UART Feedback:** Sends status updates every 2 seconds (Non-blocking).
* **Visual Indicators:** 3 LEDs indicate the duty cycle level (Low, Medium, High).
* **Optimized Firmware:** Uses **ADC Scan Mode** and non-blocking polling mechanics.

---

## 🛠️ System Architecture

### 1. Theoretical Study (MATLAB)
Before implementation, the system was modeled in **MATLAB** to verify the relationship between the timer clock, prescaler, and auto-reload registers ($ARR$).
$$Frequency = \frac{f_{clk}}{(ARR + 1) \times (PSC + 1)}$$

### 2. Embedded Implementation (STM32)
* **Hardware:** STM32F407G-DISC1 Board.
* **Timer 1 (TIM1):** Configured for PWM generation on pin **PE9**.
* **ADC1:** Configured in **Scan Mode** to read two channels sequentially (Potentiometer 1 & 2).
* **UART:** Transmits data to the PC at **115200 baud**.

### 3. Monitoring Dashboard (Python)
A Python script reads the serial data and displays:
* Current Frequency (Hz)
* Current Duty Cycle (%)
* Visual Gauge Bar

---

## 🔌 Pinout Configuration

| Component | Pin | Function |
| :--- | :--- | :--- |
| **Potentiometer 1** | PA1 (ADC1_IN1) | Control Frequency |
| **Potentiometer 2** | PA2 (ADC1_IN2) | Control Duty Cycle |
| **PWM Output** | PE9 (TIM1_CH1) | Signal Output |
| **LED 1** | PD12 | ON if Duty ≥ 33% |
| **LED 2** | PD13 | ON if Duty ≥ 66% |
| **LED 3** | PD14 | ON if Duty ≥ 100% |
| **UART TX** | PA2 | Transmit Data |
| **UART RX** | PA3 | Receive Data |

---

## 💻 How to Run

### 1. Hardware Setup
Connect the potentiometers and the FTDI (UART) module according to the pinout table above.

### 2. Flash the Firmware
1. Open the project in **STM32CubeIDE**.
2. Build the project.
3. Flash the `.elf` file to the STM32F407 board.

### 3. Run the Dashboard
Ensure you have Python installed, then run the dashboard script:
```bash
python dashboard.py


