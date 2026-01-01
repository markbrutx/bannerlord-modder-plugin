# UIExtenderEx - UI Modification Guide

Extend and modify Bannerlord's Gauntlet UI without overwriting files.

## Setup

```csharp
using Bannerlord.UIExtenderEx;

public class SubModule : MBSubModuleBase
{
    private UIExtender? _extender;

    protected override void OnSubModuleLoad()
    {
        base.OnSubModuleLoad();
        
        _extender = new UIExtender("YourModId");
        _extender.Register(typeof(SubModule).Assembly);
        _extender.Enable();
    }
}
```

## PrefabExtension - Modify XML Prefabs

### Insert Element

```csharp
using Bannerlord.UIExtenderEx.Attributes;
using Bannerlord.UIExtenderEx.Prefabs2;

// Insert custom button into MapBar
[PrefabExtension("MapBar", "descendant::ListPanel[@Id='LeftContent']/Children")]
public class MapBarExtension : PrefabExtensionInsertPatch
{
    public override string Id => "MyCustomButton";
    public override int Position => 3; // Insert at position 3
    
    // Loads: GUI/PrefabExtensions/MyCustomButton.xml
}
```

### Insert as Sibling

```csharp
[PrefabExtension("EncyclopediaHeroPage", "descendant::Widget[@Id='InformationPanel']")]
public class HeroPageExtension : PrefabExtensionInsertAsSiblingPatch
{
    public override string Id => "CustomHeroInfo";
    public override InsertType Type => InsertType.Append; // After target
}
```

### Replace Element

```csharp
[PrefabExtension("Inventory", "descendant::Widget[@Id='OldWidget']")]
public class InventoryReplacePatch : PrefabExtensionReplacePatch
{
    public override string Id => "NewWidget";
}
```

### Set Attribute

```csharp
[PrefabExtension("CharacterDeveloper", "descendant::ButtonWidget[@Id='ResetButton']")]
public class ResetButtonPatch : PrefabExtensionSetAttributePatch
{
    public override List<Attribute> Attributes => new()
    {
        new Attribute("IsVisible", "true"),
        new Attribute("IsEnabled", "@CanReset")
    };
}
```

### Custom Patch (Full Control)

```csharp
[PrefabExtension("Options")]
public class OptionsCustomPatch : CustomPatch<XmlDocument>
{
    public override void Apply(XmlDocument document)
    {
        var node = document.SelectSingleNode("//Widget[@Id='OptionsPanel']");
        if (node != null)
        {
            var newAttr = document.CreateAttribute("MarginTop");
            newAttr.Value = "50";
            node.Attributes?.Append(newAttr);
        }
    }
}
```

## PrefabExtension XML Files

Place in `GUI/PrefabExtensions/`:

```xml
<!-- GUI/PrefabExtensions/MyCustomButton.xml -->
<Prefab>
  <Window>
    <ButtonWidget Id="MyButton" 
                  WidthSizePolicy="Fixed" 
                  HeightSizePolicy="Fixed"
                  SuggestedWidth="40" 
                  SuggestedHeight="40"
                  Command.Click="ExecuteMyAction"
                  Brush="ButtonBrush1"
                  IsVisible="@IsMyButtonVisible">
      <Children>
        <ImageWidget WidthSizePolicy="StretchToParent"
                     HeightSizePolicy="StretchToParent"
                     Sprite="my_icon"/>
      </Children>
    </ButtonWidget>
  </Window>
</Prefab>
```

## ViewModelMixin - Extend ViewModels

Add properties and methods to existing ViewModels:

