"""Enhanced Midjourney Assistant Tool v3.0 with comprehensive improvements."""
import os
import json
import random
import logging
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import Dict, List, Optional

# Import our new modules
from config_manager import ConfigManager, ConfigData
from style_manager import StyleManager
from prompt_manager import PromptManager, PromptTemplate, PromptHistoryItem
from ui_components import (TooltipManager, StatusBar, SearchableListbox, 
                          TabManager, AdvancedParameterFrame, ThemeManager)

class EnhancedMATGUI:
    """Enhanced Midjourney Assistant Tool with comprehensive improvements."""
    
    def __init__(self, root):
        self.root = root
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize managers
        self.base_path = os.path.dirname(__file__)
        self.config_manager = ConfigManager(os.path.join(self.base_path, "config.json"))
        self.style_manager = StyleManager(os.path.join(self.base_path, "Styles"))
        self.prompt_manager = PromptManager(os.path.join(self.base_path, "data"))
        self.theme_manager = ThemeManager()
        self.tooltip_manager = TooltipManager()
        
        # Load configuration
        self.config = self.config_manager.load_config()
        
        # Setup window
        self.setup_window()
        self.setup_theme()
        
        # UI Variables
        self.setup_variables()
        
        # Create UI
        self.create_main_ui()
        self.setup_keybindings()
        
        # Load initial data
        self.load_initial_data()
        
        # Start auto-save
        self.start_auto_save()
        
        self.logger.info("Enhanced MAT GUI initialized successfully")
    
    def setup_logging(self):
        """Setup logging configuration."""
        log_file = os.path.join(os.path.dirname(__file__), "mat.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def setup_window(self):
        """Setup main window properties."""
        self.root.title("Hexxed BitHeadz - Midjourney Assistant Tool v3.0 Enhanced")
        self.root.resizable(True, True)  # Allow resizing for better UX
        
        # Window geometry from config
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        if self.config.window_x and self.config.window_y:
            self.root.geometry(f"+{self.config.window_x}+{self.config.window_y}")
        else:
            # Center window
            self.center_window()
        
        # Window protocols
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        
        # Icon
        icon_path = os.path.join(self.base_path, "HeBi.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
    
    def center_window(self):
        """Center window on screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.config.window_width // 2)
        y = (screen_height // 2) - (self.config.window_height // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def setup_theme(self):
        """Setup application theme."""
        self.theme_manager.set_theme(self.config.theme)
        theme = self.theme_manager.get_theme()
        self.root.configure(bg=theme["bg"])
        
        # Configure ttk style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", foreground=theme["fg"], background=theme["bg"])
        self.style.configure("TCombobox", foreground=theme["fg"], background=theme["bg"])
    
    def setup_variables(self):
        """Setup UI variables."""
        # Radio button variables
        self.radio_mode = tk.IntVar(value=self.config.radioMode)
        self.radio_stylize = tk.IntVar(value=self.config.radioStylize)
        self.radio_chaos = tk.IntVar(value=self.config.radioChaos)
        
        # Checkbox variables
        self.check_vars = {}
        for i in range(1, 5):
            self.check_vars[i] = tk.IntVar(value=self.config.check_vars.get(str(i), 0))
        
        # Other variables
        self.repeat_var = tk.StringVar(value="none")
        self.current_style = tk.StringVar()
        self.search_term = tk.StringVar()
        
        # Advanced parameters
        self.advanced_params = {}
    
    def create_main_ui(self):
        """Create the main user interface with tabs."""
        # Create main frame
        main_frame = tk.Frame(self.root, bg=self.theme_manager.get_theme()["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tab manager
        self.tab_manager = TabManager(main_frame)
        
        # Create tabs
        self.create_prompt_tab()
        self.create_templates_tab()
        self.create_history_tab()
        self.create_settings_tab()
        
        self.tab_manager.pack(fill=tk.BOTH, expand=True)
        
        # Create status bar
        self.status_bar = StatusBar(self.root)
        self.status_bar.set_message("Enhanced MAT v3.0 Ready")
    
    def create_prompt_tab(self):
        """Create the main prompt creation tab."""
        prompt_frame = tk.Frame(self.root, bg=self.theme_manager.get_theme()["bg"])
        self.tab_manager.add_tab("prompt", prompt_frame, "Prompt Builder")
        
        # Main prompt text area
        prompt_text_frame = tk.LabelFrame(prompt_frame, text="Prompt Text", 
                                         bg=self.theme_manager.get_theme()["bg"], 
                                         fg=self.theme_manager.get_theme()["fg"])
        prompt_text_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.prompt_text = scrolledtext.ScrolledText(
            prompt_text_frame, height=4, wrap=tk.WORD, font=("Arial", 12),
            bg=self.theme_manager.get_theme()["entry_bg"],
            fg=self.theme_manager.get_theme()["entry_fg"],
            insertbackground=self.theme_manager.get_theme()["fg"]
        )
        self.prompt_text.pack(fill=tk.X, padx=5, pady=5)
        self.prompt_text.insert(tk.END, self.config.selected_text)
        
        # Create content frame for main controls
        content_frame = tk.Frame(prompt_frame, bg=self.theme_manager.get_theme()["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left side - Style selection
        self.create_style_selection(content_frame)
        
        # Middle - Parameters
        self.create_parameters_section(content_frame)
        
        # Right side - Actions
        self.create_actions_section(content_frame)
        
        # Bottom - Preview
        self.create_preview_section(prompt_frame)
        
        # Bind events for live preview
        self.setup_preview_bindings()
    
    def create_style_selection(self, parent):
        """Create style selection section."""
        style_frame = tk.LabelFrame(parent, text="Style Selection", 
                                   bg=self.theme_manager.get_theme()["bg"], 
                                   fg=self.theme_manager.get_theme()["fg"])
        style_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Category dropdown
        tk.Label(style_frame, text="Category:", bg=self.theme_manager.get_theme()["bg"], 
                fg=self.theme_manager.get_theme()["fg"]).pack(anchor=tk.W, padx=5, pady=2)
        
        self.category_combo = ttk.Combobox(style_frame, state="readonly", width=20)
        self.category_combo.pack(fill=tk.X, padx=5, pady=2)
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_change)
        
        # Searchable style listbox
        tk.Label(style_frame, text="Styles:", bg=self.theme_manager.get_theme()["bg"], 
                fg=self.theme_manager.get_theme()["fg"]).pack(anchor=tk.W, padx=5, pady=(10,2))
        
        self.style_listbox = SearchableListbox(style_frame, on_select=self.on_style_select)
        self.style_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        # Favorites section
        favorites_frame = tk.Frame(style_frame, bg=self.theme_manager.get_theme()["bg"])
        favorites_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.favorite_btn = tk.Button(favorites_frame, text="★", command=self.toggle_favorite,
                                     bg=self.theme_manager.get_theme()["bg"], 
                                     fg=self.theme_manager.get_theme()["fg"], font=("Arial", 12))
        self.favorite_btn.pack(side=tk.LEFT, padx=2)
        
        show_favorites_btn = tk.Button(favorites_frame, text="Show Favorites", 
                                      command=self.show_favorites,
                                      bg=self.theme_manager.get_theme()["bg"], 
                                      fg=self.theme_manager.get_theme()["fg"])
        show_favorites_btn.pack(side=tk.LEFT, padx=2)
        
        # Add tooltips
        self.tooltip_manager.add_tooltip(self.favorite_btn, "Add/Remove from favorites")
        self.tooltip_manager.add_tooltip(show_favorites_btn, "Show only favorite styles")
    
    def create_parameters_section(self, parent):
        """Create parameters selection section with scrollable content."""
        params_main_frame = tk.LabelFrame(parent, text="Parameters", 
                                         bg=self.theme_manager.get_theme()["bg"], 
                                         fg=self.theme_manager.get_theme()["fg"])
        params_main_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(params_main_frame, bg=self.theme_manager.get_theme()["bg"], 
                          highlightthickness=0, width=250, height=400)
        scrollbar = tk.Scrollbar(params_main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_params_frame = tk.Frame(canvas, bg=self.theme_manager.get_theme()["bg"])
        
        # Configure scrolling
        self.scrollable_params_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_params_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas only when mouse is over it
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        # Bind mouse enter/leave events for the canvas
        canvas.bind('<Enter>', _bind_mousewheel)
        canvas.bind('<Leave>', _unbind_mousewheel)
        
        # Also bind to the scrollable frame for better coverage
        self.scrollable_params_frame.bind('<Enter>', _bind_mousewheel)
        self.scrollable_params_frame.bind('<Leave>', _unbind_mousewheel)
        
        # Now create all the parameter controls in the scrollable frame
        params_frame = self.scrollable_params_frame
        
        # Checkboxes
        checkbox_options = [("No people", 1), ("T-shirt vector", 2), ("Logo vector", 3), ("Draft", 4)]
        for text, var_id in checkbox_options:
            chk = tk.Checkbutton(params_frame, text=text, variable=self.check_vars[var_id],
                               bg=self.theme_manager.get_theme()["bg"], 
                               fg=self.theme_manager.get_theme()["fg"])
            chk.pack(anchor=tk.W, padx=5, pady=2)
            
            if text == "Draft":
                self.draft_chk = chk
                self.check_vars[var_id].trace("w", self.on_draft_toggle)
        
        # Mode selection
        self.create_radio_group(params_frame, "Mode", 
                               [(1, "Niji"), (2, "Midjourney")], self.radio_mode)
        
        # Stylize selection
        self.create_radio_group(params_frame, "Stylize", 
                               [(1, "0"), (2, "250"), (3, "500"), (4, "750"), (5, "1000")], 
                               self.radio_stylize)
        
        # Chaos selection
        self.create_radio_group(params_frame, "Chaos", 
                               [(1, "0"), (2, "25"), (3, "50"), (4, "100")], 
                               self.radio_chaos)
        
        # Repeat option
        tk.Label(params_frame, text="Repeat:", bg=self.theme_manager.get_theme()["bg"], 
                fg=self.theme_manager.get_theme()["fg"]).pack(anchor=tk.W, padx=5, pady=(10,2))
        
        repeat_combo = ttk.Combobox(params_frame, textvariable=self.repeat_var, 
                                   values=["none", "3", "6", "10"], state="readonly", width=10)
        repeat_combo.pack(padx=5, pady=2)
        
        # Advanced parameters
        self.advanced_frame = AdvancedParameterFrame(params_frame)
        self.advanced_frame.pack(fill=tk.X, padx=5, pady=10)
    
    def create_radio_group(self, parent, label, options, variable):
        """Create a group of radio buttons."""
        frame = tk.LabelFrame(parent, text=label, 
                             bg=self.theme_manager.get_theme()["bg"], 
                             fg=self.theme_manager.get_theme()["fg"])
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        radio_buttons = []
        for val, text in options:
            rb = tk.Radiobutton(frame, text=text, variable=variable, value=val,
                              bg=self.theme_manager.get_theme()["bg"], 
                              fg=self.theme_manager.get_theme()["fg"])
            rb.pack(anchor=tk.W, padx=5, pady=1)
            radio_buttons.append(rb)
        
        if label == "Mode":
            self.radio_mode_buttons = radio_buttons
            variable.trace("w", self.on_mode_change)
    
    def create_actions_section(self, parent):
        """Create actions section."""
        actions_frame = tk.LabelFrame(parent, text="Actions", 
                                     bg=self.theme_manager.get_theme()["bg"], 
                                     fg=self.theme_manager.get_theme()["fg"])
        actions_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        # Main action buttons
        buttons = [
            ("Random Style", self.select_random, "Ctrl+R"),
            ("Clear All", self.clear_all, "Ctrl+Alt+C"),
            ("Copy Prompt", self.copy_prompt, "Ctrl+C"),
            ("Save Template", self.save_as_template, "Ctrl+T"),
            ("Validate", self.validate_prompt, "Ctrl+V")
        ]
        
        for text, command, shortcut in buttons:
            btn = tk.Button(actions_frame, text=text, command=command,
                           bg=self.theme_manager.get_theme()["bg"], 
                           fg=self.theme_manager.get_theme()["fg"], width=15)
            btn.pack(padx=5, pady=3, fill=tk.X)
            self.tooltip_manager.add_tooltip(btn, f"Shortcut: {shortcut}")
        
        # Quick actions
        quick_frame = tk.LabelFrame(actions_frame, text="Quick Actions",
                                   bg=self.theme_manager.get_theme()["bg"], 
                                   fg=self.theme_manager.get_theme()["fg"])
        quick_frame.pack(fill=tk.X, padx=5, pady=10)
        
        quick_buttons = [
            ("Export History", self.export_history),
            ("Import Styles", self.import_styles),
            ("Settings", lambda: self.tab_manager.select_tab("settings"))
        ]
        
        for text, command in quick_buttons:
            btn = tk.Button(quick_frame, text=text, command=command,
                           bg=self.theme_manager.get_theme()["bg"], 
                           fg=self.theme_manager.get_theme()["fg"], width=15)
            btn.pack(padx=2, pady=2, fill=tk.X)
    
    def create_preview_section(self, parent):
        """Create preview section."""
        preview_frame = tk.LabelFrame(parent, text="Prompt Preview", 
                                     bg=self.theme_manager.get_theme()["bg"], 
                                     fg=self.theme_manager.get_theme()["fg"])
        preview_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame, height=4, wrap=tk.WORD, state="disabled",
            bg=self.theme_manager.get_theme()["bg"], 
            fg=self.theme_manager.get_theme()["preview_fg"], font=("Arial", 11)
        )
        self.preview_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Validation display
        self.validation_frame = tk.Frame(preview_frame, bg=self.theme_manager.get_theme()["bg"])
        self.validation_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.validation_label = tk.Label(self.validation_frame, text="", 
                                        bg=self.theme_manager.get_theme()["bg"], 
                                        fg="orange", font=("Arial", 9))
        self.validation_label.pack(side=tk.LEFT)
    
    def create_templates_tab(self):
        """Create templates management tab."""
        templates_frame = tk.Frame(self.root, bg=self.theme_manager.get_theme()["bg"])
        self.tab_manager.add_tab("templates", templates_frame, "Templates")
        
        # Templates list
        list_frame = tk.LabelFrame(templates_frame, text="Saved Templates",
                                  bg=self.theme_manager.get_theme()["bg"], 
                                  fg=self.theme_manager.get_theme()["fg"])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.templates_listbox = SearchableListbox(list_frame, on_select=self.on_template_select)
        self.templates_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Template details
        details_frame = tk.LabelFrame(templates_frame, text="Template Details",
                                     bg=self.theme_manager.get_theme()["bg"], 
                                     fg=self.theme_manager.get_theme()["fg"])
        details_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Template name
        tk.Label(details_frame, text="Name:", bg=self.theme_manager.get_theme()["bg"], 
                fg=self.theme_manager.get_theme()["fg"]).pack(anchor=tk.W, padx=5, pady=2)
        
        self.template_name_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=self.template_name_var, width=30,
                bg=self.theme_manager.get_theme()["entry_bg"], 
                fg=self.theme_manager.get_theme()["entry_fg"]).pack(padx=5, pady=2)
        
        # Template description
        tk.Label(details_frame, text="Description:", bg=self.theme_manager.get_theme()["bg"], 
                fg=self.theme_manager.get_theme()["fg"]).pack(anchor=tk.W, padx=5, pady=2)
        
        self.template_desc_text = scrolledtext.ScrolledText(details_frame, height=3, width=30,
                                                           bg=self.theme_manager.get_theme()["entry_bg"], 
                                                           fg=self.theme_manager.get_theme()["entry_fg"])
        self.template_desc_text.pack(padx=5, pady=2)
        
        # Template content
        tk.Label(details_frame, text="Template:", bg=self.theme_manager.get_theme()["bg"], 
                fg=self.theme_manager.get_theme()["fg"]).pack(anchor=tk.W, padx=5, pady=2)
        
        self.template_content_text = scrolledtext.ScrolledText(details_frame, height=8, width=30,
                                                              bg=self.theme_manager.get_theme()["entry_bg"], 
                                                              fg=self.theme_manager.get_theme()["entry_fg"])
        self.template_content_text.pack(padx=5, pady=2)
        
        # Template actions
        template_actions = tk.Frame(details_frame, bg=self.theme_manager.get_theme()["bg"])
        template_actions.pack(fill=tk.X, padx=5, pady=10)
        
        tk.Button(template_actions, text="Save Template", command=self.save_template,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT, padx=2)
        
        tk.Button(template_actions, text="Load Template", command=self.load_template,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT, padx=2)
        
        tk.Button(template_actions, text="Delete Template", command=self.delete_template,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT, padx=2)
    
    def create_history_tab(self):
        """Create history management tab."""
        history_frame = tk.Frame(self.root, bg=self.theme_manager.get_theme()["bg"])
        self.tab_manager.add_tab("history", history_frame, "History")
        
        # History list
        list_frame = tk.LabelFrame(history_frame, text="Prompt History",
                                  bg=self.theme_manager.get_theme()["bg"], 
                                  fg=self.theme_manager.get_theme()["fg"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Search and filter
        search_frame = tk.Frame(list_frame, bg=self.theme_manager.get_theme()["bg"])
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(search_frame, text="Search:", bg=self.theme_manager.get_theme()["bg"], 
                fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT)
        
        self.history_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.history_search_var,
                               bg=self.theme_manager.get_theme()["entry_bg"], 
                               fg=self.theme_manager.get_theme()["entry_fg"])
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Button(search_frame, text="Search", command=self.search_history,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.RIGHT)
        
        # History listbox
        history_list_frame = tk.Frame(list_frame, bg=self.theme_manager.get_theme()["bg"])
        history_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.history_listbox = tk.Listbox(history_list_frame, 
                                         bg=self.theme_manager.get_theme()["bg"], 
                                         fg=self.theme_manager.get_theme()["fg"])
        
        history_scrollbar = tk.Scrollbar(history_list_frame, orient=tk.VERTICAL, 
                                        command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)
        self.history_listbox.bind("<Double-Button-1>", self.load_from_history)
        
        # History actions
        history_actions = tk.Frame(list_frame, bg=self.theme_manager.get_theme()["bg"])
        history_actions.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(history_actions, text="Load to Editor", command=self.load_from_history,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT, padx=2)
        
        tk.Button(history_actions, text="Copy", command=self.copy_from_history,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT, padx=2)
        
        tk.Button(history_actions, text="Clear History", command=self.clear_history,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.RIGHT, padx=2)
    
    def create_settings_tab(self):
        """Create settings tab."""
        settings_frame = tk.Frame(self.root, bg=self.theme_manager.get_theme()["bg"])
        self.tab_manager.add_tab("settings", settings_frame, "Settings")
        
        # Theme settings
        theme_frame = tk.LabelFrame(settings_frame, text="Appearance",
                                   bg=self.theme_manager.get_theme()["bg"], 
                                   fg=self.theme_manager.get_theme()["fg"])
        theme_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(theme_frame, text="Theme:", bg=self.theme_manager.get_theme()["bg"], 
                fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT, padx=5)
        
        self.theme_var = tk.StringVar(value=self.config.theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                  values=self.theme_manager.get_available_themes(),
                                  state="readonly")
        theme_combo.pack(side=tk.LEFT, padx=5)
        theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)
        
        # Auto-save settings
        autosave_frame = tk.LabelFrame(settings_frame, text="Auto-save",
                                      bg=self.theme_manager.get_theme()["bg"], 
                                      fg=self.theme_manager.get_theme()["fg"])
        autosave_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(autosave_frame, text="Interval (seconds):", 
                bg=self.theme_manager.get_theme()["bg"], 
                fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT, padx=5)
        
        self.autosave_var = tk.IntVar(value=self.config.auto_save_interval // 1000)
        autosave_spin = tk.Spinbox(autosave_frame, from_=5, to=60, 
                                  textvariable=self.autosave_var, width=5,
                                  bg=self.theme_manager.get_theme()["entry_bg"], 
                                  fg=self.theme_manager.get_theme()["entry_fg"])
        autosave_spin.pack(side=tk.LEFT, padx=5)
        
        # Settings actions
        settings_actions = tk.Frame(settings_frame, bg=self.theme_manager.get_theme()["bg"])
        settings_actions.pack(fill=tk.X, padx=10, pady=20)
        
        tk.Button(settings_actions, text="Save Settings", command=self.save_settings,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT, padx=5)
        
        tk.Button(settings_actions, text="Reset to Defaults", command=self.reset_settings,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.LEFT, padx=5)
        
        tk.Button(settings_actions, text="Open Data Folder", command=self.open_data_folder,
                 bg=self.theme_manager.get_theme()["bg"], 
                 fg=self.theme_manager.get_theme()["fg"]).pack(side=tk.RIGHT, padx=5)
    
    def setup_keybindings(self):
        """Setup keyboard shortcuts."""
        bindings = [
            ("<Control-c>", self.copy_prompt),
            ("<Control-s>", self.save_settings),
            ("<Control-r>", self.select_random),
            ("<Control-t>", self.save_as_template),
            ("<Control-v>", self.validate_prompt),
            ("<Control-Alt-c>", self.clear_all),
            ("<F5>", self.refresh_data)
        ]
        
        for key, command in bindings:
            self.root.bind(key, lambda e, cmd=command: cmd())
    
    def setup_preview_bindings(self):
        """Setup bindings for live preview updates."""
        # Text changes
        self.prompt_text.bind("<<Modified>>", self.on_text_change)
        
        # Variable traces
        for var in [self.radio_mode, self.radio_stylize, self.radio_chaos, self.repeat_var]:
            var.trace("w", self.update_preview)
        
        for var in self.check_vars.values():
            var.trace("w", self.update_preview)
    
    def load_initial_data(self):
        """Load initial data into UI components."""
        # Load categories
        categories = self.style_manager.get_categories()
        self.category_combo['values'] = categories
        if self.config.dropdown in categories:
            self.category_combo.set(self.config.dropdown)
            self.on_category_change()
        
        # Load templates
        self.refresh_templates_list()
        
        # Load history
        self.refresh_history_list()
        
        # Update preview
        self.update_preview()
    
    def start_auto_save(self):
        """Start auto-save timer."""
        self.auto_save()
        self.root.after(self.config.auto_save_interval, self.start_auto_save)
    
    # Event handlers
    def on_category_change(self, event=None):
        """Handle category selection change."""
        category = self.category_combo.get()
        if category:
            styles = self.style_manager.get_styles_for_category(category)
            self.style_listbox.set_items(styles)
            self.status_bar.set_message(f"Loaded {len(styles)} styles from {category}")
            self.update_preview()
    
    def on_style_select(self, style):
        """Handle style selection."""
        self.current_style.set(style)
        self.style_manager.increment_usage(style)
        
        # Update favorite button
        if self.style_manager.is_favorite(style):
            self.favorite_btn.config(text="★", fg="gold")
        else:
            self.favorite_btn.config(text="☆", fg=self.theme_manager.get_theme()["fg"])
        
        self.update_preview()
    
    def on_mode_change(self, *args):
        """Handle mode change (disable draft for Niji)."""
        if self.radio_mode.get() == 1:  # Niji
            self.draft_chk.config(state=tk.DISABLED)
            self.check_vars[4].set(0)
        else:
            self.draft_chk.config(state=tk.NORMAL)
        self.update_preview()
    
    def on_draft_toggle(self, *args):
        """Handle draft toggle (force Midjourney)."""
        if self.check_vars[4].get():
            self.radio_mode.set(2)  # Force Midjourney
            for rb in self.radio_mode_buttons:
                if rb["text"] == "Niji":
                    rb.config(state=tk.DISABLED)
        else:
            for rb in self.radio_mode_buttons:
                if rb["text"] == "Niji":
                    rb.config(state=tk.NORMAL)
        self.update_preview()
    
    def on_text_change(self, event=None):
        """Handle text area changes."""
        if self.prompt_text.edit_modified():
            self.update_preview()
            self.prompt_text.edit_modified(False)
    
    def on_template_select(self, template_name):
        """Handle template selection."""
        template = self.prompt_manager.get_template(template_name)
        if template:
            self.template_name_var.set(template.name)
            self.template_desc_text.delete("1.0", tk.END)
            self.template_desc_text.insert(tk.END, template.description)
            self.template_content_text.delete("1.0", tk.END)
            self.template_content_text.insert(tk.END, template.template)
    
    def on_history_select(self, event=None):
        """Handle history selection."""
        pass  # Preview could be shown here
    
    def on_theme_change(self, event=None):
        """Handle theme change."""
        new_theme = self.theme_var.get()
        if self.theme_manager.set_theme(new_theme):
            self.status_bar.set_message(f"Theme changed to {new_theme}. Restart recommended for full effect.")
    
    # Core functionality methods
    def build_prompt(self) -> str:
        """Build the complete prompt from current UI state."""
        try:
            prompt = self.prompt_text.get("1.0", tk.END).strip()
            
            # Add selected style
            selected_style = self.current_style.get()
            if selected_style:
                prompt += f", {selected_style} style"
            
            # Add checkbox parameters
            if self.check_vars[1].get():
                prompt += ", no people, woman, man"
            if self.check_vars[2].get():
                prompt += ", tshirt vector, black background"
            if self.check_vars[3].get():
                prompt += ", logo vector, black background"
            if self.check_vars[4].get():
                prompt += " --draft"
            
            # Add radio button parameters
            stylize_map = {1: " --s 0", 2: " --s 250", 3: " --s 500", 4: " --s 750", 5: " --s 1000"}
            chaos_map = {1: " --c 0", 2: " --c 25", 3: " --c 50", 4: " --c 100"}
            mode_map = {1: " --niji 6", 2: " --v 7"}
            
            if self.radio_stylize.get() in stylize_map:
                prompt += stylize_map[self.radio_stylize.get()]
            if self.radio_chaos.get() in chaos_map:
                prompt += chaos_map[self.radio_chaos.get()]
            if self.radio_mode.get() in mode_map:
                prompt += mode_map[self.radio_mode.get()]
            
            # Add advanced parameters
            advanced_params = self.advanced_frame.get_parameters()
            if 'aspect_ratio' in advanced_params and advanced_params['aspect_ratio'] != "7:4":
                prompt += f" --ar {advanced_params['aspect_ratio']}"
            elif self.radio_mode.get() in mode_map:
                prompt += " --ar 7:4"  # Default aspect ratio
            
            if 'quality' in advanced_params and advanced_params['quality'] != "1":
                prompt += f" --q {advanced_params['quality']}"
            
            if 'seed' in advanced_params:
                prompt += f" --seed {advanced_params['seed']}"
            
            if 'weird' in advanced_params and int(advanced_params['weird']) > 0:
                prompt += f" --weird {advanced_params['weird']}"
            
            # Add repeat parameter
            if self.repeat_var.get() != "none":
                prompt += f" --repeat {self.repeat_var.get()}"
            
            return prompt
            
        except Exception as e:
            self.logger.error(f"Error building prompt: {e}")
            return ""
    
    def update_preview(self, *args):
        """Update the preview display."""
        try:
            prompt = self.build_prompt()
            
            self.preview_text.config(state="normal")
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert(tk.END, prompt)
            self.preview_text.config(state="disabled")
            
            # Validate and show issues
            issues = self.prompt_manager.validate_prompt(prompt)
            if issues:
                self.validation_label.config(text=f"⚠ {len(issues)} issues found", fg="orange")
                self.tooltip_manager.add_tooltip(self.validation_label, "\\n".join(issues))
            else:
                self.validation_label.config(text="✓ Prompt looks good", fg="green")
                
        except Exception as e:
            self.logger.error(f"Error updating preview: {e}")
    
    def select_random(self):
        """Select random style."""
        try:
            categories = self.style_manager.get_categories()
            if not categories:
                return
            
            # Select random category
            random_category = random.choice(categories)
            self.category_combo.set(random_category)
            self.on_category_change()
            
            # Select random style from category
            styles = self.style_manager.get_styles_for_category(random_category)
            if styles:
                random_style = random.choice(styles)
                self.current_style.set(random_style)
                # Update the listbox selection
                self.style_listbox.listbox.selection_clear(0, tk.END)
                try:
                    index = self.style_listbox.filtered_items.index(random_style)
                    self.style_listbox.listbox.selection_set(index)
                    self.style_listbox.listbox.see(index)
                except ValueError:
                    pass
                
                self.on_style_select(random_style)
                self.status_bar.set_message(f"Random style selected: {random_style}")
                
        except Exception as e:
            self.logger.error(f"Error selecting random style: {e}")
            messagebox.showerror("Error", f"Failed to select random style: {e}")
    
    def copy_prompt(self):
        """Copy current prompt to clipboard."""
        try:
            prompt = self.build_prompt()
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt)
            self.root.update()
            
            # Add to history
            current_style = self.current_style.get()
            parameters = {
                "mode": self.radio_mode.get(),
                "stylize": self.radio_stylize.get(),
                "chaos": self.radio_chaos.get(),
                "repeat": self.repeat_var.get()
            }
            
            self.prompt_manager.add_to_history(prompt, current_style, parameters)
            self.refresh_history_list()
            
            self.status_bar.set_message("Prompt copied to clipboard!")
            
        except Exception as e:
            self.logger.error(f"Error copying prompt: {e}")
            messagebox.showerror("Error", f"Failed to copy prompt: {e}")
    
    def clear_all(self):
        """Clear all inputs."""
        try:
            self.prompt_text.delete("1.0", tk.END)
            self.category_combo.set("")
            self.style_listbox.set_items([])
            self.current_style.set("")
            
            for var in self.check_vars.values():
                var.set(0)
            
            self.radio_mode.set(0)
            self.radio_stylize.set(0)
            self.radio_chaos.set(0)
            self.repeat_var.set("none")
            
            # Clear advanced parameters
            for var in self.advanced_frame.vars.values():
                var.set("")
            
            self.update_preview()
            self.status_bar.set_message("All fields cleared")
            
        except Exception as e:
            self.logger.error(f"Error clearing fields: {e}")
    
    def validate_prompt(self):
        """Validate current prompt and show detailed results."""
        try:
            prompt = self.build_prompt()
            issues = self.prompt_manager.validate_prompt(prompt)
            
            if issues:
                message = "Prompt Issues Found:\\n\\n" + "\\n".join(f"• {issue}" for issue in issues)
                messagebox.showwarning("Prompt Validation", message)
            else:
                messagebox.showinfo("Prompt Validation", "✓ Prompt looks good! No issues found.")
                
        except Exception as e:
            self.logger.error(f"Error validating prompt: {e}")
            messagebox.showerror("Error", f"Failed to validate prompt: {e}")
    
    def save_as_template(self):
        """Save current prompt as template."""
        try:
            prompt = self.build_prompt()
            if not prompt.strip():
                messagebox.showwarning("Warning", "Cannot save empty prompt as template")
                return
            
            # Switch to templates tab and populate fields
            self.tab_manager.select_tab("templates")
            self.template_name_var.set(f"Template {len(self.prompt_manager.get_templates()) + 1}")
            self.template_content_text.delete("1.0", tk.END)
            self.template_content_text.insert(tk.END, prompt)
            
            self.status_bar.set_message("Ready to save template")
            
        except Exception as e:
            self.logger.error(f"Error preparing template: {e}")
            messagebox.showerror("Error", f"Failed to prepare template: {e}")
    
    def save_template(self):
        """Save template from templates tab."""
        try:
            name = self.template_name_var.get().strip()
            description = self.template_desc_text.get("1.0", tk.END).strip()
            template_text = self.template_content_text.get("1.0", tk.END).strip()
            
            if not name or not template_text:
                messagebox.showwarning("Warning", "Name and template content are required")
                return
            
            template = PromptTemplate(name=name, template=template_text, description=description)
            
            if self.prompt_manager.save_template(template):
                self.refresh_templates_list()
                self.status_bar.set_message(f"Template '{name}' saved successfully")
            else:
                messagebox.showerror("Error", "Failed to save template")
                
        except Exception as e:
            self.logger.error(f"Error saving template: {e}")
            messagebox.showerror("Error", f"Failed to save template: {e}")
    
    def load_template(self):
        """Load selected template to main editor."""
        try:
            template_name = self.templates_listbox.get_selection()
            if not template_name:
                messagebox.showwarning("Warning", "Please select a template to load")
                return
            
            template = self.prompt_manager.get_template(template_name)
            if template:
                self.prompt_text.delete("1.0", tk.END)
                self.prompt_text.insert(tk.END, template.template)
                self.tab_manager.select_tab("prompt")
                self.update_preview()
                self.status_bar.set_message(f"Template '{template_name}' loaded")
            
        except Exception as e:
            self.logger.error(f"Error loading template: {e}")
            messagebox.showerror("Error", f"Failed to load template: {e}")
    
    def delete_template(self):
        """Delete selected template."""
        try:
            template_name = self.templates_listbox.get_selection()
            if not template_name:
                messagebox.showwarning("Warning", "Please select a template to delete")
                return
            
            if messagebox.askyesno("Confirm Delete", f"Delete template '{template_name}'?"):
                if self.prompt_manager.delete_template(template_name):
                    self.refresh_templates_list()
                    self.template_name_var.set("")
                    self.template_desc_text.delete("1.0", tk.END)
                    self.template_content_text.delete("1.0", tk.END)
                    self.status_bar.set_message(f"Template '{template_name}' deleted")
                else:
                    messagebox.showerror("Error", "Failed to delete template")
                    
        except Exception as e:
            self.logger.error(f"Error deleting template: {e}")
            messagebox.showerror("Error", f"Failed to delete template: {e}")
    
    def toggle_favorite(self):
        """Toggle favorite status of current style."""
        try:
            style = self.current_style.get()
            if not style:
                return
            
            if self.style_manager.is_favorite(style):
                self.style_manager.remove_favorite(style)
                self.favorite_btn.config(text="☆", fg=self.theme_manager.get_theme()["fg"])
                self.status_bar.set_message(f"Removed '{style}' from favorites")
            else:
                self.style_manager.add_favorite(style)
                self.favorite_btn.config(text="★", fg="gold")
                self.status_bar.set_message(f"Added '{style}' to favorites")
                
        except Exception as e:
            self.logger.error(f"Error toggling favorite: {e}")
    
    def show_favorites(self):
        """Show only favorite styles."""
        try:
            favorites = self.style_manager.get_favorites()
            self.style_listbox.set_items(favorites)
            self.category_combo.set("Favorites")
            self.status_bar.set_message(f"Showing {len(favorites)} favorite styles")
            
        except Exception as e:
            self.logger.error(f"Error showing favorites: {e}")
    
    def search_history(self):
        """Search prompt history."""
        try:
            search_term = self.history_search_var.get()
            if search_term.strip():
                results = self.prompt_manager.search_history(search_term)
            else:
                results = self.prompt_manager.get_history()
            
            self.history_listbox.delete(0, tk.END)
            for item in results:
                timestamp = item.timestamp[:19].replace('T', ' ')  # Format timestamp
                display_text = f"[{timestamp}] {item.prompt[:80]}..."
                self.history_listbox.insert(tk.END, display_text)
            
            self.status_bar.set_message(f"Found {len(results)} history items")
            
        except Exception as e:
            self.logger.error(f"Error searching history: {e}")
    
    def load_from_history(self, event=None):
        """Load selected history item to editor."""
        try:
            selection = self.history_listbox.curselection()
            if not selection:
                return
            
            history_items = self.prompt_manager.get_history()
            if selection[0] < len(history_items):
                item = history_items[selection[0]]
                self.prompt_text.delete("1.0", tk.END)
                self.prompt_text.insert(tk.END, item.prompt)
                self.tab_manager.select_tab("prompt")
                self.update_preview()
                self.status_bar.set_message("History item loaded to editor")
                
        except Exception as e:
            self.logger.error(f"Error loading from history: {e}")
    
    def copy_from_history(self):
        """Copy selected history item to clipboard."""
        try:
            selection = self.history_listbox.curselection()
            if not selection:
                return
            
            history_items = self.prompt_manager.get_history()
            if selection[0] < len(history_items):
                item = history_items[selection[0]]
                self.root.clipboard_clear()
                self.root.clipboard_append(item.prompt)
                self.root.update()
                self.status_bar.set_message("History item copied to clipboard")
                
        except Exception as e:
            self.logger.error(f"Error copying from history: {e}")
    
    def clear_history(self):
        """Clear prompt history."""
        try:
            if messagebox.askyesno("Confirm Clear", "Clear all prompt history?"):
                if self.prompt_manager.clear_history():
                    self.refresh_history_list()
                    self.status_bar.set_message("History cleared")
                else:
                    messagebox.showerror("Error", "Failed to clear history")
                    
        except Exception as e:
            self.logger.error(f"Error clearing history: {e}")
    
    def export_history(self):
        """Export history to file."""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export History",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                format_type = "json" if file_path.endswith('.json') else "txt"
                if self.prompt_manager.export_history(file_path, format_type):
                    self.status_bar.set_message(f"History exported to {file_path}")
                else:
                    messagebox.showerror("Error", "Failed to export history")
                    
        except Exception as e:
            self.logger.error(f"Error exporting history: {e}")
            messagebox.showerror("Error", f"Failed to export history: {e}")
    
    def import_styles(self):
        """Import styles from file."""
        # This would be implemented based on specific requirements
        messagebox.showinfo("Feature", "Style import feature coming soon!")
    
    def save_settings(self):
        """Save current settings."""
        try:
            # Update config with current values
            self.config.selected_text = self.prompt_text.get("1.0", tk.END).strip()
            self.config.dropdown = self.category_combo.get()
            self.config.radioMode = self.radio_mode.get()
            self.config.radioStylize = self.radio_stylize.get()
            self.config.radioChaos = self.radio_chaos.get()
            self.config.check_vars = {str(k): v.get() for k, v in self.check_vars.items()}
            self.config.theme = self.theme_var.get()
            self.config.auto_save_interval = self.autosave_var.get() * 1000
            
            # Save window position and size
            geometry = self.root.geometry()
            size_part, pos_part = geometry.split('+', 1)
            width, height = map(int, size_part.split('x'))
            x, y = map(int, pos_part.split('+'))
            
            self.config.window_width = width
            self.config.window_height = height
            self.config.window_x = x
            self.config.window_y = y
            
            if self.config_manager.save_config(self.config):
                self.status_bar.set_message("Settings saved successfully")
            else:
                messagebox.showerror("Error", "Failed to save settings")
                
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def reset_settings(self):
        """Reset settings to defaults."""
        try:
            if messagebox.askyesno("Confirm Reset", "Reset all settings to defaults?"):
                self.config = ConfigData()  # Create new default config
                self.theme_var.set(self.config.theme)
                self.autosave_var.set(self.config.auto_save_interval // 1000)
                self.status_bar.set_message("Settings reset to defaults")
                
        except Exception as e:
            self.logger.error(f"Error resetting settings: {e}")
    
    def open_data_folder(self):
        """Open data folder in file explorer."""
        try:
            data_folder = os.path.join(self.base_path, "data")
            os.makedirs(data_folder, exist_ok=True)
            
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{data_folder}"')
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", data_folder])
            else:  # Linux
                subprocess.Popen(["xdg-open", data_folder])
                
        except Exception as e:
            self.logger.error(f"Error opening data folder: {e}")
            messagebox.showerror("Error", f"Failed to open data folder: {e}")
    
    def refresh_data(self):
        """Refresh all data (F5)."""
        try:
            self.style_manager.clear_cache()
            self.load_initial_data()
            self.status_bar.set_message("Data refreshed")
            
        except Exception as e:
            self.logger.error(f"Error refreshing data: {e}")
    
    def refresh_templates_list(self):
        """Refresh templates list."""
        try:
            templates = self.prompt_manager.get_templates()
            template_names = [t.name for t in templates]
            self.templates_listbox.set_items(template_names)
            
        except Exception as e:
            self.logger.error(f"Error refreshing templates: {e}")
    
    def refresh_history_list(self):
        """Refresh history list."""
        try:
            history_items = self.prompt_manager.get_history(50)  # Last 50 items
            self.history_listbox.delete(0, tk.END)
            
            for item in history_items:
                timestamp = item.timestamp[:19].replace('T', ' ')  # Format timestamp
                display_text = f"[{timestamp}] {item.prompt[:80]}..."
                self.history_listbox.insert(tk.END, display_text)
                
        except Exception as e:
            self.logger.error(f"Error refreshing history: {e}")
    
    def auto_save(self):
        """Auto-save current state."""
        try:
            # Auto-save current prompt
            autosave_path = os.path.join(self.base_path, "autosave_prompt.txt")
            with open(autosave_path, 'w', encoding='utf-8') as file:
                file.write(self.build_prompt())
            
            # Auto-save configuration
            self.save_settings()
            
        except Exception as e:
            self.logger.error(f"Error in auto-save: {e}")
    
    def on_exit(self):
        """Handle application exit."""
        try:
            self.auto_save()
            self.logger.info("Application exiting")
            self.root.destroy()
            
        except Exception as e:
            self.logger.error(f"Error during exit: {e}")
            self.root.destroy()

def main():
    """Main application entry point."""
    try:
        root = tk.Tk()
        app = EnhancedMATGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
