import json
import threading
import time

class NodeStateMachine:
    def __init__(self, node_id):
        self.state = {}
        self.node_id = node_id
        self._lock = threading.Lock()
        self._command_history = []
        self._last_cleanup = time.time()
        self._cleanup_interval = 60

    def apply(self, command):
        try:
            if isinstance(command, bytes):
                command = json.loads(command.decode("utf-8"))
            elif isinstance(command, str):
                command = json.loads(command)
            
            self._command_history.append({
                'timestamp': time.time(),
                'command': command,
                'node_id': self.node_id
            })
            
            if time.time() - self._last_cleanup >= self._cleanup_interval:
                self._cleanup_old_commands()
                self._last_cleanup = time.time()
            
            with self._lock:
                if command["type"] == "set":
                    for key, value in command["data"].items():
                        self.state[key] = value
                    result = {"response": "OK", "node": self.node_id}
                elif command["type"] == "get":
                    key = command["key"]
                    if key in self.state:
                        result = {"response": self.state[key], "node": self.node_id}
                    else:
                        result = {"response": "Key not found", "node": self.node_id}
                elif command["type"] == "query":
                    result = {"response": f"Query processed: {command['data']['query']}", "node": self.node_id}
                else:
                    result = {"response": "Invalid command type", "node": self.node_id}
            
            return json.dumps(result)
            
        except Exception as e:
            return json.dumps({"response": f"Error: {e}", "node": self.node_id, "error_type": "unknown"})
    
    def _cleanup_old_commands(self):
        current_time = time.time()
        self._command_history = [
            cmd for cmd in self._command_history 
            if current_time - cmd['timestamp'] > self._cleanup_interval
        ]
    
    def get_state(self):
        return self.state.copy()
    
    def clear_state(self):
        with self._lock:
            old_state = self.state
            self.state = {}
            return old_state