# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

PawPal+ now includes algorithmic features that make the scheduler more intelligent:

**Sorting by time** — `Scheduler.sort_by_time()` returns scheduled items in chronological order.

**Filtering** — Two filter methods let you slice the schedule by pet or status:
- `filter_by_pet(pet_name)` — returns only tasks for a named pet (case-insensitive)
- `filter_by_status(status)` — returns tasks matching `"pending"` or `"done"`

**Recurring tasks** — When `mark_done()` is called on a `daily` or `weekly` task, `_spawn_next_occurrence()` automatically creates the next instance using Python's `timedelta`:
- Daily → due tomorrow (`schedule_date + timedelta(days=1)`)
- Weekly → due in 7 days (`schedule_date + timedelta(days=7)`)

**Conflict detection** — `detect_conflicts()` checks every unique pair of scheduled items using `itertools.combinations` and returns warning strings (never crashes). Two tasks conflict when their time windows overlap: `a.start < b.end AND b.start < a.end`.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
