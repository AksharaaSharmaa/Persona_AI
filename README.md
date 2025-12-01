# 🌟 Persona-Based Storyline API

This project is a FastAPI app that powers a cognitive intelligence game by creating personalized 7-day storylines tailored to your personality. Think of it as your creative storytelling companion that adapts to who you are and what you want to achieve.

We've built it with two phases in mind—starting with a baseline story that gets to know you, then evolving into something more personalized based on your goals. Under the hood, it uses Groq's powerful Llama-3.3-70b model to craft narratives that feel psychologically authentic and keep you engaged with meaningful challenges.

## 🚀 What Makes This Special

* **Two-Phase Magic:** We start with a foundation (Phase 1), then adapt and grow with you (Phase 2). Both are ready to go from day one.
* **Your Personality, Your Story:** Choose from four unique archetypes—**Explorer**, **Builder**, **Dreamer**, or **Challenger**—and watch your storyline come alive in a way that resonates with you.
* **Rock-Solid Structure:** Using Pydantic, we ensure every story follows a clean format with an overarching narrative, your main scenario, and bite-sized micro-challenges you can actually tackle.
* **Smart Prompting:** We use a clever two-part system—one AI agent creates your story, another validates it—so everything stays consistent and follows the rules we've set up.

## 🛠️ What's Powering This

| Component | What It Does |
|:---|:---|
| **Backend** | Python (the brain of the operation) |
| **API Framework** | FastAPI (makes everything fast and reliable) |
| **LLM Provider** | Groq API (connects us to cutting-edge AI) |
| **LLM Model** | `llama-3.3-70b-versatile` (the storyteller) |
| **Data Validation** | Pydantic (keeps outputs clean and structured) |
| **Where It Lives** | Render or similar hosting platforms |

## ⚙️ How to Use It

We've got two main ways you can interact with the API, plus a simple health check:

| Method | Path | What It Does | Phase |
|:---|:---|:---|:---|
| `POST` | `/generate-storyline` | Creates your initial 7-day story based purely on your chosen persona. | Phase 1 |
| `POST` | `/generate-storyline/adaptive` | Takes your previous story and evolves it, weaving in your personal goals and advancing the plot. | Phase 2 |
| `GET` | `/` | Quick check to see if everything's running smoothly. | |

### 1. Getting Started: Your First Story (Phase 1)

This is where it all begins—your foundational storyline that sets the stage.

* **What You Send:** A simple request with your persona choice
* **Example:**

```json
{
  "persona": "explorer"
}
```

### 2. Growing Together: Adaptive Stories (Phase 2)

Now things get interesting. Tell us your goals, and we'll evolve your story to help you get there.

* **What You Send:** Your persona, your goal, and the story we created before
* **Example:**

```json
{
  "persona": "challenger",
  "goal": "Gain more clarity in decision-making",
  "previous_scenario": {
    // ... Everything from your last story goes here ...
  }
}
```

## 📦 Getting This Running on Your Machine

Let me walk you through setting this up—it's easier than you think!

**1. Grab the Code:**

```bash
git clone <your-repo-url-here>
cd persona-storyline-api
```

**2. Set Up Your Python Environment:**

```bash
python -m venv venv
source venv/bin/activate  # If you're on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Add Your API Key:**

Right now, there's a placeholder API key in `storyline_generator.py`. **Before you go live, you'll need to set up a real `GROQ_API_KEY` as an environment variable** and update the code to use it. This is important for security!

**4. Fire It Up:**

```bash
uvicorn main:app --reload
```

Once it's running, head over to `http://127.0.0.1:8000` to see it in action. 
