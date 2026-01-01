# Campaign Events Reference

## Event Registration

All events registered in `RegisterEvents()` of `CampaignBehaviorBase`:

```csharp
public override void RegisterEvents()
{
    CampaignEvents.EventName.AddNonSerializedListener(this, OnEventHandler);
}
```

## Time-Based Events

```csharp
CampaignEvents.HourlyTickEvent           // Every hour
CampaignEvents.DailyTickEvent            // Every day
CampaignEvents.WeeklyTickEvent           // Every week
CampaignEvents.HourlyTickPartyEvent      // Per party, hourly
CampaignEvents.DailyTickPartyEvent       // Per party, daily
CampaignEvents.DailyTickSettlementEvent  // Per settlement, daily
CampaignEvents.DailyTickHeroEvent        // Per hero, daily
CampaignEvents.DailyTickClanEvent        // Per clan, daily
CampaignEvents.MobilePartyHourlyTick     // MobileParty param
```

### Usage
```csharp
CampaignEvents.DailyTickEvent.AddNonSerializedListener(this, OnDailyTick);

private void OnDailyTick()
{
    foreach (var hero in Hero.AllAliveHeroes)
    {
        // Daily processing
    }
}

CampaignEvents.DailyTickPartyEvent.AddNonSerializedListener(this, OnPartyDailyTick);

private void OnPartyDailyTick(MobileParty party)
{
    if (party.IsMainParty)
    {
        // Player party daily tick
    }
}
```

## Battle & Combat Events

```csharp
// Before battle
CampaignEvents.OnPlayerBattleEndEvent           // (MapEvent)
CampaignEvents.MapEventEnded                    // (MapEvent)
CampaignEvents.OnBattleEndedEvent               // ()
CampaignEvents.OnSiegeEventEndedEvent           // (SiegeEvent)
CampaignEvents.OnSiegeBombardmentHitEvent       // (...)

// Combat results
CampaignEvents.OnPlayerCharacterChangedEvent    // ()
CampaignEvents.HeroWounded                      // (Hero)
CampaignEvents.HeroKilledEvent                  // (Hero victim, Hero killer, KillCharacterAction.KillCharacterActionDetail, bool)
CampaignEvents.OnHeroGetsBusyEvent              // (Hero, HeroGetsBusyReasons)

// Troops
CampaignEvents.OnTroopRecruitedEvent            // (Hero, Settlement, Hero, CharacterObject, int)
CampaignEvents.OnTroopGivenToSettlementEvent    // (Hero, Settlement, TroopRoster)
CampaignEvents.OnUnitRecruitedEvent             // (CharacterObject, int)
```

### Battle Event Example
```csharp
CampaignEvents.MapEventEnded.AddNonSerializedListener(this, OnMapEventEnded);

private void OnMapEventEnded(MapEvent mapEvent)
{
    if (mapEvent.IsPlayerMapEvent && mapEvent.WinningSide == mapEvent.PlayerSide)
    {
        var renownGained = mapEvent.InfluenceExchangeDecided;
        InformationManager.DisplayMessage(
            new InformationMessage($"Victory! +{renownGained:F0} renown"));
    }
}
```

## Settlement Events

```csharp
CampaignEvents.OnSettlementOwnerChangedEvent    // Settlement, bool, Hero, Hero, Hero, ChangeOwnerOfSettlementAction.ChangeOwnerOfSettlementDetail
CampaignEvents.SettlementEntered                // (MobileParty, Settlement, Hero)
CampaignEvents.OnSettlementLeftEvent            // (MobileParty, Settlement)
CampaignEvents.OnHideoutSpottedEvent            // (PartyBase, PartyBase)
CampaignEvents.VillageBeingRaided               // (Village)
CampaignEvents.VillageLooted                    // (Village)
CampaignEvents.OnSiegeEventStartedEvent         // (SiegeEvent)
CampaignEvents.OnPlayerJoinedTournamentEvent    // (Town, bool)
CampaignEvents.TournamentFinished               // (CharacterObject, MBReadOnlyList<CharacterObject>, Town, ItemObject)
```

### Settlement Change Example
```csharp
CampaignEvents.OnSettlementOwnerChangedEvent.AddNonSerializedListener(this, OnSettlementOwnerChanged);

private void OnSettlementOwnerChanged(
    Settlement settlement, 
    bool openToClaim, 
    Hero newOwner, 
    Hero oldOwner, 
    Hero capturerHero,
    ChangeOwnerOfSettlementAction.ChangeOwnerOfSettlementDetail detail)
{
    if (newOwner == Hero.MainHero)
    {
        InformationManager.DisplayMessage(
            new InformationMessage($"You now own {settlement.Name}!"));
    }
}
```

## Hero & Character Events

