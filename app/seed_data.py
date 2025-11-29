from datetime import datetime, date
from config import SessionLocal
from models.entities import Member, Trainer, Room, ClassSession, PTSession

# This script just fills the database with some basic data so I can test my project.
# I’m adding a couple of trainers, rooms, one member, one class, and one PT session.
# Nothing fancy, just enough to get things running.

def seed():
    db = SessionLocal()

    # adding some trainers
    trainer1 = Trainer(
        full_name="Sarah Johnson",
        email="sarah@club.com",
        specialty="Yoga"
    )

    trainer2 = Trainer(
        full_name="Mark Thompson",
        email="mark@club.com",
        specialty="Strength Training"
    )

    # adding rooms inside the gym
    room1 = Room(name="Studio A", capacity=20)
    room2 = Room(name="Studio B", capacity=15)

    # adding a member (using my name just for testing)
    member1 = Member(
        full_name="Abdulrahman Aldousari",
        email="abd@example.com",
        date_of_birth=date(2004, 10, 15),
        gender="Male",
        phone="123-456-7890"
    )

    # a sample group class
    class1 = ClassSession(
        title="Morning Yoga",
        start_time=datetime(2025, 1, 5, 9, 0),
        end_time=datetime(2025, 1, 5, 10, 0),
        capacity=20,
        room=room1,
        trainer=trainer1
    )

    # a PT session so I can test trainer scheduling and booking later
    pt1 = PTSession(
        start_time=datetime(2025, 1, 6, 14, 0),
        end_time=datetime(2025, 1, 6, 15, 0),
        status="scheduled",
        member=member1,
        trainer=trainer2,
        room=room2
    )

    # saving everything to the database
    db.add_all([trainer1, trainer2, room1, room2, member1, class1, pt1])
    db.commit()
    db.close()

    print("Sample data inserted successfully.")

if __name__ == "__main__":
    seed()
