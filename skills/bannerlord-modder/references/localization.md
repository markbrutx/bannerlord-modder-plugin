# Localization - Multi-Language Support

Best practices for making your mod translatable.

## TextObject Basics

All user-visible strings must use TextObject with a unique string ID:

```csharp
using TaleWorlds.Localization;

// Format: {=8charID}Text
private const string MyString = "{=xK7nM2pQ}Hello, traveler!";
public static TextObject MyText => new TextObject(MyString);

// Without ID - NOT translatable (avoid!)
var badText = new TextObject("This won't be translatable");
```

### String ID Rules

- **8 alphanumeric characters** (TaleWorlds standard)
- **Global scope** - IDs must be unique across ALL mods
- **No spaces or special characters**
- Generate random IDs: https://www.random.org/strings/
- Long IDs affect performance

```csharp
// GOOD - random 8-char ID
"{=xK7nM2pQ}Some text"
"{=Ab3Cd4Ef}Another text"

// BAD - semantic IDs risk conflicts
"{=greeting_text}Hello"     // Another mod might use same ID!
"{=my_mod_button_1}Click"   // Too long, hurts performance
```

## Folder Structure

```
Modules/
└── YourMod/
    └── ModuleData/
        └── Languages/
            ├── std_module_strings_xml.xml     # English (reference)
            ├── language_data.xml              # Language registration
            ├── RU/                            # Russian
            │   ├── language_data.xml
            │   └── std_module_strings_xml.xml
            ├── DE/                            # German
            │   ├── language_data.xml
            │   └── std_module_strings_xml.xml
            └── CNs/                           # Simplified Chinese
                ├── language_data.xml
                └── std_module_strings_xml.xml
```

## XML Files

### std_module_strings_xml.xml (English Reference)

```xml
<?xml version="1.0" encoding="utf-8"?>
<base xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
      type="string">
  <tags>
    <tag language="English"/>
  </tags>
  <strings>
    <string id="xK7nM2pQ" text="Hello, traveler!"/>
    <string id="mN3bV7cX" text="Welcome to {TOWN_NAME}"/>
    <string id="pL9kJ2hG" text="{HERO_NAME} has {GOLD_AMOUNT} gold"/>
    <string id="qW4eR5tY" text="You have {COUNT} {?COUNT.PLURAL_FORM}items{?}item{\?}"/>
  </strings>
</base>
```

### Translation File (e.g., RU/std_module_strings_xml.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<base xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
      type="string">
  <tags>
    <tag language="Русский"/>
  </tags>
  <strings>
    <string id="xK7nM2pQ" text="Привет, путник!"/>
    <string id="mN3bV7cX" text="Добро пожаловать в {TOWN_NAME}"/>
    <string id="pL9kJ2hG" text="У {HERO_NAME} есть {GOLD_AMOUNT} золота"/>
    <string id="qW4eR5tY" text="У вас {COUNT} {?COUNT.PLURAL_FORM}предметов{?}предмет{\?}"/>
  </strings>
</base>
```

### language_data.xml (Per Language Folder)

```xml
<?xml version="1.0" encoding="utf-8"?>
<LanguageData id="Русский">
  <LanguageFile xml_path="RU/std_module_strings_xml.xml"/>
</LanguageData>
```

## Language IDs

| Language | ID | Folder |
|----------|-----|--------|
| English | `English` | (root) |
| Russian | `Русский` | RU |
| German | `Deutsch` | DE |
| French | `Français` | FR |
| Spanish | `Español` | SP |
| Turkish | `Türkçe` | TR |
| Polish | `Polski` | PL |
| Chinese Simplified | `简体中文` | CNs |
| Chinese Traditional | `繁體中文` | CNt |
| Japanese | `日本語` | JP |
| Korean | `한국어` | KO |
| Portuguese (Brazil) | `Português (BR)` | PTBR |
| Italian | `Italiano` | IT |

## Variables in TextObject

### Basic Variables

```csharp
// Define string with variable
const string greeting = "{=abc12345}Welcome, {PLAYER_NAME}!";

// Set variable
TextObject text = new TextObject(greeting);
text.SetTextVariable("PLAYER_NAME", Hero.MainHero.Name);

// Result: "Welcome, Eragon!"
string result = text.ToString();
```

### Multiple Variables

```csharp
const string report = "{=def67890}{HERO} earned {GOLD} gold in {TOWN}";

TextObject text = new TextObject(report);
text.SetTextVariable("HERO", hero.Name);
text.SetTextVariable("GOLD", goldAmount);
text.SetTextVariable("TOWN", town.Name);
```

### Nested TextObjects

```csharp
const string main = "{=aaa11111}You found {ITEM_DESC}!";
const string itemDesc = "{=bbb22222}a {QUALITY} {ITEM_NAME}";

TextObject itemText = new TextObject(itemDesc);
itemText.SetTextVariable("QUALITY", "legendary");
itemText.SetTextVariable("ITEM_NAME", "sword");

TextObject mainText = new TextObject(main);
mainText.SetTextVariable("ITEM_DESC", itemText);

