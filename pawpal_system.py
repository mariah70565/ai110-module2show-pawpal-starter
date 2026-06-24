# Simple PawPal+ system class skeletons
from __future__ import annotations
from dataclasses import dataclass, field
import datetime
from typing import List, Optional
import uuid


@dataclass
class Task:
	name: str
	task_type: str
	duration_minutes: int
	priority: str = "medium"
	scheduled_time: Optional[datetime.datetime] = None
	id: str = field(default_factory=lambda: str(uuid.uuid4()))

	def reschedule(self, new_time: datetime.datetime) -> None:
		"""Reschedule the task to a new time."""
		self.scheduled_time = new_time


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
	available_minutes_per_day: Optional[int] = None

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to the owner's list of pets."""
		self.pets.append(pet)

	def remove_pet(self, pet_name: str) -> None:
		"""Remove a pet by name. Raises ValueError if not found."""
		original_count = len(self.pets)
		self.pets = [p for p in self.pets if p.name != pet_name]
		if len(self.pets) == original_count:
			raise ValueError(f"Pet not found: {pet_name}")


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
		"""Return a simple ordered list of tasks for the day.

		Current behavior: flatten tasks and sort by priority (high, medium, low).
		"""
		priority_order = {"high": 0, "medium": 1, "low": 2}
		tasks = self._collect_all_tasks()
		tasks.sort(key=lambda t: (priority_order.get(t.priority.lower(), 1), t.duration_minutes))  # primary sort by priority, secondary sort by duration
		return tasks

	def explain_schedule(self) -> str:
		"""Return a human-readable explanation of the generated schedule."""
		tasks = self.generate_schedule()
		reasons = [f"{t.name}: priority={t.priority}, duration={t.duration_minutes}m" for t in tasks]
		return "; ".join(reasons)


if __name__ == "__main__":
	# quick demo
	owner = Owner(name="Jordan", available_minutes_per_day=180)
	dog = Pet(name="Mochi", species="dog")
	dog.add_task(Task(name="Morning walk", task_type="walk", duration_minutes=30, priority="high"))
	dog.add_task(Task(name="Feed", task_type="feeding", duration_minutes=10, priority="high"))
	owner.add_pet(dog)

	sched = Scheduler(owner)
	plan = sched.generate_schedule()
	print("Daily plan:")
	for t in plan:
		print(f" - {t.name} ({t.duration_minutes}m) [{t.priority}]")

