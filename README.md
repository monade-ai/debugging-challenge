# Debugging Assignment: Distributed RAG System

## Overview
You have been given a broken distributed RAG (Retrieval-Augmented Generation) system that implements RAFT consensus. The system has multiple layers of bugs that interact with each other, making it challenging to debug and fix.

## System Architecture
The system consists of:
- **Raft Consensus Layer**: Manages leader election and log replication
- **State Machine**: Handles command application and state management
- **RAG Pipeline**: Processes queries using document retrieval and LLM generation
- **gRPC Server**: Handles client requests and forwards them to the appropriate components

## Your Task
Debug and fix the system so that it can:
1. Successfully elect a leader using RAFT consensus
2. Process queries through the RAG pipeline
3. Maintain consistency across all nodes
4. Handle errors gracefully without silent failures

## Debugging Tips

### 1. Start with the Basics
- Check if the system starts up without immediate crashes
- Verify that all required dependencies are available
- Look for obvious import errors or missing modules

### 2. Follow the Request Flow
- Trace a query from the gRPC server through the RAG pipeline
- Identify where the request fails or produces unexpected results
- Check the logs for error messages (though many are masked)

### 3. Check RAFT Consensus
- Monitor leader election attempts
- Look for frequent leader changes
- Check if nodes can communicate with each other

### 4. Examine Resource Usage
- Monitor memory usage over time
- Check for file descriptor leaks
- Look for threads that don't terminate properly

### 5. Test Edge Cases
- Try queries with empty or malformed input
- Test system behavior under load
- Check what happens when nodes fail or restart

## What Makes This Challenging

### 1. Interdependent Bugs
Many bugs interact with each other, so fixing one might reveal or create others. You need to understand the system holistically.

### 2. Silent Failures
The system is designed to fail silently in many cases, making it hard to identify the root cause of problems.

### 3. Race Conditions
Many bugs are timing-dependent and may not reproduce consistently, making debugging more difficult.

### 4. Resource Leaks
Memory and resource leaks accumulate over time, so the system might work initially but fail after running for a while.

### 5. Configuration Mismatches
Different components expect different configurations, leading to subtle integration issues.

## Success Criteria
Your system is considered fixed when:
1. A leader is successfully elected and maintains leadership
2. Queries can be processed and return meaningful responses
3. The system can handle multiple concurrent requests
4. No memory leaks or resource exhaustion occurs
5. Error messages are clear and helpful
6. The system can recover from node failures

## Submission
Submit your fixed code along with:
1. A summary of all bugs you found and fixed
2. An explanation of how the bugs interacted with each other
3. Any design improvements you made beyond just fixing bugs
4. A brief description of your debugging approach and tools used

## Hints (Use Sparingly)
- Start by running the system and observing the logs
- Use debugging tools like `pdb`, logging, or IDE debuggers
- Check the system's behavior under different load conditions
- Remember that some bugs are intentionally subtle and require careful analysis

Good luck! This assignment is designed to test your debugging skills, so expect it to be challenging.
