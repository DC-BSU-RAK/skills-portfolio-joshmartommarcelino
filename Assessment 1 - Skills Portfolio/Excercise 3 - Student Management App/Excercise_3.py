import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from typing import List, Dict, Tuple
import os


class Student:
    """Class to represent a student with their marks"""
    
    def __init__(self, code: str, name: str, mark1: int, mark2: int, mark3: int, exam: int):
        self.code = code
        self.name = name
        self.mark1 = mark1
        self.mark2 = mark2
        self.mark3 = mark3
        self.exam = exam
    
    @property
    def coursework_total(self) -> int:
        """Calculate total coursework marks (out of 60)"""
        return self.mark1 + self.mark2 + self.mark3
    
    @property
    def overall_percentage(self) -> float:
        """Calculate overall percentage (out of 160 total marks)"""
        total = self.coursework_total + self.exam
        return (total / 160) * 100
    
    @property
    def grade(self) -> str:
        """Determine grade based on percentage"""
        percentage = self.overall_percentage
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def format_record(self) -> str:
        """Format student record for display"""
        return f"""Student Name: {self.name}
Student Number: {self.code}
Total Coursework Mark: {self.coursework_total}/60
Exam Mark: {self.exam}/100
Overall Percentage: {self.overall_percentage:.2f}%
Grade: {self.grade}
{'-' * 50}"""


class StudentManager:
    """Manages student data operations"""
    
    def __init__(self):
        self.students: List[Student] = []
    
    def load_from_file(self, filename: str) -> bool:
        """Load student data from file"""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                
            if not lines:
                return False
            
            # First line is number of students (optional to use)
            num_students = int(lines[0].strip())
            
            self.students = []
            for line in lines[1:]:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 6:
                        code = parts[0]
                        name = parts[1]
                        mark1 = int(parts[2])
                        mark2 = int(parts[3])
                        mark3 = int(parts[4])
                        exam = int(parts[5])
                        
                        student = Student(code, name, mark1, mark2, mark3, exam)
                        self.students.append(student)
            
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def load_from_text(self, text: str) -> bool:
        """Load student data from text input"""
        try:
            lines = text.strip().split('\n')
            
            if not lines:
                return False
            
            # First line is number of students
            num_students = int(lines[0].strip())
            
            self.students = []
            for line in lines[1:]:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 6:
                        code = parts[0]
                        name = parts[1]
                        mark1 = int(parts[2])
                        mark2 = int(parts[3])
                        mark3 = int(parts[4])
                        exam = int(parts[5])
                        
                        student = Student(code, name, mark1, mark2, mark3, exam)
                        self.students.append(student)
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_all_records(self) -> str:
        """Get formatted string of all student records"""
        if not self.students:
            return "No student data loaded."
        
        output = "=" * 50 + "\n"
        output += "ALL STUDENT RECORDS\n"
        output += "=" * 50 + "\n\n"
        
        for student in self.students:
            output += student.format_record() + "\n"
        
        # Add summary
        avg_percentage = sum(s.overall_percentage for s in self.students) / len(self.students)
        output += "\n" + "=" * 50 + "\n"
        output += f"SUMMARY\n"
        output += f"Total Students: {len(self.students)}\n"
        output += f"Average Percentage: {avg_percentage:.2f}%\n"
        output += "=" * 50
        
        return output
    
    def get_student_by_code(self, code: str) -> Student:
        """Find student by student code"""
        for student in self.students:
            if student.code == code:
                return student
        return None
    
    def get_student_by_name(self, name: str) -> Student:
        """Find student by name (case-insensitive partial match)"""
        name_lower = name.lower()
        for student in self.students:
            if name_lower in student.name.lower():
                return student
        return None
    
    def get_highest_scoring_student(self) -> Student:
        """Get student with highest overall percentage"""
        if not self.students:
            return None
        return max(self.students, key=lambda s: s.overall_percentage)
    
    def get_lowest_scoring_student(self) -> Student:
        """Get student with lowest overall percentage"""
        if not self.students:
            return None
        return min(self.students, key=lambda s: s.overall_percentage)
    
    def get_all_student_names(self) -> List[str]:
        """Get list of all student names"""
        return [f"{s.name} ({s.code})" for s in self.students]


