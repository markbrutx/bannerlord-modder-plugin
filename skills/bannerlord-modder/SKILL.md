---
name: bannerlord-modder
description: Create Mount & Blade II Bannerlord mods using Harmony, ButterLib, MCM (Mod Configuration Menu), and UIExtenderEx. Use when creating Bannerlord mods, patching game methods with Harmony (Prefix/Postfix/Transpiler), adding mod settings via MCM, creating CampaignBehaviors, GameModels, SubModule.xml configuration, or any C# modding for Bannerlord.
---

# Bannerlord Modder

Create professional Bannerlord mods using the BUTR modding stack.

## Core Dependencies (Load Order)

1. **Bannerlord.Harmony** - Runtime patching library
2. **Bannerlord.ButterLib** - Core modding utilities, DI, logging
3. **Bannerlord.UIExtenderEx** - UI modification library
4. **Bannerlord.MCM** (Mod Configuration Menu) - In-game settings UI

## Project Setup

### SubModule.xml Template

```xml
<?xml version="1.0" encoding="utf-8"?>
<Module>
  <Name value="Your Mod Name"/>
  <Id value="YourModId"/>
  <Version value="v1.0.0"/>
  <SingleplayerModule value="true"/>
  <MultiplayerModule value="false"/>
  <DependedModules>
    <DependedModule Id="Bannerlord.Harmony" DependentVersion="v2.3.0"/>
    <DependedModule Id="Bannerlord.ButterLib" DependentVersion="v2.8.0"/>
    <DependedModule Id="Bannerlord.UIExtenderEx" DependentVersion="v2.8.0"/>
    <DependedModule Id="Bannerlord.MBOptionScreen" DependentVersion="v5.10.0"/>
    <DependedModule Id="Native"/>
    <DependedModule Id="SandBoxCore"/>
    <DependedModule Id="Sandbox"/>
    <DependedModule Id="StoryMode"/>
  </DependedModules>
  <SubModules>
    <SubModule>
      <Name value="YourModId"/>
      <DLLName value="YourModId.dll"/>
      <SubModuleClassType value="YourNamespace.SubModule"/>
      <Tags>
        <Tag key="DedicatedServerType" value="none"/>
        <Tag key="IsNoRenderModeElement" value="false"/>
      </Tags>
    </SubModule>
  </SubModules>
</Module>
```

### .csproj NuGet References

```xml
<ItemGroup>
  <PackageReference Include="Bannerlord.ButterLib" Version="2.9.0" IncludeAssets="compile"/>
  <PackageReference Include="Bannerlord.MCM" Version="5.10.0" IncludeAssets="compile"/>
  <PackageReference Include="Bannerlord.UIExtenderEx" Version="2.12.0" IncludeAssets="compile"/>
  <PackageReference Include="Lib.Harmony" Version="2.3.3" IncludeAssets="compile"/>
</ItemGroup>
```

**Critical**: Always use `IncludeAssets="compile"` to prevent DLL conflicts.

## Module Structure

```
Modules/
└── YourMod/
    ├── SubModule.xml
    ├── bin/
    │   └── Win64_Shipping_Client/
    │       └── YourMod.dll
    ├── ModuleData/           # XML data files
    └── GUI/                  # UI prefabs (optional)
        └── Prefabs/
```

## SubModule Entry Point

```csharp
using HarmonyLib;
using TaleWorlds.Core;
using TaleWorlds.MountAndBlade;
using TaleWorlds.CampaignSystem;

namespace YourNamespace
{
    public class SubModule : MBSubModuleBase
    {
        private Harmony? _harmony;

        protected override void OnSubModuleLoad()
        {
            base.OnSubModuleLoad();
            _harmony = new Harmony("com.yourname.yourmod");
            _harmony.PatchAll();
        }

        protected override void OnSubModuleUnloaded()
        {
            base.OnSubModuleUnloaded();
            _harmony?.UnpatchAll("com.yourname.yourmod");
        }

        protected override void OnGameStart(Game game, IGameStarter starter)
        {
            base.OnGameStart(game, starter);
            if (game.GameType is Campaign && starter is CampaignGameStarter campaignStarter)
            {
                campaignStarter.AddBehavior(new YourCampaignBehavior());
                // campaignStarter.AddModel(new YourGameModel());
            }
        }
    }
}
```

## Harmony Patching

