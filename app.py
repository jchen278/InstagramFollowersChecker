import customtkinter as ctk
from tkinter import filedialog
from logic import analyze_relationships

class IGApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IG Relationship Auditor")
        self.geometry("600x500")
        
        # UI Setup
        self.label = ctk.CTkLabel(self, text="Instagram Auditor", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        self.btn = ctk.CTkButton(self, text="Select Data Folder", command=self.select_folder)
        self.btn.pack(pady=10)

        self.result_box = ctk.CTkTextbox(self, width=500, height=300)
        self.result_box.pack(pady=20)

    def select_folder(self):
        data_dir = filedialog.askdirectory(title="Select Instagram Data Folder")
        if data_dir:
            self.run_audit(data_dir)

    def run_audit(self, folder):
        self.result_box.delete("0.0", "end") # Clear previous results
        
        # Call our logic
        data = analyze_relationships(folder)
        
        # Display results
        self.result_box.insert("end", f"Following: {data['counts']['following']}\n")
        self.result_box.insert("end", f"Followers: {data['counts']['followers']}\n")
        self.result_box.insert("end", "-"*30 + "\n")
        self.result_box.insert("end", "NOT FOLLOWING YOU BACK:\n")
        
        for user in data["not_following_back"]:
            self.result_box.insert("end", f" - {user}\n")