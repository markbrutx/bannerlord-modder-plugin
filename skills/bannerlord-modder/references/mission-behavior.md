# MissionBehavior - Battle & Scene Modding

MissionBehavior is for modifying battles, arena fights, and any "mission" (scene with agents).

## Basic MissionBehavior

```csharp
using TaleWorlds.MountAndBlade;

public class MyMissionBehavior : MissionBehavior
{
    public override MissionBehaviorType BehaviorType => MissionBehaviorType.Other;

    public override void OnMissionTick(float dt)
    {
        // Called every frame during mission
    }

    public override void OnAgentBuild(Agent agent, Banner banner)
    {
        // Called when agent is ready to be used
        // Best place to modify spawned agents
    }
}
```

## Registering MissionBehavior

### Method 1: OnMissionBehaviorInitialize (All Missions)

```csharp
public class SubModule : MBSubModuleBase
{
    public override void OnMissionBehaviorInitialize(Mission mission)
    {
        base.OnMissionBehaviorInitialize(mission);
        
        // Add to ALL missions
        mission.AddMissionBehavior(new MyMissionBehavior());
        
        // Or conditionally
        if (mission.CombatType == Mission.MissionCombatType.Combat)
        {
            mission.AddMissionBehavior(new BattleBehavior());
        }
    }
}
```

### Method 2: From CampaignBehavior (Campaign Only)

```csharp
public class MyCampaignBehavior : CampaignBehaviorBase
{
    public override void RegisterEvents()
    {
        CampaignEvents.OnMissionStartedEvent.AddNonSerializedListener(this, OnMissionStarted);
    }

    private void OnMissionStarted(IMission mission)
    {
        if (mission is Mission m)
        {
            m.AddMissionBehavior(new MyMissionBehavior());
        }
    }

    public override void SyncData(IDataStore dataStore) { }
}
```

## Key Callbacks

### Agent Lifecycle

```csharp
public override void OnAgentCreated(Agent agent)
{
    // Agent created on engine side, before build
    // Good place to add AgentComponents
    agent.AddComponent(new MyAgentComponent(agent));
}

public override void OnAgentBuild(Agent agent, Banner banner)
{
    // Agent fully built, ready to use
    // Recommended for agent modifications
    
    if (agent.IsHuman && agent.Team?.IsPlayerTeam == true)
    {
        // Buff player team agents
        agent.BaseHealthLimit *= 1.5f;
        agent.Health = agent.HealthLimit;
    }
}

public override void OnAgentRemoved(Agent affectedAgent, Agent affectorAgent, 
    AgentState agentState, KillingBlow blow)
{
    // Agent removed from mission (killed, fled, etc.)
    if (agentState == AgentState.Killed)
    {
        InformationManager.DisplayMessage(
            new InformationMessage($"{affectedAgent.Name} was killed!"));
    }
}

public override void OnAgentDeleted(Agent affectedAgent)
{
    // Agent completely deleted from memory
}
```

### Combat Events

```csharp
public override void OnAgentHit(Agent affectedAgent, Agent affectorAgent,
    in MissionWeapon affectorWeapon, in Blow blow, in AttackCollisionData collisionData)
{
    // Called when agent is hit
    // Note: Called AFTER damage applied
    
    if (affectorAgent?.IsMainAgent == true)
    {
        // Track player damage
    }
}

public override void OnScoreHit(Agent affectedAgent, Agent affectorAgent,
    WeaponComponentData attackerWeapon, bool isBlocked, bool isSiegeEngineHit,
    in Blow blow, in AttackCollisionData collisionData, float damageDone,
    float hitDistance, float shotDifficulty)
{
    // Called with damage scoring info
}

public override void OnAgentShootMissile(Agent shooterAgent, EquipmentIndex weaponIndex,
    Vec3 position, Vec3 velocity, Mat3 orientation, bool hasRigidBody, int forcedMissileIndex)
{
    // Arrow/bolt/throwing weapon launched
}

public override void OnMissileHit(Agent attacker, Agent victim, bool isCanceled,
    AttackCollisionData collisionData)
{
    // Missile hit something
}

public override void OnMeleeHit(Agent attacker, Agent victim, bool isCanceled,
    AttackCollisionData collisionData)
{
    // Melee attack connected
}
```

### Mission Flow

```csharp
public override void OnMissionTick(float dt)
{
    // Every frame - use sparingly!
    // dt = delta time since last frame
}

public override void OnPreDisplayMissionTick(float dt)
{
    // Before agents/teams ticked, before OnMissionTick
}

public override void AfterStart()
{
    // Mission started, scene loaded
    // Good for initial setup
}

public override void OnEndMission()
{
    // Mission ending - cleanup here
    // Unregister events
}

public override void OnClearScene()
{
    // Scene being cleared
    // Reset mission behavior state
}

public override void OnMissionModeChange(MissionMode oldMode, bool atStart)
{
    // Mission mode changed (e.g., battle to conversation)
}
```

### Formation & Morale

