from datetime import datetime, date
from config import SessionLocal
from models.entities import Member, Trainer, Room, ClassSession, PTSession, HealthMetric, Invoice


# I’m using one shared session per run. For a bigger app I’d manage this differently,
# but for this project and the demo it keeps things simple.
db = SessionLocal()


#MEMBER FUNCTIONS


def register_member():
    print("\n=== Register New Member ===")
    full_name = input("Full name: ").strip()
    email = input("Email (must be unique): ").strip()
    dob_str = input("Date of birth (YYYY-MM-DD) or leave empty: ").strip()
    gender = input("Gender (optional): ").strip()
    phone = input("Phone (optional): ").strip()

    dob = None
    if dob_str:
        try:
            dob = date.fromisoformat(dob_str)
        except ValueError:
            print("Invalid date format, saving without date of birth.")
            dob = None

    member = Member(
        full_name=full_name,
        email=email,
        date_of_birth=dob,
        gender=gender if gender else None,
        phone=phone if phone else None
    )

    try:
        db.add(member)
        db.commit()
        print(f"Member created with id: {member.id}")
    except Exception as e:
        db.rollback()
        print("Error creating member:", e)


def update_member_goal():
    print("\n=== Update Member Fitness Goal ===")
    member_id_str = input("Member id: ").strip()
    if not member_id_str.isdigit():
        print("Member id must be a number.")
        return

    member = db.get(Member, int(member_id_str))
    if not member:
        print("Member not found.")
        return

    print(f"Current goal: {member.fitness_goal}")
    print(f"Current target weight: {member.target_weight}")
    new_goal = input("New goal description (leave empty to keep current): ").strip()
    target_weight_str = input("New target weight (kg, optional): ").strip()

    if new_goal:
        member.fitness_goal = new_goal

    if target_weight_str:
        try:
            member.target_weight = float(target_weight_str)
        except ValueError:
            print("Invalid number for target weight, keeping old value.")

    try:
        db.commit()
        print("Member goal updated.")
    except Exception as e:
        db.rollback()
        print("Error updating goal:", e)


def add_health_metric():
    print("\n=== Add Health Metric ===")
    member_id_str = input("Member id: ").strip()
    if not member_id_str.isdigit():
        print("Member id must be a number.")
        return

    member = db.get(Member, int(member_id_str))
    if not member:
        print("Member not found.")
        return

    time_str = input("Recorded at (YYYY-MM-DD HH:MM) or leave empty for now: ").strip()
    if time_str:
        try:
            recorded_at = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date/time format, using current time instead.")
            recorded_at = datetime.now()
    else:
        recorded_at = datetime.now()

    weight_str = input("Weight (kg, optional): ").strip()
    heart_rate_str = input("Heart rate (bpm, optional): ").strip()
    body_fat_str = input("Body fat % (optional): ").strip()

    weight = float(weight_str) if weight_str else None
    heart_rate = int(heart_rate_str) if heart_rate_str else None
    body_fat = float(body_fat_str) if body_fat_str else None

    metric = HealthMetric(
        member_id=member.id,
        recorded_at=recorded_at,
        weight=weight,
        heart_rate=heart_rate,
        body_fat_percentage=body_fat
    )

    try:
        db.add(metric)
        db.commit()
        print("Health metric saved.")
    except Exception as e:
        db.rollback()
        print("Error saving health metric:", e)


def book_pt_session():
    print("\n=== Book Personal Training Session ===")
    member_id_str = input("Member id: ").strip()
    trainer_id_str = input("Trainer id: ").strip()
    room_id_str = input("Room id: ").strip()

    start_str = input("Start time (YYYY-MM-DD HH:MM): ").strip()
    end_str = input("End time (YYYY-MM-DD HH:MM): ").strip()

    if not (member_id_str.isdigit() and trainer_id_str.isdigit() and room_id_str.isdigit()):
        print("Ids must be numbers.")
        return

    try:
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date/time format.")
        return

    if end_time <= start_time:
        print("End time must be after start time.")
        return

    member = db.get(Member, int(member_id_str))
    trainer = db.get(Trainer, int(trainer_id_str))
    room = db.get(Room, int(room_id_str))

    if not member:
        print("Member not found.")
        return
    if not trainer:
        print("Trainer not found.")
        return
    if not room:
        print("Room not found.")
        return

    # very simple overlap check for trainer and room
    overlapping_pt = (
        db.query(PTSession)
        .filter(
            PTSession.trainer_id == trainer.id,
            PTSession.start_time < end_time,
            PTSession.end_time > start_time,
            PTSession.status != "cancelled",
        )
        .all()
    )

    overlapping_room = (
        db.query(PTSession)
        .filter(
            PTSession.room_id == room.id,
            PTSession.start_time < end_time,
            PTSession.end_time > start_time,
            PTSession.status != "cancelled",
        )
        .all()
    )

    if overlapping_pt:
        print("Trainer already has a session at that time.")
        return

    if overlapping_room:
        print("Room is already booked at that time.")
        return

    session = PTSession(
        member_id=member.id,
        trainer_id=trainer.id,
        room_id=room.id,
        start_time=start_time,
        end_time=end_time,
        status="scheduled",
    )

    try:
        db.add(session)
        db.commit()
        print(f"PT session booked with id: {session.id}")
    except Exception as e:
        db.rollback()
        print("Error booking PT session:", e)


#TRAINER FUNCTIONS


