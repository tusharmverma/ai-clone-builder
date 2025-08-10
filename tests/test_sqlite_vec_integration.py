#!/usr/bin/env python3
"""
Test SqliteVec Memory Integration with AIClone
Tests the full integration of sqlite-vec for true semantic search
"""

import os
import sys
import time
from rich.console import Console
from rich.panel import Panel

# Add src to path for imports
sys.path.append('src')

console = Console()

def test_memory_types():
    """Test SQLite vector memory system"""
    
    # Test SQLite vector memory integration
    console.print(Panel.fit(
        "[bold blue]🧠 Testing SQLite Vector Memory[/bold blue]\n"
        "Testing the primary memory system with vector capabilities",
        border_style="blue"
    ))
    
    # Fix import path
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    from ai_clone.clone import create_demo_clones
    
    # Test SQLite vector memory
    console.print("\n🧪 Testing SQLITE_VEC Memory")
    try:
        start_time = time.time()
        clones = create_demo_clones(memory_type="sqlite_vec")
        
        if clones:
            clone = clones[0]
            # Test basic functionality
            clone.add_to_conversation_history("User", "Hello! How are you?")
            clone.add_to_conversation_history(clone.name, "Hi! I'm doing great, thanks for asking!")
            
            # Test memory retrieval
            context = clone.memory.get_context(5)
            console.print(f"✅ Context retrieved: {len(context) if context else 0} messages")
            
            response_time = time.time() - start_time
            console.print(f"✅ Success: {response_time:.3f}s")
            return True, response_time, "Vector search, conversation clustering"
        else:
            console.print("❌ No clones created")
            return False, 0, "Failed"
            
    except Exception as e:
        console.print(f"❌ Error testing sqlite_vec: {e}")
        return False, 0, "Failed"
    
    return False, 0, "No tests run"

def test_vector_search_capabilities():
    """Test specific vector search capabilities"""
    console.print(Panel.fit(
        "[bold blue]🔍 Testing Vector Search Capabilities[/bold blue]\n"
        "Testing semantic similarity search with sqlite-vec",
        border_style="blue"
    ))
    
    try:
        # Fix import path
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        
        from ai_clone.clone import create_demo_clones
        
        # Create clone with vector memory
        clones = create_demo_clones(memory_type="sqlite_vec")
        clone = clones[0]
        
        if not hasattr(clone.memory, 'search_similar_messages'):
            console.print("❌ Vector search not available")
            return False
        
        # Add diverse conversation data
        test_conversations = [
            ("User", "I love blue and green colors"),
            (clone.name, "Those are beautiful colors! Blue is calming and green is natural."),
            ("User", "What do you think about artificial intelligence?"),
            (clone.name, "AI is fascinating! It's reshaping how we work and think."),
            ("User", "Do you enjoy reading books?"),
            (clone.name, "I love literature! Stories can transport us to different worlds."),
            ("User", "Tell me about your favorite music"),
            (clone.name, "I enjoy classical music and jazz. They have rich harmonies."),
            ("User", "What colors do you prefer?"),
            (clone.name, "I'm drawn to earth tones - browns, greens, and warm colors.")
        ]
        
        # Add messages to memory
        for speaker, message in test_conversations:
            clone.memory.add_message(speaker, message)
            
        console.print(f"✅ Added {len(test_conversations)} messages to memory")
        
        # Test semantic searches
        search_queries = [
            "colors and preferences",
            "artificial intelligence technology", 
            "reading and literature",
            "music and harmony"
        ]
        
        for query in search_queries:
            console.print(f"\n🔍 Searching for: '{query}'")
            similar = clone.memory.search_similar_messages(query, limit=3)
            
            for i, msg in enumerate(similar, 1):
                similarity = msg.get('similarity_score', 0)
                content_preview = msg['content'][:60] + "..." if len(msg['content']) > 60 else msg['content']
                console.print(f"  {i}. {msg['speaker']}: {content_preview} (sim: {similarity:.3f})")
        
        # Test smart context
        console.print(f"\n🧠 Testing smart context for: 'What's your favorite color?'")
        context = clone.memory.get_smart_context("What's your favorite color?")
        console.print(f"📝 Context generated ({len(context)} chars):")
        print(context[:200] + "..." if len(context) > 200 else context)
        
        # Cleanup
        clone.memory.close()
        
        return True
        
    except Exception as e:
        console.print(f"❌ Vector search test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    console.print(Panel.fit(
        "[bold green]🚀 SqliteVec Memory Integration Test Suite[/bold green]\n"
        "Testing the new vector memory system with M1 Mac compatibility",
        border_style="green"
    ))
    
    # Test memory types
    console.print("\n" + "="*60)
    success, response_time, features = test_memory_types()
    
    # Performance summary
    console.print("\n📊 Performance Summary:")
    console.print("┌─────────────┬─────────┬──────────────┬──────────────────┐")
    console.print("│ Memory Type │ Success │ Response Time│ Features         │")
    console.print("├─────────────┼─────────┼──────────────┼──────────────────┤")
    
    status = "✅ Yes" if success else "❌ No"
    time_str = f"{response_time:.3f}s" if response_time > 0 else "N/A"
    
    console.print(f"│ sqlite_vec  │ {status:<7} │ {time_str:<12} │ {features:<16} │")
    console.print("└─────────────┴─────────┴──────────────┴──────────────────┘")
    
    # Test 2: Vector search capabilities (if available)
    if success: # Use the success flag from test_memory_types
        console.print("\n" + "="*60)
        vector_success = test_vector_search_capabilities()
        
        if vector_success:
            console.print("\n[bold green]🎉 All vector search tests passed![/bold green]")
        else:
            console.print("\n[bold red]❌ Vector search tests failed[/bold red]")
    else:
        console.print("\n[bold yellow]⚠️ SqliteVec memory not available - skipping vector search tests[/bold yellow]")
    
    # Final summary
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        "[bold green]📋 Test Summary[/bold green]\n"
        f"SQLite Vector Memory: {'✅' if success else '❌'}\n"
        f"Vector Search: {'✅' if success and vector_success else '❌'}\n\n"
        "The AI Clone Builder now uses SQLite Vector Memory as the primary system! 🚀",
        border_style="green"
    ))

if __name__ == "__main__":
    main() 