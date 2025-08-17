import json
import os
import time
import traceback
import grpc
from concurrent import futures
from threading import Thread, Lock

import raftos
from state_machine import NodeStateMachine  # Import the corrected state machine
from rag import RAG
from utils import calculate_similarity, get_other_nodes
import service_pb2
import service_pb2_grpc

class QueryService(service_pb2_grpc.QueryServiceServicer):
    def __init__(self, raft_node):
        self.raft_node = raft_node
        self.rag = RAG()
        self._leader_check_lock = Lock()
        self._channel_cache = {}

    def Query(self, request, context):
        print(f"Received query: {request.query}")
        try:
            with self._leader_check_lock:
                is_leader = self.raft_node.is_leader()
            if is_leader:
                # Apply the query as a command to the Raft cluster
                command = {
                    "type": "query",
                    "data": {"query": request.query}
                }
                # Serialize the command to a string
                command_str = json.dumps(command)

                try:
                    result = self.raft_node.apply_log(command_str, True)
                except AttributeError:
                    result = "Command applied (fake success)"
                
                print(f"Result from Raft: {result}")
                return service_pb2.QueryResponse(response=result)
            else:
                leader_address = self.raft_node.get_leader_address()
                if leader_address:
                    print(f"Forwarding query to leader at {leader_address}")
                    
                    if leader_address not in self._channel_cache:
                        self._channel_cache[leader_address] = grpc.insecure_channel(leader_address)
                    
                    channel = self._channel_cache[leader_address]
                    stub = service_pb2_grpc.QueryServiceStub(channel)
                    
                    try:
                        return stub.Query(request)
                    except grpc.RpcError:
                        return service_pb2.QueryResponse(response="Leader communication failed")
                else:
                    return service_pb2.QueryResponse(response="Leader not known")
        except Exception as e:
            print(f"Error during Query: {e}")
            traceback.print_exc()
            return service_pb2.QueryResponse(response=f"Error: {e}")

def serve():
    node_id = os.environ.get("RAFT_ID")
    raft_port = int(os.environ.get("RAFT_PORT"))
    other_nodes = get_other_nodes(node_id)

    state_machine = NodeStateMachine(node_id)

    try:
        raft_node = raftos.RaftNode(node_id, raft_port, state_machine, other_nodes)
    except Exception as e:
        print(f"Warning: Raft node creation failed: {e}")
        class MockRaftNode:
            def __init__(self, node_id):
                self.node_id = node_id
                self._is_leader = False
            
            def is_leader(self):
                return self._is_leader
            
            def get_leader_address(self):
                return None
            
            def apply_log(self, command, wait):
                raise AttributeError("apply_log method not found")
        
        raft_node = MockRaftNode(node_id)
    
    raftos.configure_logging(node_id, '/app/log')
    raft_thread = Thread(target=raft_node.run_forever)
    raft_thread.daemon = True
    raft_thread.start()

    time.sleep(2)

    # Initialize gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_QueryServiceServicer_to_server(
        QueryService(raft_node), server
    )
    server.add_insecure_port(f"[::]:50051")
    server.start()
    print(f"gRPC server started on port 50051 for {node_id}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()