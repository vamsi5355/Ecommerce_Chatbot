# Report: Zero-Shot vs One-Shot Prompting - Local LLM Chatbot for E-Commerce

**Name:** Vamsi  
**Date:** June 2025  
**Model Used:** Llama 3.2 3B (via Ollama)

---

## 1. Introduction

In this project I built a customer support chatbot for a fictional online
store called Chic Boutique. The chatbot runs completely offline using Ollama
and the Llama 3.2 3B model on local machine. No data is sent to internet.

The main reason for doing it offline is data privacy. When we use cloud
based AI APIs like OpenAI, the customer data like names, emails and order
details gets sent to third party servers. This is risky and illegal in many
countries under laws like GDPR in Europe and DPDP Act 2023 in India. So
running the model locally is a much safer option for companies.

I also compared two prompt engineering techniques in this project - zero-shot
and one-shot prompting - to see which one gives better responses for customer
support questions.

---

## 2. Methodology

### 2.1 How I Prepared the Queries

I used the Ubuntu Dialogue Corpus dataset to get the queries. This dataset
has millions of technical support conversations. I picked 20 conversations
from it and rewrote them to fit e-commerce context.

For example:
- Original: "My wifi driver stopped working after the latest update."
- Adapted: "My discount code stopped working after I updated my account details."

- Original: "How do I check the logs for the Apache server?"
- Adapted: "How do I track the shipping status of my recent order?"

- Original: "I was billed twice for the same subscription."
- Adapted: "I was charged twice for the same order. How do I get a refund?"

I made sure the 20 queries cover different types of customer problems like
order tracking, cancellations, returns, refunds, account issues, shipping
time, wishlist and contacting support.

### 2.2 Prompt Templates

I created two prompt template files inside the prompts/ folder.

**Zero-Shot Template:** This just tells the model it is a support agent for
Chic Boutique and gives it the customer query directly. No example is given.
The model has to decide the tone and format on its own.

**One-Shot Template:** This has the same role instruction but also includes
one example of a good customer query and a good agent response before the
actual question. The example I used was about the return policy. This helps
the model understand what kind of tone and format I want.

### 2.3 Scoring Rubric

After running the chatbot I manually read all 40 responses (20 queries times
2 methods) and gave each one a score from 1 to 5 on three things:

- **Relevance (1-5):** Does the response answer the customer's question?
  1 means completely wrong topic, 5 means perfectly on point.

- **Coherence (1-5):** Is the response easy to read and grammatically
  correct? 1 means confusing, 5 means very clear and smooth.

- **Helpfulness (1-5):** Does the response give useful information or next
  steps? 1 means not helpful at all, 5 means very actionable and helpful.

---

## 3. Results and Analysis

### 3.1 Average Scores

| Prompting Method | Avg Relevance | Avg Coherence | Avg Helpfulness | Overall Avg |
|------------------|---------------|---------------|-----------------|-------------|
| Zero-Shot        | 4.90          | 5.00          | 4.60            | 4.83        |
| One-Shot         | 5.00          | 5.00          | 5.00            | 5.00        |

Both methods performed well overall which I did not expect from a small 3B
model. But one-shot was clearly better specially in helpfulness.

### 3.2 What I Observed

The biggest difference between the two methods was in tone and helpfulness.
Zero-shot responses were mostly correct but they felt a bit flat and dry.
One-shot responses were warmer and more friendly. They almost always started
with "Hi there!" and ended with an offer to help more. This came directly
from the example I gave in the one-shot prompt.

**Example - Query 1 (Discount code not working):**

Zero-Shot response:
> "I'm sorry to hear that your discount code isn't working. This can sometimes
> happen after account changes. I'd recommend double-checking that the code
> hasn't expired and that it applies to the items in your cart..."

One-Shot response:
> "Hi there! Sorry for the trouble with your discount code. Account updates
> can occasionally cause session issues - try logging out and back in, then
> re-applying the code at checkout. If it still doesn't work please contact
> our support team!"

Both answers are correct but the one-shot version feels more like a real
support person. It gives an immediate tip to try first and then escalates
only if needed. The zero-shot version just explains what might have happened
without giving a clear first step.

**Example - Query 20 (Contacting live support):**

Zero-Shot just listed all contact options flatly - chat, email, phone.
One-Shot told the customer to use live chat first because it is the fastest
option for urgent issues. That is actually more useful advice.

For coherence both methods scored 5.00 average. The model always wrote clean
and grammatically correct sentences which is good. Even without any example
the model knew how to write proper English responses.

For relevance zero-shot scored 4 instead of 5 on two queries. These were
more open ended questions like asking about shipping time and contacting
support. The zero-shot model gave slightly generic answers for those. One-shot
handled them better because it already had a pattern to follow from the
example.

Overall one-shot was more consistent. Across all 20 queries it never dropped
below 5 on any dimension. Zero-shot had 4 small drops mainly in helpfulness
where the response was correct but did not give a clear next step to the
customer.

---

## 4. Conclusion and Limitations

### 4.1 Conclusion

From this experiment I can say that Llama 3.2 3B running locally with Ollama
is a good starting point for a customer support chatbot. It handles common
questions well and the responses are always grammatically correct and easy
to read.

One-shot prompting is clearly better than zero-shot for this use case. Just
adding one good example to the prompt made the responses more friendly, more
helpful and more consistent. So if someone is building a real chatbot they
should definitely use at least one-shot prompting. Few-shot (3-5 examples)
would probably be even better.

### 4.2 Limitations

**No real data access:** The model does not know actual order details,
inventory or customer accounts. Every response is based on general knowledge
only. For a real system you would need to connect it to the actual database
using something like RAG (Retrieval Augmented Generation).

**Hallucination:** Sometimes the model generates specific details that are
not in the prompt like a support email address or an exact delivery time.
These may not be accurate. This is a known problem with all LLMs.

**Slow on CPU:** Running a language model on CPU takes 5 to 30 seconds per
response. For a real customer support system with many users this would be
too slow. You would need a GPU or a more powerful server.

**No conversation memory:** Each query is treated as a fresh conversation.
The chatbot cannot remember what the customer said earlier in the same chat.
Real chatbots need to maintain conversation history.

### 4.3 Next Steps

1. Add RAG so the chatbot can look up real order and policy information
   before answering.
2. Add conversation history so it can handle multi-turn chats.
3. Try few-shot prompting with 3-5 examples for even better results.
4. Test bigger models like Llama 3.1 8B or Mistral 7B to compare quality.
5. Do A/B testing with real users to get more reliable evaluation scores.

---
