from flask import Flask, request, jsonify, render_template
import pyodbc

app = Flask(__name__, template_folder='templates', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')


def create_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=USHYDPNETHRAVA1;'  # Replace with your server name
            'DATABASE=EmployeeDB;'
            'Trusted_Connection=yes;'
        )
        print("Database connection established")
        return conn
    except pyodbc.Error as e:
        print("Error: ", e)
        return None


@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.json
    print("Received data for adding employee:", data)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Employees (FirstName, LastName, Email, Position, Salary)
                VALUES (?, ?, ?, ?, ?)
            """, (data['firstName'], data['lastName'], data['email'], data['position'], data['salary']))
            conn.commit()
            print("Employee added successfully")
            return jsonify(success=True)
        except pyodbc.Error as e:
            print("Error executing SQL query:", e)
            return jsonify(success=False, error=str(e))
        finally:
            conn.close()
    return jsonify(success=False, error="Database connection failed")

@app.route('/update_employee', methods=['PUT'])
def update_employee():
    data = request.json
    print("Received data for updating employee:", data)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Employees
                SET FirstName = ?, LastName = ?, Email = ?, Position = ?, Salary = ?
                WHERE EmployeeID = ?
            """, (data['firstName'], data['lastName'], data['email'], data['position'], data['salary'], data['id']))
            conn.commit()
            print("Employee updated successfully")
            return jsonify(success=True)
        except pyodbc.Error as e:
            print("Error executing SQL query:", e)
            return jsonify(success=False, error=str(e))
        finally:
            conn.close()
    return jsonify(success=False, error="Database connection failed")

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee():
    data = request.json
    print("Received data for deleting employee:", data)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Employees WHERE EmployeeID = ?", (data['id'],))
            conn.commit()
            print("Employee deleted successfully")
            return jsonify(success=True)
        except pyodbc.Error as e:
            print("Error executing SQL query:", e)
            return jsonify(success=False, error=str(e))
        finally:
            conn.close()
    return jsonify(success=False, error="Database connection failed")

@app.route('/view_employees', methods=['GET'])
def view_employees():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Employees")
            rows = cursor.fetchall()
            employees = [
                {
                    'id': row.EmployeeID,
                    'firstName': row.FirstName,
                    'lastName': row.LastName,
                    'email': row.Email,
                    'position': row.Position,
                    'salary': row.Salary
                }
                for row in rows
            ]
            return jsonify(employees=employees)
        except pyodbc.Error as e:
            print("Error executing SQL query:", e)
            return jsonify(success=False, error=str(e))
        finally:
            conn.close()
    return jsonify(success=False, error="Database connection failed")

@app.route('/search_employee', methods=['GET'])
def search_employee():
    name = request.args.get('name', '').lower()
    position = request.args.get('position', '').lower()
    print("Searching for employees with name:", name, "and position:", position)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM Employees
                WHERE (LOWER(FirstName) LIKE ? OR LOWER(LastName) LIKE ?) AND LOWER(Position) LIKE ?
            """, ('%' + name + '%', '%' + name + '%', '%' + position + '%'))
            rows = cursor.fetchall()
            employees = [
                {
                    'id': row.EmployeeID,
                    'firstName': row.FirstName,
                    'lastName': row.LastName,
                    'email': row.Email,
                    'position': row.Position,
                    'salary': row.Salary
                }
                for row in rows
            ]
            return jsonify(employees=employees)
        except pyodbc.Error as e:
            print("Error executing SQL query:", e)
            return jsonify(success=False, error=str(e))
        finally:
            conn.close()
    return jsonify(success=False, error="Database connection failed")

if __name__ == '__main__':
    app.run(debug=True)
