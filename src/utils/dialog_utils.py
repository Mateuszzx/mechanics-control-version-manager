from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton


def create_info_dialog(parent, title, message):
    """Create and display an info dialog."""
    info_window = CTkToplevel(parent)
    info_window.title(title)
    info_window.geometry("300x150")

    CTkLabel(info_window, text=message, wraplength=280, font=("Arial", 12)).pack(pady=20)
    ok_button = CTkButton(info_window, text="OK", command=info_window.destroy)
    ok_button.pack(pady=10)

    ok_button.focus_set()
    info_window.bind("<Return>", lambda event: ok_button.invoke())

    return info_window


def create_input_dialog(parent, title, prompt):
    """Create and display an input dialog."""
    input_window = CTkToplevel(parent)
    input_window.title(title)
    input_window.geometry("300x150")

    CTkLabel(input_window, text=prompt, wraplength=280, font=("Arial", 12)).pack(pady=10)
    input_var = CTkEntry(input_window, width=250)
    input_var.pack(pady=10)

    return input_window, input_var
