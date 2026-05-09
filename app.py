import customtkinter as ctk
from tkinter import filedialog
from logic import analyze_relationships

class IGApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IG Follower Stats")
        self.geometry("600x800")

        # Main Scrollable Container
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=550, height=750)
        self.scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.scroll_frame, text="Instagram Follower Stats", font=("Arial", 24, "bold"))
        self.label.pack(pady=10)

        # Main Action Button
        self.select_btn = ctk.CTkButton(self.scroll_frame, text="Select Data Folder", command=self.select_folder)
        self.select_btn.pack(pady=10)

        # Summary Label
        self.summary_label = ctk.CTkLabel(self.scroll_frame, text="Select a folder to begin", font=("Arial", 14))
        self.summary_label.pack(pady=10)

        # --- SECTIONS ---

        # Not Following Back
        self.nf_btn = ctk.CTkButton(self.scroll_frame, text="▶ Not Following Back", 
                                    command=lambda: self.toggle_section(self.nf_box, self.nf_btn))
        self.nf_btn.pack(fill="x", pady=(10, 0))
        self.nf_box = ctk.CTkTextbox(self.scroll_frame, height=200)
        # Commented to start in hidden position
        # self.nf_box.pack(fill="x", padx=10)

        # Fans
        self.fans_btn = ctk.CTkButton(self.scroll_frame, text="▶ Fans", 
                                      command=lambda: self.toggle_section(self.fans_box, self.fans_btn))
        self.fans_btn.pack(fill="x", pady=(10, 0))
        self.fans_box = ctk.CTkTextbox(self.scroll_frame, height=200)
        # Commented to start in hidden position
        # self.fans_box.pack(fill="x", padx=10)

        # Mutually Following
        self.mut_btn = ctk.CTkButton(self.scroll_frame, text="▶ Mutually Following", 
                                     command=lambda: self.toggle_section(self.mut_box, self.mut_btn))
        self.mut_btn.pack(fill="x", pady=(10, 0))
        self.mut_box = ctk.CTkTextbox(self.scroll_frame, height=200)
        # Commented to start in hidden position
        # self.mut_box.pack(fill="x", padx=10)

    def toggle_section(self, section, button):
        """Hides or shows a section and updates the arrow."""
        if section.winfo_viewable():
            section.pack_forget()
            button.configure(text=button.cget("text").replace("▼", "▶"))
        else:
            section.pack(fill="x", padx=10, after=button)
            button.configure(text=button.cget("text").replace("▶", "▼"))

    def select_folder(self):
        data_dir = filedialog.askdirectory(title="Select Instagram Data Folder")
        if data_dir:
            self.run_audit(data_dir)

    def update_box(self, box, user_list):
        """Helper to clear and fill a specific textbox."""
        box.delete("0.0", "end")
        if not user_list:
            box.insert("end", "No users found in this category.")
        else:
            for user in user_list:
                box.insert("end", f" {user}\n")

    def run_audit(self, folder):
        # Call logic
        data = analyze_relationships(folder)
        
        # Update Summary
        self.summary_label.configure(
            text=f"Following: {data['counts']['following']} | Followers: {data['counts']['followers']}"
        )
        
        # Update each specific box
        self.update_box(self.nf_box, data["not_following_back"])
        self.update_box(self.fans_box, data["fans"])
        self.update_box(self.mut_box, data["mutuals"])