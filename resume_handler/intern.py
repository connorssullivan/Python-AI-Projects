import sys
import csv
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QComboBox, QDateEdit, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor

class JobTracker(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set window title and size
        self.setWindowTitle("Connor's Application Tracker")
        self.setGeometry(200, 100, 600, 400)
        
        # Print current working directory for debugging
        print(f"Current working directory: {os.getcwd()}")

        # Create layout and table
        layout = QVBoxLayout()
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Company", "Position", "Date Applied", "State", "Status"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable editing cells directly
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Select entire row
        self.table.cellClicked.connect(self.row_clicked)
        
        layout.addWidget(self.table)
        
        # Add buttons for job entry
        self.addButton = QPushButton("Add Job Entry")
        self.addButton.clicked.connect(self.add_job_dialog)
        layout.addWidget(self.addButton)

        self.modifyButton = QPushButton("Modify Job Entry")
        self.modifyButton.clicked.connect(self.modify_job_entry)
        layout.addWidget(self.modifyButton)

        self.deleteButton = QPushButton("Delete Job Entry")
        self.deleteButton.clicked.connect(self.delete_job_entry)
        layout.addWidget(self.deleteButton)

        self.setLayout(layout)
        
        # Load saved entries from CSV file
        self.load_jobs_from_file()
        
        # Track selected row
        self.selected_row = -1
    
    # Function to open dialog to add new job
    def add_job_dialog(self):
        dialog = AddJobDialog(self)
        if dialog.exec_() == QDialog.Accepted:  # Only add if the dialog was accepted
            company = dialog.company_input.text()
            position = dialog.position_input.text()
            date_applied = dialog.date_input.date()
            state = dialog.state_input.text()
            status = dialog.status_input.currentText()

            # Add the job entry to the table and save it to the CSV
            self.add_job_entry(company, position, date_applied, state, status)

    # Function to add new job entry to the table
    def add_job_entry(self, company, position, date_applied, state, status, save=True):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Set the values in the new row
        self.table.setItem(row_position, 0, QTableWidgetItem(company))
        self.table.setItem(row_position, 1, QTableWidgetItem(position))
        self.table.setItem(row_position, 2, QTableWidgetItem(date_applied.toString("yyyy-MM-dd")))
        self.table.setItem(row_position, 3, QTableWidgetItem(state))
        self.table.setItem(row_position, 4, QTableWidgetItem(status))

        # Color-code based on the status
        if status == "Interview":
            self.set_row_color(row_position, QColor(255, 215, 0))
        elif status == "Accepted":
            self.set_row_color(row_position, Qt.green)
        elif status == "Rejected":
            self.set_row_color(row_position, Qt.red)
        
        # Save to CSV if save is True
        if save:
            self.save_job_to_file(company, position, date_applied, state, status)
    
    # Function to set row color based on status
    def set_row_color(self, row, color):
        for col in range(5):
            self.table.item(row, col).setBackground(color)
    
    # Save job entry to CSV
    def save_job_to_file(self, company, position, date_applied, state, status):
        try:
            with open('job_entries.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company, position, date_applied.toString("yyyy-MM-dd"), state, status])
            print(f"Saved job entry: {company}, {position}")
        except Exception as e:
            print(f"Error saving job entry: {e}")

    # Load job entries from CSV
    def load_jobs_from_file(self):
        try:
            with open('job_entries.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    company, position, date_str, state, status = row
                    date_applied = QDate.fromString(date_str, "yyyy-MM-dd")
                    self.add_job_entry(company, position, date_applied, state, status, save=False)
        except FileNotFoundError:
            print("No CSV file found, starting fresh.")
    
    # Function to detect row selection
    def row_clicked(self, row, column):
        self.selected_row = row

    # Modify job entry
    # Modify job entry
    def modify_job_entry(self):
        if self.selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a job entry to modify.")
            return

        # Get current values
        company = self.table.item(self.selected_row, 0).text()
        position = self.table.item(self.selected_row, 1).text()
        date_applied = QDate.fromString(self.table.item(self.selected_row, 2).text(), "yyyy-MM-dd")
        state = self.table.item(self.selected_row, 3).text()
        status = self.table.item(self.selected_row, 4).text()

        # Open dialog for modifying entry
        dialog = AddJobDialog(self, company, position, date_applied, state, status)
        if dialog.exec_():
            # Update the entry in the table
            self.table.setItem(self.selected_row, 0, QTableWidgetItem(dialog.company_input.text()))
            self.table.setItem(self.selected_row, 1, QTableWidgetItem(dialog.position_input.text()))
            self.table.setItem(self.selected_row, 2, QTableWidgetItem(dialog.date_input.date().toString("yyyy-MM-dd")))
            self.table.setItem(self.selected_row, 3, QTableWidgetItem(dialog.state_input.text()))
            new_status = dialog.status_input.currentText()
            self.table.setItem(self.selected_row, 4, QTableWidgetItem(new_status))

            # Update row color based on the new status
            if new_status == "Interview":
                self.set_row_color(self.selected_row, QColor(255, 215, 0))  # Gold
            elif new_status == "Accepted":
                self.set_row_color(self.selected_row, Qt.green)
            elif new_status == "Rejected":
                self.set_row_color(self.selected_row, Qt.red)

            # Re-save all entries to the file after modification
            self.save_all_jobs_to_file()
            
    # Delete selected job entry
    def delete_job_entry(self):
        if self.selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a job entry to delete.")
            return
        
        # Confirm deletion
        confirm = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this job entry?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.table.removeRow(self.selected_row)
            self.selected_row = -1
            self.save_all_jobs_to_file()

    # Save all jobs to the CSV file (used after modifying/deleting)
    def save_all_jobs_to_file(self):
        try:
            with open('job_entries.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                for row in range(self.table.rowCount()):
                    company = self.table.item(row, 0).text()
                    position = self.table.item(row, 1).text()
                    date_applied = self.table.item(row, 2).text()
                    state = self.table.item(row, 3).text()
                    status = self.table.item(row, 4).text()
                    writer.writerow([company, position, date_applied, state, status])
            print("All job entries saved.")
        except Exception as e:
            print(f"Error saving all job entries: {e}")

# Dialog to add/modify job entry
class AddJobDialog(QDialog):
    def __init__(self, parent=None, company="", position="", date_applied=QDate.currentDate(), state="", status="In Progress"):
        super().__init__(parent)
        
        self.setWindowTitle("Add Job Entry" if not company else "Modify Job Entry")
        self.setGeometry(300, 200, 300, 200)
        
        layout = QVBoxLayout()
        
        # Create input fields
        self.company_input = QLineEdit(self)
        self.company_input.setPlaceholderText("Company")
        self.company_input.setText(company)
        
        self.position_input = QLineEdit(self)
        self.position_input.setPlaceholderText("Position")
        self.position_input.setText(position)
        
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(date_applied)
        
        self.state_input = QLineEdit(self)
        self.state_input.setPlaceholderText("State")
        self.state_input.setText(state)
        
        self.status_input = QComboBox(self)
        self.status_input.addItems(["In Progress", "Interview", "Accepted", "Rejected"])
        self.status_input.setCurrentText(status)
        
        # Add widgets to layout
        layout.addWidget(self.company_input)
        layout.addWidget(self.position_input)
        layout.addWidget(self.date_input)
        layout.addWidget(self.state_input)
        layout.addWidget(self.status_input)
        
        # Add Save and Cancel buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = JobTracker()
    main_window.show()

    # Add a test job entry when the app starts to check CSV writing
    #main_window.add_job_entry("TestCompany", "TestPosition", QDate.currentDate(), "TestState", "In Progress")

    sys.exit(app.exec_())
