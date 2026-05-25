import customtkinter as ctk
from tkinter import filedialog, messagebox

from logic import analyze_relationships
from ui.dpi import configure_dpi_awareness
from ui.results import create_result_sections, update_result_box
from ui.scrolling import ScrollManager


class IGApp(ctk.CTk):
    def __init__(self):
        configure_dpi_awareness()
        super().__init__()

        self.title("IG Follower Stats")
        self.geometry("600x600")

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=550, height=750)
        self.scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.scroll_manager = ScrollManager(self, self.scroll_frame)
        self._build_header()
        self._build_folder_picker()
        self._build_search_bar()
        self._build_result_sections()
        self.scroll_manager.bind_window()

    def _build_header(self):
        self.label = ctk.CTkLabel(
            self.scroll_frame,
            text="Instagram Follower Stats",
            font=("Arial", 24, "bold"),
        )
        self.label.pack(pady=10)

    def _build_folder_picker(self):
        self.select_btn = ctk.CTkButton(
            self.scroll_frame,
            text="Select Data Folder",
            command=self.select_folder,
        )
        self.select_btn.pack(pady=10)

        self.summary_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Select a folder to begin",
            font=("Arial", 14),
        )
        self.summary_label.pack(pady=10)

    def _build_search_bar(self):
        self.search_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.search_frame.pack(pady=10)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_results)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search names...",
            textvariable=self.search_var,
            width=350,
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        self.clear_btn = ctk.CTkButton(
            self.search_frame,
            text="X",
            width=30,
            fg_color="gray30",
            hover_color="red",
            command=self.clear_search,
        )
        self.clear_btn.pack(side="left")

        self.bind("<Control-f>", lambda event: self.search_entry.focus())

    def _build_result_sections(self):
        self.result_sections = create_result_sections(
            self.scroll_frame,
            bind_scroll_lock=self.scroll_manager.bind_textbox,
            on_toggle=self.update_scroll_region,
        )

        self.nf_box = self.result_sections["not_following_back"].textbox
        self.fans_box = self.result_sections["fans"].textbox
        self.mut_box = self.result_sections["mutuals"].textbox

    def select_folder(self):
        data_dir = filedialog.askdirectory(title="Select Instagram Data Folder")
        if data_dir:
            self.run_audit(data_dir)

    def run_audit(self, folder):
        try:
            data = analyze_relationships(folder)
            print("LOGIC DATA KEYS:", data.keys())          # <--- Add this temporarily
            print("LOGIC COUNTS KEYS:", data['counts'].keys())
            self.full_data = data
            self.summary_label.configure(
                text=f"Following: {data['counts']['following']} | Followers: {data['counts']['followers']}"
            )

            self.result_sections["not_following_back"].button.configure(
                text=f"▶ Not Following Back ({data['counts']['not_following_back']})"
            )
            self.result_sections["fans"].button.configure(
                text=f"▶ Fans ({data['counts']['fans']})"
            )
            self.result_sections["mutuals"].button.configure(
                text=f"▶ Mutually Following ({data['counts']['mutuals']})"
            )

            self.filter_results()
            self.update_scroll_region()
        except Exception as e:
            messagebox.showerror(
                "Audit Error",
                f"An error occurred while processing the data:\n\n{str(e)}\n\n"
                "Make sure you selected the correct folder.",
            )

    def filter_results(self, *args):
        if not hasattr(self, "full_data"):
            return

        search_term = self.search_var.get().lower()

        for key, section in self.result_sections.items():
            filtered_list = [
                user for user in self.full_data[key]
                if search_term in user.lower()
            ]
            update_result_box(section.textbox, filtered_list)

    def clear_search(self):
        self.search_var.set("")
        self.search_entry.focus()

    def update_scroll_region(self):
        self.scroll_manager.update_scroll_region()