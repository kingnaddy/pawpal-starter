import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from pawpal_system import Task, Pet


# ── Test 1: mark_complete() stamps last_completed ─────────────────────────────
def test_mark_complete_updates_last_completed():
    task = Task(
        name="Morning Walk",
        category="walk",
        priority="high",
        frequency="daily",
        duration_minutes=30,
        preferred_time="morning",
    )

    assert task.last_completed is None          # should start empty

    timestamp = datetime(2026, 3, 29, 8, 0)
    task.mark_complete(timestamp)

    assert task.last_completed == timestamp     # should now be set


# ── Test 2: add_task() increases pet's task count ─────────────────────────────
def test_add_task_increases_task_count():
    pet = Pet(name="Mango", species="Dog", age=4)

    assert len(pet.tasks) == 0                  # should start empty

    task = Task(
        name="Breakfast",
        category="feeding",
        priority="high",
        frequency="daily",
        duration_minutes=10,
        preferred_time="morning",
    )
    pet.add_task(task)

    assert len(pet.tasks) == 1                  # should now have one task
    assert pet.tasks[0].name == "Breakfast"     # and it should be the right one
    assert task.pet is pet                      # back-reference should be set too
