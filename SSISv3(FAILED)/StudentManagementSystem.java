import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class StudentManagementSystem extends JFrame {
    private JTextField idNumberField, firstNameField, lastNameField;
    private JRadioButton maleRadio, femaleRadio, otherRadio;
    private JSlider yearLevelSlider;
    private JSlider courseCodeSlider;
    private JSlider courseNameSlider;
    private JTable studentTable;
    private DefaultTableModel tableModel;
    private List<Student> students;

    public StudentManagementSystem() {
        setTitle("Manage Students");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLocationRelativeTo(null);

        // Initialize components (create labels, buttons, text fields, etc.)
        JLabel idNumberLabel = new JLabel("ID Number:");
        idNumberField = new JTextField(5);

        JLabel firstNameLabel = new JLabel("First Name:");
        firstNameField = new JTextField(10);

        JLabel lastNameLabel = new JLabel("Last Name:");
        lastNameField = new JTextField(10);

        JLabel genderLabel = new JLabel("Gender:");
        maleRadio = new JRadioButton("Male");
        femaleRadio = new JRadioButton("Female");
        otherRadio = new JRadioButton("Other");

        ButtonGroup genderGroup = new ButtonGroup();
        genderGroup.add(maleRadio);
        genderGroup.add(femaleRadio);
        genderGroup.add(otherRadio);

        JLabel yearLevelLabel = new JLabel("Year Level:");
        yearLevelSlider = new JSlider(JSlider.HORIZONTAL, 1, 4, 1);
        yearLevelSlider.setMajorTickSpacing(1);
        yearLevelSlider.setPaintTicks(true);
        yearLevelSlider.setPaintLabels(true);

        JLabel courseCodeLabel = new JLabel("Course Code:");
        courseCodeSlider = new JSlider(JSlider.HORIZONTAL, 100, 999, 100);
        courseCodeSlider.setMajorTickSpacing(100);
        courseCodeSlider.setPaintTicks(true);
        courseCodeSlider.setPaintLabels(true);

        JLabel courseNameLabel = new JLabel("Course Name:");
        courseNameSlider = new JSlider(JSlider.HORIZONTAL, 1, 10, 1);
        courseNameSlider.setMajorTickSpacing(1);
        courseNameSlider.setPaintTicks(true);
        courseNameSlider.setPaintLabels(true);

        JButton addButton = new JButton("Add");
        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addStudent();
            }
        });

        JButton editButton = new JButton("Edit");
        editButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                editStudent();
            }
        });

        JButton deleteButton = new JButton("Delete");
        deleteButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                deleteStudent();
            }
        });

        // Load student data from students.csv
        loadStudents();

        // Create table model
        tableModel = new DefaultTableModel();
        tableModel.addColumn("ID Number");
        tableModel.addColumn("First Name");
        tableModel.addColumn("Last Name");
        tableModel.addColumn("Gender");
        tableModel.addColumn("Year Level");
        tableModel.addColumn("Course Code");
        tableModel.addColumn("Course Name");

        // Populate table with existing student data
        for (Student student : students) {
            tableModel.addRow(student.toTableRow());
        }

        studentTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(studentTable);

        // Add components to the frame
        JPanel inputPanel = new JPanel(new GridLayout(0, 2));
        inputPanel.add(idNumberLabel);
        inputPanel.add(idNumberField);
        inputPanel.add(firstNameLabel);
        inputPanel.add(firstNameField);
        inputPanel.add(lastNameLabel);
        inputPanel.add(lastNameField);
        inputPanel.add(genderLabel);
        JPanel genderPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        genderPanel.add(maleRadio);
        genderPanel.add(femaleRadio);
        genderPanel.add(otherRadio);
        inputPanel.add(genderPanel);
        inputPanel.add(yearLevelLabel);
        inputPanel.add(yearLevelSlider);
        inputPanel.add(courseCodeLabel);
        inputPanel.add(courseCodeSlider);
        inputPanel.add(courseNameLabel);
        inputPanel.add(courseNameSlider);

        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        buttonPanel.add(addButton);
        buttonPanel.add(editButton);
        buttonPanel.add(deleteButton);

        JPanel inputContainerPanel = new JPanel(new BorderLayout());
        inputContainerPanel.add(inputPanel, BorderLayout.CENTER);
        inputContainerPanel.add(buttonPanel, BorderLayout.SOUTH);

        JPanel contentPanel = new JPanel(new BorderLayout());
        contentPanel.add(inputContainerPanel, BorderLayout.WEST);
        contentPanel.add(scrollPane, BorderLayout.CENTER);

        getContentPane().add(contentPanel);

        // Save student data to students.csv on program exit
        addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                saveStudents();
            }
        });

        setVisible(true);
    }

    private void loadStudents() {
        students = new ArrayList<>();
        try {
            BufferedReader reader = new BufferedReader(new FileReader("students.csv"));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 7) {
                    int idNumber = Integer.parseInt(parts[0]);
                    String firstName = parts[1];
                    String lastName = parts[2];
                    String gender = parts[3];
                    String yearLevel = parts[4];
                    String courseCode = parts[5];
                    String courseName = parts[6];
                    students.add(new Student(idNumber, firstName, lastName, gender, yearLevel, courseCode, courseName));
                }
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void saveStudents() {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter("students.csv"));
            for (Student student : students) {
                writer.write(student.toCsvLine());
                writer.newLine();
            }
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void addStudent() {
        int idNumber = Integer.parseInt(idNumberField.getText());
        String firstName = firstNameField.getText();
        String lastName = lastNameField.getText();
        String gender = maleRadio.isSelected() ? "Male" : femaleRadio.isSelected() ? "Female" : otherRadio.isSelected() ? "Other" : "";
        int yearLevel = yearLevelSlider.getValue();
        int courseCode = courseCodeSlider.getValue();
        int courseName = courseNameSlider.getValue();

        Object[] rowData = {idNumber, firstName, lastName, gender, yearLevel, courseCode, courseName};
        tableModel.addRow(rowData);
        students.add(new Student(idNumber, firstName, lastName, gender, String.valueOf(yearLevel), String.valueOf(courseCode), String.valueOf(courseName)));

        clearFields();
    }

    private void editStudent() {
        int selectedRow = studentTable.getSelectedRow();
        if (selectedRow != -1) {
            int idNumber = Integer.parseInt(idNumberField.getText());
            String firstName = firstNameField.getText();
            String lastName = lastNameField.getText();
            String gender = maleRadio.isSelected() ? "Male" : femaleRadio.isSelected() ? "Female" : otherRadio.isSelected() ? "Other" : "";
            int yearLevel = yearLevelSlider.getValue();
            int courseCode = courseCodeSlider.getValue();
            int courseName = courseNameSlider.getValue();

            tableModel.setValueAt(idNumber, selectedRow, 0);
            tableModel.setValueAt(firstName, selectedRow, 1);
            tableModel.setValueAt(lastName, selectedRow, 2);
            tableModel.setValueAt(gender, selectedRow, 3);
            tableModel.setValueAt(yearLevel, selectedRow, 4);
            tableModel.setValueAt(courseCode, selectedRow, 5);
            tableModel.setValueAt(courseName, selectedRow, 6);

            Student student = students.get(selectedRow);
            student.setIdNumber(idNumber);
            student.setFirstName(firstName);
            student.setLastName(lastName);
            student.setGender(gender);
            student.setYearLevel(String.valueOf(yearLevel));
            student.setCourseCode(String.valueOf(courseCode));
            student.setCourseName(String.valueOf(courseName));

            clearFields();
        } else {
            JOptionPane.showMessageDialog(this, "Please select a student to edit.");
        }
    }

    private void deleteStudent() {
        int selectedRow = studentTable.getSelectedRow();
        if (selectedRow != -1) {
            tableModel.removeRow(selectedRow);
            students.remove(selectedRow);
            clearFields();
        } else {
            JOptionPane.showMessageDialog(this, "Please select a student to delete.");
        }
    }

    private void clearFields() {
        idNumberField.setText("");
        firstNameField.setText("");
        lastNameField.setText("");
        maleRadio.setSelected(false);
        femaleRadio.setSelected(false);
        otherRadio.setSelected(false);
        yearLevelSlider.setValue(1);
        courseCodeSlider.setValue(100);
        courseNameSlider.setValue(1);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(StudentManagementSystem::new);
    }
}

