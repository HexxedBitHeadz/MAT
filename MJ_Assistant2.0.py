import os, json, random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        root.title("Hexxed BitHeadz - Midjourney Assistant Tool v1.2")
        root.resizable(False, False)

        # Get screen resolution
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Default window size
        window_width = 900
        window_height = 600

        # Adjust if the screen is too small
        if screen_width < 1000:  # Adjust for small screens
            window_width = int(screen_width * 0.9)
            window_height = int(screen_height * 0.9)

        # Set the dynamic window size
        root.geometry(f"{window_width}x{window_height}")

        # Prevent window from getting larger than the screen
        root.maxsize(screen_width, screen_height)

        # Configure background
        root.configure(bg='black')

        # Set up a consistent theme
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Ensures ttk buttons render correctly
        self.style.configure("TButton", foreground="green", background="black", font=("Arial", 12))

        # Store recent selections
        self.history = []

        self.create_widgets()
        self.create_menu()
        self.load_configuration()


    def create_widgets(self):
        """Create the main UI widgets."""
        self.scrolled_text = scrolledtext.ScrolledText(
            self.root, width=74, height=4, wrap=tk.WORD, font=("Arial", 14), 
            bg="black", fg="green", insertbackground="green"
        )
        self.scrolled_text.place(x=10, y=10)

        self.dropdown = ttk.Combobox(self.root, values=self.get_style_options(), state="readonly")
        self.dropdown.place(x=10, y=120)
        self.dropdown.bind("<<ComboboxSelected>>", self.update_listbox_options)

        self.listbox = tk.Listbox(self.root, width=25, height=15, bg='black', fg='green', font=("Arial", 12))
        self.listbox.place(x=220, y=120)

        self.create_checkboxes()
        self.create_radio_buttons()

        self.search_entry = ttk.Entry(self.root, font=("Arial", 12))
        self.search_entry.place(x=10, y=160)

        search_button = ttk.Button(self.root, text="Search", command=self.search_styles)
        search_button.place(x=10, y=200)

                # 🔥 Buttons with improved spacing
        clear_button = ttk.Button(self.root, text="Clear", command=self.clear_gui)
        clear_button.place(x=720, y=120)

        random_button = ttk.Button(self.root, text="Random", command=self.select_random)
        random_button.place(x=720, y=260)

        copy_button = ttk.Button(self.root, text="Copy", command=self.copy_selection)
        copy_button.place(x=720, y=320)

        # Recent selections dropdown
        self.history_dropdown = ttk.Combobox(self.root, state="readonly")
        self.history_dropdown.place(x=10, y=300)
        self.history_dropdown.bind("<<ComboboxSelected>>", self.load_recent_selection)


    def create_checkboxes(self):
        """Create properly spaced checkboxes."""
        options = [("No people", 1), ("Tshirt vector", 2), ("Logo vector", 3)]
        self.check_vars = {}

        for idx, (text, var_id) in enumerate(options):
            self.check_vars[var_id] = tk.IntVar()
            chk = tk.Checkbutton(
                self.root, text=text, variable=self.check_vars[var_id], 
                bg='black', fg='green', font=("Arial", 12)
            )
            chk.place(x=500, y=120 + (idx * 30))  # Adjusted Y-coordinates

    def create_radio_buttons(self):
        """Create spaced radio buttons for Mode, Stylize, and Chaos."""
        self.radioMode = tk.IntVar()
        self.radioStylize = tk.IntVar()
        self.radioChaos = tk.IntVar()

        # Mode selection
        self.create_radio_group("Mode", [(1, "Niji"), (2, "Midjourney")], self.radioMode, x=620, y=140)

        # Stylize selection
        self.create_radio_group("Stylize", [(1, "S0"), (2, "S250"), (3, "S500"), (4, "S750"), (5, "S1000")], 
                                self.radioStylize, x=500, y=240)

        # Chaos selection
        self.create_radio_group("Chaos", [(1, "C0"), (2, "C25"), (3, "C50"), (4, "C100")], 
                                self.radioChaos, x=620, y=240)  # Adjusted spacing

    def create_radio_group(self, label, options, variable, x, y):
        """Reusable function to create a properly spaced set of radio buttons."""
        tk.Label(self.root, text=label, bg='black', fg='green', font=("Arial", 12)).place(x=x, y=y - 20)

        for idx, (val, text) in enumerate(options):
            rb = tk.Radiobutton(
                self.root, text=text, variable=variable, value=val, 
                bg='black', fg='green', font=("Arial", 12)
            )
            rb.place(x=x, y=y + (idx * 30))

    def select_random(self):
        """Randomly selects a style and ensures the selection is always highlighted and visible."""
        style_options = self.get_style_options()
        if not style_options:
            return  # Prevent crash if no styles are available

        # Select a random option from the dropdown styles
        random_option = random.choice(style_options)
        self.dropdown.set(random_option)
        self.update_listbox_options()

        # Ensure a random selection is made from the listbox
        if self.listbox.size() > 0:
            random_index = random.randint(0, self.listbox.size() - 1)
            self.listbox.selection_clear(0, tk.END)  # Clear previous selections
            self.listbox.selection_set(random_index)  # Select the new item
            self.listbox.activate(random_index)  # Highlight the selected item
            self.listbox.see(random_index)  # ✅ Ensure it is visible in the listbox

    def search_styles(self):
        """Searches styles dynamically based on user input."""
        self.listbox.delete(0, tk.END)
        search_term = self.search_entry.get().lower().strip()

        if not search_term:
            return  # Prevent searching if input is empty

        styles_folder = os.path.join(os.path.dirname(__file__), "Styles")

        for filename in os.listdir(styles_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(styles_folder, filename)
                try:
                    with open(file_path, 'r', encoding="utf-8") as file:
                        for line in file:
                            if search_term in line.lower():
                                self.listbox.insert(tk.END, line.strip())
                except FileNotFoundError:
                    messagebox.showwarning("Error", f"File not found: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while searching: {str(e)}")

    def copy_selection(self):
        """Copies the generated prompt text to the clipboard, displays it, and stores it in history."""
        selected_text = self.scrolled_text.get("1.0", tk.END).strip()
        listbox_selection = self.listbox.get(tk.ACTIVE)

        # Construct the copied text
        copied_text = selected_text
        if listbox_selection:
            copied_text += f", {listbox_selection} style --ar 7:4"

        # Include checkbox selections
        if self.check_vars[2].get():  # Tshirt vector
            copied_text += ", tshirt vector, black background"
        if self.check_vars[3].get():  # Logo vector
            copied_text += ", logo vector, black background"
        if self.check_vars[1].get():  # No people
            copied_text += " --no people, woman, man"

        # Include Stylize settings
        stylize_options = {1: " --s 0", 2: " --s 250", 3: " --s 500", 4: " --s 750", 5: " --s 1000"}
        if self.radioStylize.get() in stylize_options:
            copied_text += stylize_options[self.radioStylize.get()]

        # Include Chaos settings
        chaos_options = {1: " --c 0", 2: " --c 25", 3: " --c 50", 4: " --c 100"}
        if self.radioChaos.get() in chaos_options:
            copied_text += chaos_options[self.radioChaos.get()]

        # Include Mode (Midjourney or Niji)
        mode_options = {1: " --niji 6", 2: " --v 6.1"}
        if self.radioMode.get() in mode_options:
            copied_text += mode_options[self.radioMode.get()]

        # Copy text to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(copied_text)
        self.root.update()  # Ensure clipboard updates correctly

        # Destroy previous label if it exists
        if hasattr(self, 'labelCopy'):
            self.labelCopy.destroy()

        # Create a label to display the copied text
        self.labelCopy = tk.Label(self.root, text=copied_text, font=("Arial Bold", 12), wraplength=800)
        self.labelCopy.place(x=10, y=500)  # Ensuring it's visible

        # Set label background to black with green text
        self.labelCopy.config(bg="black", fg="green")

        # Update history dropdown
        if copied_text and copied_text not in self.history:
            self.history.insert(0, copied_text)
        if len(self.history) > 5:
            self.history.pop()
        
        self.history_dropdown["values"] = self.history

    def load_recent_selection(self, event):
        """Loads a recent selection back into the text box."""
        selected_prompt = self.history_dropdown.get()
        self.scrolled_text.delete("1.0", tk.END)
        self.scrolled_text.insert(tk.END, selected_prompt)


    def clear_gui(self):
        """Clears all input fields and selections."""
        self.scrolled_text.delete("1.0", tk.END)
        self.dropdown.set("")
        self.listbox.delete(0, tk.END)
        for var in self.check_vars.values():
            var.set(0)
        self.radioMode.set(0)
        self.radioStylize.set(0)
        self.radioChaos.set(0)

    def save_configuration(self):
        """Saves the current settings to a JSON file."""
        config = {
            "selected_text": self.scrolled_text.get("1.0", tk.END).strip(),
            "dropdown": self.dropdown.get(),
            "radioMode": self.radioMode.get(),
            "radioStylize": self.radioStylize.get(),
            "radioChaos": self.radioChaos.get(),
            "check_vars": {k: v.get() for k, v in self.check_vars.items()}
        }
        
        try:
            config_path = os.path.join(os.path.dirname(__file__), "config.json")
            with open(config_path, 'w', encoding='utf-8') as file:
                json.dump(config, file, indent=4)
            messagebox.showinfo("Saved", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")


    def load_configuration(self):
        """Loads saved configuration from a JSON file."""
        config_path = os.path.join(os.path.dirname(__file__), "config.json")

        if not os.path.exists(config_path):
            return  # Skip loading if config file doesn't exist

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

            # Restore the saved settings
            self.scrolled_text.delete("1.0", tk.END)
            self.scrolled_text.insert(tk.END, config.get("selected_text", ""))

            self.dropdown.set(config.get("dropdown", ""))
            self.radioMode.set(config.get("radioMode", 0))
            self.radioStylize.set(config.get("radioStylize", 0))
            self.radioChaos.set(config.get("radioChaos", 0))

            for key, value in config.get("check_vars", {}).items():
                if int(key) in self.check_vars:
                    self.check_vars[int(key)].set(value)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")


    def create_menu(self):
        """Create a simple menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_configuration)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Hexxed BitHeadz - Midjourney Assistant v2.0"))
        menubar.add_cascade(label="Help", menu=help_menu)

    def get_style_options(self):
        """Returns a list of style options dynamically."""
        return ["Abstract", "Animal", "Baroque", "Bold", "BW", "Cinematic", "Comics", "Fantasy", "Sci-fi", "Surreal", "Urban", "Vivid"]

    def update_listbox_options(self, event=None):
        """Load style suggestions from files dynamically."""
        self.listbox.delete(0, tk.END)
        selected_option = self.dropdown.get()
        file_path = os.path.join(os.path.dirname(__file__), f"Styles/{selected_option}.txt")

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    self.listbox.insert(tk.END, line.strip())

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