class StudentManagerGUI:
    """Main GUI application for Student Manager"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager System")
        self.root.geometry("900x700")
        
        self.manager = StudentManager()
        
        # Create main UI
        self.create_menu()
        self.create_widgets()
        
        # Load sample data
        self.load_sample_data()

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data", command=self.load_data_dialog)
        file_menu.add_command(label="Load studentMarks.txt", command=self.auto_load_student_marks)
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
        """Create main GUI widgets"""
        # Title
        title = tk.Label(self.root, text="Student Manager System", 
                        font=("Arial", 20, "bold"), bg="#2196F3", fg="white", pady=10)
        title.pack(fill="x")
        
        # Button frame
        btn_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        btn_frame.pack(fill="x")
        
        # Buttons
        tk.Button(btn_frame, text="View All Student Records", 
                 command=self.view_all_records, bg="#4CAF50", fg="white",
                 font=("Arial", 11), padx=10, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="View Individual Record", 
                 command=self.view_individual_record, bg="#2196F3", fg="white",
                 font=("Arial", 11), padx=10, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Highest Score", 
                 command=self.show_highest_student, bg="#FF9800", fg="white",
                 font=("Arial", 11), padx=10, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Lowest Score", 
                 command=self.show_lowest_student, bg="#f44336", fg="white",
                 font=("Arial", 11), padx=10, pady=5).pack(side="left", padx=5)
        
        # Output area
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(output_frame, text="Output:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                     font=("Courier", 10), height=25)
        self.output_text.pack(fill="both", expand=True)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def load_sample_data(self):
        """Load sample data for demonstration"""
        sample_data = """3
S001,Alice Johnson,18,19,20,85
S002,Bob Smith,15,16,14,72
S003,Charlie Brown,20,19,18,90"""
        
        if self.manager.load_from_text(sample_data):
            self.update_status("Sample data loaded")
            self.display_output("Sample data loaded successfully.\nClick 'View All Student Records' to see results.")

    def auto_load_student_marks(self):
        """Automatically load studentMarks.txt from the same folder."""
        filename = "studentMarks.txt"

        if os.path.exists(filename):
            if self.manager.load_from_file(filename):
                self.update_status(f"Loaded {len(self.manager.students)} students from {filename}")
                self.display_output(
                    f"Successfully loaded {len(self.manager.students)} students from {filename}.\n\n"
                    "Click 'View All Student Records' to see results."
                )
            else:
                self.update_status("Failed to load studentMarks.txt")
                messagebox.showerror("Error", "studentMarks.txt found but could not be loaded.")
        else:
            self.update_status("studentMarks.txt not found")
            messagebox.showwarning(
                "File Not Found",
                "studentMarks.txt was not found in this folder.\n"
                "Please place it beside the .py file."
            )

    def load_data_dialog(self):
        """Open a file dialog to load a student marks file."""
        filename = filedialog.askopenfilename(
            title="Select studentMarks.txt file",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if filename:
            if self.manager.load_from_file(filename):
                self.update_status(f"Loaded data from {filename}")
                self.display_output(
                    f"Successfully loaded {len(self.manager.students)} student records."
                )
            else:
                messagebox.showerror("Error", "Failed to load the selected file.")

    def view_all_records(self):
        """Display all student records"""
        output = self.manager.get_all_records()
        self.display_output(output)
        self.update_status(f"Displaying {len(self.manager.students)} student records")

    def view_individual_record(self):
        """Display individual student record"""
        if not self.manager.students:
            messagebox.showwarning("No Data", "Please load student data first.")
            return
        
        # Create dialog for student selection
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Student")
        dialog.geometry("400x150")
        
        tk.Label(dialog, text="Enter Student Code or Name:", font=("Arial", 11)).pack(pady=10)
        
        entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        entry.pack(pady=5)
        entry.focus()
        
        def search_student():
            search_term = entry.get().strip()
            if not search_term:
                messagebox.showwarning("Input Required", "Please enter a student code or name.")
                return
            
            # Try searching by code first
            student = self.manager.get_student_by_code(search_term)
            
            # If not found, try by name
            if not student:
                student = self.manager.get_student_by_name(search_term)
            
            if student:
                self.display_output(student.format_record())
                self.update_status(f"Displaying record for {student.name}")
                dialog.destroy()
            else:
                messagebox.showerror("Not Found", f"No student found with code or name: {search_term}")
        
        tk.Button(dialog, text="Search", command=search_student, 
                 bg="#2196F3", fg="white", font=("Arial", 11), padx=20, pady=5).pack(pady=10)
        
        entry.bind('<Return>', lambda e: search_student())

    def show_highest_student(self):
        """Display highest scoring student"""
        student = self.manager.get_highest_scoring_student()
        if student:
            output = "=" * 50 + "\n"
            output += "HIGHEST SCORING STUDENT\n"
            output += "=" * 50 + "\n\n"
            output += student.format_record()
            self.display_output(output)
            self.update_status(f"Highest score: {student.name} ({student.overall_percentage:.2f}%)")
        else:
            messagebox.showwarning("No Data", "Please load student data first.")

    def show_lowest_student(self):
        """Display lowest scoring student"""
        student = self.manager.get_lowest_scoring_student()
        if student:
            output = "=" * 50 + "\n"
            output += "LOWEST SCORING STUDENT\n"
            output += "=" * 50 + "\n\n"
            output += student.format_record()
            self.display_output(output)
            self.update_status(f"Lowest score: {student.name} ({student.overall_percentage:.2f}%)")
        else:
            messagebox.showwarning("No Data", "Please load student data first.")

    def display_output(self, text: str):
        """Display text in output area"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, text)

    def update_status(self, message: str):
        """Update status bar"""
        self.status_label.config(text=message)


def main():
    root = tk.Tk()
    app = StudentManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()