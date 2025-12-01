import json
import os
from typing import List

from groq import Groq

from .models import StorylineResponse
from .personas import Persona, get_persona_profile


_client: Groq | None = None


def _get_client() -> Groq:

    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY") 
        
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable is not configured. This is required for deployment.")
        
        _client = Groq(api_key=api_key)
    return _client


def _generate_persona_scenario(persona: Persona, instructions: dict) -> dict:

    client = _get_client()

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the Generator for a cognitive intelligence game. Your task is to draft "
                    "the overarching story and the 7-day main scenario lines. You must strictly "
                    "follow the schema and validation rules provided."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(instructions),
            },
        ],
    )

    raw_content = completion.choices[0].message.content
    try:
        payload = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Groq response was not valid JSON for scenario: {exc}") from exc

    required_keys = {"overall_story", "persona_scenario"}
    missing = required_keys.difference(payload.keys())
    if missing:
        raise RuntimeError(f"Groq response missing required scenario keys: {', '.join(sorted(missing))}.")
    
    if len(payload.get("persona_scenario", [])) != 8:
        raise RuntimeError("persona_scenario did not return exactly 8 lines.")

    return {
        "overall_story": str(payload["overall_story"]),
        "persona_scenario": payload["persona_scenario"],
    }


def _generate_persona_subscenario(persona: Persona, scenario_data: dict, instructions: dict) -> List[List[str]]:

    client = _get_client()

    combined_instructions = {
        **instructions,
        "scenario_data_to_match": scenario_data,
        "task": (
            "As the Generator, you must create exactly 7 arrays of concise, actionable "
            "micro-events (persona_subscenario) that directly correspond to and support the "
            "provided 'scenario_data_to_match' 7-day arc. Each array must contain 2-4 concrete events."
        ),
        "output_schema_example": {
            "persona_subscenario": [
                [
                    "Short actionable micro-event 1 for Day 1.",
                    "Short actionable micro-event 2 for Day 1.",
                ],
                ["... Day 2 micro-events ..."],
                ["... Day 3 micro-events ..."],
                ["... Day 4 micro-events ..."],
                ["... Day 5 micro-events ..."],
                ["... Day 6 micro-events ..."],
                ["... Day 7 micro-events ..."],
            ],
        }
    }

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the Validator for a cognitive intelligence game. Your task is to generate "
                    "the micro-events, ensuring they align perfectly with the given 7-day scenario. "
                    "You must strictly follow the schema and validation rules provided."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(combined_instructions),
            },
        ],
    )

    raw_content = completion.choices[0].message.content
    try:
        payload = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Groq response was not valid JSON for subscenario: {exc}") from exc

    subscenario_data = payload.get("persona_subscenario")

    if not subscenario_data:
        raise RuntimeError("Groq response missing required subscenario key.")
    
    if len(subscenario_data) != 7:
        raise RuntimeError("persona_subscenario did not return exactly 7 arrays.")

    return subscenario_data


def generate_storyline(persona: Persona) -> StorylineResponse:

    profile = get_persona_profile(persona)

    scenario_instructions = {
        "mode": "baseline_scenario",
        "persona_key": persona.value,
        "persona_display_name": profile.display_name,
        "core_traits": profile.core_traits,
        "cognitive_style": profile.cognitive_style,
        "narrative_tone": profile.narrative_tone,
        "task": (
            "Create a psychologically coherent 7-day continuous storyline (persona_scenario) "
            "and an overall story seed (overall_story) for this persona. The world should be shaped "
            "by the persona's traits, evolving, reactive, and challenge-driven. "
            "Anchor all content to the persona's traits and cognitive style."
        ),
        "output_schema_example": {
            "overall_story": (
                "A single short paragraph describing the overarching 7-day arc."
            ),
            "persona_scenario": [
                "Overall: One sentence summary of the whole 7-day journey.",
                "Day 1: One short line describing the main cognitive scenario for Day 1.",
                "Day 2: One short line describing the main cognitive scenario for Day 2.",
                "Day 3: One short line describing the main cognitive scenario for Day 3.",
                "Day 4: One short line describing the main cognitive scenario for Day 4.",
                "Day 5: One short line describing the main cognitive scenario for Day 5.",
                "Day 6: One short line describing the main cognitive scenario for Day 6.",
                "Day 7: One short line describing the main cognitive scenario for Day 7.",
            ],
        },
        "constraints": [
            "Return JSON ONLY, no extra text.",
            "Top-level keys MUST be exactly: overall_story, persona_scenario.",
            "persona_scenario must contain exactly 8 strings: index 0 is the overall line, indices 1-7 are Day 1..Day 7 lines.",
            "Use plain ASCII hyphens '-' instead of fancy dashes to avoid encoding issues.",
        ],
    }

    scenario_result = _generate_persona_scenario(persona, scenario_instructions)

    subscenario_instructions = {
        "mode": "baseline_subscenario",
        "persona_key": persona.value,
        "persona_display_name": profile.display_name,
        "core_traits": profile.core_traits,
        "cognitive_style": profile.cognitive_style,
        "narrative_tone": profile.narrative_tone,
        "constraints": [
            "Return JSON ONLY, no extra text.",
            "Top-level key MUST be exactly: persona_subscenario.",
            "persona_subscenario must contain exactly 7 arrays, one per day, each with 2-4 short strings.",
            "Produce symbolic micro-events and subtle cognitive challenges.",
        ],
    }
    
    subscenario_result = _generate_persona_subscenario(
        persona,
        scenario_data=scenario_result,
        instructions=subscenario_instructions
    )
    
    return StorylineResponse(
        persona=persona,
        overall_story=scenario_result["overall_story"],
        persona_scenario=scenario_result["persona_scenario"],
        persona_subscenario=subscenario_result,
    )


