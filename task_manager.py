import queue
import threading
from config import TASK_QUEUE_SIZE, DATA_INPUT_FILE, DATA_OUTPUT_FILE

class TaskManager:
    def __init__(self):
        self.task_queue = queue.Queue(maxsize=TASK_QUEUE_SIZE)
        self.lock = threading.Lock()
        self.data_output_file = DATA_OUTPUT_FILE  # 添加输出文件路径

    def load_tasks(self):
        try:
            with open(DATA_INPUT_FILE, 'r') as file:
                data = file.readlines()
                # 将数据分割为小任务
                for i, line in enumerate(data):
                    task = {"id": i, "data": line.strip()}
                    self.task_queue.put(task)
                    print(f"Task {i} added to queue")
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def get_task(self):
        try:
            task = self.task_queue.get(timeout=5)
            return task
        except queue.Empty:
            return None

    def task_done(self):
        self.task_queue.task_done()

    def write_result(self, task_id, result):
        # 添加线程安全的文件写入方法
        with self.lock:
            with open(self.data_output_file, 'a') as file:
                file.write(f"Task {task_id} result: {result}\n")