from enum import Enum
from dataclasses import dataclass
from typing import List


class Persona(str, Enum):
    EXPLORER = "explorer"
    BUILDER = "builder"
    DREAMER = "dreamer"
    CHALLENGER = "challenger"


@dataclass(frozen=True)
class PersonaProfile:

    key: Persona
    display_name: str
    core_traits: List[str]
    cognitive_style: str
    narrative_tone: str


PERSONA_PROFILES: dict[Persona, PersonaProfile] = {
    Persona.EXPLORER: PersonaProfile(
        key=Persona.EXPLORER,
        display_name="The Explorer",
        core_traits=[
            "curious",
            "pattern-finding",
            "connects distant clues",
            "brings order to confusion",
        ],
        cognitive_style="Divergent observation, pattern detection, and synthesis.",
        narrative_tone="curious, investigative, slightly mysterious but optimistic.",
    ),
    Persona.BUILDER: PersonaProfile(
        key=Persona.BUILDER,
        display_name="The Builder",
        core_traits=[
            "learns by trial and error",
            "adapts quickly",
            "builds structure from chaos",
        ],
        cognitive_style="Iterative experimentation, feedback-driven refinement.",
        narrative_tone="pragmatic, constructive, grounded and methodical.",
    ),
    Persona.DREAMER: PersonaProfile(
        key=Persona.DREAMER,
        display_name="The Dreamer",
        core_traits=[
            "imaginative",
            "emotionally attuned",
            "blends dreams with reality",
            "deeply reflective",
        ],
        cognitive_style="Associative, symbolic, emotionally layered thinking.",
        narrative_tone="lyrical, introspective, slightly surreal but warm.",
    ),
    Persona.CHALLENGER: PersonaProfile(
        key=Persona.CHALLENGER,
        display_name="The Challenger",
        core_traits=[
            "calm under stress",
            "decisive",
            "resilient",
            "values integrity",
        ],
        cognitive_style="High-pressure decision-making, ethical reasoning, resilience.",
        narrative_tone="steady, resolute, clear and integrity-focused.",
    ),
}


def get_persona_profile(persona: Persona) -> PersonaProfile:

    return PERSONA_PROFILES[persona]


