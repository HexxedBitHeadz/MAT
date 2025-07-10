"""Prompt management module for MAT."""
import os
import json
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class PromptTemplate:
    """Represents a prompt template."""
    name: str
    template: str
    description: str = ""
    tags: List[str] = None
    created_at: str = ""
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

@dataclass
class PromptHistoryItem:
    """Represents a prompt history item."""
    prompt: str
    timestamp: str
    style_used: str = ""
    parameters: Dict[str, any] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class PromptManager:
    """Manages prompt templates, history, and operations."""
    
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        self.logger = logging.getLogger(__name__)
        self.templates_file = os.path.join(data_folder, "prompt_templates.json")
        self.history_file = os.path.join(data_folder, "prompt_history.json")
        self.log_file = os.path.join(data_folder, "prompt_log.txt")
        
        # Ensure data folder exists
        os.makedirs(data_folder, exist_ok=True)
        
        self._templates: List[PromptTemplate] = []
        self._history: List[PromptHistoryItem] = []
        self._load_templates()
        self._load_history()
    
    def save_template(self, template: PromptTemplate) -> bool:
        """Save a prompt template."""
        try:
            # Check if template with same name exists
            existing_index = next(
                (i for i, t in enumerate(self._templates) if t.name == template.name),
                None
            )
            
            if existing_index is not None:
                self._templates[existing_index] = template
            else:
                self._templates.append(template)
            
            self._save_templates()
            self.logger.info(f"Template '{template.name}' saved successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save template: {e}")
            return False
    
    def delete_template(self, name: str) -> bool:
        """Delete a prompt template."""
        try:
            self._templates = [t for t in self._templates if t.name != name]
            self._save_templates()
            self.logger.info(f"Template '{name}' deleted successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete template: {e}")
            return False
    
    def get_templates(self) -> List[PromptTemplate]:
        """Get all prompt templates."""
        return self._templates.copy()
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get a specific template by name."""
        return next((t for t in self._templates if t.name == name), None)
    
    def search_templates(self, search_term: str) -> List[PromptTemplate]:
        """Search templates by name, description, or tags."""
        if not search_term.strip():
            return self._templates.copy()
        
        search_term = search_term.lower()
        results = []
        
        for template in self._templates:
            if (search_term in template.name.lower() or
                search_term in template.description.lower() or
                any(search_term in tag.lower() for tag in template.tags)):
                results.append(template)
        
        return results
    
    def add_to_history(self, prompt: str, style_used: str = "", parameters: Dict = None) -> None:
        """Add a prompt to history."""
        if parameters is None:
            parameters = {}
        
        history_item = PromptHistoryItem(
            prompt=prompt,
            timestamp=datetime.now().isoformat(),
            style_used=style_used,
            parameters=parameters
        )
        
        # Add to beginning and limit size
        self._history.insert(0, history_item)
        if len(self._history) > 100:  # Keep last 100 items
            self._history = self._history[:100]
        
        self._save_history()
        self._append_to_log(prompt)
    
    def get_history(self, limit: int = 50) -> List[PromptHistoryItem]:
        """Get prompt history."""
        return self._history[:limit]
    
    def search_history(self, search_term: str) -> List[PromptHistoryItem]:
        """Search prompt history."""
        if not search_term.strip():
            return self._history.copy()
        
        search_term = search_term.lower()
        return [item for item in self._history 
                if search_term in item.prompt.lower() or 
                search_term in item.style_used.lower()]
    
    def clear_history(self) -> bool:
        """Clear prompt history."""
        try:
            self._history.clear()
            self._save_history()
            self.logger.info("Prompt history cleared")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear history: {e}")
            return False
    
    def export_history(self, file_path: str, format_type: str = "json") -> bool:
        """Export history to file in specified format."""
        try:
            if format_type.lower() == "json":
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump([asdict(item) for item in self._history], file, indent=2)
            elif format_type.lower() == "txt":
                with open(file_path, 'w', encoding='utf-8') as file:
                    for item in self._history:
                        file.write(f"[{item.timestamp}] {item.prompt}\n")
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            
            self.logger.info(f"History exported to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export history: {e}")
            return False
    
    def validate_prompt(self, prompt: str) -> List[str]:
        """Validate prompt and return list of potential issues."""
        issues = []
        
        if not prompt.strip():
            issues.append("Prompt is empty")
        
        if len(prompt) > 4000:
            issues.append("Prompt is very long (>4000 characters)")
        
        # Check for common issues
        if prompt.count("--") > 10:
            issues.append("Too many parameters (might cause issues)")
        
        if "," not in prompt and len(prompt.split()) > 1:
            issues.append("Consider using commas to separate concepts")
        
        return issues
    
    def _load_templates(self) -> None:
        """Load templates from file."""
        if not os.path.exists(self.templates_file):
            return
        
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as file:
                templates_data = json.load(file)
            
            self._templates = [PromptTemplate(**data) for data in templates_data]
        except (IOError, json.JSONDecodeError, TypeError) as e:
            self.logger.error(f"Error loading templates: {e}")
    
    def _save_templates(self) -> None:
        """Save templates to file."""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as file:
                json.dump([asdict(template) for template in self._templates], file, indent=2)
        except IOError as e:
            self.logger.error(f"Error saving templates: {e}")
    
    def _load_history(self) -> None:
        """Load history from file."""
        if not os.path.exists(self.history_file):
            return
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as file:
                history_data = json.load(file)
            
            self._history = [PromptHistoryItem(**data) for data in history_data]
        except (IOError, json.JSONDecodeError, TypeError) as e:
            self.logger.error(f"Error loading history: {e}")
    
    def _save_history(self) -> None:
        """Save history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as file:
                json.dump([asdict(item) for item in self._history], file, indent=2)
        except IOError as e:
            self.logger.error(f"Error saving history: {e}")
    
    def _append_to_log(self, prompt: str) -> None:
        """Append prompt to log file."""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(f"[{datetime.now().isoformat()}] {prompt}\n")
        except IOError as e:
            self.logger.error(f"Error appending to log: {e}")
