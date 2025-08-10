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
        """Load historical performance data"""
        if os.path.exists(self.performance_file):
            try:
                with open(self.performance_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "memory_types": {},
            "last_updated": datetime.now().isoformat(),
            "total_tests": 0
        }
    
    def _save_performance_data(self):
        """Save performance data"""
        self.performance_data["last_updated"] = datetime.now().isoformat()
        with open(self.performance_file, 'w') as f:
            json.dump(self.performance_data, f, indent=2)
    
    def _get_memory(self, memory_type: str):
        """Get or create memory instance"""
        if memory_type not in self.memories:
            try:
                if memory_type == "simple":
                    return SimpleMemory(self.clone_name)
                elif memory_type == "enhanced":
                    return EnhancedMemory(self.clone_name)
                elif memory_type == "sqlite_vec":
                    return SqliteVecMemory(self.clone_name)
                else:
                    print(f"Unknown memory type: {memory_type}, using enhanced")
                    return EnhancedMemory(self.clone_name)
            except Exception as e:
                print(f"Failed to initialize {memory_type} memory: {e}")
                return EnhancedMemory(self.clone_name)
        
        return self.memories[memory_type]
    
    def _select_best_memory_type(self) -> str:
        """Intelligently select the best memory type based on data and performance"""
        
        # Prioritize SQLite vector memory as the primary choice
        try:
            # Test if SQLite vector memory is available
            test_memory = SqliteVecMemory(self.clone_name)
            if test_memory.conn:
                print("✅ SQLite vector memory available - using as primary system")
                return "sqlite_vec"
        except Exception as e:
            print(f"⚠️ SQLite vector memory not available: {e}")
        
        # Check if we have performance data
        if not self.performance_data.get("memory_types"):
            # No performance data, use enhanced as fallback
            print("⚠️ No performance data - using enhanced memory as fallback")
            return "enhanced"
        
        # Get best performing memory from historical data
        best_type = self._get_best_performing_memory()
        print(f"📊 Using best performing memory: {best_type}")
        return best_type
    
    def _estimate_data_size(self) -> int:
        """Estimate current data size"""
        try:
            # Try to get message count from any available memory
            for memory_type in ["sqlite_vec", "enhanced", "simple"]:
                try:
                    memory = self._get_memory(memory_type)
                    if hasattr(memory, 'get_memory_stats'):
                        stats = memory.get_memory_stats()
                        return stats.get('total_messages', 0)
                except:
                    continue
        except:
            pass
        return 0
    
    def _get_best_performing_memory(self) -> str:
        """Get the best performing memory type based on historical data"""
        memory_types = self.performance_data.get("memory_types", {})
        
        if not memory_types:
            return "enhanced"
        
        # Calculate average response time for each memory type
        best_memory = "enhanced"
        best_time = float('inf')
        
        for memory_type, data in memory_types.items():
            if data.get("tests", 0) > 0:
                avg_time = data.get("total_time", 0) / data.get("tests", 1)
                if avg_time < best_time:
                    best_time = avg_time
                    best_memory = memory_type
        
        return best_memory
    
    def add_message(self, speaker: str, content: str, metadata: Dict = None):
        """Add message to current memory system"""
        if self.memory:
            self.memory.add_message(speaker, content, metadata)
    
    def get_smart_context(self, message: str, max_total: int = 8) -> str:
        """Get smart context from current memory system"""
        if self.memory and hasattr(self.memory, 'get_smart_context'):
            return self.memory.get_smart_context(message, max_total)
        elif self.memory and hasattr(self.memory, 'get_context'):
            return self.memory.get_context(max_total)
        else:
            return "No previous conversation."
    
    def search_messages(self, query: str, limit: int = 10) -> List[Dict]:
        """Search messages using current memory system"""
        if self.memory and hasattr(self.memory, 'search_messages'):
            return self.memory.search_messages(query, limit)
        return []
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get stats from current memory system"""
        if self.memory and hasattr(self.memory, 'get_memory_stats'):
            stats = self.memory.get_memory_stats()
            stats["memory_manager_type"] = self.current_memory_type
            return stats
        return {"memory_manager_type": self.current_memory_type, "total_messages": 0}
    
    def save_memory(self):
        """Save current memory"""
        if self.memory and hasattr(self.memory, 'save_memory'):
            self.memory.save_memory()
    
    def close(self):
        """Close all memory systems"""
        for memory in self.memories.values():
            if hasattr(memory, 'close'):
                memory.close()
    
    def performance_test(self, test_messages: List[str] = None) -> Dict[str, float]:
        """Run performance test on all memory types"""
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
        """Switch to a different memory type"""
        if new_type in ["simple", "enhanced", "sqlite_vec"]:
            self.current_memory_type = new_type
            self.memory = self._get_memory(new_type)
            print(f"Switched to {new_type} memory")
        else:
            print(f"Unknown memory type: {new_type}")
    
    def get_performance_report(self) -> str:
        """Get a performance report"""
        report = f"Memory Performance Report for {self.clone_name}\n"
        report += f"Current memory type: {self.current_memory_type}\n"
        report += f"Total tests run: {self.performance_data.get('total_tests', 0)}\n\n"
        
        memory_types = self.performance_data.get("memory_types", {})
        for memory_type, data in memory_types.items():
            if data.get("tests", 0) > 0:
                avg_time = data.get("avg_time", 0)
                report += f"{memory_type}: {avg_time:.2f}s avg ({data['tests']} tests)\n"
        
        return report 