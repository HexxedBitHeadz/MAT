import os, json, random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Button

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        root.title("Hexxed BitHeadz - Midjourney Assistant Tool v1.1")
        root.resizable(False, False)
        root.configure(bg='black')

        # Set icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "HeBi.ico")
        root.iconbitmap(icon_path)

        # Set the window size and position
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        app_width = screen_width // 2
        app_height = screen_height // 2
        root.geometry(f"{app_width}x{app_height}+{screen_width//4}+{screen_height//4}")

        # ScrolledText box
        self.scrolled_text = scrolledtext.ScrolledText(self.root, width=74, height=4, wrap=tk.WORD, font=("Arial", 14))
        self.scrolled_text.place(x=10, y=10, anchor="nw")
        self.scrolled_text.focus()
        self.scrolled_text.configure(bg="black", fg="green", insertbackground="green")

        self.create_widgets()
        self.create_menu()


        # Load configuration on startup 
        self.load_configuration()

        # Search entry and button
        self.search_entry = ttk.Entry(self.root, font=("Arial", 12))
        self.search_entry.place(x=10, y=200, anchor="w")

        search_button = Button(self.root, text="Search", width=12, bg="green", fg="white", command=self.search_styles)
        search_button.place(x=10, y=220)

        # Search results listbox
        self.search_results_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=25, height=8, justify=tk.LEFT)
        self.search_results_listbox.place(x=10, y=345, anchor="w")
        self.search_results_listbox.configure(bg='black', fg='green', font=("Arial", 12))

        # Bind double-click event to load_selected_result method
        self.search_results_listbox.bind("<Double-Button-1>", self.load_selected_result)



    def load_selected_result(self, event):
        selected_item = self.search_results_listbox.get(tk.ACTIVE)
        if selected_item:
            # Clear previous listbox content
            self.listbox.delete(0, tk.END)

            # Extract text after colon in each line and load into listbox
            for line in selected_item.split('\n'):
                parts = line.split(': ', 1)
                if len(parts) == 2:
                    result_text = parts[1].strip()
                    self.listbox.insert(tk.END, result_text)

            # Clear selection in the dropdown menu
            self.dropdown.set("")

    def search_styles(self):
            # Clear previous search results
            self.search_results_listbox.delete(0, tk.END)

            # Get the search term
            search_term = self.search_entry.get().lower()

            # Iterate through all Styles/*.txt files and search for the term
            styles_folder = os.path.join(os.path.dirname(__file__), "Styles")
            for filename in os.listdir(styles_folder):
                if filename.endswith(".txt"):
                    file_path = os.path.join(styles_folder, filename)
                    try:
                        with open(file_path, 'r') as file:
                            lines = file.readlines()
                            for line in lines:
                                # Check if the search term is in the line (case-insensitive)
                                if search_term in line.lower():
                                    # Insert the file name and line into the search results listbox
                                    result_text = f"{filename}: {line.strip()}"
                                    self.search_results_listbox.insert(tk.END, result_text)
                    except FileNotFoundError:
                        messagebox.showwarning("File Not Found", f"File '{file_path}' not found.")


    def save_configuration(self, config):
            # Save the configuration to a JSON file
            config_filename = "config.json"
            config_path = os.path.join(os.path.dirname(__file__), config_filename)
            print(config_path)
            try:
                with open(config_path, 'w') as config_file:
                    json.dump(config, config_file)
            except Exception as e:
                messagebox.showerror("Error", f"Error saving configuration: {str(e)}")
            messagebox.showinfo("Save", "Configuration saved!")

    def read_configuration(self):
            # Load configuration from the JSON file
            config_filename = "config.json"
            config_path = os.path.join(os.path.dirname(__file__), config_filename)

            if os.path.exists(config_path):
                with open(config_path, 'r') as config_file:
                    return json.load(config_file)
            return {}
    
            

    def save_file(self):
            # Get the selected text and configuration options
            selected_text = self.scrolled_text.get("1.0", tk.END).strip()
            selected_option = self.dropdown.get()
            listbox_selection = self.listbox.get(tk.ACTIVE)
            
            # Get the values of checkboxes and radio button
            config = {
                "no_people_checked": self.var1.get(),
                "tshirt_vector_checked": self.var2.get(),
                "radioMode": self.radioMode.get(),
                "radioStylize": self.radioStylize.get(),
                "selected_text": selected_text,
                "selected_option": selected_option,
                "listbox_selection": listbox_selection
            }

            # Save the configuration
            self.save_configuration(config)

    def load_configuration(self):
            # Load configuration
            config = self.read_configuration()

            # Set the values based on the loaded configuration
            self.var1.set(config.get("no_people_checked", 0))
            self.var2.set(config.get("tshirt_vector_checked", 0))
            self.radioMode.set(config.get("radioMode", 0))
            self.radioStylize.set(config.get("radioStylize", 0))

            # Load the text into scrolled_text
            self.scrolled_text.delete("1.0", tk.END)
            self.scrolled_text.insert(tk.END, config.get("selected_text", ""))

            # Set the selected option in the dropdown
            selected_option = config.get("selected_option", "")
            self.dropdown.set(selected_option)

            # Load listbox options and highlight the selected item
            listbox_selection = config.get("listbox_selection", "")
            self.update_listbox_options(selected_option)
            if listbox_selection:
                try:
                    index = self.listbox.get(0, tk.END).index(listbox_selection)
                    self.listbox.selection_set(index)
                    self.listbox.see(index)  # Make the selected item visible
                except ValueError:
                    pass

    def clear_gui(self):
        # Clear scrolled_text
        self.scrolled_text.delete("1.0", tk.END)
        
        # Clear dropdown selection
        self.dropdown.set("")
        
        # Clear listbox selection
        self.listbox.delete(0, tk.END)

        # Clear checkboxes
        self.var1.set(0)
        self.var2.set(0)

        # Clear radio buttons
        self.radioMode.set(0)
        self.radioStylize.set(0)

        # Clear label
        self.label_var.set("")

    def create_widgets(self):

        # Label
        self.label_var = tk.StringVar()
        label = tk.Label(self.root, textvariable=self.label_var)
        label.place(x=10, y=130, anchor="w")

        # Set label background to black and text color to green
        label.configure(bg='black', fg='green')

        # Dropdown menu
        style_options = [
            "Abstract", "Animal", "Baroque", "Bold", "BoldLines", "BroadBrushstrokes",
            "BW", "Characters", "Cinematic", "Classical", "Comics", "Cute", "Dark", "Detailed",
            "Documentary", "Drawing", "Dreamy", "Epic", "Erotic", "Ethnic", "Expressive",
            "Fantasy", "FineBrushstrokes", "FineLines", "Floral", "Funny", "Geometric",
            "Illustrative", "Landscapes", "Letters", "LGBTQ", "Light", "Madness", "Minimalist",
            "Moody", "Motion", "Painterly", "Pastel", "Patterns", "Portraits", "Psychedelic",
            "Realistic", "Religious", "Retro", "Scenes", "Sci-fi", "StillLife",
            "Subdued", "Surreal", "Urban", "Vivid"
        ]
        self.dropdown = ttk.Combobox(self.root, values=style_options, state="readonly", font=("Arial", 12))
        self.dropdown.place(x=10, y=160, anchor="w")
        self.dropdown.bind("<<ComboboxSelected>>", self.on_select)
                
        # Set dropdown background to black and text color to green
        self.dropdown.configure(style='TCombobox', foreground='green', background='black')

        # Listbox
        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=25, height=15, justify=tk.LEFT)
        self.listbox.place(x=260, y=280, anchor="w")

        # Set listbox background to black and text color to green
        self.listbox.configure(bg='black', fg='green', font=("Arial", 12))

        # Make a checkbox for people option
        self.var1 = tk.IntVar()
        check1 = tk.Checkbutton(self.root, text="No people", variable=self.var1, onvalue=1, offvalue=0)
        # Set checkbox background to black and text color to green
        check1.configure(bg='black', fg='green', font=("Arial", 12))
        check1.place(x=500, y=130)
        
        # Make a checkbox for tshirt option
        self.var2 = tk.IntVar()
        check2 = tk.Checkbutton(self.root, text="Tshirt vector", variable=self.var2, onvalue=1, offvalue=0)

        # Make a checkbox for tshirt option
        self.var3 = tk.IntVar()
        check3 = tk.Checkbutton(self.root, text="Logo vector", variable=self.var3, onvalue=1, offvalue=0)
       
        # Set checkbox background to black and text color to green
        check2.configure(bg='black', fg='green', font=("Arial", 12))
        check2.place(x=625, y=130)

        # Set checkbox background to black and text color to green
        check3.configure(bg='black', fg='green', font=("Arial", 12))
        check3.place(x=500, y=160)

        self.radioMode = tk.IntVar()

        # Make two radio buttons to choose between niji or midjourney
        radioNiji = tk.Radiobutton(self.root, text="niji", variable=self.radioMode, value=1)
        radioNiji.configure(bg='black', fg='green', font=("Arial", 12))
        radioNiji.place(x=500, y=200)

        radioMidjourney = tk.Radiobutton(self.root, text="midjourney", variable=self.radioMode, value=2)
        radioMidjourney.configure(bg='black', fg='green', font=("Arial", 12))
        radioMidjourney.place(x=625, y=200)

        # Make a radio button for stylize option
        self.radioStylize = tk.IntVar()

        # Make five radio buttons to choose between stylize 0, 250, 500, 750 and 1000
        radioStylize0 = tk.Radiobutton(self.root, text="stylize 0", variable=self.radioStylize, value=1)
        radioStylize0.configure(bg='black', fg='green', font=("Arial", 12))
        radioStylize0.place(x=500, y=240)
        radioStylize250 = tk.Radiobutton(self.root, text="stylize 250", variable=self.radioStylize, value=2)
        radioStylize250.configure(bg='black', fg='green', font=("Arial", 12))
        radioStylize250.place(x=500, y=270)
        radioStylize500 = tk.Radiobutton(self.root, text="stylize 500", variable=self.radioStylize, value=3)
        radioStylize500.configure(bg='black', fg='green', font=("Arial", 12))
        radioStylize500.place(x=500, y=300)
        radioStylize750 = tk.Radiobutton(self.root, text="stylize 750", variable=self.radioStylize, value=4)
        radioStylize750.configure(bg='black', fg='green', font=("Arial", 12))
        radioStylize750.place(x=500, y=330)
        radioStylize1000 = tk.Radiobutton(self.root, text="stylize 1000", variable=self.radioStylize, value=5)
        radioStylize1000.configure(bg='black', fg='green', font=("Arial", 12))
        radioStylize1000.place(x=500, y=360)

        # Make a radio button for stylize option
        self.radioChaos = tk.IntVar()

        # Make five radio buttons to choose between stylize 0, 250, 500, 750 and 1000
        radioChaos0 = tk.Radiobutton(self.root, text="chaos 0", variable=self.radioChaos, value=1)
        radioChaos0.configure(bg='black', fg='green', font=("Arial", 12))
        radioChaos0.place(x=625, y=240)
        radioChaos25 = tk.Radiobutton(self.root, text="chaos 25", variable=self.radioChaos, value=2)
        radioChaos25.configure(bg='black', fg='green', font=("Arial", 12))
        radioChaos25.place(x=625, y=270)
        radioChaos50 = tk.Radiobutton(self.root, text="chaos 50", variable=self.radioChaos, value=3)
        radioChaos50.configure(bg='black', fg='green', font=("Arial", 12))
        radioChaos50.place(x=625, y=300)
        radioChaos100 = tk.Radiobutton(self.root, text="chaos 100", variable=self.radioChaos, value=4)
        radioChaos100.configure(bg='black', fg='green', font=("Arial", 12))
        radioChaos100.place(x=625, y=330)

        # Make a button to clear all selections
        buttonClear = Button(self.root, text="Clear", width=12, bg="gray", fg="white", command=self.clear_gui)
        buttonClear.place(x=750, y=140)

        # Make a random button to randomize selections
        random_button = Button(self.root, text="Random", width=12, bg="blue", fg="white", command=self.select_random)
        random_button.place(x=750, y=180)

        # Make a button that prints all the selected items
        buttonCopy = Button(self.root, text="Copy", width=12, height=4, bg="brown", fg="white", command=lambda : copySelection(self))
        buttonCopy.place(x=750, y=260)

        # Make rows and columns expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="About", command=self.show_about)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

    def on_select(self, event):
        selected_option = self.dropdown.get()
        self.label_var.set(f"Selected Option: {selected_option}")
        self.update_listbox_options(selected_option)

    def update_listbox_options(self, selected_option):
        self.listbox.delete(0, tk.END)

        if selected_option is None:
            # Just return
            return

        # Mapping of selected options to file paths (relative to the "Styles" folder)
        file_mapping = {
            "Abstract": "Styles/Abstract.txt",
            "Animal": "Styles/Animal.txt",
            "Baroque": "Styles/Baroque.txt",
            "Bold": "Styles/Bold.txt",
            "BoldLines": "Styles/BoldLines.txt",
            "BroadBrushstrokes": "Styles/BroadBrushstrokes.txt",
            "BW": "Styles/BW.txt",
            "Characters": "Styles/Characters.txt",
            "Cinematic": "Styles/Cinematic.txt",
            "Classical": "Styles/Classical.txt",
            "Comics": "Styles/Comics.txt",
            "Cute": "Styles/Cute.txt",
            "Dark": "Styles/Dark.txt",
            "Detailed": "Styles/Detailed.txt",
            "Documentary": "Styles/Documentary.txt",
            "Drawing": "Styles/Drawing.txt",
            "Dreamy": "Styles/Dreamy.txt",
            "Epic": "Styles/Epic.txt",
            "Erotic": "Styles/Erotic.txt",
            "Ethnic": "Styles/Ethnic.txt",
            "Expressive": "Styles/Expressive.txt",
            "Fantasy": "Styles/Fantasy.txt",
            "FineBrushstrokes": "Styles/FineBrushstrokes.txt",
            "FineLines": "Styles/FineLines.txt",
            "Floral": "Styles/Floral.txt",
            "Funny": "Styles/Funny.txt",
            "Geometric": "Styles/Geometric.txt",
            "Illustrative": "Styles/Illustrative.txt",
            "Landscapes": "Styles/Landscapes.txt",
            "Letters": "Styles/Letters.txt",
            "LGBTQ": "Styles/LGBTQ.txt",
            "Light": "Styles/Light.txt",
            "Madness": "Styles/Madness.txt",
            "Minimalist": "Styles/Minimalist.txt",
            "Moody": "Styles/Moody.txt",
            "Motion": "Styles/Motion.txt",
            "Painterly": "Styles/Painterly.txt",
            "Pastel": "Styles/Pastel.txt",
            "Patterns": "Styles/Patterns.txt",
            "Portraits": "Styles/Portraits.txt",
            "Psychedelic": "Styles/Psychedelic.txt",
            "Realistic": "Styles/Realistic.txt",
            "Religious": "Styles/Religious.txt",
            "Retro": "Styles/Retro.txt",
            "Scenes": "Styles/Scenes.txt",
            "Sci-fi": "Styles/Sci-fi.txt",
            "StillLife": "Styles/StillLife.txt",
            "Subdued": "Styles/Subdued.txt",
            "Surreal": "Styles/Surreal.txt",
            "Urban": "Styles/Urban.txt",
            "Vivid": "Styles/Vivid.txt"
        }

    # Load contents from file based on the selected option
        file_name = file_mapping.get(selected_option)
        if file_name:
            file_path = os.path.join(os.path.dirname(__file__), file_name)
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        # Insert each line with anchor set to "w" for left justification
                        self.listbox.insert(tk.END, line.strip())
            except FileNotFoundError:
                messagebox.showwarning("File Not Found", f"File '{file_path}' not found.")
        else:
            pass
