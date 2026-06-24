# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Identify 3 core actions a user should be able to perform.
    - Add a pet, schedule a feeding, view today's tasks
- Briefly describe your initial UML design.
    - I created 4 objects, scheduler, owner, pet, and task. The scheduler is assigned to an owner, which holds a list of pets, where each pet holds a list of tasks. This allows for an owner to view tasks for all of their pets if they have more than 1. I also added various functions that provide the ability to add or remove task, generate the schedule, receive an explanation for the schedule, add or remove a pet, and reschedule a task.
- What classes did you include, and what responsibilities did you assign to each?
    - the classes I included were Scheduler, Owner, Pet, and Task. Scheduler has the ability to add or remove a task to the schedule, generate the schedule, and explain how the schedule was created. Owner has the ability to add or remove a pet to track its tasks. Pet has the ability to add a task. Task has the ability to reschedule a task.

**b. Design changes**

- Did your design change during implementation?
    - yes
- If yes, describe at least one change and why you made it.
    - when it came to removing a task, I was originally removing by the task object, rather than its name. But then I realized removing by name wouldn't work either, in the case where a pet may have multiple feedings, then how do we identify which feeding task to remove? I change the task object to have a unique id, such that it can be referenced for removal, instead of by its object or by its name.

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
