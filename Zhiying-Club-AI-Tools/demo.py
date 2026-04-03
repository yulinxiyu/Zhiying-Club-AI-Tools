"""
ZhiyingAI-Engine 快速启动演示
"""
import os
import cv2
import numpy as np
from zhiying_engine import VideoWorkflowManager
from processors.plugins import FrameEnhancer, CartoonStyleProcessor

def create_test_video(filename="input.mp4"):
    """自动生成测试视频，确保开箱即用"""
    print(f"[*] 未检测到测试视频，正在自动生成 {filename} ...")
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
    for i in range(90):  # 生成 3 秒的视频
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # 画一个移动的彩色圆圈
        x = 320 + int(200 * np.sin(i * 0.1))
        cv2.circle(frame, (x, 240), 80, (0, 150, 255), -1)
        cv2.putText(frame, "Zhiying Club AI Test", (150, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        out.write(frame)
    out.release()
    print("[*] 测试视频生成完毕！\n")

if __name__ == "__main__":
    print("="*40)
    print(" 🚀 欢迎使用 ZhiyingAI-Engine v1.0")
    print("="*40)

    # 1. 确保有输入视频
    if not os.path.exists("input.mp4"):
        create_test_video("input.mp4")

    # 2. 初始化引擎
    manager = VideoWorkflowManager(source_path="input.mp4", output_dir="./output")

    # 3. 挂载插件库 (先放大，再转成卡通画风)
    manager.add_processor(FrameEnhancer(scale_factor=1.5))
    manager.add_processor(CartoonStyleProcessor())

    # 4. 启动！
    manager.start()