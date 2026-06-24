from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
	t = Task(name="Test Task", duration_minutes=5)
	assert t.is_complete is False
	t.mark_complete()
	assert t.is_complete is True


def test_add_task_increases_count():
	p = Pet(name="Fido", species="dog")
	before = len(p.tasks)
	p.add_task(Task(name="Feed", duration_minutes=10))
	assert len(p.tasks) == before + 1
	p.add_task(Task(name="Walk", duration_minutes=30))
	assert len(p.tasks) == before + 2

