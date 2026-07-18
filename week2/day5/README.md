# Prompt Engineering Guide: The 6 Pillars of Production-Ready Prompts


Prompt engineering is not about "magic phrases" or secret tricks. It is the application of structured common sense to make Large Language Model (LLM) outputs **predictable, stable, and secure** enough to be parsed by software applications in production.

---

## 1. The Core Problem: Why Do We Need Prompt Engineering?

*   **Non-deterministic Behavior:** Unlike standard software (where $2 + 2$ is always $4$), LLMs are non-deterministic. The same question asked in different sessions can yield slightly different responses, sentence structures, or formatting.
*   **Downstream Code Parsing:** In production, AI outputs are processed by backend code (e.g., parsing a string to determine database routing), not read directly by humans. If the LLM randomly adds conversational filler (e.g., *"Sure, here is your category: Return"*), the code will break.
*   **Security & Domain Boundaries:** Without strict prompt engineering, users can abuse application chatbots (e.g., asking a food delivery bot for relationship advice or using it as a free Python coding assistant). Prompt engineering keeps the LLM within its defined boundary.

---

## 2. The 6 Pillars of a Production-Grade Prompt

To secure and stabilize LLM outputs, every production prompt should include the following six structural components:

### 1. Role
*   **Definition:** Assigning a specific persona, domain, or area of responsibility to the LLM.
*   **Production Tip:** Define roles by **responsibility and domain** (e.g., *Python Security Auditor* or *Laptop Support Assistant*), not fake competence words like *"genius"* which do not increase the model's actual intelligence.
*   **Example:** `"You are a support assistant at a mobile/laptop company."`

### 2. Task
*   **Definition:** A clear, active instruction defining the exact work to be done.
*   **Production Tip:** Use strong, unambiguous verbs (*classify*, *summarize*, *extract*, *validate*) and keep the target focused.
*   **Example:** `"You have to classify the issue in a category."`

### 3. Constraints
*   **Definition:** Strict boundaries and rules restricting the model's options.
*   **Production Tip:** Restrict the model to a fixed set of choices so your code can anticipate every possible output.
*   **Example:** `"You have to classify the issue in one of three categories namely billing, technical, return."`

### 4. Output Format
*   **Definition:** Dictating the exact syntax, layout, or character limitations of the response.
*   **Production Tip:** Keep it as simple as possible (e.g., one word, single digit, or structured JSON) to make parsing trivial.
*   **Example:** `"Your answer should be in one word only. The one word should be one of the categories given in constraints."`

### 5. Examples (One-shot / Few-shot)
*   **Definition:** Providing input-output pairs inside the prompt to show the model how to behave.
*   **Production Tip:** Providing even a single example (one-shot) or a few examples (few-shot) helps the model mirror the exact output structure and tone.
*   **Example:** `"For instance if a user complaint says he wants a refund then the category is Return."`

### 6. Fallback
*   **Definition:** A safety rule telling the LLM what to do if the input doesn't fit the constraints or the "happy path".
*   **Production Tip:** If a user inputs something completely out-of-domain (e.g., *"My marriage is broke"*), the fallback stops the LLM from hallucinating or forcing it into a wrong category.
*   **Example:** `"If the issue is unrelated to any of the categories mentioned in constraints, then the answer should be OTHER."`

---

## 3. The Unified Production Prompt Template

Putting all six pillars together, the final system prompt looks like this:

```markdown
# ROLE:
You are a support assistant at a mobile/laptop company.

# TASK:
You have to classify the issue in a category.

# CONSTRAINT:
You have to classify the issue in one of three categories namely billing, technical, return.

# OUTPUT FORMAT:
Your answer should be in one word only. The one word should be one of the categories given in constraints.

# EXAMPLE:
For instance if a user complaint says he wants a refund then the category is Return.

# FALLBACK:
If the issue is unrelated to any of the categories mentioned in constraints, then the answer should be OTHER.

This is a user complaint:
[USER_COMPLAINT]
```

---

# Day 5: Prompt Engineering Setup

This document records the exact sequence of terminal commands used to initialize this project, configure the virtual environment, and install dependencies using `uv`.

---

## 1. Project Initialization

First, navigate to the `week2` directory and initialize a new `day5` project:
```powershell
# Navigate to the week2 folder
cd week2

# Initialize a new day5 project using uv
uv init day5

# Change directory into the newly created day5 folder
cd day5

# Create a virtual environment specifying Python version 3.11
uv venv --python 3.11

# Activate the virtual environment on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Add Groq SDK and python-dotenv for environment variables
uv add groq python-dotenv

```

### Expected Output
1.  **Bad Prompt Output:** A paragraph apologizing for the marriage issue or explaining why it cannot help.
2.  **Engineered Prompt (Happy Path):** `TECHNICAL`
3.  **Engineered Prompt (Edge Case):** `OTHER`
