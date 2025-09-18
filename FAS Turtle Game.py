import turtle as t
import time

# ---------- 可调参数 ----------
STEP = 20           # 每次按键移动像素
WINDOW = 0.3                # 统计窗口长度（秒）：最近0.3秒的平均KPS
HUD_POS = (-350, 260)
# ----------------------------


# 画笔与HUD
pen = t.Turtle(visible=True)
pen.shape("turtle")
pen.speed(0)
pen.pensize(2)

hud = t.Turtle(visible=False)
hud.penup()
hud.hideturtle()

screen = t.Screen()
screen.setup(800, 600)
screen.title("FAS Sample")
screen.tracer(False)  # 手动刷新，减少闪烁

# 统计数据
keystamps = []       # 记录每次按键的时间戳
total_keys = 0       # 总按键数
is_drawing = True    # 是否落笔

def record_key():
    """记录一次按键事件（用于速度统计）。"""
    global total_keys
    now = time.time()
    keystamps.append(now)
    total_keys += 1
    # 清理窗口外的旧时间
    cutoff = now - WINDOW
    while keystamps and keystamps[0] < cutoff:
        keystamps.pop(0)

import time
CURRENT_KPS = 0.0  # 当前KPS

start_mhz=1000
def refresh_kps():
    global CURRENT_KPS
    now = time.time()
    cutoff = now - WINDOW
    while keystamps and keystamps[0] < cutoff:
        keystamps.pop(0)
    CURRENT_KPS = len(keystamps) / WINDOW  # 固定用窗口归一化
smallCoreFreqMax = 3200
bigCoreFreqMax   = 4600

coreChoice = 0         # 0=小核, 1=大核
overloadCount   = 0    # 小核顶频计数（触发上切）
underloadCount  = 0    # 大核低载计数（触发下切）

# 迟滞阈值（帧数）：顶频≥N帧才上切；低载≥M帧才下切
SWITCH_UP_FRAMES   = 200
SWITCH_DOWN_FRAMES = 400

# 判定“低载”的门槛：KPS / 频率
LOW_KPS_THRESH   = 2.0
LOW_FREQ_THRESH  = 1400





    
default_frametime=1000   #基准值，0.8ms≈120fps
STEP_MHZ   = 200
STEP_US    = 100
TARGET_US  = 1000            # 1250 FPS = 800 μs
MARGIN_FPS = 10             # FAS 的容忍带(±10 FPS)
MARGIN_US  = 1_000_000 / (1250 - MARGIN_FPS) - 1000 if MARGIN_FPS > 0 else 0




