from dataclasses import dataclass, field
from datetime import datetime, date as Date, timedelta
from typing import Optional


# ── ScheduledItem ─────────────────────────────────────────────────────────────
@dataclass
class ScheduledItem:
    task: "Task"
    pet: "Pet"
    start_time: datetime
    status: str = "pending"          # pending | done
    reason: str = ""                 # why it was placed in this slot


# ── Task ──────────────────────────────────────────────────────────────────────
@dataclass
class Task:
    name: str
    category: str                    # walk | feeding | meds | grooming | enrichment
    priority: str                    # high | medium | low
    frequency: str                   # daily | weekly | as-needed
    duration_minutes: int
    preferred_time: str              # morning | afternoon | evening
    last_completed: Optional[datetime] = None
    pet: Optional["Pet"] = field(default=None, repr=False)  # back-ref to owning Pet

    def is_due(self, check_date: Date) -> bool:
        """Return True if this task should happen on the given date."""
        if self.frequency == "daily":
            return True
        if self.frequency == "as-needed":
            return True
        if self.frequency == "weekly":
            if self.last_completed is None:
                return True
            days_since = (check_date - self.last_completed.date()).days
            return days_since >= 7
        return False

    def mark_complete(self, timestamp: datetime) -> None:
        """Log the task as completed at the given timestamp."""
        self.last_completed = timestamp
        print(f"  [done] '{self.name}' marked complete at {timestamp.strftime('%H:%M')}")


# ── Pet ───────────────────────────────────────────────────────────────────────
@dataclass
class Pet:
    name: str
    species: str
    age: int
    medical_conditions: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Associate a care task with this pet and set the back-reference."""
        task.pet = self
        self.tasks.append(task)

    def get_due_tasks(self, check_date: Date) -> list[Task]:
        """Return all tasks due on the given date."""
        return [t for t in self.tasks if t.is_due(check_date)]

    def get_profile(self) -> str:
        """Return a summary string of this pet's info."""
        conditions = ", ".join(self.medical_conditions) if self.medical_conditions else "none"
        return (
            f"{self.name} | {self.species} | Age: {self.age} | "
            f"Conditions: {conditions} | Tasks: {len(self.tasks)}"
        )


# ── Owner ─────────────────────────────────────────────────────────────────────
class Owner:
    def __init__(self, name: str, preferences: dict = None):
        self.name: str = name
        self.pets: list[Pet] = []
        self.availability: dict = {}     # { date: [(start_hour, end_hour), ...] }
        self.preferences: dict = preferences or {}

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def set_availability(self, check_date: Date, windows: list[tuple]) -> None:
        """Define available time windows for a given date.
        windows: list of (start_hour, end_hour) tuples, e.g. [(7, 9), (17, 20)]
        """
        self.availability[check_date] = windows

    def get_availability(self, check_date: Date) -> list[tuple]:
        """Return the list of available time windows for a given date."""
        return self.availability.get(check_date, [])

    def get_all_due_tasks(self, check_date: Date) -> list[tuple["Task", "Pet"]]:
        """Collect (task, pet) pairs for every due task across all pets."""
        pairs = []
        for pet in self.pets:
            for task in pet.get_due_tasks(check_date):
                pairs.append((task, pet))
        return pairs


