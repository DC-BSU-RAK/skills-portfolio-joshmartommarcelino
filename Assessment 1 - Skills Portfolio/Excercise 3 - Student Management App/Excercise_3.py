"""
Student Manager System - GUI Application

This application manages student records including coursework marks, exam scores,
and grade calculations. It provides a Tkinter-based GUI for viewing, searching,
and analyzing student performance data.

Features:
- Load student data from text files
- View all student records with grades and statistics
- Search for individual students by code or name
- Identify highest and lowest scoring students
- Calculate overall percentages and letter grades

Data Format:
First line: number of students
Each subsequent line: code,name,mark1,mark2,mark3,exam_mark
Example: 1345,John Curry,8,15,7,45

Author: Refactored for maintainability and robustness
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from typing import List, Optional
import os


class Student:
    """
    Represents a student with coursework marks and exam score.
    
    Attributes:
        code (str): Student identification code
        name (str): Student's full name
        mark1 (int): First coursework mark (out of 20)
        mark2 (int): Second coursework mark (out of 20)
        mark3 (int): Third coursework mark (out of 20)
        exam (int): Exam mark (out of 100)
    """
    
    # Class constants for grading thresholds
    GRADE_THRESHOLDS = {
        'A': 70,
        'B': 60,
        'C': 50,
        'D': 40
    }
    
    MAX_COURSEWORK = 60  # Total marks available for coursework (3 x 20)
    MAX_EXAM = 100       # Total marks available for exam
    MAX_TOTAL = 160      # Total marks available overall
    
    def __init__(self, code: str, name: str, mark1: int, mark2: int, 
                 mark3: int, exam: int):
        """
        Initialize a Student instance.
        
        Args:
            code: Student identification code
            name: Student's full name
            mark1: First coursework mark (0-20)
            mark2: Second coursework mark (0-20)
            mark3: Third coursework mark (0-20)
            exam: Exam mark (0-100)
        """
        self.code = code.strip()
        self.name = name.strip()
        self.mark1 = mark1
        self.mark2 = mark2
        self.mark3 = mark3
        self.exam = exam
    
    @property
    def coursework_total(self) -> int:
        """Calculate total coursework marks (out of 60)."""
        return self.mark1 + self.mark2 + self.mark3
    
    @property
    def overall_percentage(self) -> float:
        """Calculate overall percentage (coursework + exam out of 160 total)."""
        total = self.coursework_total + self.exam
        return (total / self.MAX_TOTAL) * 100
    
    @property
    def grade(self) -> str:
        """
        Determine letter grade based on overall percentage.
        
        Returns:
            str: Letter grade (A, B, C, D, or F)
        """
        percentage = self.overall_percentage
        
        for letter_grade, threshold in self.GRADE_THRESHOLDS.items():
            if percentage >= threshold:
                return letter_grade
        
        return 'F'  # Below 40%
    
    def format_record(self) -> str:
        """
        Format student record for display.
        
        Returns:
            str: Formatted multi-line string with student information
        """
        return (
            f"Student Name: {self.name}\n"
            f"Student Number: {self.code}\n"
            f"Total Coursework Mark: {self.coursework_total}/{self.MAX_COURSEWORK}\n"
            f"Exam Mark: {self.exam}/{self.MAX_EXAM}\n"
            f"Overall Percentage: {self.overall_percentage:.2f}%\n"
            f"Grade: {self.grade}\n"
            f"{'-' * 50}"
        )
    
    def __str__(self) -> str:
        """String representation for debugging."""
        return f"Student({self.code}, {self.name}, {self.overall_percentage:.1f}%)"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return (
            f"Student(code='{self.code}', name='{self.name}', "
            f"marks=[{self.mark1}, {self.mark2}, {self.mark3}], "
            f"exam={self.exam})"
        )


class StudentManager:
    """
    Manages a collection of Student objects and provides data operations.
    
    This class handles loading student data from files or text input,
    and provides methods for querying and analyzing the student data.
    """
    
    def __init__(self):
        """Initialize an empty StudentManager."""
        self.students: List[Student] = []
    
    def load_from_file(self, filename: str) -> bool:
        """
        Load student data from a text file.
        
        Expected format:
        - First line: number of students (integer)
        - Subsequent lines: code,name,mark1,mark2,mark3,exam
        
        Args:
            filename: Path to the student data file
            
        Returns:
            bool: True if loading succeeded, False otherwise
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if not lines:
                print("Error: File is empty")
                return False
            
            # Parse number of students from first line
            try:
                num_students = int(lines[0].strip())
            except ValueError:
                print("Error: First line must contain number of students")
                return False
            
            # Parse student records
            self.students = []
            for i, line in enumerate(lines[1:], start=2):
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Parse student data
                student = self._parse_student_line(line, line_number=i)
                if student:
                    self.students.append(student)
            
            # Verify we loaded the expected number of students
            if len(self.students) != num_students:
                print(f"Warning: Expected {num_students} students, loaded {len(self.students)}")
            
            return len(self.students) > 0
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            return False
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def load_from_text(self, text: str) -> bool:
        """
        Load student data from a text string.
        
        Uses the same format as load_from_file().
        
        Args:
            text: Multi-line string containing student data
            
        Returns:
            bool: True if loading succeeded, False otherwise
        """
        try:
            lines = text.strip().split('\n')
            
            if not lines:
                return False
            
            # Parse number of students
            try:
                num_students = int(lines[0].strip())
            except ValueError:
                print("Error: First line must contain number of students")
                return False
            
            # Parse student records
            self.students = []
            for i, line in enumerate(lines[1:], start=2):
                line = line.strip()
                
                if not line:
                    continue
                
                student = self._parse_student_line(line, line_number=i)
                if student:
                    self.students.append(student)
            
            return len(self.students) > 0
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def _parse_student_line(self, line: str, line_number: int = 0) -> Optional[Student]:
        """
        Parse a single line of student data into a Student object.
        
        Args:
            line: Comma-separated string with student data
            line_number: Line number for error reporting
            
        Returns:
            Student object if parsing succeeded, None otherwise
        """
        try:
            parts = [part.strip() for part in line.split(',')]
            
            if len(parts) < 6:
                print(f"Warning: Line {line_number} has insufficient fields, skipping")
                return None
            
            # Extract and validate data
            code = parts[0]
            name = parts[1]
            
            # Parse numeric fields with validation
            try:
                mark1 = int(parts[2])
                mark2 = int(parts[3])
                mark3 = int(parts[4])
                exam = int(parts[5])
            except ValueError:
                print(f"Warning: Line {line_number} has invalid numeric values, skipping")
                return None
            
            # Basic validation of mark ranges
            if not (0 <= mark1 <= 20 and 0 <= mark2 <= 20 and 0 <= mark3 <= 20):
                print(f"Warning: Line {line_number} has coursework marks outside 0-20 range")
            
            if not (0 <= exam <= 100):
                print(f"Warning: Line {line_number} has exam mark outside 0-100 range")
            
            return Student(code, name, mark1, mark2, mark3, exam)
            
        except Exception as e:
            print(f"Error parsing line {line_number}: {e}")
            return None
    
    def get_all_records(self) -> str:
        """
        Generate formatted string of all student records with summary statistics.
        
        Returns:
            str: Formatted display of all student records and class summary
        """
        if not self.students:
            return "No student data loaded."
        
        output = "=" * 50 + "\n"
        output += "ALL STUDENT RECORDS\n"
        output += "=" * 50 + "\n\n"
        
        # Display each student record
        for student in self.students:
            output += student.format_record() + "\n"
        
        # Calculate and display summary statistics
        total_students = len(self.students)
        avg_percentage = sum(s.overall_percentage for s in self.students) / total_students
        
        output += "\n" + "=" * 50 + "\n"
        output += "SUMMARY\n"
        output += f"Total Students: {total_students}\n"
        output += f"Average Percentage: {avg_percentage:.2f}%\n"
        output += "=" * 50
        
        return output
    
    def get_student_by_code(self, code: str) -> Optional[Student]:
        """
        Find a student by their student code (exact match).
        
        Args:
            code: Student identification code to search for
            
        Returns:
            Student object if found, None otherwise
        """
        code = code.strip()
        for student in self.students:
            if student.code == code:
                return student
        return None
    
    def get_student_by_name(self, name: str) -> Optional[Student]:
        """
        Find a student by name (case-insensitive partial match).
        
        Args:
            name: Full or partial name to search for
            
        Returns:
            First matching Student object if found, None otherwise
        """
        name_lower = name.strip().lower()
        for student in self.students:
            if name_lower in student.name.lower():
                return student
        return None
    
    def get_highest_scoring_student(self) -> Optional[Student]:
        """
        Get the student with the highest overall percentage.
        
        Returns:
            Student object with highest score, or None if no students loaded
        """
        if not self.students:
            return None
        return max(self.students, key=lambda s: s.overall_percentage)
    
    def get_lowest_scoring_student(self) -> Optional[Student]:
        """
        Get the student with the lowest overall percentage.
        
        Returns:
            Student object with lowest score, or None if no students loaded
        """
        if not self.students:
            return None
        return min(self.students, key=lambda s: s.overall_percentage)
    
    def get_student_count(self) -> int:
        """Get the total number of students loaded."""
        return len(self.students)
    def sort_students(self, key: str, ascending: bool = True):
        """Sort student records by name or percentage."""
        if key == "name":
            self.students.sort(key=lambda s: s.name.lower(), reverse=not ascending)
        elif key == "percentage":
            self.students.sort(key=lambda s: s.overall_percentage, reverse=not ascending)

    def add_student(self, student: Student):
        """Add a new student to memory."""
        self.students.append(student)

    def delete_student(self, identifier: str) -> bool:
        """Delete student by code or name."""
        for s in self.students:
            if s.code == identifier or identifier.lower() in s.name.lower():
                self.students.remove(s)
                return True
        return False

    def update_student(self, code: str, updated: Student) -> bool:
        """Update an existing student's full record."""
        for i, s in enumerate(self.students):
            if s.code == code:
                self.students[i] = updated
                return True
        return False

    def save_to_file(self, filename: str):
        """Persist student records to file."""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(len(self.students)) + "\n")
            for s in self.students:
                line = f"{s.code},{s.name},{s.mark1},{s.mark2},{s.mark3},{s.exam}\n"
                f.write(line)
