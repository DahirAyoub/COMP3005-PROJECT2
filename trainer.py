from psycopg2 import DatabaseError

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

def create_room_booking(conn, room_id, staff_id, start_time, end_time, class_type):
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
            """, (room_id, staff_id, start_time, end_time, class_type))
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


def trainer_operations(conn, trainer_id, choice):
    if choice == '1':
        member_id = int(input("Enter the member ID to view profile: "))
        view_member_profile_by_trainer(conn, member_id)
    elif choice == '2':
        new_email = input("Enter your new email: ")
        update_trainer_email(conn, trainer_id, new_email)
    elif choice == '3':
        create_room_booking(conn, trainer_id)
    elif choice == '4':
        view_my_booked_rooms(conn, trainer_id)
    elif choice == '5':
        view_available_rooms(conn)
    else:
        print("Invalid choice. Please enter a number from 1 to 7.")


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

        