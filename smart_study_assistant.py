from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import re


@dataclass
class LearnerProfile:
    name: str
    level: str
    goals: str
    preferred_style: str


class SmartStudyAssistant:
    """Core logic for summarization, quiz generation, level assessment and guidance."""

    LEVELS = ["weak", "intermediate", "intelligent"]

    def summarize_notes(self, text: str, max_points: int = 7) -> List[str]:
        cleaned = re.sub(r"\s+", " ", text.strip())
        if not cleaned:
            return ["Add notes to generate a summary."]

        sentences = re.split(r"(?<=[.!?])\s+", cleaned)
        if len(sentences) == 1:
            chunks = [s.strip() for s in cleaned.split(";") if s.strip()]
            if not chunks:
                chunks = [cleaned]
            return [f"• {c}" for c in chunks[:max_points]]

        ranked = sorted(
            sentences,
            key=lambda s: (
                len(re.findall(r"\b(formula|theorem|proof|derive|application|example|law|assume)\b", s.lower())),
                len(s),
            ),
            reverse=True,
        )
        return [f"• {s.strip()}" for s in ranked[:max_points]]

    def generate_iit_level_questions(self, notes: str, count: int = 5) -> List[Dict[str, str]]:
        topics = self._extract_topics(notes)
        base_topic = topics[0] if topics else "the topic"

        templates = [
            "Derive the governing equation for {topic} from first principles and clearly state assumptions.",
            "Compare two valid solving approaches for {topic}. When does each approach fail?",
            "Solve a multi-step numerical problem on {topic} and estimate the error bounds.",
            "Explain a common misconception in {topic} and correct it with a rigorous argument.",
            "Create a real-world IIT-JEE style application of {topic} and solve it completely.",
            "If one core condition in {topic} changes, how does the solution strategy adapt?",
            "Design a challenging conceptual MCQ on {topic} with explanation for every option.",
        ]

        questions: List[Dict[str, str]] = []
        for i in range(count):
            prompt = templates[i % len(templates)].format(topic=topics[i % len(topics)] if topics else base_topic)
            questions.append({
                "id": str(i + 1),
                "difficulty": "IIT-Advanced",
                "question": prompt,
            })
        return questions

    def assess_level(self, score_percent: float) -> str:
        if score_percent < 45:
            return "weak"
        if score_percent < 75:
            return "intermediate"
        return "intelligent"

    def recommendations(self, subject: str, level: str) -> Dict[str, List[str]]:
        subject_key = subject.lower().strip()
        common_books = {
            "physics": [
                "Concepts of Physics - H.C. Verma",
                "Problems in General Physics - I.E. Irodov",
                "Understanding Physics (Mechanics) - D.C. Pandey",
            ],
            "chemistry": [
                "Physical Chemistry - O.P. Tandon",
                "Organic Chemistry - Morrison & Boyd",
                "Concise Inorganic Chemistry - J.D. Lee",
            ],
            "mathematics": [
                "IIT Mathematics - M.L. Khanna",
                "Problems Plus in IIT Mathematics - A. Das Gupta",
                "Higher Algebra - Hall & Knight",
            ],
        }

        common_youtube = {
            "physics": [
                "Physics Wallah - Advanced Problem Solving Playlists",
                "IIT-PAL Physics lectures",
                "Neso Academy - Concept revision",
            ],
            "chemistry": [
                "Unacademy JEE Chemistry sessions",
                "IIT-PAL Chemistry lectures",
                "Vedantu JEE Chemistry crash revision",
            ],
            "mathematics": [
                "Mohit Tyagi - JEE Mathematics",
                "IIT-PAL Maths lectures",
                "Nexus JEE Advanced problem marathons",
            ],
        }

        style_tips = {
            "weak": [
                "Focus on fundamentals and solved examples before timed practice.",
                "Use short 25-minute Pomodoro sessions with 5-minute breaks.",
                "After each chapter, solve 10 basic and 5 medium questions.",
            ],
            "intermediate": [
                "Practice mixed-topic question sets to improve selection strategy.",
                "Track mistakes by category: concept, calculation, and time pressure.",
                "Start weekly full-length tests and analyze deeply.",
            ],
            "intelligent": [
                "Use advanced mocks under strict time conditions.",
                "Prioritize high-weightage and high-difficulty problems.",
                "Teach concepts to peers; teaching exposes hidden gaps.",
            ],
        }

        return {
            "books": common_books.get(subject_key, ["NCERT + one standard reference book"]),
            "youtube": common_youtube.get(subject_key, ["IIT-PAL official channel", "NPTEL basics"]),
            "tips": style_tips.get(level, style_tips["intermediate"]),
        }

    def explain_for_student(self, concept: str, level: str) -> str:
        style = {
            "weak": "simple words + daily life analogy + one formula",
            "intermediate": "intuitive explanation + formula derivation + one solved example",
            "intelligent": "compact theory + edge cases + exam strategy",
        }
        tone = style.get(level, style["intermediate"])
        return (
            f"Concept: {concept}\n"
            f"Teaching mode: {tone}.\n"
            "1) Start with what it means physically.\n"
            "2) Show the key equation and define every symbol.\n"
            "3) Solve one representative problem.\n"
            "4) End with common traps and quick checks."
        )

    def build_study_plan(self, profile: LearnerProfile) -> Dict[str, str]:
        now = datetime.utcnow().strftime("%Y-%m-%d")
        intensity = {
            "weak": "2 hours/day with heavy concept revision",
            "intermediate": "3.5 hours/day with mixed problem sets",
            "intelligent": "5 hours/day with advanced mock and review",
        }.get(profile.level, "3 hours/day balanced plan")

        return {
            "date": now,
            "intensity": intensity,
            "goal": profile.goals,
            "method": f"Preferred learning style: {profile.preferred_style}",
        }

    def _extract_topics(self, notes: str) -> List[str]:
        words = re.findall(r"[A-Za-z][A-Za-z0-9+-]{3,}", notes)
        stop = {
            "that", "this", "with", "from", "into", "have", "were", "which", "their",
            "there", "about", "after", "before", "because", "while", "where", "when",
        }
        filtered = [w for w in words if w.lower() not in stop]
        unique: List[str] = []
        for w in filtered:
            if w.lower() not in [u.lower() for u in unique]:
                unique.append(w)
        return unique[:6]


class DistractionBlocker:
    """
    Safe simulation of app-blocking workflow.

    Real system-level blocking requires OS permissions and integration.
    This class keeps a configurable blocklist and emits deterministic
    enforcement instructions that can later be connected to platform APIs.
    """

    def __init__(self) -> None:
        self.blocklist: List[str] = []
        self.active: bool = False
        self.session_minutes: int = 0

    def configure(self, apps: List[str], session_minutes: int) -> None:
        self.blocklist = sorted({a.strip() for a in apps if a.strip()})
        self.session_minutes = max(1, int(session_minutes))

    def start(self) -> str:
        self.active = True
        if not self.blocklist:
            return "No apps selected. Session started without blocking rules."
        joined = ", ".join(self.blocklist)
        return (
            f"Study lock enabled for {self.session_minutes} minutes. "
            f"Block these distractions: {joined}."
        )

    def end(self) -> str:
        self.active = False
        return "Study lock ended. All restrictions are now lifted."
