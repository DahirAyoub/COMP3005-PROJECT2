import psycopg2
from psycopg2 import DatabaseError
from werkzeug.security import generate_password_hash, check_password_hash



def admin_registration(conn):
    print("Register New Staff")
    name = input("Name: ")
    phone_number = input("Phone Number: ")
    email = input("Email: ")
    password = input("Password:")
    hashed_password = generate_password_hash(password)
    try:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO Staff (Name, PhoneNumber, Email, Password, JoinDate)
        VALUES (%s, %s, %s, %s, CURRENT_DATE);
        """, (name, phone_number, email, hashed_password))

        conn.commit()
        print("Staff registered successfully.")
    except psycopg2.IntegrityError:
        print("This email is already registered.")
        conn.rollback()
    except DatabaseError as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        
def authenticate_admin (conn):
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    try:
        cur = conn.cursor()
        cur.execute("SELECT StaffID, Password FROM Staff WHERE Email = %s;", (email,))

        user = cur.fetchone()
        if user:
            stored_password = user[1]
            # Check if the stored password is hashed (by checking if it follows a typical hash pattern)
            if check_password_hash(stored_password, password):
                return user[0]
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




def add_fitness_equipment(conn, equipment_name, status, last_maintenance_date, warranty_date):
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Equipment (EquipmentName, Status, LastMaintenanceDate, WarrantyDate)
            VALUES (%s, %s, %s, %s);
            """, (equipment_name, status, last_maintenance_date, warranty_date))
        conn.commit()
        print("Equipment added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()


def delete_fitness_equipment(conn, equipment_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Equipment WHERE EquipmentID = %s;", (equipment_id,))
        conn.commit()
        if cur.rowcount:
            print("Equipment deleted successfully.")
        else:
            print("No equipment found with that ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()


def update_fitness_equipment_status(conn, equipment_id, new_status):
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Equipment
            SET Status = %s
            WHERE EquipmentID = %s;
            """, (new_status, equipment_id))
        conn.commit()
        if cur.rowcount:
            print("Equipment status updated successfully.")
        else:
            print("No equipment found with that ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()


def update_equipment_maintenance_date(conn, equipment_id, new_maintenance_date):
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Equipment
            SET LastMaintenanceDate = %s
            WHERE EquipmentID = %s;
            """, (new_maintenance_date, equipment_id))
        conn.commit()
        if cur.rowcount:
            print("Maintenance date updated successfully.")
        else:
            print("No equipment found with that ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()

def monitor_fitness_equipment_maintenance(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT EquipmentID, EquipmentName, LastMaintenanceDate, WarrantyDate, Status
            FROM Equipment
            WHERE Status = 'Needs Maintenance' OR LastMaintenanceDate <= CURRENT_DATE - INTERVAL '6 months';
            """)
        results = cur.fetchall()
        if results:
            print("Equipment needing maintenance:")
            for item in results:
                print(f"ID: {item[0]}, Name: {item[1]}, Last Maintained: {item[2].strftime('%Y-%m-%d')}, Status: {item[4]}")
        else:
            print("No equipment requires maintenance at the moment.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()


def view_all_fitness_equipment(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT EquipmentID, EquipmentName, Status, LastMaintenanceDate, WarrantyDate FROM Equipment;")
        equipments = cur.fetchall()
        if equipments:
            print("\nList of All Fitness Equipment:")
            for eq in equipments:
                print(f"EquipmentID: {eq[0]}, Name: {eq[1]}, Status: {eq[2]}, Last Maintenance: {eq[3]}, Warranty Until: {eq[4]}")
        else:
            print("No fitness equipment found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()


def check_if_owner(conn, staff_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT IsOwner FROM Staff WHERE StaffID = %s;", (staff_id,))
        result = cur.fetchone()
        if result:
            return result[0]  # Returns True if IsOwner is True, otherwise False
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        cur.close()

def delete_admin_staff(conn, staff_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Staff WHERE StaffID = %s;", (staff_id,))
        conn.commit()
        if cur.rowcount:
            print("Admin staff deleted successfully.")
        else:
            print("No admin staff found with that ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()

def update_admin_staff_details(conn, staff_id):
    new_name = input("Enter new name: ")
    new_phone_number = input("Enter new phone number: ")
    new_email = input("Enter new email: ")
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Staff
            SET Name = %s, PhoneNumber = %s, Email = %s
            WHERE StaffID = %s;
            """, (new_name, new_phone_number, new_email, staff_id))
        conn.commit()
        if cur.rowcount:
            print("Admin staff details updated successfully.")
        else:
            print("No admin staff found with that ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()

def view_admin_staff_details(conn, staff_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT StaffID, Name, PhoneNumber, Email FROM Staff WHERE StaffID = %s;", (staff_id,))
        staff_details = cur.fetchone()
        if staff_details:
            print(f"Staff ID: {staff_details[0]}, Name: {staff_details[1]}, Phone Number: {staff_details[2]}, Email: {staff_details[3]}")
        else:
            print("No admin staff found with that ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()

def view_all_staff(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT StaffID, Name, PhoneNumber, Email FROM Staff ORDER BY StaffID;")
        staff_list = cur.fetchall()
        if staff_list:
            print("\nList of All Admin Staff:")
            for staff in staff_list:
                print(f"Staff ID: {staff[0]}, Name: {staff[1]}, Phone Number: {staff[2]}, Email: {staff[3]}")
        else:
            print("No admin staff found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()


def view_all_rooms(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT RoomID, RoomName, Capacity, Type, Status FROM Room ORDER BY RoomID;")
        rooms_list = cur.fetchall()
        if rooms_list:
            print("\nList of All Rooms:")
            for room in rooms_list:
                print(f"Room ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}, Type: {room[3]}, Status: {room[4]}")
        else:
            print("No rooms found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()


def add_room(conn):
    room_name = input("Enter the room name: ")
    capacity = input("Enter the room capacity: ")
    room_type = input("Enter the room type: ")
    status = input("Enter the room status: ")
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Room (RoomName, Capacity, Type, Status) VALUES (%s, %s, %s, %s);",
                    (room_name, capacity, room_type, status))
        conn.commit()
        print("Room added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()


def delete_room(conn):
    room_id = input("Enter the room ID to delete: ")
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Room WHERE RoomID = %s;", (room_id,))
        conn.commit()
        if cur.rowcount:
            print("Room deleted successfully.")
        else:
            print("No room found with that ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()

def edit_room_status(conn):
    room_id = input("Enter the room ID to update the status: ")
    new_status = input("Enter the new status for the room: ")
    try:
        cur = conn.cursor()
        cur.execute("UPDATE Room SET Status = %s WHERE RoomID = %s;", (new_status, room_id))
        conn.commit()
        if cur.rowcount:
            print("Room status updated successfully.")
        else:
            print("No room found with that ID or no changes made.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
