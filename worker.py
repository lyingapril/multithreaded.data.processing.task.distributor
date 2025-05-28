import threading
from data_processor import DataProcessor
from task_manager import TaskManager

class Worker(threading.Thread):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.data_processor = DataProcessor()
        self.running = True  # 添加线程运行标志

    def run(self):
        while self.running:
            task = self.task_manager.get_task()
            if task is None:
                continue  # 如果没有任务，继续等待
            try:
                result = self.data_processor.process(task["data"])
                self.task_manager.task_done()
                # 将结果写入输出文件
                self.task_manager.write_result(task["id"], result)
                print(f"Task {task['id']} processed by {self.name}")
            except Exception as e:
                print(f"Error processing task {task['id']}: {e}")

    def stop(self):
        self.running = False  # 设置线程停止标志