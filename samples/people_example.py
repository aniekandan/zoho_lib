# people_example.py
# This script demonstrates how to work with Zoho People APIs
# (attendance bulk import, form updates, holiday lookup, biometric ID resolution)
# using the zoho_lib library.

import sys
import os

# Add the parent directory of this script to the Python system path.
# This ensures that zoho_lib can be imported cleanly, regardless of whether 
# you run this script from the project root or from inside the samples/ directory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from zoho_lib import conn_mgr, ZPeople

# Initialize the People service adapter using the connection named 'my_people_conn'
# (or 'people_conn') from your external connections.json configuration file.
people_service = ZPeople(conn_mgr, "my_people_conn")


def bulk_import_attendance_demo():
    print("--- Bulk Importing Attendance Entries ---")

    attendance_data = [
        {
            "empId": "1001",
            "checkIn": "2024-11-07 09:01:00",
            "checkOut": "2024-11-07 17:30:00"
        },
        {
            "empId": "1002",
            "checkIn": "2024-11-07 08:55:00",
            "checkOut": "2024-11-07 17:15:00"
        }
    ]

    response = people_service.bulk_import_attendance(
        data=attendance_data,
        date_format="yyyy-MM-dd HH:mm:ss"
    )

    print("Response from Zoho People:")
    print(response)


def get_holidays_demo():
    print("\n--- Fetching Holidays ---")

    from_date = "2024-01-01"
    to_date = "2024-12-31"

    holidays = people_service.get_holidays(from_date=from_date, to_date=to_date)

    print(f"Holidays between {from_date} and {to_date}:")
    print(holidays)


def update_form_record_demo():
    print("\n--- Updating a Form Record ---")

    form_link_name = "P_Employee"
    record_id = "1234567890"
    input_data = {
        "Department": "Engineering",
        "Mobile": "1234567890"
    }

    response = people_service.update_form_record(
        form_link_name=form_link_name,
        record_id=record_id,
        input_data=input_data
    )

    print("Response from Zoho People:")
    print(response)


def biometric_lookup_demo():
    print("\n--- Employee Lookup by Biometric ID ---")

    biometric_id = "BIO_9901"
    emp_id = people_service.get_employee_by_biometric_id(biometric_id)

    if emp_id:
        print(f"Found Zoho Employee ID: {emp_id} for Biometric ID: {biometric_id}")
    else:
        print(f"No employee found with Biometric ID: {biometric_id}")


if __name__ == "__main__":
    # 1. Bulk import attendance
    # bulk_import_attendance_demo()

    # 2. Get holidays range
    get_holidays_demo()

    # 3. Update form record (uncomment to test with valid record ID)
    # update_form_record_demo()

    # 4. Lookup employee by Biometric ID
    # biometric_lookup_demo()
