// DOM Elements
const recordForm = document.getElementById('record-form');
const nameInput = document.getElementById('name');
const idInput = document.getElementById('id');
const yearlevelInput = document.getElementById('yearlevel');
const genderInput = document.getElementById('gender');
const coursecodeInput = document.getElementById('coursecode');
const courseInput = document.getElementById('course');
const pictureInput = document.getElementById('picture'); // Added picture input
const recordList = document.getElementById('record-list');
const editIndexInput = document.getElementById('edit-index');
const filterInputs = document.querySelectorAll('.filter-input');
const filterButton = document.getElementById('filter-toggle-button');
const filterBox = document.getElementById('filter-box');

// Records Initialization
let records = [];

// Function to load records from CSV
function loadRecordsFromCSV() {
    fetch('StudentData.csv')
        .then(response => response.text())
        .then(data => {
            const rows = data.split('\n');
            records = rows.map(row => {
                const columns = row.split(',');
                return {
                    name: columns[0],
                    id: columns[1],
                    yearlevel: columns[2],
                    gender: columns[3],
                    coursecode: columns[4],
                    course: columns[5],
                    picture: columns[6]
                };
            });
            displayRecords();
        })
        .catch(error => console.error('Error loading records from CSV:', error));
}

// Display Records
function displayRecords(recordsToDisplay = records) {
    recordList.innerHTML = '';
    if (recordsToDisplay.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `<td colspan="9" style="text-align:center;color:red;">No Record Found</td>`;
        recordList.appendChild(row);
    } else {
        recordsToDisplay.forEach((record, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${record.name}</td>
                <td>${record.id}</td>
                <td>${record.yearlevel}</td>
                <td>${record.gender}</td>
                <td>${record.coursecode}</td>
                <td>${record.course}</td>
                <td><img src="${record.picture}" width="50" height="50"></td>
                <td><button onclick="editRecord(${index})">Edit</button></td>
                <td class="deleteButton"><button onclick="deleteRecord(${index})">Delete</button></td>
            `;
            recordList.appendChild(row);
        });
    }
}

// Function to write records to CSV
function writeToCSV() {
    let csvContent = "Name,ID,Year Level,Gender,Course Code,Course,Picture\r\n";

    records.forEach(record => {
        const row = Object.values(record).join(",");
        csvContent += row + "\r\n";
    });

    const encodedURI = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedURI);
    link.setAttribute("download", "StudentData.csv");
    document.body.appendChild(link); // Required for Firefox
    link.click();
}

// Preview Picture Function
function previewPicture(event) {
    const preview = document.getElementById('preview');
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onloadend = function() {
        preview.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
        document.getElementById('picture-preview').style.display = 'block';
    } else {
        preview.src = "";
        document.getElementById('picture-preview').style.display = 'none';
    }
}

// Add or Update a Record
recordForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const name = nameInput.value;
    const id = idInput.value;
    const yearlevel = yearlevelInput.value;
    const gender = genderInput.value;
    const coursecode = coursecodeInput.value;
    const course = courseInput.value;
    const picture = pictureInput.files[0]; // Get the selected picture file

    if (name && id && yearlevel && gender && coursecode && course && picture) {
        const reader = new FileReader();
        reader.readAsDataURL(picture);
        reader.onload = function () {
            const pictureBase64 = reader.result; // Convert picture to base64
            const editIndex = parseInt(editIndexInput.value);

            if (editIndex === -1) {
                records.push({ name, id, yearlevel, gender, coursecode, course, picture: pictureBase64 });
            } else {
                records[editIndex] = { name, id, yearlevel, gender, coursecode, course, picture: pictureBase64 };
                editIndexInput.value = -1;
            }

            writeToCSV(); // Update CSV
            displayRecords();
        };
    }
});

// Edit a Record
function editRecord(index) {
    const recordToEdit = records[index];
    nameInput.value = recordToEdit.name;
    idInput.value = recordToEdit.id;
    yearlevelInput.value = recordToEdit.yearlevel;
    genderInput.value = recordToEdit.gender;
    coursecodeInput.value = recordToEdit.coursecode;
    courseInput.value = recordToEdit.course;
    editIndexInput.value = index;
}

// Delete a Record
function deleteRecord(index) {
    const confirmDelete = confirm("Are you sure you want to delete this record?");
    if (confirmDelete) {
        records.splice(index, 1);
        writeToCSV(); // Update CSV
        displayRecords();
    }
}

// Filter Records
function filterRecords() {
    const filters = {
        name: nameFilter.value.toLowerCase(),
        id: idFilter.value.toLowerCase(),
        yearlevel: yearlevelFilter.value.toLowerCase(),
        gender: genderFilter.value.toLowerCase(),
        coursecode: coursecodeFilter.value.toLowerCase(),
        course: courseFilter.value.toLowerCase(),
    };

    const filteredRecords = records.filter(record => {
        for (const key in filters) {
            if (filters[key] !== '' && !record[key].toLowerCase().includes(filters[key])) {
                return false;
            }
        }
        return true;
    });

    displayRecords(filteredRecords);
}

// Initialize Filter Event Listeners
filterInputs.forEach(input => {
    input.addEventListener('input', filterRecords);
});

// Function to Clear Input Fields
function clearInputs() {
    nameInput.value = '';
    idInput.value = '';
    yearlevelInput.value = '';
    genderInput.value = '';
    coursecodeInput.value = '';
    courseInput.value = '';
    pictureInput.value = ''; 
    document.getElementById('picture-preview').style.display = 'none'; // Hide picture preview
    editIndexInput.value = -1;
}

// Toggle Filter Box Visibility
filterButton.addEventListener('click', () => {
    filterBox.classList.toggle('show');
});

// Load records from CSV when the page loads
loadRecordsFromCSV();
