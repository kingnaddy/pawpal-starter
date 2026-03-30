import streamlit as st
from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# Session State Vault
# Check before creating - Owner and Pet survive every rerun
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner("Jordan")

owner: Owner = st.session_state["owner"]

# Owner Setup
st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name

# Availability
st.markdown("#### Availability Windows (today)")
st.caption("Set the time blocks you're free to care for your pets.")

col1, col2 = st.columns(2)
with col1:
    start_hour = st.number_input("Window start (hour)", min_value=0, max_value=23, value=7)
with col2:
    end_hour = st.number_input("Window end (hour)", min_value=1, max_value=24, value=21)

if st.button("Set Availability"):
    owner.set_availability(date.today(), [(start_hour, end_hour)])
    st.success(f"Availability set: {start_hour}:00 - {end_hour}:00")

st.divider()

# Add a Pet
st.subheader("Pets")

with st.form("add_pet_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        age = st.number_input("Age", min_value=0, max_value=30, value=3)
    conditions = st.text_input("Medical conditions (comma-separated, or leave blank)")
    submitted = st.form_submit_button("Add Pet")

if submitted:
    condition_list = [c.strip() for c in conditions.split(",") if c.strip()]
    new_pet = Pet(name=pet_name, species=species, age=age, medical_conditions=condition_list)
    owner.add_pet(new_pet)
    st.success(f"Added {pet_name}!")

# show current pets
if owner.pets:
    st.markdown("**Current pets:**")
    for pet in owner.pets:
        st.markdown(f"- {pet.get_profile()}")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# Add a Task
st.subheader("Tasks")

if not owner.pets:
    st.warning("Add a pet first before adding tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_names   = [p.name for p in owner.pets]
        target_pet  = st.selectbox("Assign to pet", pet_names)

        col1, col2 = st.columns(2)
        with col1:
            task_name = st.text_input("Task name", value="Morning walk")
            category  = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment"])
            priority  = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with col2:
            frequency      = st.selectbox("Frequency", ["daily", "weekly", "as-needed"])
            duration       = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            preferred_time = st.selectbox("Preferred time", ["morning", "afternoon", "evening"])

        task_submitted = st.form_submit_button("Add Task")

    if task_submitted:
        new_task = Task(
            name=task_name,
            category=category,
            priority=priority,
            frequency=frequency,
            duration_minutes=int(duration),
            preferred_time=preferred_time,
        )
        pet_obj = next(p for p in owner.pets if p.name == target_pet)
        pet_obj.add_task(new_task)
        st.success(f"Added '{task_name}' to {target_pet}!")

    # show all tasks across pets
    all_tasks = [(t, p) for p in owner.pets for t in p.tasks]
    if all_tasks:
        st.markdown("**All tasks:**")
        for task, pet in all_tasks:
            st.markdown(
                f"- **{pet.name}** | {task.name} | {task.priority} priority | "
                f"{task.duration_minutes} min | {task.preferred_time}"
            )

st.divider()

# Generate Schedule
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    if not owner.pets or not any(p.tasks for p in owner.pets):
        st.warning("Add at least one pet and one task first.")
    elif not owner.get_availability(date.today()):
        st.warning("Set your availability windows before generating a schedule.")
    else:
        scheduler = Scheduler(owner=owner, schedule_date=date.today())
        scheduler.build_plan()

        st.success("Schedule generated!")

        for item in sorted(scheduler.scheduled_items, key=lambda i: i.start_time):
            end_dt = item.start_time + timedelta(minutes=item.task.duration_minutes)
            with st.container(border=True):
                st.markdown(
                    f"**[{item.start_time.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}]**  "
                    f"{item.pet.name}: {item.task.name}"
                )
                st.caption(f">> {item.reason}")

        if scheduler.unscheduled_tasks:
            st.warning(f"Could not fit {len(scheduler.unscheduled_tasks)} task(s):")
            for t in scheduler.unscheduled_tasks:
                label = f"- {t.name} | {t.priority} priority | {t.duration_minutes} min"
                st.markdown(label)