```csharp
public override void OnAgentFleeing(Agent affectedAgent)
{
    // Agent started fleeing
}

public override void OnAgentPanicked(Agent affectedAgent)
{
    // Agent panicked
}

public override void OnFormationUnitsSpawned(Team team)
{
    // Formation finished spawning units
}

public override void OnDeploymentFinished()
{
    // Deployment phase complete
}
```

## AgentComponent

For per-agent behavior/data:

```csharp
public class MyAgentComponent : AgentComponent
{
    private float _customTimer = 0f;
    
    public MyAgentComponent(Agent agent) : base(agent) { }

    public override void OnTickAsAI(float dt)
    {
        // Called for AI agents every tick
        _customTimer += dt;
        
        if (_customTimer > 5f)
        {
            _customTimer = 0f;
            // Do something every 5 seconds
        }
    }

    public override void OnHit(Agent affectorAgent, int damage, in MissionWeapon weapon)
    {
        // This specific agent was hit
    }

    public override void OnMount(Agent mount)
    {
        // Agent mounted a horse
    }

    public override void OnDismount(Agent mount)
    {
        // Agent dismounted
    }

    public override void OnItemPickup(SpawnedItemEntity item)
    {
        // Agent picked up item
    }
}

// Add component in MissionBehavior
public override void OnAgentCreated(Agent agent)
{
    agent.AddComponent(new MyAgentComponent(agent));
}
```

## Practical Examples

### Damage Multiplier

```csharp
public class DamageMultiplierBehavior : MissionBehavior
{
    public override MissionBehaviorType BehaviorType => MissionBehaviorType.Other;
    
    private float _playerDamageMultiplier = 1.5f;

    public override void OnRegisterBlow(Agent attacker, Agent victim,
        GameEntity realHitEntity, Blow b, ref AttackCollisionData collisionData,
        in MissionWeapon attackerWeapon)
    {
        if (attacker?.IsMainAgent == true)
        {
            // Modify damage before it's applied
            b.InflictedDamage = (int)(b.InflictedDamage * _playerDamageMultiplier);
        }
    }
}
```

### Kill Counter

```csharp
public class KillCounterBehavior : MissionBehavior
{
    public int PlayerKills { get; private set; } = 0;
    public int TeamKills { get; private set; } = 0;

    public override MissionBehaviorType BehaviorType => MissionBehaviorType.Other;

    public override void OnAgentRemoved(Agent affectedAgent, Agent affectorAgent,
        AgentState agentState, KillingBlow blow)
    {
        if (agentState == AgentState.Killed && affectorAgent != null)
        {
            if (affectorAgent.IsMainAgent)
            {
                PlayerKills++;
            }
            else if (affectorAgent.Team?.IsPlayerTeam == true)
            {
                TeamKills++;
            }
        }
    }

    public override void OnEndMission()
    {
        InformationManager.DisplayMessage(
            new InformationMessage($"Battle ended! You: {PlayerKills}, Team: {TeamKills}"));
    }
}
```

### Slow Motion on Player Hit

```csharp
public class SlowMoBehavior : MissionBehavior
{
    private float _slowMoTimer = 0f;
    private const float SlowMoDuration = 0.5f;

    public override MissionBehaviorType BehaviorType => MissionBehaviorType.Other;

    public override void OnAgentHit(Agent affectedAgent, Agent affectorAgent,
        in MissionWeapon weapon, in Blow blow, in AttackCollisionData collisionData)
    {
        if (affectedAgent?.IsMainAgent == true && blow.InflictedDamage > 20)
        {
            Mission.Current.Scene.SlowMotionMode = true;
            Mission.Current.Scene.SlowMotionFactor = 0.2f;
            _slowMoTimer = SlowMoDuration;
        }
    }

    public override void OnMissionTick(float dt)
    {
        if (_slowMoTimer > 0)
        {
            _slowMoTimer -= dt;
            if (_slowMoTimer <= 0)
            {
                Mission.Current.Scene.SlowMotionMode = false;
            }
        }
    }
}
```

## Mission Properties

```csharp
// Access current mission
Mission mission = Mission.Current;

// Get agents
var allAgents = mission.Agents;
var playerAgent = mission.MainAgent;
var aliveEnemies = mission.Agents.Where(a => 
    a.IsActive() && a.Team?.IsEnemyOf(mission.PlayerTeam) == true);

// Teams
Team playerTeam = mission.PlayerTeam;
Team enemyTeam = mission.PlayerEnemyTeam;

// Scene info
Scene scene = mission.Scene;
string sceneName = mission.SceneName;

// Mission type
bool isBattle = mission.CombatType == Mission.MissionCombatType.Combat;
bool isSiege = mission.IsSiegeBattle;
bool isFieldBattle = mission.IsFieldBattle;
bool isTournament = mission.SceneName.Contains("tournament");

// Time
float missionTime = mission.CurrentTime;
```

## BehaviorType Options

```csharp
public override MissionBehaviorType BehaviorType => 
    MissionBehaviorType.Logic;      // Core mission logic
    MissionBehaviorType.Other;      // General behavior (most common)
    MissionBehaviorType.CommanderAI; // AI command behavior
```
