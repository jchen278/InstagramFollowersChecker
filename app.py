import customtkinter as ctk
from tkinter import filedialog
from logic import analyze_relationships

class IGApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IG Follower Stats")
        self.geometry("600x800")

        self.allow_main_scroll = True

        # Main Scrollable Container
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=550, height=750)
        self.scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Universal bind for the mouse wheel
        self.bind_all("<MouseWheel>", self._check_scroll_condition)

        self.label = ctk.CTkLabel(self.scroll_frame, text="Instagram Follower Stats", font=("Arial", 24, "bold"))
        self.label.pack(pady=10)

        # Touch screen functionality
        self.canvas = self.scroll_frame._parent_canvas
        self.canvas.bind("<Button-1>", self._on_touch_start)
        self.canvas.bind("<B1-Motion>", self._on_touch_drag)

        # Main Action Button
        self.select_btn = ctk.CTkButton(self.scroll_frame, text="Select Data Folder", command=self.select_folder)
        self.select_btn.pack(pady=10)

        # Summary Label
        self.summary_label = ctk.CTkLabel(self.scroll_frame, text="Select a folder to begin", font=("Arial", 14))
        self.summary_label.pack(pady=10)

        # --- SEARCH BAR ---
        self.search_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.search_frame.pack(pady=10)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_results)

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search names...", 
                                         textvariable=self.search_var, width=350)
        self.search_entry.pack(side="left", padx=(0, 10))

        self.clear_btn = ctk.CTkButton(self.search_frame, text="X", width=30, 
                                       fg_color="gray30", hover_color="red",
                                       command=self.clear_search)
        self.clear_btn.pack(side="left")

        self.bind("<Control-f>", lambda event: self.search_entry.focus())

        # --- SECTIONS ---

        # Not Following Back
        self.nf_btn = ctk.CTkButton(self.scroll_frame, text="▶ Not Following Back", 
                                    command=lambda: self.toggle_section(self.nf_box, self.nf_btn))
        self.nf_btn.pack(fill="x", pady=(10, 0))
        self.nf_box = ctk.CTkTextbox(self.scroll_frame, height=200)
        self._bind_scroll_lock(self.nf_box)

        # Fans
        self.fans_btn = ctk.CTkButton(self.scroll_frame, text="▶ Fans", 
                                      command=lambda: self.toggle_section(self.fans_box, self.fans_btn))
        self.fans_btn.pack(fill="x", pady=(10, 0))
        self.fans_box = ctk.CTkTextbox(self.scroll_frame, height=200)
        self._bind_scroll_lock(self.fans_box)

        # Mutually Following
        self.mut_btn = ctk.CTkButton(self.scroll_frame, text="▶ Mutually Following", 
                                     command=lambda: self.toggle_section(self.mut_box, self.mut_btn))
        self.mut_btn.pack(fill="x", pady=(10, 0))
        self.mut_box = ctk.CTkTextbox(self.scroll_frame, height=200)
        self._bind_scroll_lock(self.mut_box)

    # --- SCROLL LOGIC ---

    def _bind_scroll_lock(self, widget):
        """Sets a flag to ignore main scroll when hovering over textboxes."""
        widget.bind("<Enter>", lambda e: self._set_main_scroll(False))
        widget.bind("<Leave>", lambda e: self._set_main_scroll(True))

    def _set_main_scroll(self, status):
        self.allow_main_scroll = status

    def _check_scroll_condition(self, event):
        """Only allows the main scroll frame to move if we aren't inside a textbox."""
        if self.allow_main_scroll:
            # Increase the multiplier (e.g., 3 or 5) to scroll faster
            scroll_speed = 3 
            
            # Use units for precise scrolling
            move_amount = int(-1 * (event.delta / 120) * scroll_speed)
            self.scroll_frame._parent_canvas.yview_scroll(move_amount, "units")

    # --- UI METHODS ---

    def toggle_section(self, section, button):
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
        box.delete("0.0", "end")
        if not user_list:
            box.insert("end", "No users found.")
        else:
            for user in user_list:
                box.insert("end", f"{user}\n")

    def run_audit(self, folder):
        data = analyze_relationships(folder)
        self.full_data = data 
        self.summary_label.configure(
            text=f"Following: {data['counts']['following']} | Followers: {data['counts']['followers']}"
        )
        self.filter_results()

    def filter_results(self, *args):
        search_term = self.search_var.get().lower()
        if not hasattr(self, 'full_data'):
            return

        categories = {
            "not_following_back": self.nf_box,
            "fans": self.fans_box,
            "mutuals": self.mut_box
        }

        for key, box in categories.items():
            filtered_list = [user for user in self.full_data[key] if search_term in user.lower()]
            self.update_box(box, filtered_list)

    def clear_search(self):
        self.search_var.set("")
        self.search_entry.focus()

    def _on_touch_start(self, event):
        """Records the initial touch position."""
        self.canvas.scan_mark(event.x, event.y)

    def _on_touch_drag(self, event):
        """Moves the canvas based on drag distance."""
        # This 'scan_dragto' is a built-in Tkinter method 
        # designed specifically for smooth 'flick' scrolling.
        self.canvas.scan_dragto(event.x, event.y, gain=1)

if __name__ == "__main__":
    app = IGApp()
    app.mainloop()