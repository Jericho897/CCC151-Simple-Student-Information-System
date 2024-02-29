// Function to toggle side navigation bar
function toggleNav() {
    var sidenav = document.querySelector('.sidenav');
    sidenav.classList.toggle('active');
}

// Function to add course
function addCourse(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    const formData = new FormData(document.getElementById('addCourseForm'));

    // Send course data to server
    fetch('/add_course', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('Course added successfully.');
            // Optionally, you can display a message here indicating success
        } else {
            throw new Error('Failed to add course.');
        }
    })
    .catch(error => console.error('Error adding course:', error));
}

// Function to add student
function addStudent(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    const formData = new FormData(document.getElementById('addStudentForm'));

    // Send student data to server
    fetch('/add_student', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('Student added successfully.');
            // Optionally, you can display a message here indicating success
        } else {
            throw new Error('Failed to add student.');
        }
    })
    .catch(error => console.error('Error adding student:', error));
}

// Add event listeners for form submissions
document.getElementById('addCourseForm').addEventListener('submit', addCourse);
document.getElementById('addStudentForm').addEventListener('submit', addStudent);