def FAS():
    global default_frametime,CURRENT_KPS,start_mhz,coreChoice,overloadCount,underloadCount
    simulate_frametime=default_frametime+CURRENT_KPS*200
    if simulate_frametime < 1000:
        return simulate_frametime,start_mhz
    else:
        if coreChoice==0:
            coreFreqMax=smallCoreFreqMax
        else:
            coreFreqMax=bigCoreFreqMax
        raw_steps = int((simulate_frametime - 1000) // 100)                # 需求步数
        max_steps = (coreFreqMax - start_mhz) // 200                    # 上限能给的步数
        used_steps = min(raw_steps, max_steps)                   # 受限步数

        nowMhz   = start_mhz + used_steps * 200
        frame_us = simulate_frametime - used_steps * 100  
        if coreChoice == 0 and used_steps == max_steps and (simulate_frametime - 1000) > max_steps * 100:
            overloadCount += 1
        else:
            overloadCount = max(0, overloadCount - 1)

        # —— 大核低载：KPS 低于阈值 → 低载计数+1，否则衰减
        if coreChoice == 1 and CURRENT_KPS < LOW_KPS_THRESH:
            underloadCount += 1
        else:
            underloadCount = max(0, underloadCount - 1)                 # 用受限步数回推
    return frame_us, nowMhz

def generic_Sched():
    simulate = default_frametime + CURRENT_KPS * 200  

    # 选当前核的上限
    coreFreqMax = smallCoreFreqMax 
    if coreChoice == 0:
        coreFreqMax=smallCoreFreqMax
    
    else:
        coreFreqMax=bigCoreFreqMax

    # 一有负载就拉满当前核的上限，否则保持基频
    freq = coreFreqMax if CURRENT_KPS > 0 else start_mhz

    # 供给步数
    supply_steps = max(0, (freq - start_mhz) // 200)

    # 原始帧时 = 负担帧时 - 可抵消的步数 * 100μs
    frame_raw_us = simulate - supply_steps * 100

    return frame_raw_us, freq


def coreAffinity():
    global coreChoice, overloadCount, underloadCount

    # 小核→大核：持续过载才上切
    if coreChoice == 0 and overloadCount >= SWITCH_UP_FRAMES:
        coreChoice = 1
        overloadCount = 0
        underloadCount = 0
        return

    # 大核→小核：持续低载才下切（只看 KPS<4）
    if coreChoice == 1 and underloadCount >= SWITCH_DOWN_FRAMES:
        coreChoice = 0
        overloadCount = 0
        underloadCount = 0
        return

    
    # ==== 功耗模型（相对单位）====
START_MHZ = start_mhz  # 和你已有的一致
P_BASE = 1.0           # 动态功耗基准（缩放系数）
P_LEAK = 0.15          # 静态/漏电功耗（常数项，可调）
ALPHA  = 1.6           # 频率-电压耦合后的总指数，1.3~2.0 之间调

def power_watt(freq_mhz: float) -> float:
    """核别功耗模型：小核泄漏更低、频率指数更小；大核更“贵”"""
    # 小核参数（相对单位）
    P_BASE_S, P_LEAK_S, ALPHA_S = 0.7, 0.10, 1.4
    # 大核参数（相对单位）
    P_BASE_B, P_LEAK_B, ALPHA_B = 1.2, 0.25, 1.8

    scale = max(1e-6, freq_mhz / START_MHZ)
    if coreChoice == 0:
        return P_BASE_S * (scale ** ALPHA_S) + P_LEAK_S
    else:
        return P_BASE_B * (scale ** ALPHA_B) + P_LEAK_B


def energy_per_frame_mJ(freq_mhz: float, frame_us: float) -> float:
    """每帧能耗(毫焦,mJ)。E = P * t"""
    return power_watt(freq_mhz) * (frame_us / 1_000_000.0) * 1000.0

def perf_per_watt(fps: float, power_w: float) -> float:
    """性能/功耗(FPS/W),越大越省电。"""
    return fps / max(power_w, 1e-9)


def update_hud():
    refresh_kps()
    frame_us, now_mhz = FAS()
    coreAffinity()
    frame_us_gen_raw, freq_gen = generic_Sched()

    # —— 计算显示用/统计用（你原来的代码保持不变）——
    DISPLAY_CAP_US = 1000
    frame_us_gen_disp = max(DISPLAY_CAP_US, frame_us_gen_raw)
    frame_us_fas_disp = max(DISPLAY_CAP_US, frame_us)

    fps_fas = 1_000_000 / frame_us_fas_disp if frame_us_fas_disp > 0 else 0.0
    fps_gen = 1_000_000 / frame_us_gen_disp if frame_us_gen_disp > 0 else 0.0

    EPS = 1.0
    frame_us_fas_stat_raw = max(EPS, frame_us)
    frame_us_gen_stat_raw = max(EPS, frame_us_gen_raw)

    frame_us_fas_for_ppw = max(DISPLAY_CAP_US, frame_us_fas_stat_raw)
    frame_us_gen_for_ppw = max(DISPLAY_CAP_US, frame_us_gen_stat_raw)

    P_fas = power_watt(now_mhz)
    P_gen = power_watt(freq_gen)
    E_fas = energy_per_frame_mJ(now_mhz, frame_us_fas_stat_raw)
    E_gen = energy_per_frame_mJ(freq_gen, frame_us_gen_stat_raw)
    PPW_fas = perf_per_watt(1_000_000 / frame_us_fas_for_ppw, P_fas)
    PPW_gen = perf_per_watt(1_000_000 / frame_us_gen_for_ppw, P_gen)

  
    core_max = smallCoreFreqMax if coreChoice == 0 else bigCoreFreqMax

    hud.clear(); hud.goto(*HUD_POS)
    text = (
        f"KPS (近{WINDOW:.0f}s): {CURRENT_KPS:.2f}\n"
        f"FAS策略:     {now_mhz:.0f} MHz | {frame_us_fas_disp:.1f} μs | {fps_fas:.1f} FPS | "
        f"P={P_fas:.2f} | E/帧={E_fas:.3f} mJ | FPS/W={PPW_fas:.1f}\n"
        f"Generic策略: {freq_gen:.0f} MHz | {frame_us_gen_disp:.1f} μs | {fps_gen:.1f} FPS | "
        f"P={P_gen:.2f} | E/帧={E_gen:.3f} mJ | FPS/W={PPW_gen:.1f}\n"
        f"CPU亲和：{'小核' if coreChoice==0 else '大核'} | 当前核上限：{core_max} MHz\n"
        f"over:{overloadCount}/{SWITCH_UP_FRAMES} | under:{underloadCount}/{SWITCH_DOWN_FRAMES}\n"
        f"操作: W/A/S/D移动 · 空格切换落/抬笔 · R重置 · Esc退出"
    )
    hud.write(text, font=("Arial", 12, "normal"))
    screen.update()
    screen.ontimer(update_hud, 8)






# ---- 键位动作 ----
def go_up():
    record_key()
    pen.sety(pen.ycor() + STEP)

def go_down():
    record_key()
    pen.sety(pen.ycor() - STEP)

def go_left():
    record_key()
    pen.setx(pen.xcor() - STEP)

def go_right():
    record_key()
    pen.setx(pen.xcor() + STEP)

def toggle_pen():
    global is_drawing
    record_key()
    if is_drawing:
        pen.penup()
        is_drawing = False
    else:
        pen.pendown()
        is_drawing = True

def reset_all():
    global keystamps, total_keys
    record_key()
    pen.clear()
    pen.penup()
    pen.home()
    if is_drawing:
        pen.pendown()
    keystamps = []
    total_keys = 0

def quit_app():
    t.bye()

# 初始为落笔
pen.pendown()

# 绑定键位（注意：窗口需要焦点）
screen.listen()
screen.onkeypress(go_up, "w")
screen.onkeypress(go_left, "a")
screen.onkeypress(go_down, "s")
screen.onkeypress(go_right, "d")
screen.onkeypress(toggle_pen, "space")
screen.onkeypress(reset_all, "r")
screen.onkeypress(quit_app, "Escape")

# 启动HUD刷新
update_hud()
t.done()






