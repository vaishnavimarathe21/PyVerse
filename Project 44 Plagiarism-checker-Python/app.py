import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def vectorize(Text):
    return TfidfVectorizer().fit_transform(Text).toarray()

def check_plagiarism(student_files, student_notes):
    vectors = vectorize(student_notes)
    s_vectors = list(zip(student_files, vectors))

    results = []
    for i in range(len(s_vectors)):
        for j in range(i+1, len(s_vectors)):
            student_a, text_vector_a = s_vectors[i]
            student_b, text_vector_b = s_vectors[j]
            sim_score = cosine_similarity([text_vector_a], [text_vector_b])[0][0]
            results.append((student_a, student_b, sim_score))
    return results

class PlagiarismCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plagiarism Checker")
        self.geometry("700x400")

        # Buttons
        self.load_btn = tk.Button(self, text="Load Folder", command=self.load_folder)
        self.load_btn.pack(pady=10)

        self.check_btn = tk.Button(self, text="Check Plagiarism", command=self.run_check, state=tk.DISABLED)
        self.check_btn.pack(pady=5)

        # Treeview for results
        self.tree = ttk.Treeview(self, columns=("File A", "File B", "Similarity"), show="headings")
        self.tree.heading("File A", text="File A")
        self.tree.heading("File B", text="File B")
        self.tree.heading("Similarity", text="Similarity (%)")
        self.tree.column("File A", width=200)
        self.tree.column("File B", width=200)
        self.tree.column("Similarity", width=100, anchor="center")
        self.tree.pack(expand=True, fill="both", pady=10)

        self.student_files = []
        self.student_notes = []

    def load_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.student_files = [os.path.join(folder, doc) for doc in os.listdir(folder) if doc.endswith(".txt")]
        if not self.student_files:
            messagebox.showerror("Error", "No .txt files found in folder!")
            return
        self.student_notes = [open(_file, encoding="utf-8").read() for _file in self.student_files]
        messagebox.showinfo("Success", f"Loaded {len(self.student_files)} text files.")
        self.check_btn.config(state=tk.NORMAL)

    def run_check(self):
        if not self.student_files:
            messagebox.showerror("Error", "Load files first!")
            return
        results = check_plagiarism(self.student_files, self.student_notes)

        # Clear old results
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new results
        for file_a, file_b, score in results:
            self.tree.insert("", tk.END, values=(os.path.basename(file_a),
                                                 os.path.basename(file_b),
                                                 f"{score*100:.2f}%"))

if __name__ == "__main__":
    app = PlagiarismCheckerApp()
    app.mainloop()
