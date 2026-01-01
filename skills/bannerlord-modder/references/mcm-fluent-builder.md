# MCM Fluent Builder API

For runtime-defined settings instead of compile-time attributes.

## Basic Usage

```csharp
using MCM.Abstractions.FluentBuilder;
using MCM.Abstractions.FluentBuilder.Implementation;
using MCM.Abstractions.Ref;

public class FluentSettingsManager
{
    private ISettingsBuilderFactory _factory;
    private FluentGlobalSettings? _settings;
    
    // Backing fields
    private bool _enableFeature = true;
    private int _maxValue = 50;
    private float _multiplier = 1.5f;
    private string _customText = "Default";
    private int _selectedIndex = 0;
    
    public void RegisterSettings()
    {
        var builder = _factory.CreateBuilder("YourMod_Fluent_v1", "Your Mod (Fluent)")
            .SetFormat("json2")
            .SetFolderName("YourMod")
            .SetSubFolder("");
        
        builder.CreateGroup("General", groupBuilder => groupBuilder
            .AddBool(
                "Enable Feature",
                new PropertyRef(() => _enableFeature, v => _enableFeature = v),
                boolBuilder => boolBuilder
                    .SetHintText("Toggle the main feature")
                    .SetRequireRestart(false)
                    .SetOrder(0))
            .AddInteger(
                "Max Value",
                0, 100,
                new PropertyRef(() => _maxValue, v => _maxValue = v),
                intBuilder => intBuilder
                    .SetHintText("Set the maximum value")
                    .SetOrder(1))
        );
        
        builder.CreateGroup("Advanced", groupBuilder => groupBuilder
            .AddFloatingInteger(
                "Multiplier",
                0.1f, 5.0f,
                new PropertyRef(() => _multiplier, v => _multiplier = v),
                floatBuilder => floatBuilder
                    .SetHintText("Damage multiplier")
                    .SetValueFormat("#0.0x")
                    .SetOrder(0))
            .AddText(
                "Custom Text",
                new PropertyRef(() => _customText, v => _customText = v),
                textBuilder => textBuilder
                    .SetHintText("Enter custom text")
                    .SetOrder(1))
        );
        
        _settings = builder.BuildAsGlobal();
        _settings.Register();
    }
    
    public void UnregisterSettings()
    {
        _settings?.Unregister();
    }
}
```

## PropertyRef Types

### Direct Property Reference
```csharp
new PropertyRef(() => _fieldValue, v => _fieldValue = v)
```

### StorageRef (Self-contained)
```csharp
new StorageRef(defaultValue)
```

### ProxyRef (Custom getter/setter)
```csharp
new ProxyRef<bool>(
    () => SomeClass.Instance.SomeBool,
    value => SomeClass.Instance.SomeBool = value
)
```

## Dropdown Settings

```csharp
private string[] _options = { "Easy", "Normal", "Hard" };
private int _selectedIndex = 1;

builder.CreateGroup("Settings", groupBuilder => groupBuilder
    .AddDropdown(
        "Difficulty",
        _selectedIndex,
        new PropertyRef(() => _selectedIndex, v => _selectedIndex = v),
        dropdownBuilder => dropdownBuilder
            .SetHintText("Select difficulty")
            .SetOptions(_options))
);
```

## Button Settings

```csharp
builder.CreateGroup("Actions", groupBuilder => groupBuilder
    .AddButton(
        "Reset All",
        "Click to Reset",
        buttonBuilder => buttonBuilder
            .SetHintText("Reset all settings to default")
            .SetAction(() => ResetAllSettings()))
);
```

## PerSave/PerCampaign Fluent Settings

```csharp
// Build as PerSave (stored in save file)
var saveSettings = builder.BuildAsPerSave();
saveSettings.Register();

// Build as PerCampaign (persists across saves in same campaign)
var campaignSettings = builder.BuildAsPerCampaign();
campaignSettings.Register();
```

**Important**: Register PerSave/PerCampaign settings AFTER campaign starts:

```csharp
protected override void OnGameStart(Game game, IGameStarter gameStarter)
{
    if (game.GameType is Campaign)
    {
        CampaignEvents.OnSessionLaunchedEvent.AddNonSerializedListener(this, _ =>
        {
            _perSaveSettings?.Register();
        });
    }
}
```

## Presets

```csharp
builder.CreatePreset("default", "Default", presetBuilder => presetBuilder
    .SetPropertyValue("Enable Feature", true)
    .SetPropertyValue("Max Value", 50)
    .SetPropertyValue("Multiplier", 1.5f));

builder.CreatePreset("hardcore", "Hardcore", presetBuilder => presetBuilder
    .SetPropertyValue("Enable Feature", true)
    .SetPropertyValue("Max Value", 100)
    .SetPropertyValue("Multiplier", 0.5f));
```

## Complete Example

```csharp
public class SubModule : MBSubModuleBase
{
    private FluentGlobalSettings? _settings;
    
    private bool _enableMod = true;
    private int _bonusDamage = 25;
    private float _speedMultiplier = 1.2f;
    
    public static bool EnableMod => Instance?._enableMod ?? true;
    public static int BonusDamage => Instance?._bonusDamage ?? 25;
    public static float SpeedMultiplier => Instance?._speedMultiplier ?? 1.2f;
    
    public static SubModule? Instance { get; private set; }
    
    protected override void OnSubModuleLoad()
    {
        Instance = this;
        
        var builder = new DefaultSettingsBuilder("MyMod_v1", "My Awesome Mod")
            .SetFormat("json2")
            .SetFolderName("MyMod");
        
        builder.CreateGroup("Gameplay", g => g
            .AddBool("Enable Mod",
                new PropertyRef(() => _enableMod, v => _enableMod = v),
                b => b.SetHintText("Toggle mod on/off"))
            .AddInteger("Bonus Damage", 0, 100,
                new PropertyRef(() => _bonusDamage, v => _bonusDamage = v),
                b => b.SetHintText("Extra damage %"))
            .AddFloatingInteger("Speed Multiplier", 0.5f, 2.0f,
                new PropertyRef(() => _speedMultiplier, v => _speedMultiplier = v),
                b => b.SetHintText("Party speed modifier").SetValueFormat("#0.0x"))
        );
        
        _settings = builder.BuildAsGlobal();
        _settings.Register();
    }
    
    protected override void OnSubModuleUnloaded()
    {
        _settings?.Unregister();
    }
}
```
