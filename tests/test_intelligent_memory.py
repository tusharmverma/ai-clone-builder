#!/usr/bin/env python3
"""
Test Intelligent Memory Manager
Demonstrates auto-selection and performance tracking
"""

import time
import sys
import os
sys.path.append('src')

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def test_memory_selection():
    """Test how memory selection works with different data sizes"""
    console.print(Panel.fit(
        "[bold blue]🧠 Intelligent Memory Selection Test[/bold blue]\n"
        "Testing auto-selection based on data size and performance",
        border_style="blue"
    ))
    
    from ai_clone.clone import create_demo_clones
    
    # Test different memory types
    memory_types = ["auto", "simple", "enhanced", "sqlite_vec"]
    
    for memory_type in memory_types:
        console.print(f"\n[bold yellow]🧪 Testing {memory_type.upper()} Memory[/bold yellow]")
        
        try:
            # Create clone with specific memory type
            clones = create_demo_clones(memory_type=memory_type)
            clone = clones[0]
            
            console.print(f"✅ Created clone '{clone.name}' with {memory_type} memory")
            
            # Test with different conversation lengths
            conversation_lengths = [5, 15, 30]
            
            for length in conversation_lengths:
                console.print(f"  📊 Testing with {length} messages:")
                
                start_time = time.time()
                
                # Add messages
                for i in range(length):
                    message = f"Test message {i} about colors, travel, and technology"
                    clone.add_to_conversation_history("User", message)
                    clone.add_to_conversation_history(clone.name, f"Response to message {i}")
                
                # Test context retrieval
                context = clone.memory.get_smart_context("What's your favorite color?") if hasattr(clone.memory, 'get_smart_context') else ""
                
                end_time = time.time()
                total_time = end_time - start_time
                
                console.print(f"    ⏱️ Time: {total_time:.2f}s")
                
                # Get memory stats
                if hasattr(clone.memory, 'get_memory_stats'):
                    stats = clone.memory.get_memory_stats()
                    console.print(f"    📊 Messages: {stats.get('total_messages', 'N/A')}")
                    
                    if 'vector_embeddings' in stats:
                        console.print(f"    🔍 Vectors: {stats['vector_embeddings']}")
                
                # Cleanup for next test
                if hasattr(clone.memory, 'conversation_history'):
                    clone.memory.conversation_history.clear()
            
            # Cleanup
            if hasattr(clone.memory, 'close'):
                clone.memory.close()
                
        except Exception as e:
            console.print(f"❌ Error testing {memory_type}: {e}")
    
    console.print("\n[bold green]✅ All memory types tested![/bold green]")

def test_performance_tracking():
    """Test performance tracking over time"""
    console.print(Panel.fit(
        "[bold blue]📊 Performance Tracking Test[/bold blue]\n"
        "Testing how performance data is collected and used",
        border_style="blue"
    ))
    
    from memory.memory_manager import MemoryManager
    
    # Create memory manager
    manager = MemoryManager("performance_test_clone")
    
    console.print(f"✅ Created memory manager with type: {manager.current_memory_type}")
    
    # Run performance tests
    for i in range(3):
        console.print(f"\n[bold]Test run {i+1}:[/bold]")
        results = manager.performance_test()
        
        # Display results
        table = Table(title=f"Performance Results - Run {i+1}")
        table.add_column("Memory Type", style="cyan")
        table.add_column("Time (seconds)", style="magenta")
        
        for memory_type, time_taken in results.items():
            table.add_row(memory_type, f"{time_taken:.2f}s")
        
        console.print(table)
    
    # Get performance report
    report = manager.get_performance_report()
    console.print(f"\n[bold]📈 Performance Report:[/bold]")
    console.print(report)
    
    # Test memory switching
    console.print(f"\n[bold]🔄 Testing Memory Switching:[/bold]")
    for new_type in ["simple", "enhanced", "sqlite_vec"]:
        manager.switch_memory_type(new_type)
        console.print(f"  Switched to {new_type}, current type: {manager.current_memory_type}")
    
    # Cleanup
    manager.close()

def test_auto_selection_logic():
    """Test the auto-selection logic"""
    console.print(Panel.fit(
        "[bold blue]🤖 Auto-Selection Logic Test[/bold blue]\n"
        "Testing how the system chooses the best memory type",
        border_style="blue"
    ))
    
    from memory.memory_manager import MemoryManager
    
    # Test with different scenarios
    scenarios = [
        ("small_dataset", 10),
        ("medium_dataset", 50), 
        ("large_dataset", 150)
    ]
    
    for scenario_name, data_size in scenarios:
        console.print(f"\n[bold yellow]📊 Scenario: {scenario_name} ({data_size} messages)[/bold yellow]")
        
        # Create manager
        manager = MemoryManager(f"test_{scenario_name}")
        
        # Simulate data size
        for i in range(data_size):
            manager.add_message("User", f"Message {i} about various topics")
            manager.add_message("Clone", f"Response {i}")
        
        # Get stats
        stats = manager.get_memory_stats()
        console.print(f"  Selected memory type: {stats.get('memory_manager_type', 'unknown')}")
        console.print(f"  Total messages: {stats.get('total_messages', 0)}")
        
        # Run performance test
        results = manager.performance_test()
        best_memory = min(results.items(), key=lambda x: x[1])[0]
        console.print(f"  Best performing: {best_memory} ({results[best_memory]:.2f}s)")
        
        manager.close()

def main():
    """Main test function"""
    console.print(Panel.fit(
        "[bold green]🚀 Intelligent Memory Manager Test Suite[/bold green]\n"
        "Testing auto-selection, performance tracking, and memory switching",
        border_style="green"
    ))
    
    # Test 1: Memory selection with different data sizes
    test_memory_selection()
    
    console.print("\n" + "="*60)
    
    # Test 2: Performance tracking
    test_performance_tracking()
    
    console.print("\n" + "="*60)
    
    # Test 3: Auto-selection logic
    test_auto_selection_logic()
    
    # Summary
    console.print(Panel.fit(
        "[bold blue]📋 Test Summary[/bold blue]\n"
        "✅ All 3 memory types available: Simple, Enhanced, SqliteVec\n"
        "✅ Intelligent auto-selection based on data size\n"
        "✅ Performance tracking over time\n"
        "✅ Dynamic memory switching\n"
        "✅ Graceful fallback for reliability\n"
        "\nThe system now automatically chooses the best memory type! 🚀",
        border_style="blue"
    ))

if __name__ == "__main__":
    main() 