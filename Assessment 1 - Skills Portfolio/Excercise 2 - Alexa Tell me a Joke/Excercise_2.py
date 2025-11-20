"""
Simple Joke Assistant - Exercise 2
Reads jokes from randomJokes.txt and displays them with setup/punchline buttons.
"""

import tkinter as tk
from tkinter import messagebox
import random
from pathlib import Path

class JokeAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke Assistant")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        
        # Load jokes from file
        self.jokes = []
        self.load_jokes()
        
        # Current joke
        self.current_joke = None
        
        # Create UI
        self.create_widgets()
    
    def load_jokes(self):
        """Load jokes from randomJokes.txt file."""
        try:
            # Get the directory where the script is located
            script_dir = Path(__file__).parent
            file_path = script_dir / "randomJokes.txt"
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if '?' in line:
                        # Split on first question mark
                        parts = line.split('?', 1)
                        setup = parts[0].strip() + '?'
                        punchline = parts[1].strip()
                        
                        if setup and punchline:
                            self.jokes.append({
                                'setup': setup,
                                'punchline': punchline
                            })
            
            if not self.jokes:
                raise ValueError("No valid jokes found in file")
                
        except FileNotFoundError:
            messagebox.showerror("Error", "randomJokes.txt file not found!\n\nPlease create it in the same folder as this script.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading jokes: {str(e)}")
            self.root.destroy()
    
    def create_widgets(self):
        """Create all UI elements."""
        
        # Title Label
        title_label = tk.Label(
            self.root,
            text="Joke Assistant",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)
        
        # Setup Display
        self.setup_label = tk.Label(
            self.root,
            text="Click 'Alexa tell me a Joke' to start!",
            font=("Arial", 14),
            bg="#ffffff",
            fg="#000000",
            wraplength=500,
            justify=tk.CENTER,
            relief=tk.RIDGE,
            borderwidth=2,
            padx=20,
            pady=30
        )
        self.setup_label.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Punchline Display (initially hidden)
        self.punchline_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
            bg="#ffffcc",
            fg="#cc0000",
            wraplength=500,
            justify=tk.CENTER,
            relief=tk.RIDGE,
            borderwidth=2,
            padx=20,
            pady=20
        )
        # Don't pack it yet - it will appear when showing punchline
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Alexa tell me a Joke button
        self.alexa_btn = tk.Button(
            button_frame,
            text="Alexa tell me a Joke",
            command=self.tell_joke,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2"
        )
        self.alexa_btn.grid(row=0, column=0, padx=5)
        
        # Show Punchline button
        self.punchline_btn = tk.Button(
            button_frame,
            text="Show Punchline",
            command=self.show_punchline,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.punchline_btn.grid(row=0, column=1, padx=5)
        
        # Next Joke button
        self.next_btn = tk.Button(
            button_frame,
            text="Next Joke",
            command=self.next_joke,
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.next_btn.grid(row=0, column=2, padx=5)
        
        # Quit button
        quit_btn = tk.Button(
            button_frame,
            text="Quit",
            command=self.quit_app,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2"
        )
        quit_btn.grid(row=0, column=3, padx=5)
    
    def tell_joke(self):
        """Display a random joke setup."""
        # Get random joke
        self.current_joke = random.choice(self.jokes)
        
        # Hide punchline if it was showing
        self.punchline_label.pack_forget()
        
        # Display setup
        self.setup_label.config(text=self.current_joke['setup'])
        
        # Update button states
        self.alexa_btn.config(state=tk.DISABLED)
        self.punchline_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.DISABLED)
    
    def show_punchline(self):
        """Display the punchline below the setup."""
        if self.current_joke:
            # Show punchline
            self.punchline_label.config(text=self.current_joke['punchline'])
            self.punchline_label.pack(pady=10, padx=20, fill=tk.X)
            
            # Update button states
            self.punchline_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.NORMAL)
            self.alexa_btn.config(state=tk.NORMAL)
    
    def next_joke(self):
        """Request another random joke."""
        self.tell_joke()
    
    def quit_app(self):
        """Close the application."""
        self.root.quit()


def main():
    root = tk.Tk()
    app = JokeAssistant(root)
    root.mainloop()


if __name__ == "__main__":
    main()