### Postfix (Most Common)

Runs after original method. Use `ref` to modify return value.

```csharp
[HarmonyPatch(typeof(DefaultPartySpeedCalculatingModel), "CalculateFinalSpeed")]
public static class PartySpeedPatch
{
    public static void Postfix(ref ExplainedNumber __result)
    {
        __result.AddFactor(0.2f, new TextObject("{=}Speed Bonus"));
    }
}
```

### Prefix

Runs before original. Return `false` to skip original method.

```csharp
[HarmonyPatch(typeof(TargetClass), "MethodName")]
public static class MyPrefixPatch
{
    public static bool Prefix(ref bool __result, int someArg)
    {
        if (someArg > 100)
        {
            __result = true;
            return false; // Skip original
        }
        return true; // Run original
    }
}
```

### Accessing Private Fields

Use `___fieldName` (triple underscore) to access private instance fields:

```csharp
[HarmonyPatch(typeof(MapEventSide), "ApplyRenownAndInfluenceChanges")]
public static class MapEventPatch
{
    public static void Postfix(MBList<MapEventParty> ___battleParties)
    {
        foreach (var party in ___battleParties)
        {
            // Access private field _battleParties
        }
    }
}
```

### Handling Method Overloads

Specify argument types when method has overloads:

```csharp
[HarmonyPatch(typeof(DefaultCharacterDevelopmentModel))]
[HarmonyPatch("CalculateLearningRate", typeof(int), typeof(int), typeof(int), typeof(int), typeof(TextObject), typeof(bool))]
public static class LearningRatePatch
{
    public static void Postfix(ref float __result) { }
}
```

### Transpiler (Advanced)

Modify IL code directly. Use sparingly.

```csharp
[HarmonyPatch(typeof(TargetClass), "TargetMethod")]
public static class MyTranspiler
{
    static IEnumerable<CodeInstruction> Transpiler(IEnumerable<CodeInstruction> instructions)
    {
        var codes = new List<CodeInstruction>(instructions);
        // Modify codes...
        return codes;
    }
}
```

### Patch Priority & Ordering

```csharp
[HarmonyPatch(typeof(SomeClass), "SomeMethod")]
[HarmonyPriority(Priority.High)]  // 400=High, 200=Low, 0=Last
[HarmonyBefore("other.mod.id")]
[HarmonyAfter("another.mod.id")]
public static class PriorityPatch { }
```

## MCM Settings

### Attribute-Based Settings (Recommended)

```csharp
using MCM.Abstractions.Attributes;
using MCM.Abstractions.Attributes.v2;
using MCM.Abstractions.Base.Global;

internal sealed class ModSettings : AttributeGlobalSettings<ModSettings>
{
    public override string Id => "YourMod_v1";
    public override string DisplayName => "Your Mod Settings";
    public override string FolderName => "YourMod";
    public override string FormatType => "json2";

    [SettingPropertyGroup("General")]
    [SettingPropertyBool("Enable Feature", Order = 0, RequireRestart = false,
        HintText = "Toggle the main feature on/off")]
    public bool EnableFeature { get; set; } = true;

    [SettingPropertyGroup("General")]
    [SettingPropertyFloatingInteger("Speed Multiplier", 0.5f, 3.0f, "#0.0%", Order = 1,
        HintText = "Adjust movement speed")]
    public float SpeedMultiplier { get; set; } = 1.0f;

    [SettingPropertyGroup("Combat")]
    [SettingPropertyInteger("Damage Bonus", 0, 100, Order = 0,
        HintText = "Additional damage percentage")]
    public int DamageBonus { get; set; } = 10;

    [SettingPropertyGroup("Combat")]
    [SettingPropertyDropdown("Difficulty", Order = 1,
        HintText = "Select difficulty level")]
    public Dropdown<string> Difficulty { get; set; } = new Dropdown<string>(
        new[] { "Easy", "Normal", "Hard" }, 1);

    [SettingPropertyGroup("Advanced", GroupOrder = 99)]
    [SettingPropertyText("Custom Name", Order = 0,
        HintText = "Enter custom name")]
    public string CustomName { get; set; } = "Default";
}
```

### Accessing Settings

```csharp
var settings = ModSettings.Instance;
if (settings?.EnableFeature == true)
{
    float multiplier = settings.SpeedMultiplier;
}
```

