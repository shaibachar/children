import tkinter as tk
from tkinter import filedialog, messagebox
import json
import random
import os
from PIL import Image, ImageTk

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("600x700")  # Set a fixed window size

        self.flashcards = []
        self.current_card = None
        self.username = None
        self.scores = {}
        self.load_scores()
        self.create_username_prompt()

    def create_username_prompt(self):
        self.username_frame = tk.Frame(self.root)
        self.username_frame.pack(expand=True)

        tk.Label(self.username_frame, text="Enter your username:", font=("Arial", 14)).pack(pady=10)
        self.username_entry = tk.Entry(self.username_frame, font=("Arial", 14))
        self.username_entry.pack(pady=10)
        self.username_entry.bind("<Return>", self.set_username)

        tk.Button(self.username_frame, text="Start", font=("Arial", 14), command=self.set_username).pack(pady=10)

    def set_username(self, event=None):
        self.username = self.username_entry.get().strip()
        if not self.username:
            self.username = "Guest"
        
        self.root.title(f"Flashcard App - {self.username}")

        if self.username not in self.scores:
            self.scores[self.username] = 0

        self.username_frame.destroy()
        self.create_widgets()
        self.load_default_flashcards()

    def create_widgets(self):
        # Header frame for the load button
        header_frame = tk.Frame(self.root)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.load_button = tk.Button(header_frame, text="Load Cards", command=self.load_flashcards)
        self.load_button.pack(pady=10)

        # Main frame for the question and options
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True)

        self.image_label = tk.Label(self.main_frame)
        self.image_label.pack(pady=10)

        self.question_label = tk.Label(self.main_frame, text="", font=("Arial", 24), wraplength=500, justify="center")
        self.question_label.pack(pady=10)

        self.option_buttons = []
        for i in range(3):
            button = tk.Button(self.main_frame, text="", font=("Arial", 18))
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.feedback_label = tk.Label(self.main_frame, text="", font=("Arial", 20), wraplength=500, justify="center")
        self.feedback_label.pack(pady=10)

        # Footer frame for the next button
        footer_frame = tk.Frame(self.root)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.next_card_button = tk.Button(footer_frame, text="Next Card", command=self.show_random_flashcard)
        self.next_card_button.pack(pady=10)

        self.score_label = tk.Label(footer_frame, text=f"Score: {self.scores.get(self.username, 0)}", font=("Arial", 14))
        self.score_label.pack(pady=10)

    def load_default_flashcards(self):
        default_path = os.path.join(os.path.dirname(__file__), "flashcards.json")
        if os.path.exists(default_path):
            try:
                with open(default_path, "r") as file:
                    self.flashcards = json.load(file)
                self.show_random_flashcard()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load default flashcards: {e}")
        else:
            messagebox.showwarning("Warning", "Default flashcards.json not found!")

    def load_flashcards(self):
        file_path = filedialog.askopenfilename(title="Open Flashcards JSON", filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.flashcards = json.load(file)
                messagebox.showinfo("Success", "Flashcards loaded successfully!")
                self.show_random_flashcard()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load flashcards: {e}")

    def show_random_flashcard(self):
        if not self.flashcards:
            self.question_label.config(text="No flashcards loaded.")
            self.image_label.config(image='')
            for button in self.option_buttons:
                button.config(text="", command=None)
            return

        self.current_card = random.choice(self.flashcards)
        self.question_label.config(text=self.current_card["question"])
        self.feedback_label.config(text="")

        if "image" in self.current_card:
            image_path = self.current_card["image"]
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((300, 200), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=self.photo)
            else:
                self.image_label.config(image='')
        else:
            self.image_label.config(image='')

        random.shuffle(self.current_card["options"])
        for button, option in zip(self.option_buttons, self.current_card["options"]):
            button.config(text=option, command=lambda opt=option: self.check_answer(opt))

    def check_answer(self, selected_answer):
        if selected_answer == self.current_card["correct_answer"]:
            self.feedback_label.config(text="Correct!", fg="green")
            self.scores[self.username] += 1
        else:
            self.feedback_label.config(text=f"Wrong! The correct answer is: {self.current_card['correct_answer']}", fg="red")
            self.scores[self.username] = max(0, self.scores[self.username] - 1)
        
        self.score_label.config(text=f"Score: {self.scores[self.username]}")
        self.save_scores()

    def load_scores(self):
        scores_path = os.path.join(os.path.dirname(__file__), "scores.json")
        if os.path.exists(scores_path):
            try:
                with open(scores_path, "r") as file:
                    self.scores = json.load(file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load scores: {e}")

    def save_scores(self):
        scores_path = os.path.join(os.path.dirname(__file__), "scores.json")
        try:
            with open(scores_path, "w") as file:
                json.dump(self.scores, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save scores: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
