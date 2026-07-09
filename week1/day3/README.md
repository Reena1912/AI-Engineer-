#  04: Tokens Explained

---

## 💡 The Food Stall Analogy
To understand tokens, imagine running a street food stall:
* **Pre-prepared Items:** You boil 100 eggs and make 10 plates of Maggi in advance because you know they are common orders. These represent **common tokens** (e.g., `"the"`, `"and"`, `"walk"`).
* **On-the-spot Prep:** If a customer orders an uncommon combination like *"Chocolate Egg Maggi"*, you prepare it on the spot. This represents **uncommon words** that the LLM breaks down into smaller sub-word tokens (e.g., `"Pratyush"` $\rightarrow$ `pr` + `ty` + `ush`) to process.

---

##  Why LLMs Need Tokens
Computers and machine learning models only process numbers. Converting text to numbers is solved by tokenization, which is the sweet spot between two older, flawed approaches:

| Encoding Method | How it Works | The Flaw / Drawback |
| :--- | :--- | :--- |
| **Character-level** | Encodes letter-by-letter (ASCII/Unicode) | Explodes prompt length. A short phrase uses dozens of numbers, causing massive computational overhead. |
| **Word-level** | Encodes word-by-word (e.g., Dictionary) | Fails on custom names, typos, slang, or new brand names (Out-of-Vocabulary error). |
| **Token-level (Sub-word)** | Splits words into common, reusable sub-words | **Optimal.** Balances vocabulary size and prompt length. Can represent *any* word by breaking it down. |

---

## 💰LLM Pricing
API providers (like Groq, OpenAI, or Anthropic) charge per **token**, not per word:
* Common words like `"bengaluru"` might cost $1$ token.
* Shorter but uncommon words like `"Pratyush"` might get split into $3$ tokens, costing $3\times$ more.
* **Total Transaction Cost** = $\text{Input/Prompt Tokens} + \text{Output/Completion Tokens}$.

---

## Python Implementation & Parameters
This directory contains a complete script (`tokens_demo.py`) showing how to interact with the Groq API, retrieve token usage, and control outputs.

### Key API Variables Explained:
1. **`max_tokens`:** Restricts the output size of the generated response to control costs.
2. **`finish_reason`:** Explains why the model stopped generating:
   * `"stop"`: The response completed naturally.
   * `"length"`: The response was cut off because it hit the `max_tokens` limit.

###  Warning: Reserved File Names
Do **NOT** name your python script `token.py`. Python has an internal module named `token` used by libraries like `dotenv`. Naming your script `token.py` will cause circular imports and throw errors. Use `tokens_demo.py or tokens.py` instead.

---

