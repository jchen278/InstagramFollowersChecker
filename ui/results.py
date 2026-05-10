from dataclasses import dataclass

import customtkinter as ctk


@dataclass
class ResultSection:
    button: ctk.CTkButton
    textbox: ctk.CTkTextbox


def create_result_sections(parent, bind_scroll_lock, on_toggle):
    sections = {}

    for key, title in (
        ("not_following_back", "Not Following Back"),
        ("fans", "Fans"),
        ("mutuals", "Mutually Following"),
    ):
        sections[key] = create_result_section(
            parent,
            title,
            bind_scroll_lock,
            on_toggle,
        )

    return sections


def create_result_section(parent, title, bind_scroll_lock, on_toggle):
    button = ctk.CTkButton(parent, text=f"▶ {title}")
    button.pack(fill="x", pady=(10, 0), padx=(20, 20))

    textbox = ctk.CTkTextbox(parent, height=200)
    bind_scroll_lock(textbox)

    section = ResultSection(button=button, textbox=textbox)
    button.configure(command=lambda: toggle_result_section(section, on_toggle))

    return section


def toggle_result_section(section, on_toggle):
    if section.textbox.winfo_viewable():
        section.textbox.pack_forget()
        section.button.configure(text=section.button.cget("text").replace("▼", "▶"))
    else:
        section.textbox.pack(fill="x", padx=20, after=section.button)
        section.button.configure(text=section.button.cget("text").replace("▶", "▼"))

    on_toggle()


def update_result_box(box, user_list):
    box.delete("0.0", "end")

    if not user_list:
        box.insert("end", "No users found.")
        return

    for user in user_list:
        box.insert("end", f"{user}\n")
