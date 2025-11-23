import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
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
        """Create main widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text="Student Manager System", 
                              font=("Arial", 20, "bold"), bg="#2c3e50", fg="white")
        title_label.pack()
        
        # Button frame
        button_frame = tk.Frame(self.root, pady=20)
        button_frame.pack(fill=tk.X)
        
        btn_style = {"font": ("Arial", 11), "width": 25, "height": 2}
        
        btn1 = tk.Button(button_frame, text="1. View All Student Records", 
                        command=self.view_all_records, bg="#3498db", fg="white", **btn_style)
        btn1.pack(pady=5)
        
        btn2 = tk.Button(button_frame, text="2. View Individual Student Record", 
                        command=self.view_individual_record, bg="#2ecc71", fg="white", **btn_style)
        btn2.pack(pady=5)
        
        btn3 = tk.Button(button_frame, text="3. Show Highest Scoring Student", 
                        command=self.show_highest_student, bg="#e74c3c", fg="white", **btn_style)
        btn3.pack(pady=5)
        
        btn4 = tk.Button(button_frame, text="4. Show Lowest Scoring Student", 
                        command=self.show_lowest_student, bg="#f39c12", fg="white", **btn_style)
        btn4.pack(pady=5)
        
        # Output frame
        output_frame = tk.LabelFrame(self.root, text="Output", font=("Arial", 12, "bold"), pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, font=("Courier", 10), 
                                                     wrap=tk.WORD, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        sample_data = """5
8439,Jake Hobbs,10,11,10,43
7234,Sarah Johnson,18,17,19,89
6521,Michael Brown,12,14,13,67
9876,Emma Wilson,15,16,14,78
5432,Oliver Davis,8,9,7,38"""
        
        if self.manager.load_from_text(sample_data):
            self.update_status(f"Sample data loaded: {len(self.manager.students)} students")
            self.display_output("Sample data loaded successfully!\n\n" + 
                              "Click 'View All Student Records' to see the data.")
        else:
            self.update_status("Failed to load sample data")
    
    def load_data_dialog(self):
        """Open dialog to load data from file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Select Student Data File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            if self.manager.load_from_file(filename):
                self.update_status(f"Loaded {len(self.manager.students)} students from {filename}")
                messagebox.showinfo("Success", f"Successfully loaded {len(self.manager.students)} students!")
            else:
                messagebox.showerror("Error", "Failed to load data from file")
    
    def view_all_records(self):
        """Display all student records"""
        if not self.manager.students:
            messagebox.showwarning("No Data", "No student data loaded!")
            return
        
        output = self.manager.get_all_records()
        self.display_output(output)
        self.update_status(f"Displaying {len(self.manager.students)} student records")
    
    def view_individual_record(self):
        """Display dialog to select and view individual student"""
        if not self.manager.students:
            messagebox.showwarning("No Data", "No student data loaded!")
            return
        
        # Create selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Student")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select a student:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Listbox with student names
        frame = tk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for student in self.manager.students:
            listbox.insert(tk.END, f"{student.name} ({student.code})")
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                student = self.manager.students[idx]
                self.display_output(student.format_record())
                self.update_status(f"Displaying record for {student.name}")
                dialog.destroy()
        
        tk.Button(dialog, text="View Record", command=on_select, 
                 bg="#3498db", fg="white", font=("Arial", 11), width=15).pack(pady=10)
    
    def show_highest_student(self):
        """Display student with highest score"""
        if not self.manager.students:
            messagebox.showwarning("No Data", "No student data loaded!")
            return
        
        student = self.manager.get_highest_scoring_student()
        if student:
            output = "=" * 50 + "\n"
            output += "HIGHEST SCORING STUDENT\n"
            output += "=" * 50 + "\n\n"
            output += student.format_record()
            self.display_output(output)
            self.update_status(f"Highest: {student.name} - {student.overall_percentage:.2f}%")
    
    def show_lowest_student(self):
        """Display student with lowest score"""
        if not self.manager.students:
            messagebox.showwarning("No Data", "No student data loaded!")
            return
        
        student = self.manager.get_lowest_scoring_student()
        if student:
            output = "=" * 50 + "\n"
            output += "LOWEST SCORING STUDENT\n"
            output += "=" * 50 + "\n\n"
            output += student.format_record()
            self.display_output(output)
            self.update_status(f"Lowest: {student.name} - {student.overall_percentage:.2f}%")
    
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