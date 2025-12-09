[🇨🇳 中文](README.md) | [🇬🇧 English](README_EN.md)

# 🐢 Python_CPUScheduler_Game_Demo
**CPU Scheduling Strategy Demo: FAS vs ondemand**

This is a simple **CPU scheduling visualization simulator** built with **Python + turtle**.  
It compares two CPU scheduling logics side by side:

---

## ⚙️ Scheduling Strategies

### 🟢 FAS Mode (Frametime-Aware Scheduler)
- Uses **frametime** as the load indicator to dynamically adjust CPU frequency  
- Aims to reduce power consumption while keeping the experience smooth  
- Seeks a **balance between performance and energy efficiency**  

### 🔴 ondemand Mode (“ondemand Governor”)
- Pushes CPU frequency to the maximum as soon as there is load  
- Simulates the typical behavior of an **ondemand governor**  

### 🌀 coreAffinity (Core Affinity)
- Automatically chooses which CPU core the game thread runs on based on frame drops  
- **Little cores**: low power, suitable for light workloads  
- **Big cores**: high performance, suitable for heavy workloads  
- Under high load it switches to big cores; when load decreases, it delays migrating back to little cores  
- This both ensures burst performance and preserves cache (L1/L2), reducing stutter and jitter  

---

## ✨ Features

- 🎮 **Interactive Load**
  Use `W/A/S/D` to move the turtle 🐢 and simulate user input load.

- 📊 **Real-Time HUD**
  Displays in real time:
  - KPS and total keypress count  
  - Frequency, frametime, and FPS for FAS and ondemand  
  - Power (W), energy per frame (mJ), energy efficiency (FPS/W)  
  - Current running core (little / big), overload and underload counters  

- ⚡ **Energy Efficiency Modeling**
  - Little cores: low power, ideal for light workloads  
  - Big cores: higher power draw but stronger performance  
  - Shows how the two scheduling strategies behave differently under the same interactive load  

---

## 📖 Background

- **FAS** is inspired by **Energy-Aware Scheduling (EAS)** in modern operating systems:  
  it gradually ramps up frequency and switches between big.LITTLE cores to balance performance and power.

- **ondemand** emulates the classic **ondemand governor**:  
  it quickly and dynamically adjusts CPU frequency based on demand—when there is CPU work, it jumps to max frequency; when idle time increases, it lowers the frequency.  

---

## 🚀 How to Run

1. Make sure **Python 3** is installed.  
2. Clone or download this project.  
3. In the terminal, run:  

   ```bash
   python "FAS Turtle Game.py"
