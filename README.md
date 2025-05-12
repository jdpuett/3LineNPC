# 3LineNPC Generator

A simple yet powerful random NPC generator for tabletop RPGs, based on Johnn Four's 3 Line NPC concept.

![3LineNPC Screenshot](screenshot.png)

## What is a 3 Line NPC?

A 3 Line NPC is a concise method for creating memorable non-player characters for tabletop RPG sessions. Each NPC consists of just three elements:

1. **Appearance**: A physical description or visual hook
2. **Role**: Their occupation, purpose, or place in society
3. **Hook**: A motivation, secret, goal, or plot hook that can drive story

This minimal approach creates NPCs that are easy to remember and use, while still providing enough detail to engage players and enrich your game world.

## Features

- Clean, simple GUI interface
- Generate NPCs with a single click
- Save and manage your generated NPCs
- Export NPCs to JSON format
- Import previously saved NPCs
- Export directly to Campaign Logger XML format
- Color-coded display for better readability
- Platform-independent (works on Windows, macOS, and Linux)
- Support for custom trait files

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone this repository:
```bash
git clone git@github.com:jdpuett/3LineNPC.git
```

2. Navigate to the directory:
```bash
cd 3LineNPC
```

3. Run the application:
```bash
python main.py
```

## Usage

### Basic Operation

1. Click the "Generate NPC" button to create a new random NPC
2. Enter a name in the "NPC Name" field (optional)
3. Click "Save NPC" to add the current NPC to your collection
4. Continue generating and saving NPCs as needed
5. Use "View Saved" to see all your saved NPCs

### Keyboard Shortcuts

- **Space**: Generate a new NPC
- **Ctrl+S**: Save the current NPC
- **Esc**: Exit the application

### Exporting and Importing

- **Export NPCs**: Save all your NPCs to a JSON file
- **Import NPCs**: Load previously saved NPCs from a JSON file
- **Export to Campaign Logger**: Export NPCs to Campaign Logger XML format for use with the Campaign Logger tool

## Customization

The generator uses three text files for its data:
- `appearances.txt` - Physical descriptions
- `roles.txt` - Occupations or social roles
- `hooks.txt` - Motivations, secrets, or plot hooks

You can edit these files to add your own content or tailor them to a specific setting, genre, or campaign. Each file should contain one trait per line, with no special formatting needed.

## Campaign Logger Integration

The 3LineNPC Generator can export your NPCs in a format compatible with Johnn Four's [Campaign Logger](https://campaign-logger.com/) tool. This feature allows you to:

1. Generate NPCs in the 3LineNPC Generator
2. Save the NPCs you like
3. Export them to Campaign Logger XML format
4. Import them into Campaign Logger for use in your game notes

The exported NPCs maintain their appearance, role, and hook information, properly formatted for Campaign Logger's interface.

## Contributing

Contributions are welcome! If you'd like to improve the app or expand the trait databases:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by Johnn Four's "3 Line NPC" concept from Roleplaying Tips
- Thanks to all the contributors who have helped expand the trait databases

## Future Plans

- Categories for different settings (fantasy, sci-fi, modern, etc.)
- Filter and search capabilities for saved NPCs
- Additional export formats (PDF, HTML)
- Editing of saved NPCs
- Trait weighting and relationships
- Custom templates for different NPC types