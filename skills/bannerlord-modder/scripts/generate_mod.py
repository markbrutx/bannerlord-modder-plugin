#!/usr/bin/env python3
"""
Bannerlord Mod Generator
Creates a new mod project with all required files from templates.
"""

import os
import sys
import argparse
from pathlib import Path


TEMPLATES = {
    "SubModule.cs": "SubModule.cs.template",
    "ModSettings.cs": "ModSettings.cs.template", 
    "Behavior.cs": "CampaignBehavior.cs.template",
    "SubModule.xml": "SubModule.xml.template",
    "Project.csproj": "ModProject.csproj.template",
}


def replace_placeholders(content: str, config: dict) -> str:
    """Replace template placeholders with actual values."""
    replacements = {
        "${ModId}": config["mod_id"],
        "${ModName}": config["mod_name"],
        "${ModNamespace}": config["namespace"],
        "${Author}": config["author"],
        "${Version}": config["version"],
        "${ModDescription}": config.get("description", "A Bannerlord mod"),
    }
    
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    return content


def create_mod_structure(output_dir: Path, config: dict, templates_dir: Path):
    """Create the complete mod directory structure."""
    
    mod_dir = output_dir / config["mod_id"]
    mod_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (mod_dir / "bin" / "Win64_Shipping_Client").mkdir(parents=True, exist_ok=True)
    (mod_dir / "ModuleData").mkdir(exist_ok=True)
    
    # Create source directory
    src_dir = mod_dir / "src"
    src_dir.mkdir(exist_ok=True)
    
    # Process templates
    for output_name, template_name in TEMPLATES.items():
        template_path = templates_dir / template_name
        
        if not template_path.exists():
            print(f"Warning: Template not found: {template_path}")
            continue
        
        content = template_path.read_text()
        content = replace_placeholders(content, config)
        
        # Determine output path
        if output_name == "SubModule.xml":
            out_path = mod_dir / "SubModule.xml"
        elif output_name == "Project.csproj":
            out_path = src_dir / f"{config['mod_id']}.csproj"
        else:
            # Rename class files appropriately
            if output_name == "Behavior.cs":
                out_path = src_dir / f"{config['mod_id']}Behavior.cs"
            elif output_name == "ModSettings.cs":
                out_path = src_dir / f"{config['mod_id']}Settings.cs"
            else:
                out_path = src_dir / output_name
        
        out_path.write_text(content)
        print(f"Created: {out_path}")
    
    # Create README
    readme_content = f"""# {config['mod_name']}

A Mount & Blade II: Bannerlord mod.

## Requirements

- Bannerlord.Harmony
- Bannerlord.ButterLib  
- Bannerlord.UIExtenderEx
- Bannerlord.MCM (Mod Configuration Menu)

## Installation

1. Install required dependencies from NexusMods or Steam Workshop
2. Copy the `{config['mod_id']}` folder to your Bannerlord `Modules` directory
3. Enable the mod in the launcher

## Building

1. Open `src/{config['mod_id']}.csproj` in Visual Studio or Rider
2. Restore NuGet packages
3. Build the solution

## License

MIT License
"""
    (mod_dir / "README.md").write_text(readme_content)
    
    print(f"\nMod created successfully at: {mod_dir}")
    print(f"\nNext steps:")
    print(f"  1. Update GameFolder path in src/{config['mod_id']}.csproj")
    print(f"  2. Open the project in Visual Studio/Rider")
    print(f"  3. Restore NuGet packages")
    print(f"  4. Build and test!")


def main():
    parser = argparse.ArgumentParser(description="Generate a new Bannerlord mod project")
    parser.add_argument("mod_id", help="Mod ID (no spaces, e.g., 'MyAwesomeMod')")
    parser.add_argument("--name", "-n", help="Display name (default: same as mod_id)")
    parser.add_argument("--namespace", "-ns", help="C# namespace (default: same as mod_id)")
    parser.add_argument("--author", "-a", default="Anonymous", help="Author name")
    parser.add_argument("--version", "-v", default="1.0.0", help="Initial version")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--templates", "-t", help="Templates directory path")
    
    args = parser.parse_args()
    
    # Build config
    config = {
        "mod_id": args.mod_id,
        "mod_name": args.name or args.mod_id,
        "namespace": args.namespace or args.mod_id,
        "author": args.author,
        "version": args.version,
    }
    
    # Find templates directory
    if args.templates:
        templates_dir = Path(args.templates)
    else:
        # Look for templates relative to script location
        script_dir = Path(__file__).parent.parent
        templates_dir = script_dir / "assets" / "templates"
    
    if not templates_dir.exists():
        print(f"Error: Templates directory not found: {templates_dir}")
        sys.exit(1)
    
    output_dir = Path(args.output)
    create_mod_structure(output_dir, config, templates_dir)


if __name__ == "__main__":
    main()
