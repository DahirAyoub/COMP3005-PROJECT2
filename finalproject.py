import psycopg2
from psycopg2 import DatabaseError, connect
from werkzeug.security import generate_password_hash, check_password_hash

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
    
def authenticate_user(conn):
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    try:
        cur = conn.cursor()
        cur.execute("SELECT memberid, password FROM Members WHERE email = %s;", (email,))
        user = cur.fetchone()
        if user:
            stored_password = user[1]
            # Check if the stored password is hashed (by checking if it follows a typical hash pattern)
            if stored_password.startswith('pbkdf2:sha256:') or stored_password.startswith('$2b$'):
                if check_password_hash(stored_password, password):
                    return user[0]  # Password match for hashed password
            else:
                # Assume plaintext comparison
                if stored_password == password:
                    return user[0]  # Password match for plaintext password
        print("Invalid email or password. Please try again.")
        return None
    except DatabaseError as e:
        print(f"An error occurred during login: {e}")
        return None
    finally:
        if cur:
            cur.close()

def view_profile(conn, member_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Members WHERE memberid = %s;", (member_id,))
        profile = cur.fetchone()
        print("Profile Information:")
        print(profile)
        
        cur.execute("SELECT * FROM HealthMetrics WHERE memberid = %s;", (member_id,))
        metrics = cur.fetchall()
        print("Health Metrics:")
        for metric in metrics:
            print(metric)
        
        cur.execute("SELECT * FROM FitnessGoals WHERE memberid = %s;", (member_id,))
        goals = cur.fetchall()
        print("Fitness Goals:")
        for goal in goals:
            print(goal)
        
    except DatabaseError as e:
        print(f"An error occurred: {e}")
    finally:
        if cur:
            cur.close()

# Function to register a new user in the system
def register_user(conn):
    print("Register New User")
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    gender = input("Gender: ")
    hashed_password = generate_password_hash(password)  # Hashing the password for security
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Members (name, email, joindate, gender, password)
            VALUES (%s, %s, CURRENT_DATE, %s, %s);
            """, (name, email, gender, hashed_password))
        conn.commit()
        print("User registered successfully.")
    except psycopg2.IntegrityError:
        print("This email is already registered.")
        conn.rollback()
    except DatabaseError as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()

# Function to view the profile of a specific user
def view_user_profile(conn, member_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT memberid, name, email, joindate, gender, password FROM Members WHERE memberid = %s;", (member_id,))
        user = cur.fetchone()
        if user:
            print(f"User Profile:\nID: {user[0]}\nName: {user[1]}\nEmail: {user[2]}\nJoin Date: {user[3]}\nGender: {user[4]}\nPassword: {user[5]}")
        else:
            print("No user found with that ID.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()

# Function to update the email of a specific user
def update_user_profile(conn, member_id, new_email):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE Members SET Email = %s WHERE MemberID = %s;", (new_email, member_id))
        conn.commit()
        if cur.rowcount:
            print("User email updated successfully.")
        else:
            print("No user found with that ID.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()

# Function to add a health metric for a specific user
def add_health_metric(conn, member_id):
    print("Adding mandatory health metrics: Height and Weight.")

    # Function to insert a metric into the database
    def insert_metric(metric_type, metric_value):
        # Define the units for each metric type
        units = {'Height': 'cm', 'Weight': 'kg'}

        # Append the unit if not provided by the user
        if not metric_value.strip().endswith(units[metric_type]):
            metric_value += f" {units[metric_type]}"

        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO HealthMetrics (MemberID, MetricType, MetricValue, DateRecorded)
                VALUES (%s, %s, %s, CURRENT_DATE);
            """, (member_id, metric_type, metric_value))
            conn.commit()
            print(f"{metric_type} metric added successfully.")
        except psycopg2.DatabaseError as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            if cur:
                cur.close()

    # Collect mandatory metrics
    height = input("Enter height (e.g., 175): ")  # Prompt without units
    weight = input("Enter weight (e.g., 80): ")   # Prompt without units

    # Insert mandatory metrics: Height and Weight
    insert_metric('Height', height)
    insert_metric('Weight', weight)

    # Ask if the user wants to add more metrics
    more_metrics = input("Do you want to add more health metrics? (yes/no): ")
    if more_metrics.lower() == 'yes':
        while True:
            metric_type = input("Enter the type of additional metric (or type 'exit' to finish): ")
            if metric_type.lower() == 'exit':
                break
            metric_value = input(f"Enter the value for {metric_type}: ")
            insert_metric(metric_type, metric_value)
            print(f"Added {metric_type} metric successfully.")

# Function to prompt the user to select a health metric type from available options
def choose_metric_type():
    metrics = {
        '1': 'Height (cm)',
        '2': 'Weight (kg)'
    }
    print("Available metrics to add:")
    for key, metric in metrics.items():
        print(f"{key}: {metric}")
    choice = input("Select a metric type to add (by number): ")
    metric_type = metrics.get(choice, None)
    if not metric_type:
        print("Invalid choice, please select a valid option.")
        return None
    return metric_type.split(' ')[0]

