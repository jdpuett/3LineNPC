# 3LineNPC

A simple and powerful random NPC generator for tabletop RPGs, based on Johnn Four's 3 Line NPC concept.

![3LineNPC Screenshot](https://github.com/jdpuett/3LineNPC/raw/main/screenshot.png)

## What is a 3 Line NPC?

A 3 Line NPC is a quick, concise way to create memorable non-player characters for your tabletop RPG sessions. Each NPC is described with just three lines:

1. **Appearance**: A physical description or visual hook
2. **Role**: Their occupation, purpose, or place in society
3. **Hook**: A motivation, secret, goal, or plot hook

This minimal approach creates NPCs that are easy to remember and use, but still have enough detail to engage your players.

## Features

- Simple GUI interface
- Generate NPCs with a single click
- Easily expandable trait files
- Lightweight and standalone
- Cross-platform (Windows, macOS, Linux)

## Installation

### Prerequisites

- Python 3.6 or higher
- Tkinter (usually included with Python installation)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/jdpuett/3LineNPC.git
```

2. Navigate to the directory:
```bash
cd 3LineNPC
```

3. Run the application:
```bash
python3 main.py
```

## Usage

1. Click the "Generate" button to create a new random NPC
2. Continue clicking to generate more NPCs
3. Copy and paste the results into your notes for game preparation

## Customization

The generator uses three text files for its data:
- `appearances.txt` - Physical descriptions
- `roles.txt` - Occupations or social roles
- `hooks.txt` - Motivations, secrets, or plot hooks

You can edit these files to add your own content or tailor them to a specific setting, genre, or campaign.

### Format

Each file should contain one trait per line. For example:

```
A scarred old warrior
A mysterious cloaked figure
A cheerful young merchant
```

No numbering or formatting is needed - just plain text entries.

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

- Save/load functionality for generated NPCs
- Export options (PDF, CSV)
- Tags and filtering for traits
- Categories for different settings (fantasy, sci-fi, modern, etc.)