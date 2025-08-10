# Troubleshooting Guide

**Fix common problems and get AI clones working.**

## Quick Fixes

### Run Diagnostics First
- Run the setup test script to tell you exactly what's wrong and how to fix it.

## Common Issues & Solutions

### 1. Ollama Not Found
**Error:** Ollama command not found

**Fix:**
- **Mac**: Install using Homebrew
- **Windows/Linux**: Download from [ollama.com](https://ollama.com/)

**Verify:**
- Check if Ollama shows a version number

### 2. Ollama Not Running
**Error:** Connection refused or Cannot connect to Ollama

**Fix:**
- Start the Ollama service

**Keep it running:** Open a new terminal for other commands.

### 3. Model Not Found
**Error:** Model llama3.2:3b not found

**Fix:**
- Download the model using Ollama

**Check available models:**
- List all available models

### 4. Python Packages Missing
**Error:** Module not found or Import error

**Fix:**
- Install the required packages using the requirements file

**If that fails:**
- Update your package installer
- Try installing the requirements again

### 5. Memory Too Low
**Error:** Out of memory or very slow responses

**Solutions:**
- Close other applications
- Use smaller model
- Restart Ollama

### 6. Clone Not Responding
**Error:** Clone created but won't chat

**Check:**
- Test basic functionality using the test script

**If test fails:** Check Ollama connection and model availability.

## System Tests

### Test Python Setup
- Check Python version (should be 3.8 or newer)
- Check installed packages

### Test Ollama
- Check Ollama version
- Check available models

### Test Project
- Run the comprehensive test script

## Platform-Specific Issues

### macOS
- **Permission denied:** Fix file permissions
- **Homebrew issues:** Update and fix Homebrew

### Windows
- **Path issues:** Add Ollama to system PATH
- **Firewall:** Allow Ollama through Windows Firewall

### Linux
- **Permission issues:** Add user to Ollama group
- **Service not starting:** Start the Ollama service

## Debug Mode

### Enable Verbose Logging
- Set environment variable for debug information
- Run with debug info

### Check Logs
- Check Ollama logs
- Check system logs 