import tkinter as tk
from tkinter import messagebox
import random

class MathsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("400x350")
        self.root.config(bg="#D4E4F7")
        
        # Quiz variables
        self.difficulty = None
        self.score = 0
        self.question_count = 0
        self.max_questions = 10
        self.current_num1 = 0
        self.current_num2 = 0
        self.current_operation = ""
        self.correct_answer = 0
        self.attempts = 0
        
        # Show difficulty menu
        self.displayMenu()
    
    def displayMenu(self):
        """Display the difficulty level menu"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Reset quiz variables
        self.score = 0
        self.question_count = 0
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="MATHS QUIZ", 
            font=("Arial", 24, "bold"),
            bg="#D4E4F7",
            fg="#6BA5D6"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root, 
            text="Select Difficulty Level", 
            font=("Arial", 14),
            bg="#D4E4F7",
            fg="#6BA5D6"
        )
        subtitle_label.pack(pady=10)
        
        # Difficulty buttons
        easy_btn = tk.Button(
            self.root,
            text="1. Easy (Single Digits)",
            command=lambda: self.startQuiz(1),
            width=25,
            height=2,
            bg="#9BC4E2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3
        )
        easy_btn.pack(pady=5)
        
        moderate_btn = tk.Button(
            self.root,
            text="2. Moderate (Double Digits)",
            command=lambda: self.startQuiz(2),
            width=25,
            height=2,
            bg="#F8B3D0",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3
        )
        moderate_btn.pack(pady=5)
        
        advanced_btn = tk.Button(
            self.root,
            text="3. Advanced (4 Digits)",
            command=lambda: self.startQuiz(3),
            width=25,
            height=2,
            bg="#C9A0DC",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3
        )
        advanced_btn.pack(pady=5)
    
    def startQuiz(self, difficulty):
        """Start the quiz with selected difficulty"""
        self.difficulty = difficulty
        self.displayProblem()
    
    def randomInt(self):
        """Generate random integers based on difficulty level"""
        if self.difficulty == 1:  # Easy: single digit (0-9)
            return random.randint(0, 9), random.randint(0, 9)
        elif self.difficulty == 2:  # Moderate: double digit (10-99)
            return random.randint(10, 99), random.randint(10, 99)
        elif self.difficulty == 3:  # Advanced: 4 digits (1000-9999)
            return random.randint(1000, 9999), random.randint(1000, 9999)
    
    def decideOperation(self):
        """Randomly decide between addition or subtraction"""
        return random.choice(['+', '-'])
    
    def displayProblem(self):
        """Display a math problem to the user"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Check if quiz is complete
        if self.question_count >= self.max_questions:
            self.displayResults()
            return
        
        # Generate new problem
        self.question_count += 1
        self.attempts = 0
        self.current_num1, self.current_num2 = self.randomInt()
        self.current_operation = self.decideOperation()
        
        # Calculate correct answer
        if self.current_operation == '+':
            self.correct_answer = self.current_num1 + self.current_num2
        else:
            self.correct_answer = self.current_num1 - self.current_num2
        
        # Display question number and score
        info_label = tk.Label(
            self.root,
            text=f"Question {self.question_count}/10 | Score: {self.score}",
            font=("Arial", 12),
            bg="#D4E4F7",
            fg="#6BA5D6"
        )
        info_label.pack(pady=10)
        
        # Display the problem
        problem_label = tk.Label(
            self.root,
            text=f"{self.current_num1} {self.current_operation} {self.current_num2} = ?",
            font=("Arial", 28, "bold"),
            bg="#D4E4F7",
            fg="#6BA5D6"
        )
        problem_label.pack(pady=30)
        
        # Answer entry
        answer_label = tk.Label(
            self.root,
            text="Your Answer:",
            font=("Arial", 14),
            bg="#D4E4F7",
            fg="#6BA5D6"
        )
        answer_label.pack(pady=5)
        
        self.answer_entry = tk.Entry(
            self.root,
            font=("Arial", 16),
            width=15,
            justify="center"
        )
        self.answer_entry.pack(pady=5)
        self.answer_entry.focus()
        
        # Feedback label (for wrong answers)
        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            bg="#D4E4F7",
            fg="#E74C3C"
        )
        self.feedback_label.pack(pady=5)
        
        # Submit button
        submit_btn = tk.Button(
            self.root,
            text="Submit Answer",
            command=self.isCorrect,
            width=20,
            height=2,
            bg="#9BC4E2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3
        )
        submit_btn.pack(pady=20)
        
        # Bind Enter key to submit
        self.answer_entry.bind("<Return>", lambda event: self.isCorrect())
    
    def isCorrect(self):
        """Check if the user's answer is correct"""
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            self.feedback_label.config(text="Please enter a valid number!")
            return
        
        if user_answer == self.correct_answer:
            # Correct answer
            if self.attempts == 0:
                self.score += 10  # First attempt
                messagebox.showinfo("Correct!", "Well done! +10 points")
            else:
                self.score += 5  # Second attempt
                messagebox.showinfo("Correct!", "Good job! +5 points")
            
            # Move to next question
            self.displayProblem()
        else:
            # Wrong answer
            self.attempts += 1
            if self.attempts < 2:
                # Give second chance
                self.feedback_label.config(text="Incorrect! Try again (one more chance)")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
            else:
                # No more chances
                messagebox.showinfo(
                    "Incorrect", 
                    f"Sorry! The correct answer was {self.correct_answer}"
                )
                self.displayProblem()
    
    def displayResults(self):
        """Display the final results"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Calculate grade
        percentage = self.score
        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        else:
            grade = "F"
        
        # Results title
        title_label = tk.Label(
            self.root,
            text="Quiz Complete!",
            font=("Arial", 24, "bold"),
            bg="#D4E4F7",
            fg="#6BA5D6"
        )
        title_label.pack(pady=20)
        
        # Score display
        score_label = tk.Label(
            self.root,
            text=f"Your Score: {self.score}/100",
            font=("Arial", 20),
            bg="#D4E4F7",
            fg="#6BA5D6"
        )
        score_label.pack(pady=10)
        
        # Grade display
        grade_label = tk.Label(
            self.root,
            text=f"Grade: {grade}",
            font=("Arial", 18, "bold"),
            bg="#D4E4F7",
            fg="#F8B3D0"
        )
        grade_label.pack(pady=10)
        
        # Play again button
        again_btn = tk.Button(
            self.root,
            text="Play Again",
            command=self.displayMenu,
            width=20,
            height=2,
            bg="#9BC4E2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3
        )
        again_btn.pack(pady=10)
        
        # Quit button
        quit_btn = tk.Button(
            self.root,
            text="Quit",
            command=self.root.quit,
            width=20,
            height=2,
            bg="#F8B3D0",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3
        )
        quit_btn.pack(pady=5)

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuiz(root)
    root.mainloop()