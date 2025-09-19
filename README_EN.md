[🇨🇳 中文](README.md) | [🇬🇧 English](README_EN.md)

# 🐢 Python_CPUScheduler_Game_Demo
**CPU Scheduling Demo: FAS vs Generic**

This is a simple **CPU scheduling visualization simulator** written in **Python + turtle**.  
It compares two CPU scheduling strategies side by side:  

---

## ⚙️ Scheduling Strategies

### 🟢 FAS Mode (Frametime-Aware Scheduler)
- Uses **frametime** as the load indicator to adjust CPU frequency dynamically  
- Reduces power consumption while maintaining smooth experience  
- Aims for a balance between **performance and efficiency**  

### 🔴 Generic Mode ("Performance Governor")
- Immediately jumps to maximum frequency once load is detected  
- Ignores efficiency, only guarantees performance  
- Simulates the common **Performance Governor** strategy  

### 🌀 coreAffinity
- Automatically chooses which CPU core the game thread runs on based on frame drops  
- **Little core**: low power, suitable for light workloads  
- **Big core**: high performance, suitable for heavy workloads  
- Switches to big core under sustained heavy load; migrates back to little core with delay when load decreases  
- This ensures burst performance while preserving cache (L1/L2) and reducing jitter  

---

## ✨ Features

- 🎮 **Interactive workload**  
  Use `W/A/S/D` to move the turtle 🐢, simulating user input and CPU load  

- 📊 **Real-time HUD**  
  - KPS (keys per second), total key presses  
  - FAS vs Generic: frequency, frametime, FPS  
  - Power (W), energy per frame (mJ), efficiency (FPS/W)  
  - Current running core (little/big), overload/underload counters  

- ⚡ **Efficiency modeling**  
  - Little core consumes less power, suited for light load  
  - Big core consumes more but delivers higher performance  
  - Shows clear differences between two scheduling strategies  

---

## 📖 Background

- **FAS** simulates the concept of **Energy-Aware Scheduling (EAS)** in modern OS kernels:  
  gradually scaling frequency and switching between big.LITTLE cores to balance performance and energy.  

- **Generic** simulates the traditional **Performance Governor**:  
  straightforward, performance-first, but inefficient.  

---

## 🚀 Run Instructions

1. Make sure **Python 3** is installed  
2. Clone or download this project  
3. Run in terminal:  
   ```bash
   python "FAS Turtle Game.py"
