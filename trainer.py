from psycopg2 import DatabaseError



def bookSession(conn):
    member_id = input("Enter member ID: ")
    trainer_id = input("Enter trainer ID: ")
    session_type = input("Enter session type (Personal or Group): ")
    start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
    end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
    class_type = input("Enter class type (if applicable, otherwise leave blank): ")
    room_id = input("Enter room ID (if applicable, otherwise leave blank): ")
    _bookSession(conn, member_id, trainer_id, session_type, start_time, end_time, class_type, room_id)

def _bookSession(conn, member_id, trainer_id, session_type, start_time, end_time, class_type, room_id):
    try:
        cur = conn.cursor()
        # Inserting the new session into the Schedule table
        cur.execute("""
            INSERT INTO Schedule (TrainerID, SessionType, StartTime, EndTime, MemberID, RoomID, Status, ClassType)
            VALUES (%s, %s, %s, %s, %s, %s, 'Booked', %s);
            """, (trainer_id, session_type, start_time, end_time, member_id or None, room_id or None, class_type))
        conn.commit()
        print("Session booked successfully.")
    except DatabaseError as e:
        print(f"Failed to book session: {e}")
        conn.rollback()
    finally:
        cur.close()

def rescheduleSession(conn):
    session_id = input("Enter session ID to reschedule: ")
    new_start_time = input("Enter new start time (YYYY-MM-DD HH:MM): ")
    new_end_time = input("Enter new end time (YYYY-MM-DD HH:MM): ")
    _rescheduleSession(conn, session_id, new_start_time, new_end_time)

def _rescheduleSession(conn, session_id, new_start_time, new_end_time):
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Schedule
            SET StartTime = %s, EndTime = %s
            WHERE SessionID = %s;
            """, (new_start_time, new_end_time, session_id))
        conn.commit()
        if cur.rowcount:
            print("Session rescheduled successfully.")
        else:
            print("No session found with that ID.")
    except DatabaseError as e:
        print(f"Failed to reschedule session: {e}")
        conn.rollback()
    finally:
        cur.close()

def cancelSession(conn):
    session_id = input("Enter session ID to cancel: ")
    _cancelSession(conn, session_id)

def _cancelSession(conn, session_id):
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Schedule
            SET Status = 'Cancelled'
            WHERE SessionID = %s;
            """, (session_id,))
        conn.commit()
        if cur.rowcount:
            print("Session cancelled successfully.")
        else:
            print("No session found with that ID.")
    except DatabaseError as e:
        print(f"Failed to cancel session: {e}")
        conn.rollback()
    finally:
        cur.close()

def setTrainerAvailability(conn):
    trainer_id = input("Enter trainer ID to set availability: ")
    print("Enter availability timeslots (one per line, format 'YYYY-MM-DD HH:MM to YYYY-MM-DD HH:MM'), type 'done' when finished:")
    availability_slots = []
    while True:
        line = input()
        if line.lower() == 'done':
            break
        availability_slots.append(line.split(" to "))
    _setTrainerAvailability(conn, trainer_id, availability_slots)

def _setTrainerAvailability(conn, trainer_id, availability_slots):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM TrainerAvailability WHERE TrainerID = %s;", (trainer_id,))
        for slot in availability_slots:
            cur.execute("""
                INSERT INTO TrainerAvailability (TrainerID, StartTime, EndTime)
                VALUES (%s, %s, %s);
                """, (trainer_id, slot[0], slot[1]))
        conn.commit()
        print("Trainer availability set successfully.")
    except DatabaseError as e:
        print(f"Failed to set trainer availability: {e}")