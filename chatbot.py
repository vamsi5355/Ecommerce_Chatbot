"""
chatbot.py
----------
Offline Customer Support Chatbot for 'Chic Boutique' (fictional e-commerce store).
Uses Ollama + Llama 3.2 (3B) running locally to generate responses.
Compares Zero-Shot vs. One-Shot prompting across 20 adapted e-commerce queries.

Dataset source: Ubuntu Dialogue Corpus (rguo12/ubuntu_dialogue_corpus v2.0)
Queries have been adapted from technical support contexts to e-commerce scenarios.
"""

import requests
import json
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"
PROMPTS_DIR = "prompts"
EVAL_DIR = "eval"
RESULTS_FILE = os.path.join(EVAL_DIR, "results.md")

# ---------------------------------------------------------------------------
# 20 E-Commerce Queries Adapted from the Ubuntu Dialogue Corpus
# ---------------------------------------------------------------------------
# Each entry is a dict with:
#   "original" : the original Ubuntu IRC technical support theme
#   "adapted"  : the rewritten e-commerce customer query
QUERIES = [
    {
        "original": "My wifi driver stopped working after a system update.",
        "adapted":  "My discount code stopped working after I updated my account details.",
    },
    {
        "original": "How do I check the logs for the Apache server?",
        "adapted":  "How do I track the shipping status of my recent order?",
    },
    {
        "original": "I installed a new package but my system won't boot.",
        "adapted":  "I placed a new order but never received a confirmation email.",
    },
    {
        "original": "How do I uninstall a program completely from Ubuntu?",
        "adapted":  "How do I cancel an order I just placed?",
    },
    {
        "original": "Can I change my default shell to zsh after installation?",
        "adapted":  "Can I change the delivery address after placing an order?",
    },
    {
        "original": "My external hard drive is not being detected.",
        "adapted":  "The item I received is damaged and not working. What should I do?",
    },
    {
        "original": "How do I reset my root password on Ubuntu?",
        "adapted":  "My account password reset email never arrived. What should I do?",
    },
    {
        "original": "How do I configure my network settings manually?",
        "adapted":  "How do I update my payment method and billing address on file?",
    },
    {
        "original": "I was billed twice for the same subscription. How do I fix this?",
        "adapted":  "I was charged twice for the same order. How do I get a refund?",
    },
    {
        "original": "How do I see a history of all commands I have run?",
        "adapted":  "How do I view my complete order history on Chic Boutique?",
    },
    {
        "original": "A package I downloaded appears to be corrupted.",
        "adapted":  "The item I received does not match the product description on the website.",
    },
    {
        "original": "How long does it take for apt-get to update a large system?",
        "adapted":  "How long does standard shipping usually take to arrive?",
    },
    {
        "original": "Can I install multiple versions of Python at the same time?",
        "adapted":  "Can I apply multiple discount codes to a single order?",
    },
    {
        "original": "How do I stop receiving spam emails from a mailing list?",
        "adapted":  "How do I unsubscribe from your promotional marketing emails?",
    },
    {
        "original": "My account got locked after too many sudo attempts.",
        "adapted":  "My account got locked after too many failed login attempts. How do I unlock it?",
    },
    {
        "original": "Is there a way to bookmark or save specific terminal sessions?",
        "adapted":  "Is there a way to save items to a wishlist for later?",
    },
    {
        "original": "How do I get notified when a software package gets an update?",
        "adapted":  "How do I get notified when an out-of-stock item becomes available again?",
    },
    {
        "original": "How do I submit a bug report for an application?",
        "adapted":  "How do I leave a review or rating for a product I purchased?",
    },
    {
        "original": "Can I downgrade a package to an older version if the new one breaks things?",
        "adapted":  "Can I exchange an item for a different size instead of returning it for a refund?",
    },
    {
        "original": "How do I reach a human operator in the Ubuntu help channel?",
        "adapted":  "How do I contact a live customer support agent for an urgent issue?",
    },
]

# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def load_template(filename: str) -> str:
    """Load a prompt template from the prompts/ directory."""
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(template: str, query: str) -> str:
    """Insert the customer query into the template."""
    return template.replace("{query}", query)