class Student {
    private int idNumber;
    private String firstName;
    private String lastName;
    private String gender;
    private String yearLevel;
    private String courseCode;
    private String courseName;

    public Student(int idNumber, String firstName, String lastName, String gender, String yearLevel, String courseCode, String courseName) {
        this.idNumber = idNumber;
        this.firstName = firstName;
        this.lastName = lastName;
        this.gender = gender;
        this.yearLevel = yearLevel;
        this.courseCode = courseCode;
        this.courseName = courseName;
    }

    public int getIdNumber() {
        return idNumber;
    }

    public void setIdNumber(int idNumber) {
        this.idNumber = idNumber;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public String getYearLevel() {
        return yearLevel;
    }

    public void setYearLevel(String yearLevel) {
        this.yearLevel = yearLevel;
    }

    public String getCourseCode() {
        return courseCode;
    }

    public void setCourseCode(String courseCode) {
        this.courseCode = courseCode;
    }

    public String getCourseName() {
        return courseName;
    }

    public void setCourseName(String courseName) {
        this.courseName = courseName;
    }

    public Object[] toTableRow() {
        return new Object[]{idNumber, firstName, lastName, gender, yearLevel, courseCode, courseName};
    }

    public String toCsvLine() {
        return idNumber + "," + firstName + "," + lastName + "," + gender + "," + yearLevel + "," + courseCode + "," + courseName;
    }
}
