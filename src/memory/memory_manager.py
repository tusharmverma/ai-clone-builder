#!/usr/bin/env python3
"""
Intelligent Memory Manager
Auto-selects the best memory type based on data size and performance
"""

import time
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

try:
    from .simple_memory import SimpleMemory
    from .enhanced_memory import EnhancedMemory
    from .sqlite_vec_memory import SqliteVecMemory
except ImportError:
    # For direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.memory.simple_memory import SimpleMemory
    from src.memory.enhanced_memory import EnhancedMemory
    from src.memory.sqlite_vec_memory import SqliteVecMemory

class MemoryManager:
    """
    Intelligent memory manager that auto-selects the best memory type
    and tracks performance over time
    """
    
    # Auto-selects optimal memory system based on performance
    
    def __init__(self, clone_name: str, auto_select: bool = True):
        self.clone_name = clone_name
        self.auto_select = auto_select
        
        # Performance tracking
        self.performance_file = f"data/memory_performance/{clone_name}_performance.json"
        os.makedirs(os.path.dirname(self.performance_file), exist_ok=True)
        
        # Memory instances
        self.memories = {}
        self.current_memory_type = None
        self.performance_data = self._load_performance_data()
        
        # Auto-select best memory type
        if auto_select:
            self.current_memory_type = self._select_best_memory_type()
        else:
            self.current_memory_type = "sqlite_vec"  # Default to SQLite vector memory
        
        # Initialize current memory
        self.memory = self._get_memory(self.current_memory_type)
    
    def _load_performance_data(self) -> Dict:
        """
        Load performance data from the performance tracking file.
        
        This method reads the performance data JSON file to track
        memory system performance over time. If the file doesn't exist,
        it creates a default structure.
        
        Returns:
            Dict: Performance data structure with test results and timing
        """
        performance_file = os.path.join(self.data_dir, "memory_performance", f"{self.clone_name}_performance.json")
        
        if os.path.exists(performance_file):
            try:
                with open(performance_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading performance data: {e}")
        
        return {
            "total_tests": 0,
            "memory_types": {}
        }
    
    def _save_performance_data(self):
        """
        Save performance data to the performance tracking file.
        
        This method persists performance data to disk, creating
        the necessary directory structure if it doesn't exist.
        """
        performance_dir = os.path.join(self.data_dir, "memory_performance")
        os.makedirs(performance_dir, exist_ok=True)
        
        performance_file = os.path.join(performance_dir, f"{self.clone_name}_performance.json")
        
        try:
            with open(performance_file, 'w') as f:
                json.dump(self.performance_data, f, indent=2)
        except Exception as e:
            print(f"Error saving performance data: {e}")
    
    def _get_memory(self, memory_type: str):
        """
        Get or create a memory instance of the specified type.
        
        This method instantiates the appropriate memory class based
        on the memory type string. It caches instances to avoid
        recreating them unnecessarily.
        
        Args:
            memory_type (str): Type of memory to create ('simple', 'enhanced', 'sqlite_vec')
            
        Returns:
            Memory instance: The requested memory system instance
            
        Raises:
            ValueError: If an unknown memory type is specified
        """
        if memory_type not in self.memories:
            if memory_type == "simple":
                self.memories[memory_type] = SimpleMemory(self.clone_name)
            elif memory_type == "enhanced":
                self.memories[memory_type] = EnhancedMemory(self.clone_name)
            elif memory_type == "sqlite_vec":
                self.memories[memory_type] = SqliteVecMemory(self.clone_name)
            else:
                raise ValueError(f"Unknown memory type: {memory_type}")
        
        return self.memories[memory_type]
    
    def _select_best_memory_type(self) -> str:
        """
        Automatically select the best memory type based on performance and data size.
        
        This method analyzes performance data and estimated data size to
        determine the optimal memory system. It considers factors like
        response time, data complexity, and system resources.
        
        Returns:
            str: The best performing memory type for the current situation
        """
        # Check if we have performance data
        if not self.performance_data.get("memory_types"):
            return "simple"  # Default to simple if no data
        
        # Get the best performing memory type
        best_type = self._get_best_performing_memory()
        
        # Estimate data size to see if we need to switch
        estimated_size = self._estimate_data_size()
        
        # If data is getting large, prefer enhanced or sqlite_vec
        if estimated_size > 1000 and best_type == "simple":
            if "enhanced" in self.performance_data.get("memory_types", {}):
                best_type = "enhanced"
            elif "sqlite_vec" in self.performance_data.get("memory_types", {}):
                best_type = "sqlite_vec"
        
        return best_type
    
    def _estimate_data_size(self) -> int:
        """
        Estimate the size of the current conversation data.
        
        This method provides a rough estimate of data complexity
        to help determine if a more sophisticated memory system
        would be beneficial.
        
        Returns:
            int: Estimated data size/complexity score
        """
        if not self.memory:
            return 0
        
        # Simple estimation based on conversation history
        if hasattr(self.memory, 'conversation_history'):
            return len(self.memory.conversation_history)
        elif hasattr(self.memory, 'get_memory_stats'):
            stats = self.memory.get_memory_stats()
            return stats.get('total_messages', 0)
        
        return 0
    
    def _get_best_performing_memory(self) -> str:
        """
        Get the memory type with the best average performance.
        
        This method analyzes performance data to find the memory
        system with the lowest average response time.
        
        Returns:
            str: The best performing memory type based on timing data
        """
        best_type = "simple"
        best_avg = float('inf')
        
        for memory_type, data in self.performance_data.get("memory_types", {}).items():
            if data.get("tests", 0) > 0:
                avg_time = data.get("avg_time", float('inf'))
                if avg_time < best_avg:
                    best_avg = avg_time
                    best_type = memory_type
        
        return best_type
    
    def add_message(self, speaker: str, content: str, metadata: Dict = None):
        """
        Add a message to the current memory system.
        
        This method delegates message storage to the currently active
        memory system, ensuring all messages are properly stored.
        
        Args:
            speaker (str): Who said the message
            content (str): The message content
            metadata (Dict, optional): Additional message metadata
        """
        if self.memory:
            self.memory.add_message(speaker, content, metadata)
    
    def get_smart_context(self, message: str, max_total: int = 8) -> str:
        """
        Get smart context from the current memory system.
        
        This method retrieves relevant conversation context to help
        generate more coherent responses. It tries different context
        methods based on what the memory system supports.
        
        Args:
            message (str): The current message to get context for
            max_total (int): Maximum number of context items to return
            
        Returns:
            str: Relevant conversation context or fallback message
        """
        if self.memory and hasattr(self.memory, 'get_smart_context'):
            return self.memory.get_smart_context(message, max_total)
        elif self.memory and hasattr(self.memory, 'get_context'):
            return self.memory.get_context(max_total)
        else:
            return "No previous conversation."
    
    def search_messages(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search messages using the current memory system.
        
        This method delegates search functionality to the active memory
        system, allowing users to find specific conversations or topics.
        
        Args:
            query (str): Search query to find relevant messages
            limit (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of matching messages with metadata
        """
        if self.memory and hasattr(self.memory, 'search_messages'):
            return self.memory.search_messages(query, limit)
        return []
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics from the current memory system.
        
        This method retrieves performance and usage statistics from
        the active memory system, including the memory manager type.
        
        Returns:
            Dict[str, Any]: Memory statistics and system information
        """
        if self.memory and hasattr(self.memory, 'get_memory_stats'):
            stats = self.memory.get_memory_stats()
            stats["memory_manager_type"] = self.current_memory_type
            return stats
        return {"memory_manager_type": self.current_memory_type, "total_messages": 0}
    
    def save_memory(self):
        """
        Save the current memory system's data.
        
        This method ensures that all memory data is persisted
        to disk for future use.
        """
        if self.memory and hasattr(self.memory, 'save_memory'):
            self.memory.save_memory()
    
    def close(self):
        """
        Close all memory systems and clean up resources.
        
        This method properly shuts down all memory instances
        to prevent data corruption and free system resources.
        """
        for memory in self.memories.values():
            if hasattr(memory, 'close'):
                memory.close()
    
    def performance_test(self, test_messages: List[str] = None) -> Dict[str, float]:
        """
        Run performance test on all memory types.
        
        This method tests the performance of all available memory systems
        by adding test messages and measuring response times. It updates
        the performance data for future memory type selection decisions.
        
        Args:
            test_messages (List[str], optional): Custom test messages to use.
                If None, uses default test messages.
                
        Returns:
            Dict[str, float]: Performance results for each memory type with timing data
        """
        if not test_messages:
            test_messages = [
                "Hello, how are you?",
                "What's your favorite color?",
                "Tell me about your hobbies",
                "Do you like traveling?",
                "What's your opinion on AI?"
            ]
        
        results = {}
        
        for memory_type in ["simple", "enhanced", "sqlite_vec"]:
            try:
                memory = self._get_memory(memory_type)
                
                # Clear any existing data for fair test
                if hasattr(memory, 'conversation_history'):
                    memory.conversation_history.clear()
                
                start_time = time.time()
                
                # Add test messages
                for i, message in enumerate(test_messages):
                    memory.add_message("User", message)
                    memory.add_message("Clone", f"Response to message {i}")
                
                # Test context retrieval
                context = memory.get_smart_context("What's your favorite color?") if hasattr(memory, 'get_smart_context') else ""
                
                end_time = time.time()
                total_time = end_time - start_time
                
                results[memory_type] = total_time
                
                # Update performance data
                if memory_type not in self.performance_data["memory_types"]:
                    self.performance_data["memory_types"][memory_type] = {
                        "tests": 0,
                        "total_time": 0,
                        "avg_time": 0
                    }
                
                data = self.performance_data["memory_types"][memory_type]
                data["tests"] += 1
                data["total_time"] += total_time
                data["avg_time"] = data["total_time"] / data["tests"]
                
            except Exception as e:
                print(f"Performance test failed for {memory_type}: {e}")
                results[memory_type] = float('inf')
        
        self.performance_data["total_tests"] += 1
        self._save_performance_data()
        
        return results
    
    def switch_memory_type(self, new_type: str):
        """
        Switch to a different memory type.
        
        This method allows manual switching between memory systems.
        It updates the current memory instance and maintains the
        existing conversation data.
        
        Args:
            new_type (str): The memory type to switch to ('simple', 'enhanced', 'sqlite_vec')
        """
        if new_type in ["simple", "enhanced", "sqlite_vec"]:
            self.current_memory_type = new_type
            self.memory = self._get_memory(new_type)
            print(f"Switched to {new_type} memory")
        else:
            print(f"Unknown memory type: {new_type}")
    
    def get_performance_report(self) -> str:
        """
        Get a comprehensive performance report.
        
        This method generates a formatted report showing performance
        statistics for all memory types, including average response times
        and test counts.
        
        Returns:
            str: Formatted performance report with timing and test data
        """
        report = f"Memory Performance Report for {self.clone_name}\n"
        report += f"Current memory type: {self.current_memory_type}\n"
        report += f"Total tests run: {self.performance_data.get('total_tests', 0)}\n\n"
        
        memory_types = self.performance_data.get("memory_types", {})
        for memory_type, data in memory_types.items():
            if data.get("tests", 0) > 0:
                avg_time = data.get("avg_time", 0)
                report += f"{memory_type}: {avg_time:.2f}s avg ({data['tests']} tests)\n"
        
        return report 