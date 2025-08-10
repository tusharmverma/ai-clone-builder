#!/usr/bin/env python3
"""
Simple Test Runner for AI Clone Builder
Runs all test scripts and provides a summary
"""

import os
import sys
import subprocess
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def run_test_script(script_path: str) -> dict:
    """Run a single test script and return results"""
    script_name = os.path.basename(script_path)
    console.print(f"\n[bold cyan]Running: {script_name}[/bold cyan]")
    
    start_time = time.time()
    
    try:
        # Run the test script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
            timeout=120  # 2 minute timeout per test
        )
        
        execution_time = time.time() - start_time
        
        if result.returncode == 0:
            status = "✅ PASSED"
            color = "green"
        else:
            status = "❌ FAILED"
            color = "red"
        
        return {
            "script": script_name,
            "status": status,
            "execution_time": execution_time,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "color": color
        }
        
    except subprocess.TimeoutExpired:
        return {
            "script": script_name,
            "status": "⏰ TIMEOUT",
            "execution_time": 120,
            "return_code": -1,
            "stdout": "",
            "stderr": "Test timed out after 2 minutes",
            "color": "yellow"
        }
    except Exception as e:
        return {
            "script": script_name,
            "status": "💥 ERROR",
            "execution_time": 0,
            "return_code": -1,
            "stdout": "",
            "stderr": str(e),
            "color": "red"
        }

def main():
    """Main test runner"""
    
    # Main test runner
    console.print(Panel.fit(
        "[bold green]🧪 AI Clone Builder Test Runner[/bold green]\n"
        "Running all test scripts to verify system functionality",
        border_style="green"
    ))
    
    # Find all test scripts
    tests_dir = "tests"
    test_scripts = []
    
    if os.path.exists(tests_dir):
        for file in os.listdir(tests_dir):
            if file.startswith("test_") and file.endswith(".py"):
                test_scripts.append(os.path.join(tests_dir, file))
    
    if not test_scripts:
        console.print("[red]No test scripts found in tests/ directory[/red]")
        return
    
    console.print(f"\n[bold]Found {len(test_scripts)} test scripts:[/bold]")
    for script in test_scripts:
        console.print(f"  • {os.path.basename(script)}")
    
    # Run tests
    results = []
    total_start = time.time()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Running tests...", total=len(test_scripts))
        
        for script in test_scripts:
            progress.update(task, description=f"Running {os.path.basename(script)}...")
            result = run_test_script(script)
            results.append(result)
            progress.advance(task)
    
    total_time = time.time() - total_start
    
    # Display results
    console.print(f"\n[bold]Test Results Summary:[/bold]")
    
    # Create results table
    table = Table(title="Test Results")
    table.add_column("Script", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Time", style="green")
    table.add_column("Details", style="dim")
    
    passed = 0
    failed = 0
    errors = 0
    
    for result in results:
        status_color = result["color"]
        table.add_row(
            result["script"],
            f"[{status_color}]{result['status']}[/{status_color}]",
            f"{result['execution_time']:.2f}s",
            f"Code: {result['return_code']}"
        )
        
        if "PASSED" in result["status"]:
            passed += 1
        elif "FAILED" in result["status"]:
            failed += 1
        else:
            errors += 1
    
    console.print(table)
    
    # Summary
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  ✅ Passed: {passed}")
    console.print(f"  ❌ Failed: {failed}")
    console.print(f"  💥 Errors: {errors}")
    console.print(f"  ⏱️  Total Time: {total_time:.2f}s")
    
    # Show detailed output for failed tests
    if failed > 0 or errors > 0:
        console.print(f"\n[bold red]Failed Tests Details:[/bold red]")
        for result in results:
            if result["return_code"] != 0:
                console.print(f"\n[bold]{result['script']}:[/bold]")
                if result["stderr"]:
                    console.print(f"[red]Error: {result['stderr']}[/red]")
                if result["stdout"]:
                    console.print(f"[dim]Output: {result['stdout'][:200]}...[/dim]")
    
    # Final status
    if failed == 0 and errors == 0:
        console.print(f"\n[bold green]🎉 All tests passed![/bold green]")
        return 0
    else:
        console.print(f"\n[bold red]⚠️  Some tests failed. Please check the details above.[/bold red]")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 