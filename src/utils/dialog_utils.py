"""Dialog utilities for the 3D File Version Tracker application.

This module provides reusable functions for creating and displaying dialogs.
"""

from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton


def create_info_dialog(parent, title, message):
    """Create an informational dialog.

    Args:
        parent (CTk): The parent window.
        title (str): The title of the dialog.
        message (str): The message to display in the dialog.

    Returns:
        CTkToplevel: The created dialog window.
    """
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
    """Create an input dialog.

    Args:
        parent (CTk): The parent window.
        title (str): The title of the dialog.
        prompt (str): The prompt message to display.

    Returns:
        tuple: A tuple containing the dialog window and the input entry widget.
    """
    input_window = CTkToplevel(parent)
    input_window.title(title)
    input_window.geometry("300x150")

    CTkLabel(input_window, text=prompt, wraplength=280, font=("Arial", 12)).pack(pady=10)
    input_var = CTkEntry(input_window, width=250)
    input_var.pack(pady=10)

    return input_window, input_var


def show_info(parent, title, message):
    """Display an informational message.

    Args:
        parent (CTk): The parent window.
        title (str): The title of the dialog.
        message (str): The message to display.
    """
    info_window = create_info_dialog(parent, title, message)
    info_window.grab_set()
    parent.wait_window(info_window)


def ask_string(parent, title, prompt):
    """Display an input dialog to get a string from the user.

    Args:
        parent (CTk): The parent window.
        title (str): The title of the dialog.
        prompt (str): The prompt message to display.

    Returns:
        str: The string entered by the user.
    """
    input_window, input_var = create_input_dialog(parent, title, prompt)

    def on_submit():
        parent.input_value = input_var.get()
        input_window.destroy()

    submit_button = CTkButton(input_window, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    input_var.focus_set()
    input_window.bind("<Return>", lambda event: submit_button.invoke())

    input_window.grab_set()
    parent.wait_window(input_window)
    return getattr(parent, "input_value", None)
