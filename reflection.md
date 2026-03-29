# PawPal+ Project Reflection

add pet info
add tasks and see added tasks
make a plan/schedule
## 1. System Design

**a. Initial design**

I went with 4 classes: `Pet`, `Task`, `Owner`, and `Scheduler`. `Pet` holds the animal's info and owns a list of tasks. `Task` stores what needs to be done, more details about the task and knows if it's due. `Owner` tracks the human's pets, time availability, and preferences. `Scheduler` takes all that info and builds a daily plan, ranks tasks, fits them into open time slots, and explains its choices.

**b. Design changes**

Yeah, a few things shifted. Added a `ScheduledItem` dataclass to replace the sketchy `list[dict]` in `Scheduler` since untyped dicts are a misspelled key away from a bug. Gave `Task` a back-reference to its `Pet` so the scheduler doesn't have to juggle that link manually. Also updated `rank_tasks()` to take `(Task, Pet)` pairs so it can factor in medical conditions when prioritizing. Dropped `skip()` and `skipped_reason` entirely because they added complexity with no real payoff.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
