from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# ── Setup Owner ────────────────────────────────────────────────────────────────
owner = Owner(
    name="Jordan",
    preferences={"walk_before": "09:00"}
)

# availability windows for today: (start_hour, end_hour)
today = date.today()
owner.set_availability(today, [(7, 10), (12, 14), (17, 21)])

# ── Setup Pets ─────────────────────────────────────────────────────────────────
mango = Pet(name="Mango", species="Dog", age=4, medical_conditions=["arthritis"])
luna  = Pet(name="Luna",  species="Cat", age=2)

owner.add_pet(mango)
owner.add_pet(luna)

# ── Add Tasks to Mango (Dog) ───────────────────────────────────────────────────
mango.add_task(Task(
    name="Morning Walk",
    category="walk",
    priority="high",
    frequency="daily",
    duration_minutes=30,
    preferred_time="morning",
))

mango.add_task(Task(
    name="Joint Supplement",
    category="meds",
    priority="high",
    frequency="daily",
    duration_minutes=5,
    preferred_time="morning",
))

mango.add_task(Task(
    name="Breakfast",
    category="feeding",
    priority="high",
    frequency="daily",
    duration_minutes=10,
    preferred_time="morning",
))

mango.add_task(Task(
    name="Evening Walk",
    category="walk",
    priority="medium",
    frequency="daily",
    duration_minutes=25,
    preferred_time="evening",
))

# ── Add Tasks to Luna (Cat) ────────────────────────────────────────────────────
luna.add_task(Task(
    name="Breakfast",
    category="feeding",
    priority="high",
    frequency="daily",
    duration_minutes=5,
    preferred_time="morning",
))

luna.add_task(Task(
    name="Playtime",
    category="enrichment",
    priority="medium",
    frequency="daily",
    duration_minutes=20,
    preferred_time="afternoon",
))

luna.add_task(Task(
    name="Brush Coat",
    category="grooming",
    priority="low",
    frequency="weekly",
    duration_minutes=15,
    preferred_time="evening",
))

# ── Run Scheduler ──────────────────────────────────────────────────────────────
scheduler = Scheduler(owner=owner, schedule_date=today)
scheduler.build_plan()

# ── Print Today's Schedule ─────────────────────────────────────────────────────
print(scheduler.explain())

# ── Quick mark_done demo ───────────────────────────────────────────────────────
print("Completing Mango's Morning Walk...")
morning_walk = mango.tasks[0]
scheduler.mark_done(morning_walk)
print(f"  Status: {scheduler.scheduled_items[0].status}")
print(f"  Last completed: {morning_walk.last_completed.strftime('%Y-%m-%d %H:%M')}\n")