def _generate_from_single_instruction_call(persona: Persona, user_instructions: dict) -> StorylineResponse:

    client = _get_client()

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a two-part system for a cognitive intelligence game:\n"
                    "- Generator: drafts the 7-day persona-based scenario, subscenario, and overall story.\n"
                    "- Validator: reviews, refines, and corrects the draft so it strictly "
                    "follows the schema and validation rules.\n"
                    "Instruction flow: Generate, Validate, Finalize. Output ONLY the final validated JSON object."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(user_instructions),
            },
        ],
    )

    raw_content = completion.choices[0].message.content
    try:
        payload = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Groq response was not valid JSON: {exc}") from exc

    required_keys = {"overall_story", "persona_scenario", "persona_subscenario"}
    missing = required_keys.difference(payload.keys())
    if missing:
        raise RuntimeError(f"Groq response missing required keys: {', '.join(sorted(missing))}.")
    
    if len(payload.get("persona_scenario", [])) != 8 or len(payload.get("persona_subscenario", [])) != 7:
        raise RuntimeError("Final payload failed required length checks (8 scenario lines, 7 subscenario arrays).")


    return StorylineResponse(
        persona=persona,
        overall_story=str(payload["overall_story"]),
        persona_scenario=payload["persona_scenario"],
        persona_subscenario=payload["persona_subscenario"],
    )


def generate_storyline_adaptive(
    persona: Persona,
    goal: str,
    previous_scenario: dict,
) -> StorylineResponse:

    profile = get_persona_profile(persona)

    user_instructions = {
        "mode": "adaptive",
        "persona_key": persona.value,
        "persona_display_name": profile.display_name,
        "core_traits": profile.core_traits,
        "cognitive_style": profile.cognitive_style,
        "narrative_tone": profile.narrative_tone,
        "user_goal": goal,
        "previous_scenario": previous_scenario,
        "task": (
            "As the Generator, create a new 7-day storyline that ADAPTS the previous_scenario "
            "instead of resetting it. You must:\n"
            "- Continue the existing narrative arc logically, as if time is moving forward.\n"
            "- Infuse the user's stated goal into the evolving challenges and realizations.\n"
            "- Maintain emotional continuity with the prior arc.\n"
            "- Reactivate symbolic elements, locations, or artifacts from previous_scenario in "
            "new ways.\n"
            "- Keep the world shaped by the persona's traits in an evolving, reactive, "
            "challenge-driven way.\n"
            "For each day:\n"
            "- Provide one concise scenario line in persona_scenario (Day 1..Day 7).\n"
            "- Provide 2-4 micro-events in persona_subscenario that are concrete, "
            "actionable, and clearly linked to both the day's theme and the user's goal."
        ),
        "output_schema_example": {
            "overall_story": (
                "A paragraph describing how the new 7-day arc extends and deepens the previous "
                "journey while moving the user closer to their goal."
            ),
            "persona_scenario": [
                "Overall: Summary of the adaptive 7-day journey.",
                "Day 1: Short line continuing from prior events and introducing the goal.",
                "Day 2: Short line escalating a conflict or test related to the goal.",
                "Day 3: Short line integrating a reactivated symbol from the previous arc.",
                "Day 4: Short line highlighting an internal shift or realization.",
                "Day 5: Short line presenting a harder, more refined challenge.",
                "Day 6: Short line showing integration of new skills or patterns.",
                "Day 7: Short line closing this chapter while leaving room for future arcs.",
            ],
            "persona_subscenario": [
                [
                    "Concrete micro-event for Day 1 tied to the goal and prior symbolism.",
                    "Second micro-event refining decision-making or reflection.",
                ],
                ["Day 2 micro-events tied to an escalated test."],
                ["Day 3 micro-events reusing symbols from previous_scenario."],
                ["Day 4 micro-events focused on internal conflict and insight."],
                ["Day 5 micro-events focused on higher difficulty trials."],
                ["Day 6 micro-events focused on integration and application."],
                ["Day 7 micro-events focused on consolidation and next-steps."],
            ],
        },
        "constraints": [
            "Return JSON ONLY, no extra text.",
            "Top-level keys MUST be exactly: overall_story, persona_scenario, persona_subscenario.",
            "persona_scenario must contain exactly 8 strings: index 0 is the overall line, indices 1-7 are Day 1..Day 7 lines.",
            "persona_subscenario must contain exactly 7 arrays, one per day, each with 2-4 short strings.",
            "Explicitly reference at least 2 symbolic elements or motifs from previous_scenario.",
            "Ensure the user's goal is clearly reflected in multiple days' micro-events.",
        ],
    }

    return _generate_from_single_instruction_call(persona, user_instructions)