def query_ollama(prompt: str) -> str:
    """
    Send a prompt to the local Ollama API and return the model's response.

    Makes an HTTP POST request to the /api/generate endpoint with stream=False
    so the full response is returned in a single JSON object.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=120)
        response.raise_for_status()
        data = json.loads(response.text)
        return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        print("  [ERROR] Cannot connect to Ollama. Is the server running?")
        return "Error: Could not connect to the Ollama server. Please ensure Ollama is running."
    except requests.exceptions.Timeout:
        print("  [ERROR] Request to Ollama timed out.")
        return "Error: The request timed out. The model may be overloaded."
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Unexpected error: {e}")
        return f"Error: Could not get a response from the model. ({e})"


def escape_md(text: str) -> str:
    """Escape pipe characters in text so they don't break Markdown tables."""
    return text.replace("|", "\\|").replace("\n", " ").strip()


def write_results_header(f):
    """Write the rubric and table header to the results file."""
    f.write("# Evaluation Results\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
    f.write(f"**Model:** `{MODEL_NAME}`  \n")
    f.write(f"**Endpoint:** `{OLLAMA_ENDPOINT}`  \n\n")
    f.write("---\n\n")
    f.write("## Scoring Rubric\n\n")
    f.write("Each response is manually scored on three dimensions (1–5):\n\n")
    f.write("| Criterion | 1 | 3 | 5 |\n")
    f.write("|-----------|---|---|---|\n")
    f.write("| **Relevance** | Completely off-topic | Partially addresses the query | Directly and fully addresses the query |\n")
    f.write("| **Coherence** | Incoherent / grammatically broken | Mostly clear with minor issues | Fluent, natural, and grammatically correct |\n")
    f.write("| **Helpfulness** | Provides no actionable guidance | Provides some helpful information | Gives clear, actionable next steps |\n\n")
    f.write("---\n\n")
    f.write("## Results Table\n\n")
    f.write("| Query # | Customer Query | Prompting Method | Response | Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |\n")
    f.write("|---------|----------------|------------------|----------|-----------------|-----------------|-------------------|\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Ensure output directory exists
    os.makedirs(EVAL_DIR, exist_ok=True)

    # Load prompt templates
    print("Loading prompt templates...")
    zero_shot_template = load_template("zero_shot_template.txt")
    one_shot_template  = load_template("one_shot_template.txt")
    print("  zero_shot_template.txt — OK")
    print("  one_shot_template.txt  — OK")
    print()

    results = []  # list of dicts to hold all query results

    print(f"Processing {len(QUERIES)} queries × 2 methods = {len(QUERIES) * 2} API calls...\n")
    print("=" * 70)

    for idx, item in enumerate(QUERIES, start=1):
        query = item["adapted"]
        print(f"[{idx:02d}/{len(QUERIES)}] Query: {query}")

        # --- Zero-Shot ---
        print("  → Zero-Shot ...", end=" ", flush=True)
        zero_prompt    = build_prompt(zero_shot_template, query)
        zero_response  = query_ollama(zero_prompt)
        print("done.")

        # --- One-Shot ---
        print("  → One-Shot  ...", end=" ", flush=True)
        one_prompt     = build_prompt(one_shot_template, query)
        one_response   = query_ollama(one_prompt)
        print("done.")
        print()

        results.append({
            "number":        idx,
            "query":         query,
            "zero_response": zero_response,
            "one_response":  one_response,
        })

    # Write results to eval/results.md
    print(f"Writing results to {RESULTS_FILE} ...")
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        write_results_header(f)
        for r in results:
            n  = r["number"]
            q  = escape_md(r["query"])
            zr = escape_md(r["zero_response"])
            or_ = escape_md(r["one_response"])

            # Zero-shot row (scores left blank for manual entry)
            f.write(f"| {n} | {q} | Zero-Shot | {zr} | | | |\n")
            # One-shot row
            f.write(f"| {n} | {q} | One-Shot  | {or_} | | | |\n")

        f.write("\n---\n\n")
        f.write("## Summary\n\n")
        f.write("_Fill in the score columns above, then calculate averages below._\n\n")
        f.write("| Prompting Method | Avg Relevance | Avg Coherence | Avg Helpfulness | Overall Avg |\n")
        f.write("|------------------|---------------|----------------|-----------------|-------------|\n")
        f.write("| Zero-Shot        |               |                |                 |             |\n")
        f.write("| One-Shot         |               |                |                 |             |\n")

    print(f"Done! Results written to {RESULTS_FILE}")
    print()
    print("Next step: Open eval/results.md and fill in the manual scores (1–5)")
    print("           for each Relevance, Coherence, and Helpfulness column.")


if __name__ == "__main__":
    main()
