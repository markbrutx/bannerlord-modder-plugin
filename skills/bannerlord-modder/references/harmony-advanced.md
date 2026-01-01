# Advanced Harmony Patterns for Bannerlord

## Late Patching (For Models)

Some patches fail during `OnSubModuleLoad` because game systems aren't initialized. Apply them in `OnGameStart`:

```csharp
private bool _lateHarmonyApplied = false;

protected override void OnGameStart(Game game, IGameStarter gameStarter)
{
    base.OnGameStart(game, gameStarter);
    
    if (_lateHarmonyApplied) return;
    _lateHarmonyApplied = true;
    
    var harmony = new Harmony("com.yourmod.late");
    var original = typeof(DefaultPartySpeedCalculatingModel)
        .GetMethod("CalculateFinalSpeed");
    var postfix = typeof(SpeedPatch)
        .GetMethod("Postfix", BindingFlags.Static | BindingFlags.NonPublic);
    
    harmony.Patch(original, postfix: new HarmonyMethod(postfix));
}
```

## State Sharing Between Prefix and Postfix

```csharp
[HarmonyPatch(typeof(SomeClass), "SomeMethod")]
public static class TimingPatch
{
    private static void Prefix(out Stopwatch __state)
    {
        __state = Stopwatch.StartNew();
    }
    
    private static void Postfix(Stopwatch __state)
    {
        __state.Stop();
        Debug.Print($"Method took {__state.ElapsedMilliseconds}ms");
    }
}
```

## Conditional Patching

```csharp
[HarmonyPatch(typeof(SomeClass), "SomeMethod")]
public static class ConditionalPatch
{
    public static bool Prepare()
    {
        // Return false to skip this patch entirely
        return ModSettings.Instance?.EnablePatch ?? false;
    }
    
    public static void Postfix() { }
}
```

## Patching Properties

```csharp
// Patch getter
[HarmonyPatch(typeof(Hero), nameof(Hero.Gold), MethodType.Getter)]
public static class HeroGoldPatch
{
    public static void Postfix(Hero __instance, ref int __result)
    {
        if (__instance.IsPlayerCompanion)
            __result *= 2;
    }
}

// Patch setter
[HarmonyPatch(typeof(Hero), nameof(Hero.Gold), MethodType.Setter)]
public static class HeroGoldSetterPatch
{
    public static void Prefix(Hero __instance, ref int value)
    {
        // Modify value being set
    }
}
```

## Patching Constructors

```csharp
[HarmonyPatch(typeof(SomeClass))]
[HarmonyPatch(MethodType.Constructor)]
[HarmonyPatch(new Type[] { typeof(string), typeof(int) })]
public static class ConstructorPatch
{
    public static void Postfix(SomeClass __instance)
    {
        // Called after constructor
    }
}
```

## Reverse Patch (Call Original)

Access original method even when patched by others:

```csharp
[HarmonyPatch]
public static class ReversePatchExample
{
    [HarmonyReversePatch]
    [HarmonyPatch(typeof(DefaultDamageModel), "CalculateDamage")]
    public static float OriginalCalculateDamage(
        DefaultDamageModel instance, /* original params */)
    {
        // Stub - Harmony fills this with original code
        throw new NotImplementedException("Harmony reverse patch stub");
    }
}
```

## Finalizer (Exception Handling)

```csharp
[HarmonyPatch(typeof(RiskyClass), "RiskyMethod")]
public static class ExceptionHandler
{
    public static Exception? Finalizer(Exception? __exception)
    {
        if (__exception != null)
        {
            Debug.Print($"Caught exception: {__exception.Message}");
            return null; // Suppress exception
        }
        return __exception;
    }
}
```

## TargetMethod for Dynamic Selection

```csharp
[HarmonyPatch]
public static class DynamicPatch
{
    public static MethodBase TargetMethod()
    {
        // Find method dynamically
        return AccessTools.Method(typeof(SomeClass), "MethodName") 
            ?? throw new Exception("Method not found");
    }
    
    public static void Postfix() { }
}
```

## Multiple Method Patches

```csharp
[HarmonyPatch]
public static class MultiMethodPatch
{
    public static IEnumerable<MethodBase> TargetMethods()
    {
        yield return AccessTools.Method(typeof(ClassA), "Method1");
        yield return AccessTools.Method(typeof(ClassB), "Method2");
        yield return AccessTools.Method(typeof(ClassC), "Method3");
    }
    
    public static void Postfix(MethodBase __originalMethod)
    {
        // __originalMethod tells you which method was called
        Debug.Print($"Called: {__originalMethod.Name}");
    }
}
```

## AccessTools Utilities

```csharp
// Get private field
var field = AccessTools.Field(typeof(SomeClass), "_privateField");
var value = field.GetValue(instance);

// Get private method
var method = AccessTools.Method(typeof(SomeClass), "PrivateMethod");
method.Invoke(instance, new object[] { arg1, arg2 });

// Get property
var prop = AccessTools.Property(typeof(SomeClass), "SomeProperty");

// Create delegate for performance
var fastCall = AccessTools.MethodDelegate<Func<SomeClass, int, bool>>(method);

// Traverse for nested access
var nested = Traverse.Create(instance)
    .Field("_private")
    .Property("Nested")
    .GetValue<int>();
```

## Common Bannerlord Patch Targets

### Party Speed
```csharp
[HarmonyPatch(typeof(DefaultPartySpeedCalculatingModel), "CalculateFinalSpeed")]
```

### Damage Calculation
```csharp
[HarmonyPatch(typeof(DefaultCombatXpModel), "GetXpFromHit")]
```

### Troop Wages
```csharp
[HarmonyPatch(typeof(DefaultPartyWageModel), "GetTroopRecruitmentCost")]
```

### Settlement Production
```csharp
[HarmonyPatch(typeof(DefaultVillageProductionCalculatorModel), "CalculateDailyProductionAmount")]
```

### Battle Rewards
```csharp
[HarmonyPatch(typeof(DefaultBattleRewardModel), "CalculateRenownGain")]
```

### Influence Cost
```csharp
[HarmonyPatch(typeof(DefaultDiplomacyModel), "GetInfluenceCostOfAnnexation")]
```