class StudentManagerGUI:
    """
    Main GUI application for the Student Manager System.
    
    Provides a Tkinter-based interface for loading student data,
    viewing records, and analyzing student performance.
    """
    
    # UI Color scheme
    COLORS = {
        'primary': '#2196F3',
        'success': '#4CAF50',
        'info': '#2196F3',
        'warning': '#FF9800',
        'danger': '#f44336',
        'light_bg': '#f0f0f0',
        'white': 'white'
    }
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the Student Manager GUI.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Student Manager System")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        
        # Initialize data manager
        self.manager = StudentManager()
        
        # Build UI components
        self.create_menu()
        self.create_widgets()
        
        # Auto-load sample or real data
        self.load_initial_data()
    
    def create_menu(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data from File...", command=self.load_data_dialog)
        file_menu.add_command(label="Auto-load studentMarks.txt", command=self.auto_load_student_marks)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="All Student Records", command=self.view_all_records)
        view_menu.add_command(label="Individual Student Record", command=self.view_individual_record)
        
        # Analysis menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        analysis_menu.add_command(label="Highest Scoring Student", command=self.show_highest_student)
        analysis_menu.add_command(label="Lowest Scoring Student", command=self.show_lowest_student)
    
    def create_widgets(self):
        """Create all GUI widgets and layout."""
        # Title bar
        title = tk.Label(
            self.root, 
            text="Student Manager System", 
            font=("Arial", 20, "bold"),
            bg=self.COLORS['primary'],
            fg=self.COLORS['white'],
            pady=10
        )
        title.pack(fill="x")
        
        # Button toolbar
        btn_frame = tk.Frame(self.root, bg=self.COLORS['light_bg'], pady=10)
        btn_frame.pack(fill="x")
        
        # Create action buttons
        buttons = [
            ("View All Student Records", self.view_all_records, 'success'),
            ("View Individual Record", self.view_individual_record, 'info'),
            ("Highest Score", self.show_highest_student, 'warning'),
            ("Lowest Score", self.show_lowest_student, 'danger'),
            ("Sort Records", self.sort_records_dialog, 'info'),
            ("Add Student", self.add_student_dialog, 'success'),
            ("Delete Student", self.delete_student_dialog, 'danger'),
            ("Update Student", self.update_student_dialog, 'warning')
        ]
        
        for text, command, color in buttons:
            tk.Button(
                btn_frame,
                text=text,
                command=command,
                bg=self.COLORS[color],
                fg=self.COLORS['white'],
                font=("Arial", 11),
                padx=10,
                pady=5,
                cursor="hand2"
            ).pack(side="left", padx=5)
        
        # Output display area
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(
            output_frame,
            text="Output:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            height=25,
            bg="white",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.output_text.pack(fill="both", expand=True)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=self.COLORS['light_bg']
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_initial_data(self):
        """
        Load initial data on startup.
        
        Tries to auto-load studentMarks.txt if it exists,
        otherwise loads sample data for demonstration.
        """
        # Try to load studentMarks.txt from current directory
        if os.path.exists("studentMarks.txt"):
            self.auto_load_student_marks()
        else:
            self.load_sample_data()
    
    def load_sample_data(self):
        """Load sample data for demonstration purposes."""
        sample_data = """3
S001,Alice Johnson,18,19,20,85
S002,Bob Smith,15,16,14,72
S003,Charlie Brown,20,19,18,90"""
        
        if self.manager.load_from_text(sample_data):
            self.update_status("Sample data loaded (studentMarks.txt not found)")
            self.display_output(
                "Sample data loaded for demonstration.\n\n"
                "To load real data:\n"
                "1. Place 'studentMarks.txt' in the same folder as this program\n"
                "2. Use File > Auto-load studentMarks.txt\n"
                "3. Or use File > Load Data from File...\n\n"
                "Click 'View All Student Records' to see the data."
            )
        else:
            self.update_status("Failed to load sample data")
            messagebox.showerror("Error", "Failed to load sample data")
    
    def auto_load_student_marks(self):
        """
        Automatically load studentMarks.txt from the current directory.
        
        Displays appropriate messages if file is found or not found.
        """
        filename = "studentMarks.txt"
        
        if os.path.exists(filename):
            if self.manager.load_from_file(filename):
                count = self.manager.get_student_count()
                self.update_status(f"Loaded {count} students from {filename}")
                self.display_output(
                    f"Successfully loaded {count} students from {filename}.\n\n"
                    "Click 'View All Student Records' to see results."
                )
            else:
                self.update_status("Failed to load studentMarks.txt")
                messagebox.showerror(
                    "Error",
                    f"{filename} was found but could not be loaded.\n"
                    "Please check the file format."
                )
        else:
            self.update_status(f"{filename} not found")
            messagebox.showwarning(
                "File Not Found",
                f"{filename} was not found in the current directory.\n\n"
                "Please place the file in the same folder as this program,\n"
                "or use 'Load Data from File...' to browse for it."
            )
    
    def load_data_dialog(self):
        """Open a file dialog to load a student data file."""
        filename = filedialog.askopenfilename(
            title="Select Student Data File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialdir=os.getcwd()
        )
        
        if filename:
            if self.manager.load_from_file(filename):
                count = self.manager.get_student_count()
                self.update_status(f"Loaded {count} students from {os.path.basename(filename)}")
                self.display_output(
                    f"Successfully loaded {count} student records from:\n{filename}\n\n"
                    "Click 'View All Student Records' to see results."
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"Failed to load the selected file:\n{filename}\n\n"
                    "Please check the file format."
                )
    
    def view_all_records(self):
        """Display all student records with summary statistics."""
        if self.manager.get_student_count() == 0:
            messagebox.showwarning("No Data", "Please load student data first.")
            return
        
        output = self.manager.get_all_records()
        self.display_output(output)
        self.update_status(f"Displaying {self.manager.get_student_count()} student records")
    
    def view_individual_record(self):
        """
        Display an individual student record.
        
        Opens a dialog for the user to search by student code or name.
        """
        if self.manager.get_student_count() == 0:
            messagebox.showwarning("No Data", "Please load student data first.")
            return
        
        # Create search dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Search for Student")
        dialog.geometry("450x180")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Instructions
        tk.Label(
            dialog,
            text="Enter Student Code or Name:",
            font=("Arial", 12, "bold")
        ).pack(pady=15)
        
        tk.Label(
            dialog,
            text="(Name search is case-insensitive and matches partial names)",
            font=("Arial", 9),
            fg="gray"
        ).pack()
        
        # Search entry
        entry = tk.Entry(dialog, font=("Arial", 12), width=30)
        entry.pack(pady=10)
        entry.focus()
        
        def search_student():
            """Perform the student search."""
            search_term = entry.get().strip()
            
            if not search_term:
                messagebox.showwarning(
                    "Input Required",
                    "Please enter a student code or name.",
                    parent=dialog
                )
                return
            
            # Try searching by code first (exact match)
            student = self.manager.get_student_by_code(search_term)
            
            # If not found, try by name (partial match)
            if not student:
                student = self.manager.get_student_by_name(search_term)
            
            if student:
                self.display_output(student.format_record())
                self.update_status(f"Displaying record for {student.name}")
                dialog.destroy()
            else:
                messagebox.showerror(
                    "Not Found",
                    f"No student found matching:\n'{search_term}'\n\n"
                    "Please check the spelling or try a different search term.",
                    parent=dialog
                )
        
        # Search button
        tk.Button(
            dialog,
            text="Search",
            command=search_student,
            bg=self.COLORS['info'],
            fg=self.COLORS['white'],
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            cursor="hand2"
        ).pack(pady=10)
        
        # Allow Enter key to trigger search
        entry.bind('<Return>', lambda e: search_student())
        
        # Center dialog on parent window
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
    
    def show_highest_student(self):
        """Display the student with the highest overall score."""
        student = self.manager.get_highest_scoring_student()
        
        if student:
            output = "=" * 50 + "\n"
            output += "HIGHEST SCORING STUDENT\n"
            output += "=" * 50 + "\n\n"
            output += student.format_record()
            
            self.display_output(output)
            self.update_status(
                f"Highest score: {student.name} ({student.overall_percentage:.2f}%)"
            )
        else:
            messagebox.showwarning("No Data", "Please load student data first.")
    
    def show_lowest_student(self):
        """Display the student with the lowest overall score."""
        student = self.manager.get_lowest_scoring_student()
        
        if student:
            output = "=" * 50 + "\n"
            output += "LOWEST SCORING STUDENT\n"
            output += "=" * 50 + "\n\n"
            output += student.format_record()
            
            self.display_output(output)
            self.update_status(
                f"Lowest score: {student.name} ({student.overall_percentage:.2f}%)"
            )
        else:
            messagebox.showwarning("No Data", "Please load student data first.")
    
    
    def sort_records_dialog(self):
        """Open sorting options dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Sort Records")
        dialog.geometry("300x220")
        dialog.grab_set()

        tk.Label(dialog, text="Sort By:", font=("Arial", 11, "bold")).pack(pady=5)

        sort_by = ttk.Combobox(dialog, values=["Name", "Percentage"], state="readonly")
        sort_by.pack()
        sort_by.current(0)

        tk.Label(dialog, text="Order:", font=("Arial", 11, "bold")).pack(pady=5)

        order = ttk.Combobox(dialog, values=["Ascending", "Descending"], state="readonly")
        order.pack()
        order.current(0)

        def apply_sort():
            key = "name" if sort_by.get() == "Name" else "percentage"
            ascending = order.get() == "Ascending"

            self.manager.sort_students(key, ascending)
            self.display_output(self.manager.get_all_records())
            self.update_status("Records sorted successfully")
            dialog.destroy()

        tk.Button(dialog, text="Sort", command=apply_sort).pack(pady=15)

    def add_student_dialog(self):
        """Dialog for adding a new student record."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Student")
        dialog.geometry("350x400")
        dialog.grab_set()

        fields = ["Student Number", "Name", "CW1", "CW2", "CW3", "Exam"]
        entries = {}

        for field in fields:
            tk.Label(dialog, text=field).pack()
            entry = tk.Entry(dialog)
            entry.pack()
            entries[field] = entry

        def save_student():
            try:
                student = Student(
                    entries["Student Number"].get(),
                    entries["Name"].get(),
                    int(entries["CW1"].get()),
                    int(entries["CW2"].get()),
                    int(entries["CW3"].get()),
                    int(entries["Exam"].get())
                )

                self.manager.add_student(student)
                self.manager.save_to_file("../../A1 - Resources/studentMarks.txt")

                self.update_status("Student added successfully")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid numeric input")

        tk.Button(dialog, text="Save", command=save_student).pack(pady=15)

    def delete_student_dialog(self):
        """Remove a student record by ID or Name."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Student")
        dialog.geometry("300x150")
        dialog.grab_set()

        tk.Label(dialog, text="Enter Student Number or Name").pack(pady=10)
        entry = tk.Entry(dialog)
        entry.pack()

        def delete():
            if self.manager.delete_student(entry.get()):
                self.manager.save_to_file("../../A1 - Resources/studentMarks.txt")
                self.update_status("Student deleted")
                dialog.destroy()
            else:
                messagebox.showerror("Not Found", "Student not found")

        tk.Button(dialog, text="Delete", command=delete).pack(pady=10)

    def update_student_dialog(self):
        """Edit an existing student's record."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Student")
        dialog.geometry("350x430")
        dialog.grab_set()

        tk.Label(dialog, text="Student Number to Update").pack()
        code_entry = tk.Entry(dialog)
        code_entry.pack()

        fields = ["Name", "CW1", "CW2", "CW3", "Exam"]
        entries = {}

        for field in fields:
            tk.Label(dialog, text=field).pack()
            entry = tk.Entry(dialog)
            entry.pack()
            entries[field] = entry

        def update():
            student = self.manager.get_student_by_code(code_entry.get())

            if not student:
                messagebox.showerror("Error", "Student not found")
                return

            try:
                updated = Student(
                    student.code,
                    entries["Name"].get(),
                    int(entries["CW1"].get()),
                    int(entries["CW2"].get()),
                    int(entries["CW3"].get()),
                    int(entries["Exam"].get())
                )

                self.manager.update_student(student.code, updated)
                self.manager.save_to_file("../../A1 - Resources/studentMarks.txt")

                self.update_status("Student record updated")
                dialog.destroy()

            except ValueError:
                messagebox.showerror("Error", "Invalid numeric input")

        tk.Button(dialog, text="Update", command=update).pack(pady=15)
    
    def display_output(self, text: str):
        """
        Display text in the output area.
        
        Args:
            text: Text to display
        """
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, text)
    
    def update_status(self, message: str):
        """
        Update the status bar message.
        
        Args:
            message: Status message to display
        """
        self.status_label.config(text=message)
def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = StudentManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()