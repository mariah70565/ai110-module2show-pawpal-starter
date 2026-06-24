import datetime
from pawpal_system import Task, Pet, Owner, Scheduler

# get today's date for scheduling
today = datetime.date.today()

# creating owner
owner = Owner(name="Jordan")

# creating pets
dog = Pet(name="Mochi", species="dog")
cat = Pet(name="Whiskers", species="cat")

# adding tasks for the dog
dog.add_task(Task(name="Morning walk", task_type="walk", duration_minutes=30, priority="high"))
dog.add_task(Task(name="Feed", task_type="feeding", duration_minutes=10, priority="high"))

# adding tasks for the cat
cat.add_task(Task(name="Playtime", task_type="play", duration_minutes=20, priority="medium"))
cat.add_task(Task(name="Vet visit", task_type="appointment", duration_minutes=60, priority="high", scheduled_time=datetime.datetime.combine(today, datetime.time(10, 0)))) #vet visit for 10am

# adding pets to the owner
owner.add_pet(dog)
owner.add_pet(cat)

# creating the scheduler and generating the schedule
scheduler = Scheduler(owner)
plan = scheduler.generate_schedule()

print(scheduler.explain_schedule())