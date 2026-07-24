import threading
import time
import queue
from datetime import datetime

class BackgroundWorker(threading.Thread):
    def __init__(self, task_queue, results_queue, worker_id):
        super().__init__(daemon=True, name=f"BackgroundWorker-{worker_id}")
        self.task_queue = task_queue
        self.results_queue = results_queue
        self.is_running = True

    def run(self):
        while self.is_running:
            try:
                # Wait for a task
                task = self.task_queue.get(timeout=2)
                
                print(f"[WORKER-{self.name}] Ejecutando tarea: {task.get('name')}")
                
                # Simulate work or execute actual function
                func = task.get('func')
                args = task.get('args', ())
                kwargs = task.get('kwargs', {})
                
                try:
                    if func:
                        result = func(*args, **kwargs)
                    else:
                        # Dummy learning loop simulation
                        time.sleep(task.get('duration', 5))
                        result = f"Tarea {task.get('name')} completada con éxito."
                        
                    self.results_queue.put({
                        'task_id': task.get('id'),
                        'name': task.get('name'),
                        'status': 'success',
                        'result': result,
                        'completed_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    self.results_queue.put({
                        'task_id': task.get('id'),
                        'name': task.get('name'),
                        'status': 'error',
                        'error': str(e),
                        'completed_at': datetime.now().isoformat()
                    })
                    
                self.task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[WORKER-{self.name}] Error general: {e}")

class MultitaskingEngine:
    def __init__(self, num_workers=2):
        self.task_queue = queue.Queue()
        self.results_queue = queue.Queue()
        self.workers = []
        self.task_counter = 0
        
        # Start workers
        for i in range(num_workers):
            worker = BackgroundWorker(self.task_queue, self.results_queue, i)
            worker.start()
            self.workers.append(worker)

    def submit_task(self, name, func=None, *args, **kwargs):
        """Submit a task to be processed in the background."""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}_{int(time.time())}"
        
        task = {
            'id': task_id,
            'name': name,
            'func': func,
            'args': args,
            'kwargs': kwargs,
            'duration': kwargs.get('duration', 5) # For mock tasks
        }
        self.task_queue.put(task)
        return task_id

    def check_results(self):
        """Retrieve all completed task results."""
        results = []
        while not self.results_queue.empty():
            try:
                results.append(self.results_queue.get_nowait())
            except queue.Empty:
                break
        return results

    def start_self_learning_loop(self):
        """A special task where KALMIYA autonomously researches or analyzes data."""
        def self_learning_process():
            # In a real scenario, this would trigger web searches, file indexing, etc.
            time.sleep(10)
            return "He analizado 3 artículos nuevos sobre Arquitectura de Software y he actualizado mi base de conocimientos."
            
        return self.submit_task("Self-Learning Loop (Autonomía)", func=self_learning_process)

    def stop_all(self):
        """Stop all background workers gracefully."""
        for worker in self.workers:
            worker.is_running = False
            
# Singleton instance
engine = MultitaskingEngine()
