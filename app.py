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

        self.scroll_accumulator = 0.0

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
        self.nf_btn.pack(fill="x", pady=(10, 0), padx=(20, 20))
        self.nf_box = ctk.CTkTextbox(self.scroll_frame, height=200)
        self._bind_scroll_lock(self.nf_box)

        # Fans
        self.fans_btn = ctk.CTkButton(self.scroll_frame, text="▶ Fans", 
                                      command=lambda: self.toggle_section(self.fans_box, self.fans_btn))
        self.fans_btn.pack(fill="x", pady=(10, 0), padx=(20, 20))
        self.fans_box = ctk.CTkTextbox(self.scroll_frame, height=200)
        self._bind_scroll_lock(self.fans_box)

        # Mutually Following
        self.mut_btn = ctk.CTkButton(self.scroll_frame, text="▶ Mutually Following", 
                                     command=lambda: self.toggle_section(self.mut_box, self.mut_btn))
        self.mut_btn.pack(fill="x", pady=(10, 0), padx=(20, 20))
        self.mut_box = ctk.CTkTextbox(self.scroll_frame, height=200)
        self._bind_scroll_lock(self.mut_box)

    # --- SCROLL LOGIC ---

    def _bind_scroll_lock(self, widget):
        widget.bind("<Enter>", lambda e: self._set_scroll_target(widget))
        widget.bind("<Leave>", lambda e: self._set_scroll_target(None))

    def _set_scroll_target(self, widget):
        self.active_textbox = widget
        # If widget is None, we are in the main area (True)
        # If widget is a textbox, we are NOT in the main area (False)
        self.allow_main_scroll = (widget is None)

    def _check_scroll_condition(self, event):
        # 1. Calculate the precise movement and add to bank
        raw_delta = -1 * (event.delta / 120)
        self.scroll_accumulator += raw_delta
        
        # 2. Only move if we have accumulated at least one full unit
        if abs(self.scroll_accumulator) >= 1:
            move_units = int(self.scroll_accumulator)
            self.scroll_accumulator -= move_units  # Keep the remainder
            
            # --- TEXTBOX SCROLLING (Speed 1) ---
            if not self.allow_main_scroll and hasattr(self, 'active_textbox'):
                top, bottom = self.active_textbox.yview()
                
                # Check if the textbox has room to move
                at_top = top <= 0.01
                at_bottom = bottom >= 0.99
                can_scroll_up = (event.delta > 0 and not at_top)
                can_scroll_down = (event.delta < 0 and not at_bottom)
                
                if can_scroll_up or can_scroll_down:
                    self.active_textbox.yview_scroll(move_units, "units")
                    return # Locked in the textbox, don't execute main scroll

            # --- MAIN WINDOW SCROLLING (Speed 3) ---
            main_top, main_bottom = self.scroll_frame._parent_canvas.yview()
            
            # Stop if hitting the top or bottom of the main app
            if event.delta > 0 and main_top <= 0:
                self.scroll_accumulator = 0
                return
            if event.delta < 0 and main_bottom >= 1.0:
                self.scroll_accumulator = 0
                return

            # Apply the faster speed (using 3 or whatever feels right)
            self.scroll_frame._parent_canvas.yview_scroll(move_units * 20, "units")
        
    # --- UI METHODS ---

    def toggle_section(self, section, button):
        if section.winfo_viewable():
            section.pack_forget()
            button.configure(text=button.cget("text").replace("▼", "▶"))
        else:
            section.pack(fill="x", padx=10, after=button)
            button.configure(text=button.cget("text").replace("▶", "▼"))

        self.update_scroll_region()

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

        self.update_scroll_region()

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

    def update_scroll_region(self):
        """Force the scrollable frame to re-calculate its internal height."""
        self.update_idletasks() # Let the UI finish rendering everything first
        self.scroll_frame._parent_canvas.configure(
            scrollregion=self.scroll_frame._parent_canvas.bbox("all")
        )

if __name__ == "__main__":
    app = IGApp()
    app.mainloop()