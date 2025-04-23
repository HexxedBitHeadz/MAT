import os, json, random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        root.title("Hexxed BitHeadz - Midjourney Assistant Tool v2.2")
        root.resizable(False, False)

        self.autosave_path = os.path.join(os.path.dirname(__file__), "autosave_prompt.txt")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.after(10000, self.auto_save_interval)  # Save every 10s

        # Get screen resolution
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Default window size
        window_width = 900
        window_height = 600

        x_offset = (screen_width // 2) - (window_width // 2)
        y_offset = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

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

        self.root.bind("<Control-c>", lambda e: self.copy_selection())
        self.root.bind("<Control-s>", lambda e: self.save_configuration())
        self.root.bind("<Control-r>", lambda e: self.select_random())

        # Store recent selections
        self.history = []
        self.log_path = os.path.join(os.path.dirname(__file__), "prompt_log.txt")

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

        def on_dropdown_change(event=None):
            self.update_listbox_options()
            self.update_preview()

        self.dropdown.bind("<<ComboboxSelected>>", on_dropdown_change)

        self.listbox = tk.Listbox(self.root, width=25, height=15, bg='black', fg='green', font=("Arial", 12))
        self.listbox.place(x=220, y=120)

        self.create_checkboxes()
        self.create_radio_buttons()

        self.search_entry = ttk.Entry(self.root, font=("Arial", 12))
        self.search_entry.place(x=10, y=160)

        search_button = ttk.Button(self.root, text="Search", command=self.search_styles)
        search_button.place(x=10, y=200)

        # Buttons with improved spacing
        clear_button = ttk.Button(self.root, text="Clear", command=self.clear_gui)
        clear_button.place(x=720, y=120)

        random_button = ttk.Button(self.root, text="Random", command=self.select_random)
        random_button.place(x=720, y=260)

        copy_button = ttk.Button(self.root, text="Copy", command=self.copy_selection)
        copy_button.place(x=720, y=320)

        # Repeat label and dropdown
        repeat_label = tk.Label(self.root, text="Repeat", bg="black", fg="green", font=("Arial", 12))
        repeat_label.place(x=720, y=380)

        self.repeat_var = tk.StringVar()
        self.repeat_dropdown = ttk.Combobox(self.root, textvariable=self.repeat_var, state="readonly", values=["none", "3", "6", "10"])
        self.repeat_dropdown.place(x=720, y=410)
        self.repeat_dropdown.set("none")  # Default value

        self.preview_box = scrolledtext.ScrolledText(
            self.root, width=90, height=5, wrap=tk.WORD,
            font=("Arial", 12), bg="black", fg="#fefe00", state="disabled"
        )
        self.preview_box.place(x=10, y=500)

        # Auto-update preview
        self.radioMode.trace_add("write", self.update_preview)
        self.radioStylize.trace_add("write", self.update_preview)
        self.radioChaos.trace_add("write", self.update_preview)
        self.repeat_var.trace_add("write", self.update_preview)

        self.scrolled_text.bind("<<Modified>>", lambda e: (self.update_preview(), self.scrolled_text.edit_modified(False)))
        self.listbox.bind("<<ListboxSelect>>", self.update_preview)

        for var in self.check_vars.values():
            var.trace_add("write", self.update_preview)

        self.update_preview()

    def create_checkboxes(self):
        """Create properly spaced checkboxes."""
        options = [("No people", 1), ("Tshirt vector", 2), ("Logo vector", 3), ("draft", 4)]
        self.check_vars = {}

        # if draft is selected, disable Niji
        self.draft_var = tk.IntVar()

        radio_buttons = []

        for idx, (text, var_id) in enumerate(options):
            self.check_vars[var_id] = tk.IntVar()
            chk = tk.Checkbutton(
                self.root, text=text, variable=self.check_vars[var_id], 
                bg='black', fg='green', font=("Arial", 12)
            )
            chk.place(x=500, y=120 + (idx * 30))

            # Save draft checkbox for reference
            if text == "draft":
                self.draft_chk = chk
                self.draft_var = self.check_vars[var_id]
                self.draft_var.trace_add("write", self.on_draft_toggle)

    def create_radio_buttons(self):
        """Create spaced radio buttons for Mode, Stylize, and Chaos."""
        self.radio_mode_buttons = []  # Initialize list here

        self.radioMode = tk.IntVar()
        self.radioMode.trace_add("write", self.on_mode_change)

        self.radioStylize = tk.IntVar()
        self.radioChaos = tk.IntVar()

        # Mode selection
        self.create_radio_group("Mode", [(1, "Niji"), (2, "Midjourney")], self.radioMode, x=620, y=140)

        # Stylize selection
        self.create_radio_group("Stylize", [(1, "S0"), (2, "S250"), (3, "S500"), (4, "S750"), (5, "S1000")], 
                                self.radioStylize, x=500, y=280)

        # Chaos selection
        self.create_radio_group("Chaos", [(1, "C0"), (2, "C25"), (3, "C50"), (4, "C100")], 
                                self.radioChaos, x=620, y=280)

    def create_radio_group(self, label, options, variable, x, y):
        """Reusable function to create a properly spaced set of radio buttons."""
        tk.Label(self.root, text=label, bg='black', fg='green', font=("Arial", 12)).place(x=x, y=y - 20)

        radio_buttons = []  # Local list to collect buttons

        for idx, (val, text) in enumerate(options):
            rb = tk.Radiobutton(
                self.root, text=text, variable=variable, value=val, 
                bg='black', fg='green', font=("Arial", 12)
            )
            rb.place(x=x, y=y + (idx * 30))
            radio_buttons.append(rb)

        if label == "Mode":
            self.radio_mode_buttons = radio_buttons  # Save for Draft/Niji mutual exclusion

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
            self.listbox.see(random_index)  # Ensure it is visible in the listbox
            # Enable the following lines to randomize style and chaos
            #self.radioStylize.set(random.choice(list({1, 2, 3, 4, 5})))
            #self.radioChaos.set(random.choice(list({1, 2, 3, 4})))

            self.update_preview()

    def search_styles(self):
        """Searches styles dynamically based on user input, sorts and deduplicates results."""
        self.listbox.delete(0, tk.END)
        search_term = self.search_entry.get().lower().strip()

        if not search_term:
            return  # Prevent searching if input is empty

        styles_folder = os.path.join(os.path.dirname(__file__), "Styles")
        results = set()

        for filename in os.listdir(styles_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(styles_folder, filename)
                try:
                    with open(file_path, 'r', encoding="utf-8") as file:
                        for line in file:
                            if search_term in line.lower():
                                results.add(line.strip())
                except FileNotFoundError:
                    messagebox.showwarning("Error", f"File not found: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while searching: {str(e)}")

        for result in sorted(results, key=str.lower):  # Sort results case-insensitively
            self.listbox.insert(tk.END, result)

    def copy_selection(self):
        """Copies the generated prompt text to the clipboard, displays it, stores it in history, and logs it."""
        copied_text = self.build_prompt()

        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(copied_text)
        self.root.update()

        # Save to history
        if copied_text and copied_text not in self.history:
            self.history.insert(0, copied_text)
        if len(self.history) > 5:
            self.history.pop()

        # Append to log
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                log_file.write(copied_text + "\n")
        except Exception as e:
            print(f"Failed to log prompt: {e}")
        
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
        self.search_entry.delete(0, tk.END)
        self.repeat_var.set("none")
        self.preview_box.config(state="normal")
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.config(state="disabled")
        self.draft_var.set(0)
        self.draft_chk.config(state=tk.NORMAL)

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

        # Load last autosaved prompt into preview
        if os.path.exists(self.autosave_path):
            with open(self.autosave_path, 'r', encoding='utf-8') as f:
                last_prompt = f.read()
            self.preview_box.config(state="normal")
            self.preview_box.delete("1.0", tk.END)
            self.preview_box.insert(tk.END, last_prompt)
            self.preview_box.config(state="disabled")

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

        menubar.add_command(label="Log", command=self.view_prompt_log)

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

    def on_mode_change(self, *args):
        """Disable draft if Niji is selected."""
        if self.radioMode.get() == 1:  # Niji
            self.draft_chk.config(state=tk.DISABLED)
            self.draft_var.set(0)
        else:
            self.draft_chk.config(state=tk.NORMAL)


    def on_draft_toggle(self, *args):
        """Force Midjourney and disable Niji if Draft is checked."""
        if self.draft_var.get():
            self.radioMode.set(2)  # Force Midjourney
            for rb in self.radio_mode_buttons:
                if rb["text"] == "Niji":
                    rb.config(state=tk.DISABLED)
        else:
            for rb in self.radio_mode_buttons:
                if rb["text"] == "Niji":
                    rb.config(state=tk.NORMAL)

    def build_prompt(self):
        """Assembles the full prompt based on current UI state."""
        selected_text = self.scrolled_text.get("1.0", tk.END).strip()
        listbox_selection = self.listbox.get(tk.ACTIVE)

        # Start building the prompt
        prompt = selected_text
        if listbox_selection:
            prompt += f", {listbox_selection} style"

        if self.check_vars[1].get():
            prompt += "no people, woman, man"
        if self.check_vars[2].get():
            prompt += ", tshirt vector, black background"
        if self.check_vars[3].get():
            prompt += ", logo vector, black background"
        if self.check_vars[4].get():
            prompt += " --draft"

        stylize = {1: " --s 0", 2: " --s 250", 3: " --s 500", 4: " --s 750", 5: " --s 1000"}
        chaos = {1: " --c 0", 2: " --c 25", 3: " --c 50", 4: " --c 100"}
        mode = {1: " --niji 6", 2: " --v 7"}

        if self.radioStylize.get() in stylize:
            prompt += stylize[self.radioStylize.get()]
        if self.radioChaos.get() in chaos:
            prompt += chaos[self.radioChaos.get()]
        if self.radioMode.get() in mode:
            prompt += mode[self.radioMode.get()] + " --ar 7:4"

        if self.repeat_var.get() != "none":
            prompt += f" --repeat {self.repeat_var.get()}"

        return prompt

    def update_preview(self, *args):
        """Updates the live prompt preview based on UI state."""
        prompt = self.build_prompt()
        self.preview_box.config(state="normal")
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, prompt)
        self.preview_box.config(state="disabled")

    def auto_save_interval(self):
        """Periodically saves the current prompt to a temp file."""
        try:
            with open(self.autosave_path, 'w', encoding='utf-8') as file:
                file.write(self.build_prompt())
        except Exception:
            pass
        self.root.after(10000, self.auto_save_interval)  # Loop

    def on_exit(self):
        """Save on exit and quit."""
        try:
            with open(self.autosave_path, 'w', encoding='utf-8') as file:
                file.write(self.build_prompt())
        except Exception:
            pass
        self.root.destroy()

    def view_prompt_log(self):
        """Displays the log of all generated prompts."""
        if not os.path.exists(self.log_path):
            messagebox.showinfo("Log", "No prompt log found yet.")
            return

        with open(self.log_path, "r", encoding="utf-8") as file:
            content = file.read()

        log_window = tk.Toplevel(self.root)
        log_window.title("Prompt Log")
        log_window.configure(bg="black")
        log_window.geometry("800x400")

        text_area = scrolledtext.ScrolledText(
            log_window, wrap=tk.WORD, bg="black", fg="#fefe00", font=("Consolas", 11)
        )
        text_area.pack(expand=True, fill="both")

        # Confirmation label (initially hidden)
        confirm_label = tk.Label(
            log_window,
            text="Copied!",
            bg="#222222",
            fg="lime",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=2
        )

        text_area.insert(tk.END, content)
        text_area.config(state="disabled")

        def copy_line(event):
            index = text_area.index(f"@{event.x},{event.y}")
            line_start = f"{index.split('.')[0]}.0"
            line_end = f"{index.split('.')[0]}.end"
            line_text = text_area.get(line_start, line_end).strip()

            if line_text:
                self.root.clipboard_clear()
                self.root.clipboard_append(line_text)
                self.root.update()

                # Show subtle confirmation label
                confirm_label.place(relx=1.0, rely=1.0, anchor="se")
                log_window.after(1500, lambda: confirm_label.place_forget())

        text_area.bind("<Double-Button-1>", copy_line)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
