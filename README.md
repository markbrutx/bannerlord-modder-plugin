# Bannerlord Modder Plugin for Claude Code

A Claude Code plugin that helps you create professional Mount & Blade II: Bannerlord mods using the BUTR modding stack.

## Features

- **Harmony Patching**: Prefix, Postfix, Transpiler patterns with proper priority handling
- **MCM Settings**: Mod Configuration Menu with attribute-based and fluent builder APIs
- **Campaign Behaviors**: Event subscriptions, save/load persistence
- **Game Models**: Override and extend game calculations
- **UIExtenderEx**: UI modification patterns
- **Localization**: TextObject, translations, plural/gender conditionals
- **XSLT Patching**: XML patching without overwriting native files
- **Mission Behaviors**: Battle modding and Agent events

## Installation

### Option 1: Install via Claude Code CLI

```bash
claude plugin install github:YOUR_USERNAME/bannerlord-modder-plugin
```

### Option 2: Clone to plugins directory

```bash
# Navigate to Claude Code plugins directory
cd ~/.claude/plugins

# Clone the repository
git clone https://github.com/YOUR_USERNAME/bannerlord-modder-plugin.git
```

### Option 3: Local installation (for development)

```bash
claude plugin install /path/to/bannerlord-modder-plugin
```

## Usage

Once installed, Claude Code will automatically use this skill when you:

- Ask about creating Bannerlord mods
- Request help with Harmony patching (Prefix/Postfix/Transpiler)
- Want to add MCM settings to your mod
- Need to create CampaignBehaviors or GameModels
- Work with SubModule.xml configuration
- Ask about any C# modding for Bannerlord

### Example Prompts

```
Create a new Bannerlord mod that increases party speed by 20%
```

```
Add MCM settings to my mod with a speed multiplier slider
```

```
Patch the DefaultCharacterDevelopmentModel to double XP gain
```

```
Create a CampaignBehavior that tracks settlement ownership changes
```

## Plugin Structure

```
bannerlord-modder-plugin/
├── .claude-plugin/
│   └── manifest.json
├── skills/
│   └── bannerlord-modder/
│       ├── SKILL.md
│       ├── references/
│       │   ├── harmony-advanced.md
│       │   ├── mcm-fluent-builder.md
│       │   ├── campaign-events.md
│       │   ├── uiextenderex.md
│       │   ├── save-system.md
│       │   ├── xslt-patching.md
│       │   ├── mission-behavior.md
│       │   └── localization.md
│       ├── assets/
│       │   └── templates/
│       │       ├── SubModule.cs.template
│       │       ├── ModSettings.cs.template
│       │       ├── CampaignBehavior.cs.template
│       │       ├── SubModule.xml.template
│       │       └── ModProject.csproj.template
│       └── scripts/
│           └── generate_mod.py
├── README.md
├── LICENSE
└── .gitignore
```

## Requirements

- Claude Code CLI
- For mod development: .NET SDK 6.0+, Bannerlord game installation

## Core Dependencies (for your mods)

1. **Bannerlord.Harmony** - Runtime patching library
2. **Bannerlord.ButterLib** - Core modding utilities, DI, logging
3. **Bannerlord.UIExtenderEx** - UI modification library
4. **Bannerlord.MCM** - Mod Configuration Menu

## Resources

- [BUTR Community Docs](https://docs.bannerlordmodding.com/)
- [Official TaleWorlds Docs](https://moddocs.bannerlord.com/)
- [MCM Documentation](https://mcm.bannerlord.aragas.org/)
- [Harmony Wiki](https://harmony.pardeike.net/)
- [BUTR GitHub](https://github.com/BUTR)

## License

MIT License - see [LICENSE](LICENSE) file for details.
