# Enhanced Midjourney Assistant Tool (MAT) v3.0

A comprehensive and enhanced version of the Midjourney Assistant Tool with advanced features, improved UI, and robust architecture. This version has not gone through much testing, issue may occur, but will be fixed as they are discovered / reported

## 🚀 What's New in v3.0

### Major Enhancements

#### 1. **Error Handling & Validation**
- Comprehensive error handling throughout the application
- Input validation with real-time feedback
- Robust file operation handling with fallbacks
- Detailed logging system for debugging

#### 2. **Code Organization & Architecture**
- Modular architecture with separate managers for different functionalities
- Clean separation of concerns (UI, business logic, data management)
- Type hints throughout the codebase
- Comprehensive logging system

#### 3. **Enhanced UI/UX**
- **Tabbed Interface**: Organized into Prompt Builder, Templates, History, and Settings
- **Searchable Components**: Smart search for styles with filtering
- **Theme System**: Dark, Light, and Matrix themes
- **Tooltips**: Helpful hints for all UI elements
- **Status Bar**: Real-time feedback and progress indication
- **Keyboard Shortcuts**: Full keyboard navigation support
- **Resizable Interface**: Adaptive layout that remembers window settings

#### 4. **Advanced Prompt Management**
- **Template System**: Save, load, and manage reusable prompt templates
- **History Tracking**: Comprehensive history with search and export capabilities
- **Prompt Validation**: Real-time validation with issue detection
- **Advanced Parameters**: Seed, quality, weird, aspect ratio controls
- **Parameter Presets**: Quick parameter combinations

### 🎯 Key Features

#### Style Management
- **50+ Style Categories**: Comprehensive style library
- **Favorites System**: Mark and quickly access favorite styles
- **Usage Analytics**: Track most-used styles
- **Smart Search**: Fuzzy search across all styles
- **Category-based Organization**: Efficient style browsing

#### Prompt Building
- **Live Preview**: Real-time prompt generation
- **Parameter Validation**: Automatic conflict detection
- **Smart Suggestions**: Context-aware parameter recommendations
- **Export Options**: Multiple format support (JSON, TXT)

#### Data Management
- **Auto-save**: Configurable auto-save intervals
- **Backup System**: Automatic data backups
- **Import/Export**: Configuration and data portability
- **Data Integrity**: Validation and error recovery

## 📋 Installation & Setup

### Requirements
- Python 3.7+ (uses dataclasses)
- No external dependencies required for basic functionality

### Quick Start
1. Clone or download the enhanced version files
2. Run the enhanced application:
   ```bash
   python MAT_Enhanced_v3.py
   ```

### File Structure
```
MAT_Enhanced/
├── MAT_Enhanced_v3.py       # Main application
├── config_manager.py        # Configuration management
├── style_manager.py         # Style loading and management
├── prompt_manager.py        # Prompt templates and history
├── ui_components.py         # UI components and widgets
├── requirements.txt         # Dependencies (optional)
├── config.json             # Application settings
├── Styles/                 # Style files directory
│   ├── Abstract.txt
│   ├── Fantasy.txt
│   └── ...
└── data/                   # Data directory (auto-created)
    ├── prompt_templates.json
    ├── prompt_history.json
    └── mat.log
```

## 🎮 Usage Guide

### Keyboard Shortcuts
- **Ctrl+C**: Copy current prompt
- **Ctrl+S**: Save settings
- **Ctrl+R**: Random style selection
- **Ctrl+T**: Save as template
- **Ctrl+V**: Validate prompt
- **Ctrl+Alt+C**: Clear all fields
- **F5**: Refresh data

### Prompt Builder Tab
1. **Enter your base prompt** in the text area
2. **Select a category** from the dropdown
3. **Choose a style** from the searchable list
4. **Configure parameters** using checkboxes and radio buttons
5. **Use advanced parameters** for fine control
6. **Preview updates** in real-time
7. **Copy or save** your final prompt

### Templates Tab
- **Save frequently used prompts** as templates
- **Add descriptions and tags** for easy organization
- **Load templates** directly to the prompt builder
- **Search templates** by name, description, or tags

### History Tab
- **View all generated prompts** with timestamps
- **Search history** by content or parameters
- **Load previous prompts** back to the editor
- **Export history** to JSON or TXT formats

### Settings Tab
- **Change themes** (Dark, Light, Matrix)
- **Configure auto-save** intervals
- **Reset to defaults** when needed
- **Access data folder** for manual management

## 🔧 Advanced Features

### Template System
Templates support variables and can include:
- Base prompt text
- Style preferences
- Parameter defaults
- Usage instructions

### Analytics & Insights
- Track most-used styles
- Monitor prompt patterns
- Export usage statistics
- Generate reports

### Customization
- **Custom Themes**: Define your own color schemes
- **Style Categories**: Add custom style collections
- **Parameter Presets**: Create quick-access parameter combinations
- **Keyboard Shortcuts**: Customize hotkeys

## 🛠️ Configuration

### Settings File (config.json)
```json
{
    "theme": "dark",
    "auto_save_interval": 10000,
    "window_width": 1200,
    "window_height": 800,
    "advanced_features": true
}
```

### Style Files
Each style category is a simple text file:
```
Style Name 1
Style Name 2
Artist Name
Movement or Technique
```

### Logging
The application maintains detailed logs in `data/mat.log`:
- Error messages and stack traces
- Performance metrics
- User actions and settings changes


### Version History
- **v3.0**: Complete rewrite with enhanced architecture
- **v2.2**: Added templates and advanced parameters
- **v1.1**: Initial release with basic functionality

## 📄 License

This project is open-source and available under the MIT License.

**Enhanced MAT v3.0** - Taking your Midjourney prompts to the next level! 🎨✨
