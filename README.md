# mediapipe-
跟随移动算法。使用 OpenCV + MediaPipe 实现手势捏合拖拽方框的交互 用食指(landmark 8)和拇指(landmark 4)之间的距离判断捏合/张开 捏合时若指尖在方框范围内,可以拖动方框 半透明绿色方框在摄像头画面上渲染 按 ESC 或 q 退出


⚠️ 重要提示:demo5.py 用的是 mp.solutions.hands 这种 旧版 Solutions API。Google 在 mediapipe 0.10.30 之后的版本里移除了 solutions 模块,如果直接 pip install mediapipe(最新版 0.10.35)会报: AttributeError: module 'mediapipe' has no attribute 'solutions'

所以 requirements.txt 里把版本固定在 0.10.21(最后一个稳定支持 solutions API 的版本之一)。README 的 FAQ 里也写明了这一点。
