"""Keyboard shortcuts, shared by the main window and Settings > Shortcuts."""

# (key sequence, description). Page shortcuts Ctrl+1..9 follow the
# order of the pages the logged-in user can see in the sidebar.
SHORTCUTS = [
    ("Ctrl+1 ... Ctrl+9", "Open the 1st ... 9th page in the sidebar"),
    ("Ctrl+N", "New item on the current page (customer, measurement, order, inventory item, user)"),
    ("F5", "Refresh the current page"),
    ("Ctrl+F", "Jump to the search box on the current page"),
    ("Ctrl+B", "Back up now"),
    ("Ctrl+Shift+P", "Change your password"),
    ("Ctrl+Shift+L", "Log out"),
    ("F1", "Show this list of shortcuts"),
    ("Enter", "In a search box: search"),
    ("Double-click a row", "Edit that customer / measurement / user"),
]
