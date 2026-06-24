# Simple PawPal+ system class skeletons
from __future__ import annotations
from dataclasses import dataclass, field
import datetime
from typing import List, Optional
import uuid


@dataclass
class Task:
	name: str
	duration_minutes: int
	priority: str = "medium"
	frequency: str = "daily"
	is_complete: bool = False
	scheduled_time: Optional[datetime.datetime] = None
	id: str = field(default_factory=lambda: str(uuid.uuid4()))

	def reschedule(self, new_time: Optional[datetime.datetime]) -> None:
		"""Reschedule task to `new_time`; pass None to clear it."""
		self.scheduled_time = new_time

	def mark_complete(self) -> None:
		"""Mark the task as complete."""
		self.is_complete = True


@dataclass
class Pet:
	name: str
	species: str
	notes: Optional[str] = None
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a task to the pet's list of tasks."""
		self.tasks.append(task)

	def remove_task(self, task_id: str) -> None:
		"""Remove a task by its ID. Raises ValueError if not found."""
		original_count = len(self.tasks)
		self.tasks = [t for t in self.tasks if t.id != task_id]
		if len(self.tasks) == original_count:
			raise ValueError(f"Task not found: {task_id}")


@dataclass
class Owner:
	name: str
	pets: List[Pet] = field(default_factory=list)
	preferences: List[str] = field(default_factory=list)
	day_start: datetime.time = field(default_factory=lambda: datetime.time(8, 0))
	day_end: datetime.time = field(default_factory=lambda: datetime.time(20, 0))

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to the owner's list of pets."""
		self.pets.append(pet)

	def remove_pet(self, pet_name: str) -> None:
		"""Remove a pet by name. Raises ValueError if not found."""
		original_count = len(self.pets)
		self.pets = [p for p in self.pets if p.name != pet_name]
		if len(self.pets) == original_count:
			raise ValueError(f"Pet not found: {pet_name}")

	def set_day_window(self, start: datetime.time, end: datetime.time) -> None:
		"""Set the owner's daily scheduling window; raises on invalid bounds."""
		if start >= end:
			raise ValueError("day_start must be before day_end")
		self.day_start = start
		self.day_end = end


class Scheduler:
	"""Simple scheduler stub. Provide an Owner and call generate_schedule().

	This implementation is intentionally minimal — later you can add
	sorting, filtering, and constraint handling.
	"""

	def __init__(self, owner: Owner):
		"""Initialize the scheduler with an owner."""
		self.owner = owner

	def add_task(self, pet_name: str, task: Task) -> None:
		"""Add a task to a specific pet by name."""
		for pet in self.owner.pets:
			if pet.name == pet_name:
				pet.add_task(task)
				return
		raise ValueError(f"Pet not found: {pet_name}")

	def remove_task(self, pet_name: str, task_id: str) -> None:
		"""Remove a task from a specific pet by task ID."""
		for pet in self.owner.pets:
			if pet.name == pet_name:
				pet.remove_task(task_id)
				return
		raise ValueError(f"Pet not found: {pet_name}")

	def _collect_all_tasks(self) -> List[Task]:
		"""Return a flat list of all tasks across all pets."""
		all_tasks: List[Task] = []
		for pet in self.owner.pets:
			all_tasks.extend(pet.tasks)
		return all_tasks

	def generate_schedule(self) -> List[Task]:
		"""Generate today's schedule by packing tasks into the owner's window."""
		# Build schedule within owner's daily window using a greedy algorithm.
		priority_order = {"high": 0, "medium": 1, "low": 2}

		today = datetime.date.today()
		window_start = datetime.datetime.combine(today, self.owner.day_start)
		window_end = datetime.datetime.combine(today, self.owner.day_end)

		tasks = [t for t in self._collect_all_tasks() if not t.is_complete]

		# Separate fixed-time tasks and flexible tasks
		fixed = [t for t in tasks if t.scheduled_time is not None]
		flexible = [t for t in tasks if t.scheduled_time is None]

		# Normalize fixed times to today's date if they are time-only
		fixed = sorted(fixed, key=lambda t: t.scheduled_time)

		# Sort flexible by priority then duration
		flexible.sort(key=lambda t: (priority_order.get(t.priority.lower(), 1), t.duration_minutes))

		scheduled: List[Task] = []
		pointer = window_start

		# Helper to try to schedule flexible tasks until a limit
		def fill_until(limit: datetime.datetime):
			"""Fill flexible tasks until `limit` by scheduling them at `pointer`."""
			nonlocal pointer
			i = 0
			while i < len(flexible):
				task = flexible[i]
				end_time = pointer + datetime.timedelta(minutes=task.duration_minutes)
				if end_time <= limit and end_time <= window_end:
					task.scheduled_time = pointer
					scheduled.append(task)
					pointer = end_time
					flexible.pop(i)
				else:
					i += 1

		# Fill before each fixed task
		for f in fixed:
			# if fixed time is outside window, skip or adjust
			f_start = f.scheduled_time
			f_end = f_start + datetime.timedelta(minutes=f.duration_minutes)
			if f_end <= window_start or f_start >= window_end:
				# fixed task outside today's window - keep as-is but don't schedule inside window
				continue
			# schedule flexible tasks before this fixed task
			fill_until(f_start)
			# ensure pointer moves to end of fixed if it's later
			if pointer < f_end:
				pointer = f_end
			scheduled.append(f)

		# Fill remaining time after last fixed
		fill_until(window_end)

		# Return scheduled tasks sorted by time
		scheduled.sort(key=lambda t: t.scheduled_time or datetime.datetime.max)
		return scheduled

	def explain_schedule(self) -> str:
		"""Return the schedule formatted like `main.py`'s print output."""
		# build task->pet mapping for quick lookup
		task_to_pet = {}
		for pet in self.owner.pets:
			for task in pet.tasks:
				task_to_pet[task.id] = pet.name

		tasks = self.generate_schedule()
		lines = []
		for t in tasks:
			ts = t.scheduled_time.strftime("%I:%M %p") if t.scheduled_time else "unscheduled"
			pet_name = task_to_pet.get(t.id, "")
			lines.append(f" - {ts} - {t.name.title()} for {pet_name} ({t.duration_minutes}m) [{t.priority} priority]")
		return "Today's Schedule:\n" + "\n".join(lines)