// Result: "You found a legendary sword!"
```

## Conditionals

### Plural Forms

```csharp
// English: "1 day" vs "5 days"
const string duration = "{=ccc33333}Wait {DAYS} {?DAYS.PLURAL_FORM}days{?}day{\\?}";

TextObject text = new TextObject(duration);
TextObject daysText = new TextObject(numberOfDays);
daysText.SetTextVariable("PLURAL_FORM", numberOfDays != 1 ? 1 : 0);
text.SetTextVariable("DAYS", daysText);
```

### Gender Conditionals

```csharp
// "He is ready" vs "She is ready"
const string status = "{=ddd44444}{?HERO.GENDER}She{?}He{\\?} is ready for battle.";

TextObject text = new TextObject(status);
StringHelpers.SetCharacterProperties("HERO", hero.CharacterObject, text);
```

### Complex Conditionals

```csharp
// Bitflag conditional
const string msg = "{=eee55555}{?IS_ALLY}Your ally{?}The enemy{\\?} approaches.";

TextObject text = new TextObject(msg);
text.SetTextVariable("IS_ALLY", isAlly ? 1 : 0);
```

## Character Properties (StringHelpers)

Always include character properties for translators - they may need gender/name info:

```csharp
using TaleWorlds.CampaignSystem;

const string dialogue = "{=fff66666}{NPC.NAME} says: I serve {LIEGE.NAME}, " +
                        "and {?LIEGE.GENDER}she{?}he{\\?} is a great ruler.";

TextObject text = new TextObject(dialogue);

// Sets NAME, GENDER, LINK, and other properties
StringHelpers.SetCharacterProperties("NPC", npcHero.CharacterObject, text);
StringHelpers.SetCharacterProperties("LIEGE", liegeHero.CharacterObject, text);
```

### Available Properties After SetCharacterProperties

- `{TAG.NAME}` - Character name
- `{TAG.GENDER}` - For gender conditionals
- `{TAG.LINK}` - Clickable encyclopedia link
- `{TAG.FACTION}` - Faction name

## Global Text Variables (MBTextManager)

For variables used across many TextObjects:

```csharp
using TaleWorlds.Localization;

// Set global variable - available to ALL TextObjects
MBTextManager.SetTextVariable("PLAYER_TITLE", "Commander");
MBTextManager.SetTextVariable("CURRENT_YEAR", CampaignTime.Now.GetYear);

// Any TextObject can now use {PLAYER_TITLE} and {CURRENT_YEAR}
```

**Warning**: Don't mix global and local variables in same TextObject.

## Common Mistakes

### 1. Using < > in XML

```xml
<!-- BAD - breaks XML parsing -->
<string id="xxx" text="Damage: 5 < 10"/>

<!-- GOOD - use escaped entities -->
<string id="xxx" text="Damage: 5 &lt; 10"/>
```

Escape codes:
- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`

### 2. Hardcoded Strings

```csharp
// BAD
InformationManager.DisplayMessage(new InformationMessage("Quest completed!"));

// GOOD
private static readonly TextObject QuestCompleteText = new TextObject("{=ggg77777}Quest completed!");
InformationManager.DisplayMessage(new InformationMessage(QuestCompleteText.ToString()));
```

### 3. Concatenating Strings

```csharp
// BAD - word order differs between languages!
string msg = hero.Name + " has arrived at " + town.Name;

// GOOD - let translator control word order
const string arrival = "{=hhh88888}{HERO} has arrived at {TOWN}";
TextObject text = new TextObject(arrival);
text.SetTextVariable("HERO", hero.Name);
text.SetTextVariable("TOWN", town.Name);
```

### 4. Nested Property Chains

```csharp
// BAD - multiple dots not supported
"{NPC.CLAN.LEADER.NAME}"  // Returns empty string!

// GOOD - set each separately
StringHelpers.SetCharacterProperties("LEADER", npc.Clan.Leader.CharacterObject, text);
```

## Helper Tools

- **[Bannerlord LocalizationParser](https://github.com/BUTR/Bannerlord.LocalizationParser)** - Extract all hardcoded strings from assemblies
- **[Bannerlord Helper](https://github.com/gengark/bannerlord-helper)** - Auto-translate and generate language files
- **Random.org** - Generate unique string IDs: https://www.random.org/strings/?num=10&len=8&digits=on&loweralpha=on&unique=on&format=html

## MCM Localization

MCM settings are localized via same system:

```csharp
[SettingPropertyBool("{=iii99999}Enable Feature", 
    HintText = "{=jjj00000}Enables the awesome feature", 
    RequireRestart = false)]
public bool EnableFeature { get; set; } = true;
```

## Best Practices Summary

1. **Always use TextObject** for any user-visible text
2. **Generate random 8-char IDs** - avoid semantic names
3. **Include character properties** even if English doesn't need them
4. **Never concatenate** translated strings
5. **Escape special characters** in XML (`<`, `>`, `&`)
6. **Create English reference file** in Languages/ folder
7. **Test with different languages** to catch word order issues