# Function to display all health metrics recorded for a specific user
def view_health_metrics(conn, member_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT MetricType, MetricValue, DateRecorded FROM HealthMetrics WHERE MemberID = %s;", (member_id,))
        metrics = cur.fetchall()
        if metrics:
            print("Health Metrics:")
            for metric in metrics:
                print(f"Type: {metric[0]}, Value: {metric[1]}, Recorded On: {metric[2]}")
        else:
            print("No health metrics found for this user.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()

# Function to update a specific health metric for a user
def update_health_metric(conn, member_id):
    try:
        cur = conn.cursor()
        # Define the units for each metric type
        units = {'Height': 'cm', 'Weight': 'kg'}

        # Display available metrics for the member
        cur.execute("SELECT MetricID, MetricType, MetricValue FROM HealthMetrics WHERE MemberID = %s;", (member_id,))
        metrics = cur.fetchall()
        if not metrics:
            print("No metrics found for this member.")
            return
        
        print("Available Metrics:")
        for metric in metrics:
            print(f"ID: {metric[0]}, Type: {metric[1]}, Value: {metric[2]}")

        # Prompting for the Metric ID to update
        metric_id = input("Enter the ID of the metric to update: ")
        selected_metric = next((m for m in metrics if m[0] == int(metric_id)), None)
        if not selected_metric:
            print("Invalid Metric ID entered.")
            return

        # Get new value and append the unit if necessary
        new_value = input(f"Enter the new value for {selected_metric[1]} (just the number): ")
        if not new_value.strip().endswith(units[selected_metric[1]]):
            new_value += f" {units[selected_metric[1]]}"

        # Execute the update statement
        cur.execute("""
            UPDATE HealthMetrics 
            SET MetricValue = %s 
            WHERE MetricID = %s AND MemberID = %s;
            """, (new_value, metric_id, member_id))
        conn.commit()

        # Check if the update was successful
        if cur.rowcount:
            print(f"{selected_metric[1]} metric updated successfully.")
        else:
            print("No changes were made.")
    except ValueError:
        print("Please enter valid numbers for Metric ID and values.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

# Function to delete a health metric for a specific user
def delete_health_metric(conn, member_id):
    try:
        cur = conn.cursor()
        # Show existing metrics
        cur.execute("SELECT MetricID, MetricType, MetricValue FROM HealthMetrics WHERE MemberID = %s;", (member_id,))
        metrics = cur.fetchall()
        print("Available Metrics:")
        for metric in metrics:
            print(f"ID: {metric[0]}, Type: {metric[1]}, Value: {metric[2]}")

        metric_id = input("Enter the ID of the metric to delete: ")
        cur.execute("DELETE FROM HealthMetrics WHERE MetricID = %s AND MemberID = %s;", (metric_id, member_id))
        conn.commit()
        if cur.rowcount:
            print("Health metric deleted successfully.")
        else:
            print("No health metric found with that ID.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        
def add_fitness_goal(conn, member_id):
    print("Add a New Fitness Goal")
    goal_type = input("Enter the goal type (e.g., 'Lose Weight', 'Gain Muscle'): ")
    goal_value = input("Enter the goal value (e.g., '5kg', '10kg'): ")
    status = input("Enter the initial status (e.g., 'Not Started', 'In Progress'): ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO FitnessGoals (MemberID, GoalType, GoalValue, StartDate, Status)
            VALUES (%s, %s, %s, %s, %s);
            """, (member_id, goal_type, goal_value, start_date, status))
        conn.commit()
        print("Fitness goal added successfully.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()

def view_fitness_goals(conn, member_id):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT GoalID, GoalType, GoalValue, StartDate, Status
            FROM FitnessGoals
            WHERE MemberID = %s;
            """, (member_id,))
        goals = cur.fetchall()
        if goals:
            print("Fitness Goals:")
            for goal in goals:
                print(f"ID: {goal[0]}, Type: {goal[1]}, Value: {goal[2]}, Start Date: {goal[3]}, Status: {goal[4]}")
        else:
            print("No fitness goals found for this member.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()

def update_fitness_goal(conn, goal_id):
    new_value = input("Enter the new goal value: ")
    new_status = input("Enter the new status: ")
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE FitnessGoals
            SET GoalValue = %s, Status = %s
            WHERE GoalID = %s;
            """, (new_value, new_status, goal_id))
        conn.commit()
        if cur.rowcount:
            print("Fitness goal updated successfully.")
        else:
            print("No changes were made.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()

def delete_fitness_goal(conn, goal_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM FitnessGoals WHERE GoalID = %s;", (goal_id,))
        conn.commit()
        if cur.rowcount:
            print("Fitness goal deleted successfully.")
        else:
            print("No fitness goal found with that ID.")
    except DatabaseError as e:
        print(f"An error occurred: {e}")
        conn.rollback()
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
        conn.rollback()
    finally:
        cur.close()
        

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