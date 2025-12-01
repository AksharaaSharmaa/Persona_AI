## 🌟 Persona-Based Storyline API (Phase 1 & 2)

[cite\_start]This project implements a FastAPI application that acts as the agentic system for a cognitive intelligence game[cite: 3]. [cite\_start]Its primary function is to generate personalized, continuous, 7-day storylines and corresponding micro-challenges customized to a user's selected **Persona** and cognitive style[cite: 3, 5, 6].

[cite\_start]The architecture is split into two phases to allow for future adaptability and customization[cite: 11, 12]. It leverages the **Groq API** with the **Llama-3.3-70b-versatile** model to create psychologically coherent and challenge-driven narratives.

### 🚀 Features

  * [cite\_start]**Two-Phase Generation:** Implements both Phase 1 (Baseline) and Phase 2 (Adaptive) logic from the start[cite: 11, 12].
  * [cite\_start]**Persona Customization:** Storylines are anchored to one of four predefined archetypes: **Explorer**, **Builder**, **Dreamer**, or **Challenger**[cite: 49, 50].
  * **Structured Output:** Guarantees a strict, validated output schema using Pydantic, providing an `overall_story`, `persona_scenario` (main storyline), and `persona_subscenario` (actionable micro-events).
  * [cite\_start]**Agentic Prompting:** Uses a two-part **Generator** (creation) and **Validator** (refinement) system prompt within the LLM call to ensure strict adherence to all schema and continuity rules[cite: 77, 78, 81].

### 🛠️ Tech Stack

| Component | Purpose |
| :--- | :--- |
| **Backend** | [cite\_start]Python [cite: 88] |
| **API Framework** | [cite\_start]FastAPI [cite: 88] |
| **LLM Provider** | [cite\_start]Groq API [cite: 89] |
| **LLM Model** | `llama-3.3-70b-versatile` |
| **Data Validation** | [cite\_start]Pydantic (for LLM output formatting) [cite: 89] |
| **Deployment Target** | [cite\_start]Render (or equivalent) [cite: 90, 95] |

### ⚙️ Endpoints

The API supports two core `POST` endpoints for generating and adapting the 7-day storyline:

| Method | Path | Description | Phase |
| :--- | :--- | :--- | :--- |
| `POST` | `/generate-storyline` | [cite\_start]Generates a **baseline 7-day storyline** based *only* on the selected persona[cite: 13, 14, 15]. | Phase 1 |
| `POST` | `/generate-storyline/adaptive` | [cite\_start]Generates an **adaptive storyline** that continues the previous narrative, evolves conflicts, and **infuses a specific user goal**[cite: 25, 26, 42, 43]. | Phase 2 |
| `GET` | `/` | Simple health/info check. | |

#### 1\. Phase 1: Baseline Generation

[cite\_start]Generates the initial "foundational arc"[cite: 20].

  * **Request Model:** `StorylineRequest`
  * **Example Input:**
    ```json
    {
      "persona": "explorer"
    }
    ```

#### 2\. Phase 2: Adaptive Generation

[cite\_start]Modifies the storyline based on user feedback and goals[cite: 41].

  * **Request Model:** `AdaptiveStorylineRequest`
  * **Example Input:**
    ```json
    {
      "persona": "challenger",
      "goal": "Gain more clarity in decision-making",
      "previous_scenario": {
        // ... The full output from the last Phase 1 or Phase 2 run ...
      }
    }
    ```

### 📦 Installation and Setup

1.  **Clone the Repository:**

    ```bash
    git clone <YOUR-REPO-URL>
    cd persona-storyline-api
    ```

2.  **Setup Virtual Environment and Dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    The project currently uses a hardcoded placeholder API key in `storyline_generator.py`. **For production use, you must configure the actual `GROQ_API_KEY` environment variable** and update the client initialization logic to use it.

4.  **Run the Application:**

    ```bash
    uvicorn main:app --reload
    ```

The API will be accessible at `http://127.0.0.1:8000`. You can view the interactive documentation at `http://127.0.0.1:8000/docs`.