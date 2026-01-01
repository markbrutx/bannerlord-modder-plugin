# Save System - Custom Data Persistence

Two approaches for saving custom mod data: Native SaveableTypeDefiner or JSON serialization via ButterLib.

## Approach 1: SaveableTypeDefiner (Native)

### Step 1: Create Saveable Classes

```csharp
using TaleWorlds.SaveSystem;

[SaveableRootClass(1)] // Unique ID within your mod
public class MyModData
{
    [SaveableField(1)]
    public int SomeValue;

    [SaveableField(2)]
    public string SomeText;

    [SaveableField(3)]
    public List<HeroTrackingData> TrackedHeroes;

    // Constructor required for deserialization
    public MyModData() { }
}

[SaveableRootClass(2)]
public class HeroTrackingData
{
    [SaveableField(1)]
    public Hero Hero; // Built-in types work directly

    [SaveableField(2)]
    public int CustomScore;

    [SaveableField(3)]
    public bool IsActive;

    public HeroTrackingData() { }

    public HeroTrackingData(Hero hero)
    {
        Hero = hero;
        CustomScore = 0;
        IsActive = true;
    }
}
```

### Step 2: Create SaveableTypeDefiner

```csharp
using TaleWorlds.SaveSystem;

public class MySaveDefiner : SaveableTypeDefiner
{
    // Use CRC32 hash of your mod name for unique base ID
    // Example: "MyAwesomeMod" -> CRC32 -> e5a3f2 -> 15049714
    // Use first 6-7 digits to avoid conflicts
    public MySaveDefiner() : base(15_049_714) { }

    protected override void DefineClassTypes()
    {
        // Local IDs (1, 2, 3...) combined with base ID
        AddClassDefinition(typeof(MyModData), 1);
        AddClassDefinition(typeof(HeroTrackingData), 2);
    }

    protected override void DefineContainerDefinitions()
    {
        // Register any containers used
        ConstructContainerDefinition(typeof(List<HeroTrackingData>));
        ConstructContainerDefinition(typeof(Dictionary<Hero, HeroTrackingData>));
    }
}
```

### Step 3: Use in CampaignBehavior

```csharp
public class MyModBehavior : CampaignBehaviorBase
{
    public MyModData Data { get; private set; } = new MyModData();

    public override void RegisterEvents()
    {
        CampaignEvents.OnSessionLaunchedEvent.AddNonSerializedListener(this, OnSessionLaunched);
    }

    private void OnSessionLaunched(CampaignGameStarter starter)
    {
        // Initialize default data if new game
        if (Data.TrackedHeroes == null)
            Data.TrackedHeroes = new List<HeroTrackingData>();
    }

    public override void SyncData(IDataStore dataStore)
    {
        dataStore.SyncData("MyMod_Data", ref Data);
    }
}
```

### CRC32 for Unique ID

Use online CRC32 calculator with your mod name, take first 6 digits:
- `MyAwesomeMod` → `e5a3f2b1` → use `15049714`
- `BetterTrades` → `c8d1a7e3` → use `13160871`

## Approach 2: JSON Serialization (ButterLib - Recommended)

Simpler, no SaveableTypeDefiner needed, survives mod removal better.

### Setup

```csharp
using Bannerlord.ButterLib.SaveSystem.Extensions;
using Newtonsoft.Json;
using TaleWorlds.SaveSystem;

[SaveableClass(1)]
public class MyModData
{
    [SaveableField(1)]
    public int Value;

    [SaveableField(2)]
    public string Text;

    [SaveableField(3)]
    public Hero TrackedHero; // ButterLib handles Hero serialization!
}

public class MyModBehavior : CampaignBehaviorBase
{
    private MyModData _data = new MyModData();

    public override void SyncData(IDataStore dataStore)
    {
        // ButterLib extension - handles complex types automatically
        dataStore.SyncDataAsJson("MyMod_JsonData", ref _data);
    }

    public override void RegisterEvents() { }
}
```

### Benefits of SyncDataAsJson

- No SaveableTypeDefiner needed
- Automatic Hero/Clan/Kingdom reference handling
- Save files remain loadable if mod is removed
- Standard containers (Dictionary, List) work automatically
- Uses Newtonsoft.Json with custom converters

## Approach 3: Simple JSON String (Manual)

For maximum compatibility without ButterLib dependency:

```csharp
using Newtonsoft.Json;

public class MyModBehavior : CampaignBehaviorBase
{
    private MyModData _data = new MyModData();

    public override void SyncData(IDataStore dataStore)
    {
        if (dataStore.IsSaving)
        {
            string json = JsonConvert.SerializeObject(_data);
            dataStore.SyncData("MyMod_JsonString", ref json);
        }
        else
        {
            string json = null;
            dataStore.SyncData("MyMod_JsonString", ref json);
            if (!string.IsNullOrEmpty(json))
            {
                _data = JsonConvert.DeserializeObject<MyModData>(json);
            }
        }
    }

    public override void RegisterEvents() { }
}

// Data class - no TaleWorlds attributes needed
public class MyModData
{
    public int Value { get; set; }
    public string Text { get; set; }
    
    // Store Hero by StringId, not direct reference!
    public string HeroId { get; set; }
    
    [JsonIgnore]
    public Hero Hero => Hero.FindFirst(h => h.StringId == HeroId);
}
```

## Important Warnings

### DO NOT Store Direct References in JSON

```csharp
// BAD - will serialize incorrectly
public class BadData
{
    public Hero MyHero;        // NO!
    public Settlement MyTown;   // NO!
    public Clan MyClan;        // NO!
}

// GOOD - store IDs, resolve at runtime
public class GoodData
{
    public string HeroId;
    public string SettlementId;
    public string ClanId;

    [JsonIgnore]
    public Hero MyHero => Hero.FindFirst(h => h.StringId == HeroId);
    
    [JsonIgnore]
    public Settlement MyTown => Settlement.Find(SettlementId);
    
    [JsonIgnore]
    public Clan MyClan => Clan.FindFirst(c => c.StringId == ClanId);
}
```

### String Size Limit

Game has ~32KB limit per string. For large data, split into array:

```csharp
public override void SyncData(IDataStore dataStore)
{
    if (dataStore.IsSaving)
    {
        string json = JsonConvert.SerializeObject(_data);
        string[] chunks = SplitString(json, 30000);
        dataStore.SyncData("MyMod_Chunks", ref chunks);
    }
    else
    {
        string[] chunks = null;
        dataStore.SyncData("MyMod_Chunks", ref chunks);
        if (chunks != null)
        {
            string json = string.Concat(chunks);
            _data = JsonConvert.DeserializeObject<MyModData>(json);
        }
    }
}

private string[] SplitString(string str, int chunkSize)
{
    int count = (str.Length + chunkSize - 1) / chunkSize;
    string[] result = new string[count];
    for (int i = 0; i < count; i++)
    {
        int start = i * chunkSize;
        int length = Math.Min(chunkSize, str.Length - start);
        result[i] = str.Substring(start, length);
    }
    return result;
}
```

## Which Approach to Choose?

| Approach | Pros | Cons |
|----------|------|------|
| SaveableTypeDefiner | Native, fast | Complex, save corruption if mod removed |
| ButterLib JSON | Simple, safe removal | Requires ButterLib dependency |
| Manual JSON | No dependencies | Must handle references manually |

**Recommendation**: Use ButterLib's `SyncDataAsJson` for most mods. It's the safest and simplest approach.
