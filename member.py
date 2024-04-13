import psycopg2
from psycopg2 import DatabaseError
from werkzeug.security import generate_password_hash, check_password_hash

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

        # Execute the statement
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