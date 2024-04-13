from psycopg2 import DatabaseError, connect
from admin import *
from member import *
from trainer import *

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