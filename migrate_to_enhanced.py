"""Migration script to transition from MAT v1.1 to Enhanced MAT v3.0."""
import os
import json
import shutil
import logging
from datetime import datetime
from typing import Dict, List

class MATMigration:
    """Handles migration from old MAT version to Enhanced v3.0."""
    
    def __init__(self, old_folder: str, new_folder: str):
        self.old_folder = old_folder
        self.new_folder = new_folder
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def setup_logging(self):
        """Setup logging for migration process."""
        log_file = os.path.join(self.new_folder, "migration.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def migrate(self) -> bool:
        """Perform complete migration."""
        try:
            self.logger.info("Starting migration from MAT v1.1 to Enhanced v3.0")
            
            # Create new folder structure
            self.create_folder_structure()
            
            # Migrate configuration
            self.migrate_configuration()
            
            # Migrate styles
            self.migrate_styles()
            
            # Migrate logs to history
            self.migrate_logs_to_history()
            
            # Create default templates
            self.create_default_templates()
            
            # Copy other files
            self.copy_other_files()
            
            self.logger.info("Migration completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Migration failed: {e}")
            return False
    
    def create_folder_structure(self):
        """Create new folder structure for enhanced version."""
        folders = [
            self.new_folder,
            os.path.join(self.new_folder, "data"),
            os.path.join(self.new_folder, "Styles"),
            os.path.join(self.new_folder, "backups")
        ]
        
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            self.logger.info(f"Created folder: {folder}")
    
    def migrate_configuration(self):
        """Migrate old configuration to new format."""
        old_config_path = os.path.join(self.old_folder, "config.json")
        new_config_path = os.path.join(self.new_folder, "config.json")
        
        if not os.path.exists(old_config_path):
            self.logger.warning("No old configuration found, using defaults")
            return
        
        try:
            with open(old_config_path, 'r', encoding='utf-8') as file:
                old_config = json.load(file)
            
            # Convert to new format
            new_config = {
                "selected_text": old_config.get("selected_text", ""),
                "dropdown": old_config.get("dropdown", ""),
                "radioMode": old_config.get("radioMode", 0),
                "radioStylize": old_config.get("radioStylize", 0),
                "radioChaos": old_config.get("radioChaos", 0),
                "check_vars": old_config.get("check_vars", {"1": 0, "2": 0, "3": 0, "4": 0}),
                "window_x": 0,
                "window_y": 0,
                "window_width": 1200,
                "window_height": 800,
                "theme": "dark",
                "auto_save_interval": 10000
            }
            
            with open(new_config_path, 'w', encoding='utf-8') as file:
                json.dump(new_config, file, indent=4)
            
            self.logger.info("Configuration migrated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to migrate configuration: {e}")
    
    def migrate_styles(self):
        """Migrate style files to new location."""
        old_styles_folder = os.path.join(self.old_folder, "Styles")
        new_styles_folder = os.path.join(self.new_folder, "Styles")
        
        if not os.path.exists(old_styles_folder):
            self.logger.warning("No old styles folder found")
            return
        
        try:
            # Copy all style files
            for filename in os.listdir(old_styles_folder):
                if filename.endswith('.txt'):
                    old_file = os.path.join(old_styles_folder, filename)
                    new_file = os.path.join(new_styles_folder, filename)
                    shutil.copy2(old_file, new_file)
                    self.logger.info(f"Migrated style file: {filename}")
            
            self.logger.info("All style files migrated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to migrate styles: {e}")
    
    def migrate_logs_to_history(self):
        """Convert old prompt logs to new history format."""
        old_log_path = os.path.join(self.old_folder, "prompt_log.txt")
        new_history_path = os.path.join(self.new_folder, "data", "prompt_history.json")
        
        if not os.path.exists(old_log_path):
            self.logger.warning("No old prompt log found")
            return
        
        try:
            history_items = []
            
            with open(old_log_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file):
                    line = line.strip()
                    if line:
                        # Create history item
                        history_item = {
                            "prompt": line,
                            "timestamp": datetime.now().isoformat(),
                            "style_used": "",
                            "parameters": {}
                        }
                        history_items.append(history_item)
            
            # Save to new format
            with open(new_history_path, 'w', encoding='utf-8') as file:
                json.dump(history_items, file, indent=2)
            
            self.logger.info(f"Migrated {len(history_items)} history items")
            
        except Exception as e:
            self.logger.error(f"Failed to migrate history: {e}")
    
    def create_default_templates(self):
        """Create some default templates."""
        templates_path = os.path.join(self.new_folder, "data", "prompt_templates.json")
        
        default_templates = [
            {
                "name": "Portrait Photography",
                "template": "professional portrait photography, studio lighting, high resolution",
                "description": "Template for portrait photography prompts",
                "tags": ["photography", "portrait", "professional"],
                "created_at": datetime.now().isoformat()
            },
            {
                "name": "Fantasy Art",
                "template": "fantasy art, digital painting, detailed, magical atmosphere",
                "description": "Template for fantasy artwork",
                "tags": ["fantasy", "art", "digital", "magical"],
                "created_at": datetime.now().isoformat()
            },
            {
                "name": "Logo Design",
                "template": "minimalist logo design, clean, professional, black background",
                "description": "Template for logo creation",
                "tags": ["logo", "design", "minimalist", "professional"],
                "created_at": datetime.now().isoformat()
            }
        ]
        
        try:
            with open(templates_path, 'w', encoding='utf-8') as file:
                json.dump(default_templates, file, indent=2)
            
            self.logger.info("Created default templates")
            
        except Exception as e:
            self.logger.error(f"Failed to create default templates: {e}")
    
    def copy_other_files(self):
        """Copy other important files."""
        files_to_copy = [
            "HeBi.ico",
            "README.md",
            "autosave_prompt.txt"
        ]
        
        for filename in files_to_copy:
            old_file = os.path.join(self.old_folder, filename)
            new_file = os.path.join(self.new_folder, filename)
            
            if os.path.exists(old_file):
                try:
                    shutil.copy2(old_file, new_file)
                    self.logger.info(f"Copied file: {filename}")
                except Exception as e:
                    self.logger.warning(f"Failed to copy {filename}: {e}")
    
    def create_backup(self):
        """Create backup of old version before migration."""
        backup_folder = os.path.join(self.new_folder, "backups", f"old_version_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        try:
            shutil.copytree(self.old_folder, backup_folder)
            self.logger.info(f"Created backup at: {backup_folder}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return False

def main():
    """Main migration function."""
    print("MAT Migration Tool - v1.1 to Enhanced v3.0")
    print("=" * 50)
    
    # Get folders from user
    old_folder = input("Enter path to old MAT folder: ").strip()
    if not old_folder:
        old_folder = "."  # Current directory
    
    new_folder = input("Enter path for new Enhanced MAT folder (or press Enter for './MAT_Enhanced'): ").strip()
    if not new_folder:
        new_folder = "./MAT_Enhanced"
    
    # Validate old folder
    if not os.path.exists(old_folder):
        print(f"Error: Old folder '{old_folder}' does not exist!")
        return
    
    # Create migrator
    migrator = MATMigration(old_folder, new_folder)
    
    # Ask for backup
    create_backup = input("Create backup of old version? (y/n): ").lower().startswith('y')
    if create_backup:
        print("Creating backup...")
        if not migrator.create_backup():
            print("Warning: Backup failed, but continuing with migration...")
    
    # Perform migration
    print("Starting migration...")
    if migrator.migrate():
        print("✓ Migration completed successfully!")
        print(f"Enhanced MAT v3.0 is ready in: {new_folder}")
        print("You can now run 'python MAT_Enhanced_v3.py' in the new folder.")
    else:
        print("✗ Migration failed! Check migration.log for details.")

if __name__ == "__main__":
    main()
