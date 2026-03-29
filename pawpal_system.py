from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ── Task ──────────────────────────────────────────────────────────────────────
@dataclass
class Task:
    name: str
    category: str                        # walk | feeding | meds | grooming | enrichment
    priority: str                        # high | medium | low
    frequency: str                       # daily | weekly | as-needed
    duration_minutes: int
    preferred_time: str                  # morning | afternoon | evening
    last_completed: Optional[datetime] = None

    def is_due(self, date) -> bool:
        """Return True if this task should happen on the given date."""
        pass

    def mark_complete(self, timestamp: datetime) -> None:
        """Log the task as completed at the given timestamp."""
        pass

    def skip(self, reason: str) -> None:
        """Skip this task and record the reason."""
        pass


# ── Pet ───────────────────────────────────────────────────────────────────────
@dataclass
class Pet:
    name: str
    species: str
    age: int
    medical_conditions: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Associate a care task with this pet."""
        pass

    def get_due_tasks(self, date) -> list[Task]:
        """Return all tasks due on the given date."""
        pass

    def get_profile(self) -> str:
        """Return a summary string of this pet's info."""
        pass


# ── Owner ─────────────────────────────────────────────────────────────────────
class Owner:
    def __init__(self, name: str, preferences: dict = None):
        self.name: str = name
        self.pets: list[Pet] = []
        self.availability: dict = {}     # {date: [(start, end), ...]}
        self.preferences: dict = preferences or {}

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        pass

    def set_availability(self, date, windows: list[tuple]) -> None:
        """Define available time windows for a given date."""
        pass

    def get_availability(self, date) -> list[tuple]:
        """Return the list of available time windows for a given date."""
        pass


# ── Scheduler ─────────────────────────────────────────────────────────────────
class Scheduler:
    def __init__(self, owner: Owner, date):
        self.owner: Owner = owner
        self.date = date
        self.scheduled_items: list[dict] = []   # {task, pet, start_time, status, reason}
        self.unscheduled_tasks: list[Task] = []

    def build_plan(self, date) -> None:
        """Generate the full daily schedule for the given date."""
        pass

    def rank_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority and urgency."""
        pass

    def fit_to_windows(self, ranked_tasks: list[Task], availability: list[tuple]) -> None:
        """Assign ranked tasks to available time windows."""
        pass

    def explain(self) -> str:
        """Return a human-readable explanation of why each task was placed when it was."""
        pass

    def mark_done(self, task: Task) -> None:
        """Mark a scheduled task as completed."""
        pass
