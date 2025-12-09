[🇨🇳 中文](README.md) | [🇬🇧 English](README_EN.md)

# 🐢 Python_CPUScheduler_Game_Demo
**CPU 调度策略演示：FAS vs ondemand**

这是一个用 **Python + turtle** 编写的简易 **CPU 调度策略可视化模拟器**。  
它并排对比了两种 CPU 调度逻辑：  

---

## ⚙️ 调度策略

### 🟢 FAS 模式（Frametime-Aware Scheduler）
- 以 **帧时间** 作为负载指标动态调整 CPU 频率  
- 在保证流畅体验的前提下降低功耗  
- 追求 **性能与能效的平衡**  

### 🔴 ondemand 模式（“ondemand Governor”）
- 一旦有负载就直接拉满频率  
- 模拟常见的 **ondemand Governor** 策略  

### 🌀 coreAffinity（核心亲和）
- 根据掉帧情况自动选择游戏线程运行的 CPU 核心  
- **小核**：低功耗，适合轻负载  
- **大核**：高性能，适合重负载  
- 在负载高时自动切换到大核，在负载下降时延迟迁回小核  
- 这样既保证突发性能，又能保留缓存 (L1/L2)，减少抖动  

---

## ✨ 功能

- 🎮 **交互式负载**  
  使用 `W/A/S/D` 控制乌龟 🐢 移动，模拟用户输入负载  

- 📊 **HUD 实时显示**  
  - KPS、总按键数  
  - FAS 与 Generic 的频率、帧时、FPS  
  - 功耗 (W)、每帧能耗 (mJ)、能效 (FPS/W)  
  - 当前运行核（小核/大核）、过载/低载计数  

- ⚡ **能效建模**  
  - 小核功耗低，适合轻载  
  - 大核功耗高但性能强  
  - 展示两种调度策略下的差异  

---

## 📖 背景

- **FAS** 模拟了现代操作系统中的 **Energy-Aware Scheduling (EAS)** 思想：  
  通过逐步加频、big.LITTLE 切换来平衡性能与能耗。  

- **ondemand** 模拟了最传统的 **ondemand Governor**：  
  按需快速动态调整CPU频率， 一有cpu计算量的任务，就会立即达到最大频率运行，空闲时间增加就降低频率。  

---

## 🚀 运行方法

1. 确保已安装 **Python 3**  
2. 克隆或下载本项目  
3. 在终端运行：  
   ```bash
   python "FAS Turtle Game.py"
