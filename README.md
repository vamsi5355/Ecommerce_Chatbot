# Chic Boutique — Offline Customer Support Chatbot

An offline, privacy-preserving customer support chatbot for the fictional e-commerce store **Chic Boutique**, powered by **Ollama** and **Meta's Llama 3.2 3B** language model. No customer data is sent to external servers — the entire pipeline runs on your local machine.

---

## Overview

This project demonstrates a practical, privacy-first approach to AI-driven customer support. Rather than relying on cloud-hosted LLM APIs (which require transmitting potentially sensitive customer data), this system runs a capable open-weight language model entirely on-premise using [Ollama](https://ollama.com).

The experiment evaluates two fundamental prompt engineering strategies across 20 realistic customer queries adapted from the **Ubuntu Dialogue Corpus**:

- **Zero-Shot Prompting** — The model is given a role description and the customer query; no examples are provided.
- **One-Shot Prompting** — A single high-quality example of a query and ideal response is added to the prompt to guide tone and format.

All responses are logged and manually scored in `eval/results.md`, and findings are analysed in `report.md`.

---

## Key Findings

| Prompting Method | Avg Relevance | Avg Coherence | Avg Helpfulness | Overall |
|---|---|---|---|---|
| Zero-Shot | 4.90 / 5 | 5.00 / 5 | 4.60 / 5 | **4.83** |
| One-Shot | 5.00 / 5 | 5.00 / 5 | 5.00 / 5 | **5.00** |

- **One-Shot consistently outperforms Zero-Shot**, particularly on helpfulness and tone.
- The single example in the One-Shot prompt reliably teaches the model to use a warmer, more customer-friendly register.
- **Llama 3.2 3B is a viable base model** for general customer support queries but requires integration with real-time data (via RAG) for production use.

---

## Architecture

```
chatbot.py
    │
    ├─► Load prompt template (zero_shot or one_shot)
    ├─► Insert customer query into template
    │
    └─► HTTP POST ──► Ollama Server (localhost:11434)
                            │
                            └─► Llama 3.2 3B (inference)
                                        │
                            ◄── JSON response ──┘
    │
    └─► Parse response ──► Write to eval/results.md
```

Everything runs locally. No internet connection is required after setup.

---

## Repository Structure

```
ecommerce-chatbot/
├── chatbot.py                  # Main Python script
├── README.md                   # This file
├── setup.md                    # Environment setup instructions
├── report.md                   # Full analytical report
├── prompts/
│   ├── zero_shot_template.txt  # Zero-shot prompt template
│   └── one_shot_template.txt   # One-shot prompt template
└── eval/
    └── results.md              # All 20 queries × 2 methods, scored
```

---

## Quick Start

**Requirements:** Python 3.9+, 8 GB RAM, ~3 GB disk space

```bash
# 1. Install Ollama (see setup.md for full instructions)
# macOS/Linux:
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull the model (~2 GB download)
ollama pull llama3.2:3b

# 3. Clone this repo
git clone https://github.com/<your-username>/ecommerce-chatbot.git
cd ecommerce-chatbot

# 4. Set up Python environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install requests datasets

# 5. Run the chatbot
python chatbot.py
```

See [setup.md](setup.md) for detailed platform-specific instructions and troubleshooting.

---

## Methodology

### Data Source
Queries were adapted from the [Ubuntu Dialogue Corpus](https://huggingface.co/datasets/rguo12/ubuntu_dialogue_corpus) (v2.0), a dataset of over 1 million multi-turn technical support conversations. Twenty conversations were selected and their core technical themes rewritten as e-commerce customer support queries.

### Prompt Design
- **Zero-Shot:** Role + query only. Tests the model's out-of-the-box instruction-following capability.
- **One-Shot:** Role + one curated example (a return policy Q&A) + query. Tests whether a single demonstration improves tone, format, and helpfulness.

### Evaluation Rubric
Responses are manually scored 1–5 on:
- **Relevance** — Does it address the actual question?
- **Coherence** — Is it grammatically correct and easy to read?
- **Helpfulness** — Does it provide actionable guidance?

---

## Limitations

- **No live data access:** The model cannot look up real orders, inventory, or accounts. RAG integration is needed for production.
- **Hallucination risk:** The model may generate plausible but invented details (e.g., contact emails, exact policy timelines).
- **CPU performance:** Inference is slow without a GPU (5–30 seconds per response).
- **Stateless:** Each query is handled independently; no multi-turn memory.

---

## Technologies Used

| Tool | Purpose |
|---|---|
| [Ollama](https://ollama.com) | Local LLM server |
| [Llama 3.2 3B](https://ollama.com/library/llama3.2) | Open-weight language model |
| Python 3 | Scripting and API interaction |
| `requests` | HTTP client for Ollama API |
| `datasets` (Hugging Face) | Ubuntu Dialogue Corpus access |

---

## License

This project is for educational purposes. The Llama 3.2 model is subject to [Meta's Llama 3 Community License](https://llama.meta.com/llama3/license/). The Ubuntu Dialogue Corpus is publicly available under its original terms.
