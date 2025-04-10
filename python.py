import tkinter as tk
from tkinter import messagebox
import os

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gradient Notes App")
        self.root.geometry("600x500")
        self.notes_dir = "notes"
        os.makedirs(self.notes_dir, exist_ok=True)

        self.current_note_file = None
        self.canvas = tk.Canvas(self.root, width=600, height=500)
        self.canvas.pack(fill="both", expand=True)

        self.show_notes_page()

    def draw_gradient(self):
        self.canvas.delete("all")
        for i in range(0, 500):
            color = f"#%02x%02x%02x" % (0, int(120 + i * 0.25), 255)
            self.canvas.create_line(0, i, 600, i, fill=color)

    def show_notes_page(self):
        self.current_note_file = None
        self.draw_gradient()

        new_note_btn = tk.Button(
            self.root, text="New Note", font=("Helvetica", 14, "bold"),
            fg="white", bg="#0066cc", activebackground="#005bb5",
            command=self.show_note_editor
        )
        self.canvas.create_window(300, 25, window=new_note_btn)

        y_pos = 70
        for filename in os.listdir(self.notes_dir):
            if filename.endswith(".txt"):
                path = os.path.join(self.notes_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                preview = f"{content[:300]}..."

                note_frame = tk.Frame(self.canvas, bg="#003366", bd=2, relief="groove")

                # Top bar with filename and Edit button
                top_line = tk.Frame(note_frame, bg="#003366")
                top_line.pack(fill="x")

                title_label = tk.Label(
                    top_line, text=filename, font=("Helvetica", 10, "bold"),
                    bg="#003366", fg="white", anchor="w"
                )
                title_label.pack(side="left", padx=10)

                btn_column = tk.Frame(note_frame, bg="#003366")
                btn_column.pack(side="right", anchor="ne", padx=10)

                edit_btn = tk.Button(
                    btn_column, text="Edit", font=("Helvetica", 10, "bold"),
                    bg="#ffaa00", fg="black",
                    command=lambda f=filename: self.edit_note(f)
                )
                edit_btn.pack(pady=(5, 2))

                delete_btn = tk.Button(
                    btn_column, text="Delete", font=("Helvetica", 10, "bold"),
                    bg="#ff4444", fg="white",
                    command=lambda f=filename: self.delete_note(f)
                )
                delete_btn.pack(pady=(2, 5))

                note_label = tk.Label(
                    note_frame, text=preview,
                    bg="#003366", fg="white",
                    wraplength=470, justify="left", anchor="nw",
                    font=("Helvetica", 12, "bold"), padx=10, pady=10
                )
                note_label.pack(side="left", fill="both", expand=True, anchor="nw")

                self.canvas.create_window(30, y_pos, window=note_frame, anchor="nw", width=540)
                y_pos += 150

    def show_note_editor(self):
        self.draw_gradient()

        self.text_area = tk.Text(
            self.canvas, wrap="word", height=20, width=60,
            bg="#002b55", fg="white", insertbackground="white",
            font=("Helvetica", 12)
        )
        self.canvas.create_window(300, 220, window=self.text_area)

        save_btn = tk.Button(
            self.root, text="Save Note", font=("Helvetica", 12, "bold"),
            fg="white", bg="#009900", activebackground="#007700",
            command=self.save_note
        )
        self.canvas.create_window(300, 450, window=save_btn)

        back_btn = tk.Button(
            self.root, text="← Back", font=("Helvetica", 10, "bold"),
            fg="white", bg="#cc0000", activebackground="#aa0000",
            command=self.show_notes_page
        )
        self.canvas.create_window(100, 25, window=back_btn)

    def save_note(self):
        content = self.text_area.get("1.0", tk.END).strip()

        if not content:
            messagebox.showwarning("Warning", "Note content is empty!")
            return

        if self.current_note_file:  # Editing existing
            path = os.path.join(self.notes_dir, self.current_note_file)
        else:  # New note
            note_id = len([f for f in os.listdir(self.notes_dir) if f.endswith(".txt")]) + 1
            path = os.path.join(self.notes_dir, f"Note_{note_id}.txt")

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        self.show_notes_page()

    def edit_note(self, filename):
        self.current_note_file = filename
        self.draw_gradient()

        with open(os.path.join(self.notes_dir, filename), "r", encoding="utf-8") as f:
            content = f.read()

        self.text_area = tk.Text(
            self.canvas, wrap="word", height=20, width=60,
            bg="#002b55", fg="white", insertbackground="white",
            font=("Helvetica", 12)
        )
        self.text_area.insert("1.0", content)
        self.canvas.create_window(300, 220, window=self.text_area)

        save_btn = tk.Button(
            self.root, text="Save Changes", font=("Helvetica", 12, "bold"),
            fg="white", bg="#009900", activebackground="#007700",
            command=self.save_note
        )
        self.canvas.create_window(300, 450, window=save_btn)

        back_btn = tk.Button(
            self.root, text="← Back", font=("Helvetica", 10, "bold"),
            fg="white", bg="#cc0000", activebackground="#aa0000",
            command=self.show_notes_page
        )
        self.canvas.create_window(100, 25, window=back_btn)

    def delete_note(self, filename):
        confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete '{filename}'?")
        if confirm:
            os.remove(os.path.join(self.notes_dir, filename))
            self.show_notes_page()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()