```csharp
using Bannerlord.UIExtenderEx.Attributes;
using Bannerlord.UIExtenderEx.ViewModels;
using TaleWorlds.Library;

[ViewModelMixin]
public class MapInfoMixin : BaseViewModelMixin<MapInfoVM>
{
    private bool _isCustomVisible = true;
    private string _customText = "Hello";

    public MapInfoMixin(MapInfoVM vm) : base(vm) { }

    [DataSourceProperty]
    public bool IsCustomVisible
    {
        get => _isCustomVisible;
        set => SetField(ref _isCustomVisible, value, nameof(IsCustomVisible));
    }

    [DataSourceProperty]
    public string CustomText
    {
        get => _customText;
        set => SetField(ref _customText, value, nameof(CustomText));
    }

    [DataSourceProperty]
    public HintViewModel CustomHint => new HintViewModel(new TextObject("Custom tooltip"));

    [DataSourceMethod]
    public void ExecuteCustomAction()
    {
        InformationManager.DisplayMessage(new InformationMessage("Button clicked!"));
        IsCustomVisible = !IsCustomVisible;
    }
}
```

### With Refresh Method

If the ViewModel has a Refresh method, specify it:

```csharp
[ViewModelMixin("RefreshValues")] // or nameof(TargetVM.RefreshValues)
public class CharacterMixin : BaseViewModelMixin<CharacterVM>
{
    public CharacterMixin(CharacterVM vm) : base(vm) { }

    // Called when RefreshValues is invoked
    public override void OnRefresh()
    {
        // Update your properties here
    }

    [DataSourceProperty]
    public int CustomStat => ViewModel?.Hero?.GetSkillValue(DefaultSkills.Tactics) ?? 0;
}
```

### Accessing Original ViewModel

```csharp
[ViewModelMixin]
public class EncyclopediaMixin : BaseViewModelMixin<EncyclopediaHeroPageVM>
{
    public EncyclopediaMixin(EncyclopediaHeroPageVM vm) : base(vm) { }

    [DataSourceProperty]
    public string HeroFullInfo
    {
        get
        {
            var hero = ViewModel?.Obj as Hero;
            if (hero == null) return "";
            return $"{hero.Name} - Age: {hero.Age:F0}, Gold: {hero.Gold}";
        }
    }
}
```

## Common UI Patterns

### Adding to Party Screen

```csharp
[PrefabExtension("PartyScreen", "descendant::Widget[@Id='TopPanel']/Children")]
public class PartyScreenExtension : PrefabExtensionInsertPatch
{
    public override string Id => "PartyCustomInfo";
    public override int Position => 0;
}

[ViewModelMixin]
public class PartyMixin : BaseViewModelMixin<PartyVM>
{
    public PartyMixin(PartyVM vm) : base(vm) { }

    [DataSourceProperty]
    public string TotalPartyWages
    {
        get
        {
            var party = MobileParty.MainParty;
            return $"Daily Wages: {party.TotalWage}";
        }
    }
}
```

### Adding Options Menu Entry

```csharp
[PrefabExtension("Options", "descendant::ListPanel[@Id='OptionsList']/Children")]
public class OptionsExtension : PrefabExtensionInsertPatch
{
    public override string Id => "ModOptionsButton";
    public override int Position => 5;
}

[ViewModelMixin]
public class OptionsMixin : BaseViewModelMixin<OptionsVM>
{
    public OptionsMixin(OptionsVM vm) : base(vm) { }

    [DataSourceMethod]
    public void ExecuteOpenModOptions()
    {
        // Open your mod options screen
    }
}
```

## Key ViewModel Classes

| Screen | ViewModel |
|--------|-----------|
| Main Map Bar | `MapInfoVM` |
| Party Screen | `PartyVM` |
| Inventory | `SPInventoryVM` |
| Character | `CharacterDeveloperVM`, `CharacterVM` |
| Encyclopedia Hero | `EncyclopediaHeroPageVM` |
| Clan Screen | `ClanVM`, `ClanLordItemVM` |
| Kingdom | `KingdomManagementVM` |
| Options | `OptionsVM` |
| Escape Menu | `EscapeMenuVM` |

## Debugging Tips

1. **Copy prefabs for testing**: Copy game's `GUI/Prefabs/*.xml` to your mod's folder for rapid iteration
2. **Use dnSpy**: Find ViewModel class names by searching for prefab names
3. **Check XPath**: Use online XPath testers to validate expressions
4. **Restart required**: New XML files need game restart; XML changes to existing files refresh on window reopen
