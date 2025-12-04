from fastapi import FastAPI

from .models import (
    StorylineRequest,
    AdaptiveStorylineRequest,
    StorylineResponse,
)
from .storyline_generator import generate_storyline, generate_storyline_adaptive

app = FastAPI(
    title="Persona-Based Storyline API",
    description=(
        "Phase 1 & 2 of an agentic system for a cognitive intelligence game.\n\n"
        "- Phase 1: baseline 7-day storyline from persona only.\n"
        "- Phase 2: adaptive storyline using persona, goal, and previous scenario."
    ),
    version="0.2.0",
)


@app.post(
    "/generate-storyline",
    response_model=StorylineResponse,
    summary="Phase 1 - Generate a baseline 7-day persona-based storyline",
    tags=["storyline"],
)
def generate_storyline_endpoint(payload: StorylineRequest) -> StorylineResponse:
    
    return generate_storyline(payload.persona)


@app.post(
    "/generate-storyline/adaptive",
    response_model=StorylineResponse,
    summary="Phase 2 - Generate an adaptive 7-day storyline",
    tags=["storyline"],
)

def generate_storyline_adaptive_endpoint(
    payload: AdaptiveStorylineRequest,
) -> StorylineResponse:

    return generate_storyline_adaptive(
        persona=payload.persona,
        goal=payload.goal,
        previous_scenario=payload.previous_scenario,
    )


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:

    return {
        "message": "Persona-Based Storyline API (Phase 1 & 2). Visit /docs for interactive API docs."
    }