### Setting Types

| Type | Attribute | Properties |
|------|-----------|------------|
| Bool | `SettingPropertyBool` | RequireRestart |
| Int | `SettingPropertyInteger` | minValue, maxValue, valueFormat |
| Float | `SettingPropertyFloatingInteger` | minValue, maxValue, valueFormat |
| Text | `SettingPropertyText` | - |
| Dropdown | `SettingPropertyDropdown` | - |
| Button | `SettingPropertyButton` | Content, action method |

### PerSave/PerCampaign Settings

```csharp
// For campaign-specific settings
internal sealed class CampaignSettings : AttributePerCampaignSettings<CampaignSettings>
{
    public override string Id => "YourMod_Campaign_v1";
    public override string DisplayName => "Your Mod (Campaign)";
    // ... properties
}

// For save-specific settings
internal sealed class SaveSettings : AttributePerSaveSettings<SaveSettings>
{
    public override string Id => "YourMod_Save_v1";
    // ... properties
}
```

## CampaignBehavior

Track state and respond to campaign events:

```csharp
using TaleWorlds.CampaignSystem;
using TaleWorlds.SaveSystem;

public class YourCampaignBehavior : CampaignBehaviorBase
{
    private Dictionary<string, int> _trackedData = new();

    public override void RegisterEvents()
    {
        CampaignEvents.DailyTickEvent.AddNonSerializedListener(this, OnDailyTick);
        CampaignEvents.OnSettlementOwnerChangedEvent.AddNonSerializedListener(
            this, OnSettlementOwnerChanged);
        CampaignEvents.HeroPrisonerTaken.AddNonSerializedListener(this, OnHeroPrisonerTaken);
    }

    private void OnDailyTick()
    {
        // Daily logic
    }

    private void OnSettlementOwnerChanged(Settlement settlement, 
        bool openToClaim, Hero newOwner, Hero oldOwner, 
        Hero capturerHero, ChangeOwnerOfSettlementAction.ChangeOwnerOfSettlementDetail detail)
    {
        // React to settlement capture
    }

    private void OnHeroPrisonerTaken(PartyBase capturer, Hero prisoner)
    {
        // React to hero capture
    }

    public override void SyncData(IDataStore dataStore)
    {
        dataStore.SyncData("_trackedData", ref _trackedData);
    }
}
```

### Common Campaign Events

- `DailyTickEvent`, `HourlyTickEvent`, `WeeklyTickEvent`
- `OnSettlementOwnerChangedEvent`
- `OnBattleEndedEvent`, `MapEventEnded`
- `HeroKilledEvent`, `HeroPrisonerTaken`
- `OnNewGameCreatedEvent`, `OnGameLoadedEvent`
- `OnSessionLaunchedEvent`
- `OnPartyDisbandedEvent`
- `OnClanChangedKingdom`

## GameModel Override

Replace or modify game calculations:

```csharp
using TaleWorlds.CampaignSystem.GameComponents;

public class CustomPartySpeedModel : DefaultPartySpeedCalculatingModel
{
    public override ExplainedNumber CalculateFinalSpeed(
        MobileParty mobileParty, ExplainedNumber finalSpeed)
    {
        var result = base.CalculateFinalSpeed(mobileParty, finalSpeed);
        
        if (mobileParty.IsMainParty && ModSettings.Instance?.EnableFeature == true)
        {
            result.AddFactor(ModSettings.Instance.SpeedMultiplier - 1f, 
                new TextObject("{=}Mod Bonus"));
        }
        
        return result;
    }
}

// Register in OnGameStart:
// campaignStarter.AddModel(new CustomPartySpeedModel());
```

## Localization

Make your mod translatable with TextObject and string IDs:

```csharp
using TaleWorlds.Localization;

// Format: {=8charID}Text - use random.org/strings for unique IDs
private const string WelcomeString = "{=xK7nM2pQ}Welcome, {PLAYER_NAME}!";

public void ShowWelcome(Hero hero)
{
    TextObject text = new TextObject(WelcomeString);
    text.SetTextVariable("PLAYER_NAME", hero.Name);
    InformationManager.DisplayMessage(new InformationMessage(text.ToString()));
}

// With gender conditionals
const string heroStatus = "{=mN3bV7cX}{?HERO.GENDER}She{?}He{\\?} is ready.";
TextObject statusText = new TextObject(heroStatus);
StringHelpers.SetCharacterProperties("HERO", hero.CharacterObject, statusText);

// With plural forms
const string itemCount = "{=pL9kJ2hG}You have {COUNT} {?COUNT.PLURAL_FORM}items{?}item{\\?}";
```

