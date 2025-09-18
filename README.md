# Python_CPUScheduler_Game_Demo
🐢 CPU Scheduler Demo: FAS vs Generic

这是一个用 Python + turtle 写的简易 CPU 调度策略可视化模拟器。
它并排对比了两种 CPU 调度逻辑：

  FAS 模式（Frequency-Aware Scheduler）：

  按需逐步提升频率

  有小核/大核的频率上限约束

  过载时切大核，低载时回小核

  追求 能效平衡

Generic 模式（“暴力”调度器）：

  一旦有负载就直接拉满频率

  无视能效，只保证性能

  模拟常见的“Performance Governor”

✨ 功能

🎮 交互式负载：通过键盘 W/A/S/D 控制乌龟 🐢 移动，模拟用户输入负载（核心负载）。

📊 HUD 实时显示：

KPS、总按键数

FAS vs Generic 的频率、帧时、FPS

功耗 (W)、每帧能耗 (mJ)、能效 (FPS/W)

当前运行核（小核/大核）、过载/低载计数

⚡ 能效建模：

小核功耗低，适合轻负载

大核功耗高但性能强

展示两种调度策略下的差异

📖 背景

FAS 模拟了现代操作系统中的 Energy-Aware Scheduling (EAS) 思想：

通过逐步加频、big.LITTLE 切换来平衡性能与能耗

Generic 模拟了最传统的 Performance Governor：

有活就全力冲，简单但能效差
