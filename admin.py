import psycopg2
from psycopg2 import DatabaseError, connect
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


#Room booking management such view and delete

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