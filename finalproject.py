import psycopg2
from psycopg2 import DatabaseError, connect
from werkzeug.security import generate_password_hash, check_password_hash
from admin import *
from member import *

# Function to retrieve database connection credentials
def get_db_credentials():
    dbname = input("Enter database name (default 'default_db_name'): ") or 'default_db_name'
    user = input("Enter username (default 'default_user'): ") or 'default_user'
    password = input("Enter password: ")
    host = input("Enter host (default 'localhost'): ") or 'localhost'
    port = input("Enter port (default '5432'): ") or '5432'
    return {
        'dbname': dbname,  # Database name
        'user': user,  # Username for database login
        'password': password,  # Password for database login
        'host': host,  # Database host address
        'port': port  # Database port
    }

# Function to establish a database connection using credentials provided by the user
def get_db_connection():
    credentials = get_db_credentials()
    try:
        conn = connect(
            dbname=credentials['dbname'],
            user=credentials['user'],
            password=credentials['password'],
            host=credentials['host'],
            port=credentials['port']
        )
        return conn
    except DatabaseError as e:
        print(f"Database connection failed: {e}")
        return None

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



if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        while True:
            print("\nWelcome to the Health and Fitness Club Management System")
            print("1: Register as a new user")
            print("2: Login")
            print("0: Exit")
            user_choice = input("Choose an option to proceed: ")

            if user_choice == '1':
                register_user(conn)
            elif user_choice == '2':
                member_id = authenticate_user(conn)
                if member_id:
                    print(f"Login successful! Welcome, Member ID: {member_id}")
                    while True:
                        print("\nChoose operation:")
                        print("1: View Your Profile")
                        print("2: Update Your Email")
                        print("3: Add Health Metric")
                        print("4: View Your Health Metrics")
                        print("5: Update Health Metric")
                        print("6: Delete Health Metric")
                        print("7: Add Fitness Goal")
                        print("8: View Your Fitness Goals")
                        print("9: Update Fitness Goal")
                        print("10: Delete Fitness Goal")
                        print("11: Book a Session")
                        print("12: Reschedule a Session")
                        print("13: Cancel a Session")
                        print("14: Set Trainer Availability")
                        print("0: Logout")
                        choice = input("Enter your choice: ")

                        if choice == '1':
                            view_user_profile(conn, member_id)
                        elif choice == '2':
                            new_email = input("Enter new email: ")
                            update_user_profile(conn, member_id, new_email)
                        elif choice == '3':
                            add_health_metric(conn, member_id)
                        elif choice == '4':
                            view_health_metrics(conn, member_id)
                        elif choice == '5':
                            update_health_metric(conn, member_id)
                        elif choice == '6':
                            delete_health_metric(conn, member_id)
                        elif choice == '7':
                            add_fitness_goal(conn, member_id)
                        elif choice == '8':
                            view_fitness_goals(conn, member_id)
                        elif choice == '9':
                            goal_id = int(input("Enter Fitness Goal ID to update: "))
                            update_fitness_goal(conn, goal_id)
                        elif choice == '10':
                            goal_id = int(input("Enter Fitness Goal ID to delete: "))
                            delete_fitness_goal(conn, goal_id)
                        elif choice == '11':
                            bookSession(conn)
                        elif choice == '12':
                            rescheduleSession(conn)
                        elif choice == '13':
                            cancelSession(conn)
                        elif choice == '14':
                            setTrainerAvailability(conn)
                        elif choice == '0':
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice. Please enter a number from 0 to 14.")
                else:
                    print("Login failed. Invalid email or password. Please try again.")
            elif user_choice == '0':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")
        conn.close()
    else:
        print("Failed to connect to the database.")