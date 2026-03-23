# Setup Guide

This guide explains how to set up and run the **Chic Boutique Offline Customer Support Chatbot** from scratch on your local machine.

---

## Prerequisites

- **Operating System:** macOS, Windows 10/11, or Linux (Ubuntu 20.04+)
- **Python:** 3.9 or higher (`python3 --version` to check)
- **RAM:** At least 8 GB recommended (the Llama 3.2 3B model requires ~4 GB)
- **Disk Space:** At least 3 GB free (for the model weights)
- **Internet Access:** Required only for initial Ollama and model download

---

## Step 1: Install Ollama

Ollama is the tool that downloads, manages, and serves the LLM locally.

### macOS
```bash
# Visit https://ollama.com and download the macOS installer (.dmg)
# Or use Homebrew:
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Download and run the installer from [https://ollama.com/download](https://ollama.com/download).

### Verify Installation
```bash
ollama --version
```
You should see something like `ollama version 0.3.x`.

---

## Step 2: Pull the Llama 3.2 3B Model

This downloads approximately 2 GB of model weights to your machine.

```bash
ollama pull llama3.2:3b
```

Wait for the download to complete. You can verify the model is available with:

```bash
ollama list
```

You should see `llama3.2:3b` listed.

---

## Step 3: Start the Ollama Server

On **macOS** and **Windows**, Ollama starts automatically in the system tray after installation.

On **Linux**, start it manually:

```bash
ollama serve
```

The server runs at `http://localhost:11434` by default. Keep this terminal open.

To verify the server is running:

```bash
curl http://localhost:11434
# Expected output: "Ollama is running"
```

---

## Step 4: Clone or Download This Project

```bash
git clone https://github.com/<your-username>/ecommerce-chatbot.git
cd ecommerce-chatbot
```

Or download and unzip the repository from GitHub.

---

## Step 5: Set Up a Python Virtual Environment

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
# macOS / Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

Your terminal prompt should now show `(venv)` at the beginning.

---

## Step 6: Install Python Dependencies

```bash
pip install requests datasets
```

These are the only two external libraries required:
- `requests` — to make HTTP calls to the Ollama API
- `datasets` — to access the Ubuntu Dialogue Corpus from Hugging Face

---

## Step 7: Run the Chatbot

With the Ollama server running and your virtual environment active:

```bash
python chatbot.py
```

The script will:
1. Load the two prompt templates from `prompts/`
2. Send each of the 20 queries to the Ollama API twice (Zero-Shot and One-Shot)
3. Write all responses to `eval/results.md`

**Expected runtime:** 3–10 minutes depending on your hardware (CPU-only execution is slower).

---

## File Structure

```
ecommerce-chatbot/
├── chatbot.py                  # Main script — run this
├── README.md                   # Project overview
├── setup.md                    # This file
├── report.md                   # Analysis report
├── prompts/
│   ├── zero_shot_template.txt  # Zero-shot prompt template
│   └── one_shot_template.txt   # One-shot prompt template (with example)
└── eval/
    └── results.md              # Generated results and scores
```

---

## Troubleshooting

### "Connection refused" or API error
- Make sure Ollama is running: check the system tray (macOS/Windows) or run `ollama serve` (Linux).
- Confirm the server is at `http://localhost:11434` — try `curl http://localhost:11434` in your terminal.

### Responses are very slow
- This is normal on CPU-only machines. A 3B model on CPU typically takes 5–30 seconds per response.
- If you have an NVIDIA GPU, Ollama will use it automatically if CUDA drivers are installed.

### "Model not found" error
- Re-run `ollama pull llama3.2:3b` and ensure it completes successfully.
- Run `ollama list` to confirm the model appears.

### ModuleNotFoundError (requests or datasets)
- Make sure your virtual environment is active (`source venv/bin/activate`).
- Re-run `pip install requests datasets`.

---

## Optional: Test the Model Interactively

You can chat with the model directly in your terminal before running the script:

```bash
ollama run llama3.2:3b
```

Type a message and press Enter. Type `/bye` to exit.
