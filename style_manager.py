"""Style management module for MAT."""
import os
import logging
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
import json

@dataclass
class StyleItem:
    """Represents a style item with metadata."""
    name: str
    category: str
    is_favorite: bool = False
    usage_count: int = 0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class StyleManager:
    """Manages style loading, caching, and operations."""
    
    def __init__(self, styles_folder: str):
        self.styles_folder = styles_folder
        self.logger = logging.getLogger(__name__)
        self._style_cache: Dict[str, List[str]] = {}
        self._all_styles: List[StyleItem] = []
        self._favorites: Set[str] = set()
        self._usage_stats: Dict[str, int] = {}
        self._load_metadata()
    
    def get_categories(self) -> List[str]:
        """Get list of available style categories."""
        if not os.path.exists(self.styles_folder):
            self.logger.warning(f"Styles folder not found: {self.styles_folder}")
            return []
        
        try:
            categories = []
            for filename in os.listdir(self.styles_folder):
                if filename.endswith(".txt"):
                    category = filename[:-4]  # Remove .txt extension
                    categories.append(category)
            return sorted(categories)
        except OSError as e:
            self.logger.error(f"Error reading styles folder: {e}")
            return []
    
    def get_styles_for_category(self, category: str) -> List[str]:
        """Get styles for a specific category with caching."""
        if category in self._style_cache:
            return self._style_cache[category]
        
        file_path = os.path.join(self.styles_folder, f"{category}.txt")
        if not os.path.exists(file_path):
            self.logger.warning(f"Style file not found: {file_path}")
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                styles = [line.strip() for line in file if line.strip()]
            
            self._style_cache[category] = styles
            return styles
        except (IOError, UnicodeDecodeError) as e:
            self.logger.error(f"Error reading style file {file_path}: {e}")
            return []
    
    def search_styles(self, search_term: str, categories: Optional[List[str]] = None) -> List[str]:
        """Search for styles across categories with fuzzy matching."""
        if not search_term.strip():
            return []
        
        search_term = search_term.lower()
        results = set()
        
        # Determine which categories to search
        search_categories = categories or self.get_categories()
        
        for category in search_categories:
            styles = self.get_styles_for_category(category)
            for style in styles:
                if search_term in style.lower():
                    results.add(style)
        
        # Sort by relevance (exact matches first, then partial matches)
        sorted_results = sorted(results, key=lambda x: (
            search_term not in x.lower(),  # Exact matches first
            len(x),  # Shorter matches first
            x.lower()  # Alphabetical
        ))
        
        return sorted_results
    
    def add_favorite(self, style: str) -> None:
        """Add a style to favorites."""
        self._favorites.add(style)
        self._save_metadata()
    
    def remove_favorite(self, style: str) -> None:
        """Remove a style from favorites."""
        self._favorites.discard(style)
        self._save_metadata()
    
    def get_favorites(self) -> List[str]:
        """Get list of favorite styles."""
        return sorted(list(self._favorites))
    
    def is_favorite(self, style: str) -> bool:
        """Check if a style is marked as favorite."""
        return style in self._favorites
    
    def increment_usage(self, style: str) -> None:
        """Increment usage count for a style."""
        self._usage_stats[style] = self._usage_stats.get(style, 0) + 1
        self._save_metadata()
    
    def get_popular_styles(self, limit: int = 10) -> List[str]:
        """Get most popular styles based on usage."""
        sorted_styles = sorted(
            self._usage_stats.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [style for style, _ in sorted_styles[:limit]]
    
    def _load_metadata(self) -> None:
        """Load style metadata (favorites, usage stats)."""
        metadata_path = os.path.join(self.styles_folder, "_metadata.json")
        if not os.path.exists(metadata_path):
            return
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as file:
                metadata = json.load(file)
            
            self._favorites = set(metadata.get("favorites", []))
            self._usage_stats = metadata.get("usage_stats", {})
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Error loading style metadata: {e}")
    
    def _save_metadata(self) -> None:
        """Save style metadata (favorites, usage stats)."""
        metadata_path = os.path.join(self.styles_folder, "_metadata.json")
        metadata = {
            "favorites": list(self._favorites),
            "usage_stats": self._usage_stats
        }
        
        try:
            with open(metadata_path, 'w', encoding='utf-8') as file:
                json.dump(metadata, file, indent=2)
        except IOError as e:
            self.logger.error(f"Error saving style metadata: {e}")
    
    def clear_cache(self) -> None:
        """Clear the style cache."""
        self._style_cache.clear()
        self.logger.info("Style cache cleared")