Create `ModuleData/Languages/std_module_strings_xml.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<base xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xmlns:xsd="http://www.w3.org/2001/XMLSchema" type="string">
  <tags><tag language="English"/></tags>
  <strings>
    <string id="xK7nM2pQ" text="Welcome, {PLAYER_NAME}!"/>
    <string id="mN3bV7cX" text="{?HERO.GENDER}She{?}He{\?} is ready."/>
  </strings>
</base>
```

See `references/localization.md` for translations, language folders, and best practices.

## Debugging Tips

1. **Enable Harmony Debug**: Check `C:\Users\<user>\AppData\Local\Mount and Blade II Bannerlord\harmony.log.txt`

2. **ButterLib Logging**:
```csharp
using Bannerlord.ButterLib.Common.Extensions;
using Microsoft.Extensions.Logging;

public class SubModule : MBSubModuleBase
{
    private ILogger? _logger;
    
    protected override void OnSubModuleLoad()
    {
        _logger = this.GetTempServiceProvider()?.GetService<ILogger<SubModule>>();
        _logger?.LogInformation("Mod loaded successfully");
    }
}
```

3. **InformationManager Messages**:
```csharp
InformationManager.DisplayMessage(new InformationMessage("Debug: value = " + value));
```

## Common Pitfalls

1. **Wrong Load Order**: Harmony must load FIRST, then ButterLib, UIExtenderEx, MCM
2. **Missing IncludeAssets="compile"**: Causes DLL conflicts
3. **Patching Models in OnSubModuleLoad**: Some game systems aren't ready. Use `OnGameStart`
4. **Forgetting Null Checks**: Always check `ModSettings.Instance` for null
5. **Not handling save/load**: Implement `SyncData` in CampaignBehavior for persistence

## Quick Reference: Key Namespaces

```csharp
using HarmonyLib;                           // Harmony patching
using TaleWorlds.Core;                       // Core types
using TaleWorlds.MountAndBlade;              // MBSubModuleBase, Mission
using TaleWorlds.CampaignSystem;             // Campaign, Hero, Settlement
using TaleWorlds.CampaignSystem.GameComponents;  // Default models
using TaleWorlds.Localization;               // TextObject
using TaleWorlds.Library;                    // MBList, Color, Vec2
using MCM.Abstractions.Attributes.v2;        // MCM attributes
using MCM.Abstractions.Base.Global;          // GlobalSettings
```

## Additional Reference Files

This skill includes detailed guides in `references/`:

| File | Topic |
|------|-------|
| `harmony-advanced.md` | Late patching, Transpilers, AccessTools, __state, Finalizers |
| `mcm-fluent-builder.md` | Runtime settings, Fluent Builder API, PerSave settings |
| `campaign-events.md` | Complete list of CampaignEvents with examples |
| `uiextenderex.md` | PrefabExtension, ViewModelMixin, UI modification |
| `save-system.md` | SaveableTypeDefiner, JSON serialization, data persistence |
| `xslt-patching.md` | XML patching without overwriting native files |
| `mission-behavior.md` | Battle modding, Agent events, MissionBehavior |
| `localization.md` | TextObject, string IDs, translations, plural/gender conditionals |

**Templates** in `assets/templates/`:
- `SubModule.cs.template` - Entry point
- `ModSettings.cs.template` - MCM settings
- `CampaignBehavior.cs.template` - Campaign behavior with events
- `SubModule.xml.template` - Module manifest
- `ModProject.csproj.template` - Project file with NuGet

## Resources

- [Community Docs](https://docs.bannerlordmodding.com/)
- [Official Docs](https://moddocs.bannerlord.com/)
- [MCM Documentation](https://mcm.bannerlord.aragas.org/)
- [Harmony Wiki](https://harmony.pardeike.net/)
- [BUTR GitHub](https://github.com/BUTR)
- [UIExtenderEx Docs](https://butr.github.io/Bannerlord.UIExtenderEx/)
- [ButterLib Docs](https://butr.github.io/Bannerlord.ButterLib/)
