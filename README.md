# Hand Pinch & Drag Demo (手势捏合拖拽方框)

基于 OpenCV + MediaPipe Hands 实现的一个有趣的实时摄像头交互 Demo:
用 **食指与拇指做"捏合"手势**,可以抓起画面中的绿色方框,并通过手指移动把它拖到屏幕任意位置。

## 效果说明

- 摄像头画面中显示一个半透明的绿色方框(初始位置 `(100, 100)`,大小 `100x100`)
- 实时检测手部 21 个关键点,并在画面上绘制骨架
- 在食指指尖(landmark 8)位置绘制一个红色圆圈作为光标
- 当 **食指与拇指(landmark 4)之间的距离 < 30 像素** 时判定为"捏合"
- 捏合状态下,若指尖位于方框内,则进入"抓起"状态,方框跟随指尖移动
- 松开(距离 ≥ 30)即放下方框

> 因为最终显示时又做了一次 `cv.flip(image, 1)`,所以视觉上是镜像的(像照镜子一样),交互逻辑更直观。

## 核心原理

```
1. 用 MediaPipe Hands 识别手部 21 个关键点
2. 取 食指指尖(landmark 8) 与 拇指指尖(landmark 4) 的坐标
3. 用 math.hypot(dx, dy) 计算两点欧氏距离
4. 距离 < 30 → 视为"捏合",进入激活态
5. 激活态下记录指尖与方框左上角的偏移 L1/L2
6. 后续每帧把方框左上角更新为 (指尖 - 偏移),实现拖拽
7. 用 cv.addWeighted 实现方框的半透明叠加效果
```

## 环境要求

- Python 3.8 ~ 3.11(MediaPipe 旧版 solutions API 对 Python 版本较敏感)
- 一个可用的摄像头
- Windows / macOS / Linux 均可

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python demo5.py
```

程序启动后会弹出名为 `win1` 的窗口,显示摄像头画面。
按 **ESC** 或 **q** 退出程序。

## 操作提示

- 手部请保持在摄像头视野内,光线充足效果更佳
- 食指和拇指做出"OK / 捏合"手势即可抓取方框
- 单手即可操作,无需双手
- 若识别不到手部,可以把整只手露出来,让 MediaPipe 完成首次检测

## 文件结构

```
day06-teacher/
├── demo5.py            # 主程序:手势捏合拖拽方框
├── README.md           # 本说明文档
├── requirements.txt    # 依赖列表
├── 1.py / 3.py         # 课堂其他示例
└── *.png               # 教学插图
```

## 常见问题

**Q: 运行时报 `AttributeError: module 'mediapipe' has no attribute 'solutions'`**
A: 你安装的 `mediapipe` 版本过高(≥ 0.10.30 已移除 solutions API)。请按 `requirements.txt` 中指定的版本重新安装:
`pip install "mediapipe==0.10.21"`

**Q: 摄像头打不开**
A: 检查系统是否允许 Python/终端访问摄像头;或修改 `cv.VideoCapture(0)` 中的索引,例如改为 `1`、`2`。

**Q: 帧率很卡**
A: 可把 `model_complexity=0` 保持为 0(已经是最快);并降低摄像头分辨率:
```python
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
```

## 技术栈

- [OpenCV](https://opencv.org/) — 摄像头采集、图像绘制、窗口显示
- [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) — 手部 21 关键点检测
- [NumPy](https://numpy.org/) — MediaPipe 依赖