#            messagebox.showwarning("File Not Mapped", f"No file mapped for the selected option '{selected_option}'.")

    def show_about(self):
        messagebox.showinfo("About", "Hexxed BitHeadz - Midjourney Assistant Tool v1.1\n\n© 2024 Hexxed BitHeadz")

    def select_random(self):
        # Get the list of options from the dropdown
        style_options = self.dropdown["values"]

        # Select a random option from the dropdown
        random_option = random.choice(style_options)
        self.dropdown.set(random_option)

        # Update the label with the selected random option
        self.label_var.set(f"Selected Option: {random_option}")

        # Update listbox options based on the selected random option
        self.update_listbox_options(random_option)

        # Select a random item from the listbox
        listbox_items = self.listbox.get(0, tk.END)
        if listbox_items:
            random_item = random.choice(listbox_items)
            index = listbox_items.index(random_item)
            self.listbox.selection_clear(0, tk.END)  # Clear any previous selections
            self.listbox.selection_set(index)  # Set the new selection
            self.listbox.activate(index)  # Highlight the selected item
            self.listbox.see(index)  # Make sure the selected item is visible

def copySelection(self):
    # Get the selected text from the scrolled_text
    selected_text = self.scrolled_text.get("1.0", tk.END).strip()

    # Get the values of checkboxes and radio button
    no_people_checked = self.var1.get()
    tshirt_vector_checked = self.var2.get()
    logo_vector_checked = self.var3.get() 

    # Construct the final copied text
    copied_text = ""

    if tshirt_vector_checked:
        copied_text += "tshirt vector, black background, "

    if logo_vector_checked:
        copied_text += "logo vector, black background, "

    #copied_text += selected_text + ", " + self.dropdown.get() + " " + self.listbox.get(tk.ACTIVE) + " style, "
    copied_text += selected_text + ", " + self.dropdown.get() + " " + self.listbox.get(tk.ACTIVE) + " style, "

    if no_people_checked:
        copied_text += "--no people, woman, man"
        
    if self.radioStylize.get() == 1:
        copied_text += ", 8k, --ar 7:4 --s 0"
    elif self.radioStylize.get() == 2:
        copied_text += ", 8k, --ar 7:4 --s 250"
    elif self.radioStylize.get() == 3:
        copied_text += ", 8k, --ar 7:4 --s 500"
    elif self.radioStylize.get() == 4:
        copied_text += ", 8k, --ar 7:4 --s 750"
    elif self.radioStylize.get() == 5:
        copied_text += ", 8k, --ar 7:4 --s 1000"

    if self.radioChaos.get() == 1:
        copied_text += " --c 0"
    elif self.radioChaos.get() == 2:
        copied_text += " --c 25"
    elif self.radioChaos.get() == 3:
        copied_text += " --c 50"
    elif self.radioChaos.get() == 4:
        copied_text += " --c 100"

    # Append radio button option
    if self.radioMode.get() == 1:
        copied_text += " --niji 6"
    elif self.radioMode.get() == 2:
        copied_text += " --v 6"

    # Print or process the copied text as needed
    print(copied_text)
    # Add further processing as needed

    # Copy text2Copy to clipboard
    root.clipboard_clear()
    root.clipboard_append(copied_text)

    # Destroy previous labelCopy if it exists
    if hasattr(self, 'labelCopy'):
        self.labelCopy.destroy()

    # Make a label that displays the text2Copy
    self.labelCopy = tk.Label(self.root, text=copied_text, font=("Arial Bold", 12), wraplength=800)
    self.labelCopy.place(x=10, y=440)

    # Make the label background black, with green text
    self.labelCopy.config(bg="black", fg="green")

    # Make a label that says "Text copied to clipboard" and times out after 5 seconds
    labelCopied = tk.Label(self.root, text="Text copied to clipboard!", font=("Arial Bold", 12))
    labelCopied.place(x=640, y=480)

    # Make the label background black, with green text
    labelCopied.config(bg="black", fg="yellow")

    # Destroy labelCopied after 5 seconds
    labelCopied.after(3000, lambda: labelCopied.destroy())

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