# ── Scheduler ─────────────────────────────────────────────────────────────────
class Scheduler:
    # Maps priority label → sort key (lower = scheduled first)
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    # Maps preferred_time → ideal start hour (used when picking a window)
    TIME_PREFERENCE = {"morning": 8, "afternoon": 13, "evening": 18}

    def __init__(self, owner: Owner, schedule_date: Date):
        self.owner: Owner = owner
        self.date: Date = schedule_date
        self.scheduled_items: list[ScheduledItem] = []
        self.unscheduled_tasks: list[Task] = []

    # ── core pipeline ──────────────────────────────────────────────────────────

    def build_plan(self) -> None:
        """Generate the full daily schedule."""
        self.scheduled_items.clear()
        self.unscheduled_tasks.clear()

        due_pairs = self.owner.get_all_due_tasks(self.date)
        ranked   = self.rank_tasks(due_pairs)
        windows  = self.owner.get_availability(self.date)
        self.fit_to_windows(ranked, windows)

    def rank_tasks(self, tasks: list[tuple[Task, Pet]]) -> list[tuple[Task, Pet]]:
        """Sort (task, pet) pairs by priority; pets with medical conditions go first."""
        def sort_key(pair: tuple[Task, Pet]):
            task, pet = pair
            priority_score  = self.PRIORITY_ORDER.get(task.priority, 99)
            medical_score   = 0 if pet.medical_conditions else 1
            return (priority_score, medical_score)

        return sorted(tasks, key=sort_key)

    def fit_to_windows(
        self,
        ranked_tasks: list[tuple[Task, Pet]],
        availability: list[tuple],
    ) -> None:
        """Assign ranked tasks to available time windows, respecting preferred_time."""
        # Build a mutable list of (start_hour, end_hour) windows with a cursor each
        windows = [{"start": s, "end": e, "cursor": s} for s, e in availability]

        for task, pet in ranked_tasks:
            duration_hrs = task.duration_minutes / 60
            placed = False

            # Try to find a window that matches preferred_time first, then any window
            ideal_hour = self.TIME_PREFERENCE.get(task.preferred_time, 8)
            windows_sorted = sorted(
                windows,
                key=lambda w: abs(w["cursor"] - ideal_hour)
            )

            for window in windows_sorted:
                slot_start  = window["cursor"]
                slot_end    = slot_start + duration_hrs

                if slot_end <= window["end"]:
                    start_dt = datetime(
                        self.date.year, self.date.month, self.date.day,
                        int(slot_start),
                        int((slot_start % 1) * 60),
                    )
                    reason = (
                        f"Scheduled at {start_dt.strftime('%H:%M')} | "
                        f"{task.priority} priority, fits {task.preferred_time} window"
                    )
                    if pet.medical_conditions:
                        reason += f" (medical flag: {', '.join(pet.medical_conditions)})"

                    self.scheduled_items.append(
                        ScheduledItem(task=task, pet=pet, start_time=start_dt, reason=reason)
                    )
                    window["cursor"] = slot_end   # advance cursor
                    placed = True
                    break

            if not placed:
                self.unscheduled_tasks.append(task)

    # ── output & interaction ───────────────────────────────────────────────────

    def explain(self) -> str:
        """Return a human-readable explanation of the daily plan."""
        if not self.scheduled_items:
            return "No tasks scheduled. Check availability windows or add tasks."

        lines = [f"\n{'='*55}", f"  Daily Plan for {self.owner.name} | {self.date}", f"{'='*55}"]

        for item in sorted(self.scheduled_items, key=lambda i: i.start_time):
            end_dt = item.start_time + timedelta(minutes=item.task.duration_minutes)
            lines.append(
                f"\n  [{item.start_time.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}]"
                f"  {item.pet.name}: {item.task.name}"
            )
            lines.append(f"    >> {item.reason}")

        if self.unscheduled_tasks:
            lines.append(f"\n  [!] Could not fit {len(self.unscheduled_tasks)} task(s):")
            for t in self.unscheduled_tasks:
                lines.append(f"    - {t.name} ({t.priority} priority, {t.duration_minutes} min)")

        lines.append(f"\n{'='*55}\n")
        return "\n".join(lines)

    def mark_done(self, task: Task) -> None:
        """Mark a scheduled task as completed and update its last_completed timestamp."""
        for item in self.scheduled_items:
            if item.task is task:
                item.status = "done"
                task.mark_complete(datetime.now())
                return
        print(f"  [!] Task '{task.name}' not found in today's schedule.")