```csharp
CampaignEvents.HeroCreated                      // (Hero, bool)
CampaignEvents.HeroKilledEvent                  // (Hero, Hero, KillCharacterAction.KillCharacterActionDetail, bool)
CampaignEvents.HeroPrisonerTaken                // (PartyBase, Hero)
CampaignEvents.HeroPrisonerReleased             // (Hero, PartyBase, IFaction, EndCaptivityDetail)
CampaignEvents.HeroRelationChanged              // (Hero, Hero, int, bool, ChangeRelationAction.ChangeRelationDetail, Hero, Hero)
CampaignEvents.HeroLevelledUp                   // (Hero, bool)
CampaignEvents.HeroGainedSkill                  // (Hero, SkillObject, int, bool)
CampaignEvents.OnHeroChangedClanEvent           // (Hero, Clan)
CampaignEvents.OnCompanionClanCreatedEvent      // (Clan)
CampaignEvents.OnHeroJoinedPartyEvent           // (Hero, MobileParty)
CampaignEvents.OnHeroOccupationChangedEvent     // (Hero, Occupation, Occupation)
CampaignEvents.OnCharacterCreationIsOverEvent   // ()
```

### Hero Event Example
```csharp
CampaignEvents.HeroPrisonerTaken.AddNonSerializedListener(this, OnHeroPrisonerTaken);

private void OnHeroPrisonerTaken(PartyBase captor, Hero prisoner)
{
    if (prisoner.Clan == Clan.PlayerClan)
    {
        InformationManager.AddQuickInformation(
            new TextObject($"{prisoner.Name} has been captured!"));
    }
}
```

## Political & Diplomacy Events

```csharp
CampaignEvents.ClanChangedKingdom               // (Clan, Kingdom, Kingdom, ChangeKingdomAction.ChangeKingdomActionDetail, bool)
CampaignEvents.OnPeaceOfferedEvent              // (IFaction, IFaction)
CampaignEvents.MakePeace                        // (IFaction, IFaction, MakePeaceAction.MakePeaceDetail)
CampaignEvents.WarDeclared                      // (IFaction, IFaction, DeclareWarAction.DeclareWarDetail)
CampaignEvents.KingdomDestroyedEvent            // (Kingdom)
CampaignEvents.KingdomCreatedEvent              // (Kingdom)
CampaignEvents.OnNewIssueCreatedEvent           // (IssueBase)
CampaignEvents.OnIssueUpdatedEvent              // (IssueBase, IssueBase.IssueUpdateDetails, Hero)
CampaignEvents.OnVassalTransferOfferEvent       // (...)
```

## Party & Army Events

```csharp
CampaignEvents.MobilePartyCreated               // (MobileParty)
CampaignEvents.MobilePartyDestroyed             // (MobileParty, PartyBase)
CampaignEvents.PartyAttachedAnotherParty        // (MobileParty)
CampaignEvents.OnPartyDisbandedEvent            // (MobileParty, Settlement)
CampaignEvents.OnPartyDisbandStartedEvent       // (MobileParty)
CampaignEvents.OnPartyJoinedArmyEvent           // (MobileParty)
CampaignEvents.OnPartyRemovedFromArmyEvent      // (MobileParty)
CampaignEvents.ArmyCreated                      // (Army)
CampaignEvents.ArmyDispersed                    // (Army, Army.ArmyDispersionReason, bool)
```

## Game State Events

```csharp
CampaignEvents.OnNewGameCreatedEvent            // (CampaignGameStarter)
CampaignEvents.OnGameLoadedEvent                // (CampaignGameStarter)
CampaignEvents.OnGameEarlyLoadedEvent           // (CampaignGameStarter)
CampaignEvents.OnSessionLaunchedEvent           // (CampaignGameStarter)
CampaignEvents.OnBeforeSaveEvent                // ()
CampaignEvents.OnSaveOverEvent                  // ()
CampaignEvents.OnCampaignTickEvent              // (float)
CampaignEvents.OnGameEndedEvent                 // ()
```

### Session Launch Example (Best for late init)
```csharp
CampaignEvents.OnSessionLaunchedEvent.AddNonSerializedListener(this, OnSessionLaunched);

private void OnSessionLaunched(CampaignGameStarter campaignGameStarter)
{
    // Safe to access all campaign systems here
    // Good place to add menus, dialogs
    campaignGameStarter.AddGameMenu("my_menu", "{=}My Menu", 
        (args) => { }, GameOverlays.MenuOverlayType.None);
}
```

## Quest Events

```csharp
CampaignEvents.QuestLogAddedEvent               // (QuestBase, bool)
CampaignEvents.OnQuestCompletedEvent            // (QuestBase, QuestBase.QuestCompleteDetails)
CampaignEvents.OnQuestStartedEvent              // (QuestBase)
```

## Trade & Economy Events

```csharp
CampaignEvents.OnPrisonerSoldEvent              // (MobileParty, TroopRoster, Settlement)
CampaignEvents.OnItemSoldEvent                  // (PartyBase, PartyBase, ItemRosterElement, int, Settlement)
CampaignEvents.OnItemProducedEvent              // (ItemObject, Settlement, int)
CampaignEvents.OnCaravanTransactionCompletedEvent // (MobileParty, Town, List<CaravanTransaction>)
```

## Conversation & Dialog Events

```csharp
CampaignEvents.OnConversationEndedEvent         // (IEnumerable<CharacterObject>)
CampaignEvents.ConversationEnded                // (IEnumerable<CharacterObject>)
```
