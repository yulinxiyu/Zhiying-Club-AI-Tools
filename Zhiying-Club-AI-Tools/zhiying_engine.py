"""
ZhiyingAI-Engine Core
Developed by Yu Linxi (Zhiying Club)
"""
import os
import cv2
import threading
import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ZhiyingAI")

class BaseProcessor(ABC):
    """插件基类：所有的 AI 处理器都必须继承它"""
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def process(self, frame):
        pass

class VideoWorkflowManager:
    """视频流处理工作流管理器"""
    def __init__(self, source_path, output_dir):
        self.source_path = source_path
        self.output_dir = output_dir
        self.processors = []
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def add_processor(self, processor):
        if isinstance(processor, BaseProcessor):
            self.processors.append(processor)
            logger.info(f"插件已挂载: {processor.name}")

    def _worker(self):
        cap = cv2.VideoCapture(self.source_path)
        if not cap.isOpened():
            logger.error("无法打开视频文件！")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 动态计算经过处理后的视频分辨率
        test_ret, test_frame = cap.read()
        for proc in self.processors:
            test_frame = proc.process(test_frame)
        out_h, out_w = test_frame.shape[:2]

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # 重置帧指针
        
        out_path = os.path.join(self.output_dir, "result.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(out_path, fourcc, fps, (out_w, out_h))

        logger.info(f"开始处理视频: 共 {frame_count} 帧, 目标分辨率: {out_w}x{out_h}")
        
        idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 流水线处理
            for proc in self.processors:
                frame = proc.process(frame)
            
            out.write(frame)
            idx += 1
            if idx % 30 == 0:
                logger.info(f"处理进度: {idx}/{frame_count} 帧 ({(idx/frame_count)*100:.1f}%)")

        cap.release()
        out.release()
        logger.info(f"处理完成！文件已保存至: {out_path}")

    def start(self):
        """开启多线程处理，防止阻塞主程序"""
        logger.info("引擎启动...")
        thread = threading.Thread(target=self._worker)
        thread.start()
        thread.join() # 演示模式下等待线程完成