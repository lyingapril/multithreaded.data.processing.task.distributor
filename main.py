from config import THREAD_COUNT
from task_manager import TaskManager
from worker import Worker

def main():
    task_manager = TaskManager()
    task_manager.load_tasks()

    workers = []
    for _ in range(THREAD_COUNT):
        worker = Worker(task_manager)
        worker.start()
        workers.append(worker)

    # 等待所有任务完成
    task_manager.task_queue.join()

    # 停止所有工作线程
    for worker in workers:
        worker.stop()
    for worker in workers:
        worker.join()

    print("All tasks completed!")

if __name__ == "__main__":
    main()