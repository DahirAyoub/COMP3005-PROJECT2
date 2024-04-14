from psycopg2 import DatabaseError, connect
from admin import *
from member import *
from trainer import *

# Function to retrieve database connection credentials
def get_db_credentials():
    dbname = input("Enter database name (default 'FinalProject'): ") or 'FinalProject'
    user = input("Enter username (default 'postgres'): ") or 'postgres'
    password = input("Enter password (default 'postgres'): ") or 'postgres'
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


def member_choices(conn, member_id):
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
        print("12: View Your Sessions")
        print("13: Reschedule a Session")
        print("14: Cancel a Session")
        print("0: Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_profile(conn, member_id)
        elif choice == '2':
            new_email = input("Enter new email: ")
            update_user_profile(conn, member_id, new_email)
        elif choice == '3':
            add_health_metric(conn, member_id)
        elif choice == '4':
            view_health_metrics(conn, member_id)
        elif choice == '5':
            metric_id = int(input("Enter the health metric ID to update: "))
            update_health_metric(conn, member_id, metric_id)
        elif choice == '6':
            metric_id = int(input("Enter the health metric ID to delete: "))
            delete_health_metric(conn, member_id, metric_id)
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
            book_session(conn, member_id)
        elif choice == '12':
            view_member_sessions(conn, member_id)
        elif choice == '13':
            session_id = int(input("Enter session ID to reschedule: "))
            reschedule_session(conn, session_id)
        elif choice == '14':
            session_id = int(input("Enter session ID to cancel: "))
            cancel_session(conn, session_id)
        elif choice == '0':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 14.")


def trainer_operations(conn, trainer_id):
    while True:
        print("\nSelect an operation:")
        print("1 - View Member Profile")
        print("2 - Update Your Email")
        print("3 - Book a Room")
        print("4 - View Your Booked Rooms")
        print("5 - View Available Rooms")
        print("6 - View Your Profile")
        print("7 - Update Your Profile")
        print("8 - Reschedule a Session")
        print("9 - Cancel a Session")
        print("0 - Logout")

        choice = input("Enter your choice (0-9): ")

        if choice == '1':
            member_id = int(input("Enter the member ID to view profile: "))
            view_member_profile_by_trainer(conn, member_id)
        elif choice == '2':
            new_email = input("Enter your new email: ")
            update_trainer_email(conn, trainer_id, new_email)
        elif choice == '3':
            room_id = int(input("Enter room ID: "))
            start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
            end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
            class_type = input("Enter class type: ")
            create_room_booking(conn, trainer_id, room_id, start_time, end_time, class_type)
        elif choice == '4':
            view_my_booked_rooms(conn, trainer_id)
        elif choice == '5':
            view_available_rooms(conn)
        elif choice == '6':
            view_trainer_profile(conn, trainer_id)
        elif choice == '7':
            update_trainer_profile(conn, trainer_id)
        elif choice == '8':
            session_id = int(input("Enter session ID to reschedule: "))
            new_start_time = input("Enter new start time (YYYY-MM-DD HH:MM): ")
            new_end_time = input("Enter new end time (YYYY-MM-DD HH:MM): ")
            rescheduleSession(conn, trainer_id, session_id, new_start_time, new_end_time)
        elif choice == '9':
            session_id = int(input("Enter session ID to cancel: "))
            cancelSession(conn, session_id)
        elif choice == '0':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 9.")
def admin_choices(conn, admin_id):
    is_owner = check_if_owner(conn, admin_id)
    
    while True:
        print("\nChoose operation:")
        print("1: View All Booked Rooms")
        print("2: Delete Booked Room")
        print("3: Add Fitness Equipment")
        print("4: Delete Fitness Equipment")
        print("5: Update Fitness Equipment Status")
        print("6: Update Equipment Maintenance Date")
        print("7: Monitor Fitness Equipment Maintenance")
        print("8: View All Fitness Equipment")

        if is_owner:
            print("9: Register New Admin Staff")
            print("10: Delete Admin Staff")
            print("11: Update Admin Staff Details")
            print("12: View Admin Staff Details")
            print("13: View All Admin Staff")
        
        print("0: Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_all_booked_rooms(conn)
        elif choice == '2':
            booking_id = int(input("Enter Booking ID to delete: "))
            delete_booked_room(conn, booking_id)
        elif choice == '3':
            equipment_name = input("Enter equipment name: ")
            status = input("Enter status: ")
            last_maintenance_date = input("Enter last maintenance date (YYYY-MM-DD): ")
            warranty_date = input("Enter warranty date (YYYY-MM-DD): ")
            add_fitness_equipment(conn, equipment_name, status, last_maintenance_date, warranty_date)
        elif choice == '4':
            equipment_id = int(input("Enter Equipment ID to delete: "))
            delete_fitness_equipment(conn, equipment_id)
        elif choice == '5':
            equipment_id = int(input("Enter Equipment ID to update status: "))
            new_status = input("Enter new status: ")
            update_fitness_equipment_status(conn, equipment_id, new_status)
        elif choice == '6':
            equipment_id = int(input("Enter Equipment ID to update maintenance date: "))
            new_maintenance_date = input("Enter new maintenance date (YYYY-MM-DD): ")
            update_equipment_maintenance_date(conn, equipment_id, new_maintenance_date)
        elif choice == '7':
            monitor_fitness_equipment_maintenance(conn)
        elif choice == '8':
            view_all_fitness_equipment(conn)
        elif is_owner and choice == '9':
            admin_registration(conn)
        elif is_owner and choice == '10':
            staff_id = int(input("Enter Staff ID to delete: "))
            delete_admin_staff(conn, staff_id)
        elif is_owner and choice == '11':
            staff_id = int(input("Enter Staff ID to update: "))
            update_admin_staff_details(conn, staff_id)
        elif is_owner and choice == '12':
            view_admin_staff_details(conn, admin_id)
        elif is_owner and choice == '13':
            view_all_staff(conn)
        elif choice == '0':
            print("Logging out...")
            return
        else:
            print("Invalid choice. Please enter a number from 0 to 12 or 0 to 8 if not owner.")


if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        while True:
            print("\nWelcome to the Health and Fitness Club Management System")
            print("1: Register as a new Member")
            print("2: Register as a new Trainer")
            print("3: Login as a Member")
            print("4: Login as a Trainer")
            print("5: Login as an Admin")
            print("0: Exit")
            user_choice = input("Choose an option to proceed: ")

            if user_choice == '1':
                register_user(conn)
            
            elif user_choice == '2':
                register_trainer(conn)  # Ensure you have a function for trainer registration
            
            elif user_choice == '3':
                member_id = authenticate_user(conn)
                if member_id:
                    print(f"Login successful! Welcome, Member ID: {member_id}")
                    member_choices(conn, member_id)  # Calls member choices if login is successful
                else:
                    print("Login failed. Invalid email or password. Please try again.")

            elif user_choice == '4':
                trainer_id = authenticate_trainer(conn)  # Assuming there's a function to authenticate trainers
                if trainer_id:
                    print(f"Login successful! Welcome, Trainer ID: {trainer_id}")
                    trainer_operations(conn, trainer_id)  # Calls trainer operations if login is successful
                else:
                    print("Login failed. Invalid email or password. Please try again.")
            
            elif user_choice == '5':
                admin_id = authenticate_admin(conn)
                if admin_id:
                    print(f"Login successful! Welcome, Admin ID: {admin_id}")
                    admin_choices(conn, admin_id)  # Admin choices to manage higher-level operations
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
