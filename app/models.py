from typing import List, Dict, Any

from pydantic import BaseModel, Field

from .personas import Persona


class StorylineRequest(BaseModel):

    persona: Persona = Field(
        ...,
        description=(
            "The persona archetype to generate a storyline for. "
            "One of: explorer, builder, dreamer, challenger."
        ),
    )


class StorylineResponse(BaseModel):

    persona: Persona = Field(..., description="Persona used to generate this storyline.")
    overall_story: str = Field(
        ...,
        description="Short paragraph describing the overarching 7-day narrative arc.",
    )
    persona_scenario: List[str] = Field(
        ...,
        min_length=8,
        max_length=8,
        description=(
            "Exactly 8 short lines: index 0 is the overall line, indices 1-7 are "
            "Day 1..Day 7 scenario lines."
        ),
    )
    persona_subscenario: List[List[str]] = Field(
        ...,
        min_length=7,
        max_length=7,
        description=(
            "Exactly 7 arrays (one per day). Each inner list contains 2-4 concise "
            "actionable micro-events for that day."
        ),
    )


class AdaptiveStorylineRequest(BaseModel):

    persona: Persona = Field(
        ...,
        description="Persona archetype (explorer, builder, dreamer, challenger).",
    )
    goal: str = Field(
        ...,
        description="User's explicit cognitive/behavioral goal for this adaptive run.",
    )
    previous_scenario: Dict[str, Any] = Field(
        ...,
        description=(
            "Previous storyline output, following the same structure as the Phase 1 "
            "response (overall_story, persona_scenario, persona_subscenario, persona)."
        ),
    )


