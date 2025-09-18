# 🐢 Python_CPUScheduler_Game_Demo
**CPU Scheduler Demo: FAS vs Generic**

A lightweight **CPU scheduling strategy visualization simulator** written in **Python + turtle**.  
It compares two CPU scheduling logics side by side:  

---

## ⚙️ Scheduling Strategies

### 🟢 FAS Mode (Frequency-Aware Scheduler)
- Incrementally scale frequency on demand  
- Respect small-core / big-core frequency limits  
- Switch to big core under overload, fall back to small core under light load  
- Aims for **performance–power balance**  

### 🔴 Generic Mode (“Brute-force Governor”)
- Immediately ramp to maximum frequency once load is detected  
- Ignores efficiency, only guarantees performance  
- Simulates the traditional **Performance Governor**  

---

## ✨ Features

🎮 **Interactive workload**  
- `W/A/S/D` → Move the turtle 🐢, simulating user input load  

📊 **Real-time HUD**  
- KPS (keystrokes per second), total key count  
- FAS vs Generic frequency, frame time, FPS  
- Power (W), energy per frame (mJ), performance per watt (FPS/W)  
- Current core (small/big), overload/underload counters  

⚡ **Energy modeling**  
- Small core = low power, efficient for light workloads  
- Big core = higher power, strong performance  
- Visualizes trade-offs between the two scheduling strategies  

---

## 📖 Background

- **FAS** simulates the idea of **Energy-Aware Scheduling (EAS)** in modern OS kernels:  
  incrementally scaling frequency and switching between big.LITTLE cores to balance performance and efficiency.  

- **Generic** simulates the classic **Performance Governor**:  
  always go max frequency under load—simple but inefficient.  

---

## 🚀 How to Run

1. Make sure **Python 3** is installed  
2. Clone or download this repository  
3. Run:  
   ```bash
   python fas_demo.py
