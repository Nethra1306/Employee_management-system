document.addEventListener('DOMContentLoaded', (event) => {
    let selectedRow = null;

    function add_employee() {
        // Get form data
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const email = document.getElementById('email').value;
        const position = document.getElementById('position').value;
        const salary = document.getElementById('salary').value;

        // Log the employee data to the console
        console.log('Employee Data:', {
            firstName: firstName,
            lastName: lastName,
            email: email,
            position: position,
            salary: salary
        });

        // Send data to the server
        fetch('/add_employee', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                firstName: firstName,
                lastName: lastName,
                email: email,
                position: position,
                salary: salary
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Employee added successfully');
                load_employees();
            } else {
                console.error('Error adding employee:', data.error);
            }
        });

        // Clear form fields
        document.getElementById('employeeForm').reset();
    }

    function update_employee() {
        if (selectedRow) {
            const id = selectedRow.cells[0].innerText;
            const firstName = document.getElementById('firstName').value;
            const lastName = document.getElementById('lastName').value;
            const email = document.getElementById('email').value;
            const position = document.getElementById('position').value;
            const salary = document.getElementById('salary').value;

            fetch('/update_employee', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: id,
                    firstName: firstName,
                    lastName: lastName,
                    email: email,
                    position: position,
                    salary: salary
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Employee updated successfully');
                    load_employees();
                } else {
                    console.error('Error updating employee:', data.error);
                }
            });

            // Clear form fields
            document.getElementById('employeeForm').reset();
            selectedRow = null;
        } else {
            alert("Please select a row to update.");
        }
    }

    function delete_employee() {
        if (selectedRow) {
            const id = selectedRow.cells[0].innerText;

            fetch('/delete_employee', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: id })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Employee deleted successfully');
                    load_employees();
                } else {
                    console.error('Error deleting employee:', data.error);
                }
            });

            // Clear form fields
            document.getElementById('employeeForm').reset();
            selectedRow = null;
        } else {
            alert("Please select a row to delete.");
        }
    }

    function search_employee() {
        const searchName = document.getElementById('searchName').value.toLowerCase();
        const searchPosition = document.getElementById('searchPosition').value.toLowerCase();

        fetch(`/search_employee?name=${searchName}&position=${searchPosition}`)
        .then(response => response.json())
        .then(data => {
            if (data.success !== false) {
                display_employees(data.employees);
            } else {
                console.error('Error searching employees:', data.error);
            }
        });
    }

    function load_employees() {
        fetch('/view_employees')
        .then(response => response.json())
        .then(data => {
            if (data.success !== false) {
                display_employees(data.employees);
            } else {
                console.error('Error loading employees:', data.error);
            }
        });
    }

    function display_employees(employees) {
        const table = document.getElementById('employeeTable').getElementsByTagName('tbody')[0];
        table.innerHTML = '';

        employees.forEach(employee => {
            const newRow = table.insertRow();
            newRow.insertCell(0).innerText = employee.id;
            newRow.insertCell(1).innerText = employee.firstName;
            newRow.insertCell(2).innerText = employee.lastName;
            newRow.insertCell(3).innerText = employee.email;
            newRow.insertCell(4).innerText = employee.position;
            newRow.insertCell(5).innerText = employee.salary;

            newRow.addEventListener('click', () => {
                selectedRow = newRow;
                document.getElementById('firstName').value = newRow.cells[1].innerText;
                document.getElementById('lastName').value = newRow.cells[2].innerText;
                document.getElementById('email').value = newRow.cells[3].innerText;
                document.getElementById('position').value = newRow.cells[4].innerText;
                document.getElementById('salary').value = newRow.cells[5].innerText;
            });
        });
    }

    load_employees();

    // Attach functions to global scope
    window.add_employee = add_employee;
    window.update_employee = update_employee;
    window.delete_employee = delete_employee;
    window.search_employee = search_employee;
});
