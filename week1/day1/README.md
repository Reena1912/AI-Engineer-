#  01: Understand Your First LLM Call
---

### 1. Virtual Environments (`venv`)
To explain why we use Virtual Environments, think of a game driver analogy:
* **The Analogy:** You have GTA 5 (which needs driver version 2.0) and GTA 6 (which needs driver version 4.0). If you update your system driver to 4.0, GTA 6 works but GTA 5 breaks. 
* **The Solution:** A Virtual Environment acts as an isolated room for your project. By activating a `venv`, you install project-specific packages without interfering with other projects or your main operating system.

### 2. Roles in LLM Calls
In API-based chat completions, every message requires a **`role`** and **`content`**. There are three key roles:

| Role | Description | Purpose |
| :--- | :--- | :--- |
| **`user`** | The human sender | Sends queries and prompts to the model. |
| **`assistant`** | The AI assistant | The generated response from the LLM. |
| **`system`** | The controller | Sets system-level instructions or behavior rules for the LLM during the entire conversation (e.g., *"You are an interviewer. Respond in one sentence"*). |

#### Why are Roles Required?
Human conversations depend heavily on context. If you ask:
1. *"Who is Virat Kohli?"* (User) $\rightarrow$ *"Virat Kohli is an Indian cricketer."* (Assistant)
2. *"What is his age?"* (User)

The LLM needs the roles and conversation history to understand that *"his"* refers back to the Assistant's description of Virat Kohli. If there were no roles, the model wouldn't know who said what, making context-aware dialogue impossible.

### 3. Understanding the API Response
An LLM API response returns a complex JSON metadata object containing:
* **`choices`:** An array of answer options. By default, it returns one choice (`response.choices[0]`), which contains the generated message `content`.
* **`usage`:** Metadata showing how many prompt tokens, completion tokens, and total tokens were consumed.

---


