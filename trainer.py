from psycopg2 import DatabaseError
from werkzeug.security import generate_password_hash, check_password_hash

def view_all_booked_rooms(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Room_Bookings")
        booked_rooms = cur.fetchall()
        if booked_rooms:
            print("Booked Rooms:")
            for room in booked_rooms:
                print(f"BookingID: {room[0]}, RoomID: {room[1]}, TrainerID: {room[2]}, Start Time: {room[3]}, End Time: {room[4]}, Class Type: {room[5]}")
        else:
            print("No booked rooms.")
    
    except DatabaseError as e:
        print(f"An error occurred during viewing all bookings: {e}")
        return None
    finally:
        if cur:
            cur.close()


def delete_booked_room(conn,booking_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Room_Bookings WHERE BookingID = %s;", (booking_id,))
        conn.commit()
        if cur.rowcount:
            print("Booking deleted successfully.")
        else:
            print("No Room Booking found with that ID.")
    
    except DatabaseError as e:
        print(f"An error occurred during deleting room booking: {e}")
        return None
    finally:
        if cur:
            cur.close()

def create_room_booking(conn, room_id, trainer_id, start_time, end_time, class_type):
    try:
        cur = conn.cursor()
        # Check for booking conflicts before inserting
        cur.execute("""
            SELECT 1 FROM Room_Bookings WHERE RoomID = %s AND NOT (
                %s >= BookingEndTime OR %s <= BookingStartTime)
            """, (room_id, end_time, start_time))
        if cur.fetchone():
            print("This booking overlaps with another. Please choose a different time.")
            return
        
        # Insert the new booking
        cur.execute("""
            INSERT INTO Room_Bookings (RoomID, StaffID, BookingStartTime, BookingEndTime, ClassType)
            VALUES (%s, %s, %s, %s, %s);
            """, (room_id, trainer_id, start_time, end_time, class_type))
        conn.commit()
        print("Room booked successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()



def update_room_booking(conn, booking_id, new_room_id, new_start_time, new_end_time, new_class_type):
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Room_Bookings SET
            RoomID = %s, BookingStartTime = %s, BookingEndTime = %s, ClassType = %s
            WHERE BookingID = %s;
            """, (new_room_id, new_start_time, new_end_time, new_class_type, booking_id))
        conn.commit()
        if cur.rowcount:
            print("Booking updated successfully.")
        else:
            print("No Room Booking found with that ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()

def view_bookings_by_date(conn, date):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM Room_Bookings WHERE DATE(BookingStartTime) = %s OR DATE(BookingEndTime) = %s;
            """, (date, date))
        bookings = cur.fetchall()
        for booking in bookings:
            print(f"BookingID: {booking[0]}, RoomID: {booking[1]}, ...")
    except Exception as e:
        print(f"An error occurred: {e}")
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
        # First delete the associated entries in ScheduleMembers
        cur.execute("""
            DELETE FROM ScheduleMembers
            WHERE SessionID = %s;
            """, (session_id,))
        # Then delete the session
        cur.execute("""
            DELETE FROM Schedule
            WHERE SessionID = %s;
            """, (session_id,))
        conn.commit()
        if cur.rowcount:
            print("Session cancelled and all associated enrollments removed successfully.")
        else:
            print("No session found with that ID.")
    except DatabaseError as e:
        print(f"Failed to cancel session: {e}")
        conn.rollback()
    finally:
        cur.close()



def authenticate_trainer(conn):
    email = input("Enter your trainer email: ")
    password = input("Enter your password: ")
    try:
        cur = conn.cursor()
        cur.execute("SELECT TrainerID, Password FROM Trainers WHERE Email = %s;", (email,))
        trainer = cur.fetchone()
        if trainer:
            stored_password = trainer[1]
            if check_password_hash(stored_password, password):
                return trainer[0]  # Return the TrainerID if the password is correct
            else:
                print("Invalid email or password. Please try again.")
                return None
        else:
            print("No trainer found with that email. Please try again.")
            return None
    except DatabaseError as e:
        print(f"An error occurred during trainer login: {e}")
        return None
    finally:
        if cur:
            cur.close()

def update_trainer_email(conn, trainer_id, new_email):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE Trainers SET Email = %s WHERE TrainerID = %s;", (new_email, trainer_id))
        conn.commit()
        if cur.rowcount:
            print("Email updated successfully.")
        else:
            print("Trainer not found.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()


def view_my_booked_rooms(conn, trainer_id):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT BookingID, RoomID, BookingStartTime, BookingEndTime, ClassType
            FROM Room_Bookings
            WHERE TrainerID = %s;
            """, (trainer_id,))
        bookings = cur.fetchall()
        if bookings:
            print("Your Booked Rooms:")
            for booking in bookings:
                print(f"BookingID: {booking[0]}, RoomID: {booking[1]}, Start: {booking[2]}, End: {booking[3]}, Class Type: {booking[4]}")
        else:
            print("No rooms currently booked.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()



def view_available_rooms(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT RoomID, RoomName, Capacity, Type, Status
            FROM Room
            WHERE Status = 'Available';
            """)
        rooms = cur.fetchall()
        if rooms:
            print("Available Rooms:")
            for room in rooms:
                print(f"RoomID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}, Type: {room[3]}, Status: {room[4]}")
        else:
            print("No available rooms currently.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()

def view_member_profile_by_trainer(conn, member_id):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT Name, Email, JoinDate, Gender
            FROM Members
            WHERE MemberID = %s;
            """, (member_id,))
        member_info = cur.fetchone()
        if member_info:
            print(f"Member Profile - Name: {member_info[0]}, Email: {member_info[1]}, Join Date: {member_info[2]}, Gender: {member_info[3]}")
        else:
            print("No member found with the provided ID.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()

def is_room_available(conn, room_id, start_time, end_time):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 1 FROM Schedule WHERE RoomID = %s AND NOT (
                %s >= EndTime OR %s <= StartTime)
            """, (room_id, end_time, start_time))
        return not cur.fetchone()
    except DatabaseError as e:
        print(f"An error occurred checking room availability: {e}")
        return False
    finally:
        if cur:
            cur.close()

