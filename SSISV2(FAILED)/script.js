const studentFunctions = {
    editStudent: function(id, firstName, lastName, gender, year, course) {
        // Populate modal fields with current data
        document.getElementById('editStudentID').value = id;
        document.getElementById('editFirstName').value = firstName;
        document.getElementById('editLastName').value = lastName;
        document.getElementById('editGender').value = gender;
        document.getElementById('editYear').value = year;
        document.getElementById('editCourse').value = course;

        // Display modal
        document.getElementById('editStudentModal').style.display = 'block';
    },
    closeEditStudentModal: function() {
        document.getElementById('editStudentModal').style.display = 'none';
    },
    updateStudent: function() {
        // Get data from modal
        const id = document.getElementById('editStudentID').value;
        const firstName = document.getElementById('editFirstName').value;
        const lastName = document.getElementById('editLastName').value;
        const gender = document.getElementById('editGender').value;
        const year = document.getElementById('editYear').value;
        const course = document.getElementById('editCourse').value;

        // Send update request to server
        fetch('/edit_student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                studentID: id,
                firstName: firstName,
                lastName: lastName,
                gender: gender,
                year: year,
                course: course
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload(); // Reload page after updating
        })
        .catch(error => {
            console.error('Error updating student:', error);
            alert('An error occurred while updating the student.');
        });
    },
    deleteStudent: function(id) {
        if (confirm(`Are you sure you want to delete student with ID ${id}?`)) {
            fetch('/delete_student', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    studentID: id
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    location.reload(); // Reload page after deleting
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error deleting student:', error);
                alert('An error occurred while deleting the student.');
            });
        }
    },
       
    deleteCourse: function(courseCode) {
        if (confirm(`Are you sure you want to delete course with code ${courseCode}?`)) {
            fetch('/delete_course', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    courseCode: courseCode
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    location.reload(); // Reload page after deleting
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error deleting course:', error);
                alert('An error occurred while deleting the course.');
            });
        }
    }
};    

document.addEventListener('DOMContentLoaded', function () {
    // Load student data
    loadStudents();
    // Load course data
    loadCourses();
});

function loadStudents() {
    fetch('students.csv')
        .then(response => response.text())
        .then(data => {
            const rows = data.trim().split('\n').map(row => row.split(','));
            const headers = rows.shift();
            const tbody = document.querySelector('#studentTable tbody');
            tbody.innerHTML = ''; // Clear existing data

            rows.forEach(rowData => {
                const row = document.createElement('tr');
                rowData.forEach(cellData => {
                    const cell = document.createElement('td');
                    cell.textContent = cellData;
                    row.appendChild(cell);
                });
                const editCell = document.createElement('td');
                const deleteCell = document.createElement('td');
                const id = rowData[0];
                editCell.innerHTML = `<button onclick="studentFunctions.editStudent('${id}', '${rowData[1]}', '${rowData[2]}', '${rowData[3]}', '${rowData[4]}', '${rowData[5]}')">Edit</button>`;
                deleteCell.innerHTML = `<button onclick="studentFunctions.deleteStudent('${id}')">Delete</button>`;
                row.appendChild(editCell);
                row.appendChild(deleteCell);
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error loading student data:', error);
        });
}

function loadCourses() {
    fetch('courses.csv')
        .then(response => response.text())
        .then(data => {
            const rows = data.trim().split('\n').map(row => row.split(','));
            const headers = rows.shift();
            const tbody = document.querySelector('#courseTable tbody');
            tbody.innerHTML = ''; // Clear existing data

            rows.forEach(rowData => {
                const row = document.createElement('tr');
                rowData.forEach(cellData => {
                    const cell = document.createElement('td');
                    cell.textContent = cellData;
                    row.appendChild(cell);
                });

                // Edit and Delete buttons for courses
                const editCell = document.createElement('td');
                const deleteCell = document.createElement('td');
                const courseCode = rowData[0];

                /*editCell.innerHTML = `<button onclick="studentFunctions.editCourse('${courseCode}', '${rowData[1]}', '${rowData[2]}')">Edit</button>`;*/
                deleteCell.innerHTML = `<button onclick="studentFunctions.deleteCourse('${courseCode}')">Delete</button>`;

                row.appendChild(editCell);
                row.appendChild(deleteCell);
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error loading course data:', error);
        });
}