def view_trainer_schedule():
    print("\n=== Trainer Schedule ===")
    trainer_id_str = input("Trainer id: ").strip()
    if not trainer_id_str.isdigit():
        print("Trainer id must be a number.")
        return

    trainer = db.get(Trainer, int(trainer_id_str))
    if not trainer:
        print("Trainer not found.")
        return

    print(f"\nSchedule for {trainer.full_name}:")

    pt_sessions = (
        db.query(PTSession)
        .filter(PTSession.trainer_id == trainer.id)
        .order_by(PTSession.start_time)
        .all()
    )

    class_sessions = (
        db.query(ClassSession)
        .filter(ClassSession.trainer_id == trainer.id)
        .order_by(ClassSession.start_time)
        .all()
    )

    print("\nPersonal training sessions:")
    if not pt_sessions:
        print("  none")
    else:
        for s in pt_sessions:
            print(f"  PT {s.id}: {s.start_time} -> {s.end_time} | member_id={s.member_id} | status={s.status}")

    print("\nGroup classes:")
    if not class_sessions:
        print("  none")
    else:
        for c in class_sessions:
            print(f"  Class {c.id}: {c.title} at {c.start_time} in room {c.room_id}")


def trainer_lookup_member():
    print("\n=== Trainer Member Lookup ===")
    name_part = input("Enter part of member name (case-insensitive): ").strip()

    members = (
        db.query(Member)
        .filter(Member.full_name.ilike(f"%{name_part}%"))
        .all()
    )

    if not members:
        print("No members found.")
        return

    for m in members:
        print(f"\nMember id: {m.id} | Name: {m.full_name} | Goal: {m.fitness_goal}")

        last_metric = (
            db.query(HealthMetric)
            .filter(HealthMetric.member_id == m.id)
            .order_by(HealthMetric.recorded_at.desc())
            .first()
        )

        if last_metric:
            print(
                f"  Last metric at {last_metric.recorded_at}: "
                f"weight={last_metric.weight}, "
                f"heart_rate={last_metric.heart_rate}, "
                f"body_fat={last_metric.body_fat_percentage}"
            )
        else:
            print("  No health metrics recorded yet.")


#ADMIN FUNCTIONS


def create_class_session():
    print("\n=== Create New Class Session (Admin) ===")
    title = input("Class title: ").strip()
    room_id_str = input("Room id: ").strip()
    trainer_id_str = input("Trainer id: ").strip()
    capacity_str = input("Capacity: ").strip()
    start_str = input("Start time (YYYY-MM-DD HH:MM): ").strip()
    end_str = input("End time (YYYY-MM-DD HH:MM): ").strip()

    if not (room_id_str.isdigit() and trainer_id_str.isdigit() and capacity_str.isdigit()):
        print("Room id, trainer id and capacity must be numbers.")
        return

    try:
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date/time format.")
        return

    if end_time <= start_time:
        print("End time must be after start time.")
        return

    room = db.get(Room, int(room_id_str))
    trainer = db.get(Trainer, int(trainer_id_str))

    if not room:
        print("Room not found.")
        return
    if not trainer:
        print("Trainer not found.")
        return

    # rough double booking check for room
    overlapping_class = (
        db.query(ClassSession)
        .filter(
            ClassSession.room_id == room.id,
            ClassSession.start_time < end_time,
            ClassSession.end_time > start_time,
        )
        .all()
    )

    if overlapping_class:
        print("Room already has a class at that time.")
        return

    new_class = ClassSession(
        title=title,
        start_time=start_time,
        end_time=end_time,
        capacity=int(capacity_str),
        room_id=room.id,
        trainer_id=trainer.id,
    )

    try:
        db.add(new_class)
        db.commit()
        print(f"Class created with id: {new_class.id}")
    except Exception as e:
        db.rollback()
        print("Error creating class:", e)


def create_invoice():
    print("\n=== Create Invoice (Admin) ===")
    member_id_str = input("Member id: ").strip()
    amount_str = input("Amount: ").strip()
    description = input("Description (e.g. monthly membership, PT package): ").strip()

    if not (member_id_str.isdigit()):
        print("Member id must be a number.")
        return

    try:
        amount = float(amount_str)
    except ValueError:
        print("Amount must be a number.")
        return

    member = db.get(Member, int(member_id_str))
    if not member:
        print("Member not found.")
        return

    invoice = Invoice(
        member_id=member.id,
        created_at=datetime.now(),
        amount=amount,
        status="unpaid",
        description=description if description else None,
    )

    try:
        db.add(invoice)
        db.commit()
        print(f"Invoice created with id: {invoice.id}")
    except Exception as e:
        db.rollback()
        print("Error creating invoice:", e)


# MENU 


def main_menu():
    while True:
        print("\n============================")
        print(" Health Club Management CLI ")
        print("============================")
        print("1. Register new member")
        print("2. Update member fitness goal")
        print("3. Add health metric for a member")
        print("4. Book PT session")
        print("5. View trainer schedule")
        print("6. Trainer member lookup")
        print("7. Create class session (admin)")
        print("8. Create invoice (admin)")
        print("9. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_member()
        elif choice == "2":
            update_member_goal()
        elif choice == "3":
            add_health_metric()
        elif choice == "4":
            book_pt_session()
        elif choice == "5":
            view_trainer_schedule()
        elif choice == "6":
            trainer_lookup_member()
        elif choice == "7":
            create_class_session()
        elif choice == "8":
            create_invoice()
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    try:
        main_menu()
    finally:
        db.close()
