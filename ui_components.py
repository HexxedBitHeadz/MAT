"""UI components module for MAT."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
from typing import Callable, Optional, Dict, Any, List

class TooltipManager:
    """Manages tooltips for UI elements."""
    
    def __init__(self):
        self.tooltips = {}
    
    def add_tooltip(self, widget, text: str):
        """Add tooltip to a widget."""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.configure(bg="black")
            
            label = tk.Label(tooltip, text=text, bg="black", fg="yellow", 
                           font=("Arial", 9), padx=5, pady=2)
            label.pack()
            
            self.tooltips[widget] = tooltip
        
        def on_leave(event):
            if widget in self.tooltips:
                self.tooltips[widget].destroy()
                del self.tooltips[widget]
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

class StatusBar:
    """Status bar component for showing messages."""
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="black", height=25)
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.label = tk.Label(self.frame, text="Ready", bg="black", fg="green", 
                             font=("Arial", 10), anchor=tk.W)
        self.label.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.progress = ttk.Progressbar(self.frame, length=100, mode='determinate')
        self.progress.pack(side=tk.RIGHT, padx=5, pady=2)
        self.progress.pack_forget()  # Hide initially
        
        self.clear_timer = None
    
    def set_message(self, message: str, duration: int = 3000):
        """Set status message with optional auto-clear."""
        self.label.config(text=message)
        
        if self.clear_timer:
            self.label.after_cancel(self.clear_timer)
        
        if duration > 0:
            self.clear_timer = self.label.after(duration, lambda: self.set_message("Ready", 0))
    
    def show_progress(self, show: bool = True):
        """Show or hide progress bar."""
        if show:
            self.progress.pack(side=tk.RIGHT, padx=5, pady=2)
        else:
            self.progress.pack_forget()
    
    def set_progress(self, value: int):
        """Set progress bar value (0-100)."""
        self.progress['value'] = value

class SearchableListbox:
    """Enhanced listbox with search functionality."""
    
    def __init__(self, parent, items: List[str] = None, on_select: Callable = None):
        self.parent = parent
        self.items = items or []
        self.filtered_items = self.items.copy()
        self.on_select = on_select
        
        self.frame = tk.Frame(parent, bg="black")
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.frame, textvariable=self.search_var, 
                                   bg="black", fg="green", font=("Arial", 10))
        self.search_entry.pack(fill=tk.X, padx=2, pady=2)
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(self.frame, bg="black")
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.listbox = tk.Listbox(listbox_frame, bg="black", fg="green", 
                                 font=("Arial", 10), selectmode=tk.SINGLE)
        
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, 
                               command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.search_var.trace('w', self._on_search)
        self.listbox.bind('<<ListboxSelect>>', self._on_listbox_select)
        
        self._populate_listbox()
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)
    
    def place(self, **kwargs):
        """Place the frame."""
        self.frame.place(**kwargs)
    
    def set_items(self, items: List[str]):
        """Set listbox items."""
        self.items = items
        self.filtered_items = items.copy()
        self._populate_listbox()
    
    def get_selection(self) -> Optional[str]:
        """Get selected item."""
        selection = self.listbox.curselection()
        if selection:
            return self.filtered_items[selection[0]]
        return None
    
    def _on_search(self, *args):
        """Handle search text change."""
        search_term = self.search_var.get().lower()
        if search_term:
            self.filtered_items = [item for item in self.items 
                                 if search_term in item.lower()]
        else:
            self.filtered_items = self.items.copy()
        self._populate_listbox()
    
    def _populate_listbox(self):
        """Populate listbox with filtered items."""
        self.listbox.delete(0, tk.END)
        for item in self.filtered_items:
            self.listbox.insert(tk.END, item)
    
    def _on_listbox_select(self, event):
        """Handle listbox selection."""
        if self.on_select:
            selected = self.get_selection()
            if selected:
                self.on_select(selected)

class TabManager:
    """Manages notebook tabs for different functionalities."""
    
    def __init__(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.tabs = {}
        self.logger = logging.getLogger(__name__)
    
    def add_tab(self, name: str, widget: tk.Widget, text: str = None) -> None:
        """Add a tab to the notebook."""
        display_text = text or name
        self.notebook.add(widget, text=display_text)
        self.tabs[name] = widget
        self.logger.debug(f"Added tab: {name}")
    
    def get_tab(self, name: str) -> Optional[tk.Widget]:
        """Get tab widget by name."""
        return self.tabs.get(name)
    
    def select_tab(self, name: str) -> bool:
        """Select tab by name."""
        if name in self.tabs:
            widget = self.tabs[name]
            try:
                tab_id = self.notebook.index(widget)
                self.notebook.select(tab_id)
                return True
            except tk.TclError:
                self.logger.error(f"Tab not found: {name}")
        return False
    
    def pack(self, **kwargs):
        """Pack the notebook."""
        self.notebook.pack(**kwargs)

class AdvancedParameterFrame:
    """Advanced parameter controls for Midjourney."""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.LabelFrame(parent, text="Advanced Parameters", 
                                  bg="black", fg="green", font=("Arial", 12))
        
        self.vars = {}
        self._create_widgets()
    
    def _create_widgets(self):
        """Create parameter controls."""
        # Aspect ratio
        aspect_frame = tk.Frame(self.frame, bg="black")
        aspect_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(aspect_frame, text="Aspect Ratio:", bg="black", fg="green", 
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.vars['aspect_ratio'] = tk.StringVar(value="7:4")
        aspect_combo = ttk.Combobox(aspect_frame, textvariable=self.vars['aspect_ratio'],
                                  values=["1:1", "4:3", "16:9", "7:4", "2:3", "3:2", "9:16"],
                                  state="readonly", width=10)
        aspect_combo.pack(side=tk.RIGHT, padx=5)
        
        # Quality
        quality_frame = tk.Frame(self.frame, bg="black")
        quality_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(quality_frame, text="Quality:", bg="black", fg="green", 
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.vars['quality'] = tk.StringVar(value="1")
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.vars['quality'],
                                   values=["0.25", "0.5", "1", "2"], state="readonly", width=10)
        quality_combo.pack(side=tk.RIGHT, padx=5)
        
        # Seed
        seed_frame = tk.Frame(self.frame, bg="black")
        seed_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(seed_frame, text="Seed:", bg="black", fg="green", 
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.vars['seed'] = tk.StringVar()
        seed_entry = tk.Entry(seed_frame, textvariable=self.vars['seed'], 
                             bg="black", fg="green", width=15)
        seed_entry.pack(side=tk.RIGHT, padx=5)
        
        # Weird
        weird_frame = tk.Frame(self.frame, bg="black")
        weird_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(weird_frame, text="Weird:", bg="black", fg="green", 
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.vars['weird'] = tk.StringVar()
        weird_scale = tk.Scale(weird_frame, from_=0, to=3000, orient=tk.HORIZONTAL,
                              variable=self.vars['weird'], bg="black", fg="green",
                              highlightbackground="black", length=150)
        weird_scale.pack(side=tk.RIGHT, padx=5)
    
    def get_parameters(self) -> Dict[str, str]:
        """Get all parameter values."""
        params = {}
        for key, var in self.vars.items():
            value = var.get().strip()
            if value:
                params[key] = value
        return params
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)

class ThemeManager:
    """Manages application themes."""
    
    def __init__(self):
        self.themes = {
            "dark": {
                "bg": "black",
                "fg": "green",
                "select_bg": "#2d2d2d",
                "select_fg": "lime",
                "entry_bg": "black",
                "entry_fg": "green",
                "preview_fg": "#fefe00"
            },
            "light": {
                "bg": "white",
                "fg": "black",
                "select_bg": "#e6e6e6",
                "select_fg": "black",
                "entry_bg": "white",
                "entry_fg": "black",
                "preview_fg": "#0066cc"
            },
            "matrix": {
                "bg": "#001100",
                "fg": "#00ff00",
                "select_bg": "#003300",
                "select_fg": "#00ff00",
                "entry_bg": "#001100",
                "entry_fg": "#00ff00",
                "preview_fg": "#ffff00"
            }
        }
        self.current_theme = "dark"
    
    def get_theme(self, theme_name: str = None) -> Dict[str, str]:
        """Get theme colors."""
        theme_name = theme_name or self.current_theme
        return self.themes.get(theme_name, self.themes["dark"])
    
    def set_theme(self, theme_name: str) -> bool:
        """Set current theme."""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def get_available_themes(self) -> List[str]:
        """Get list of available themes."""
        return list(self.themes.keys())
    
    def apply_theme_to_widget(self, widget, theme_name: str = None):
        """Apply theme to a widget."""
        theme = self.get_theme(theme_name)
        try:
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        except tk.TclError:
            pass  # Some widgets don't support all options
