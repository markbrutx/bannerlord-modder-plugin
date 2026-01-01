# XSLT XML Patching

Modify native XML files without overwriting them. XSLT transformations are applied at load time.

## How It Works

1. Create `.xslt` file with same name as target XML
2. Place in same path as your mod's XML
3. Game applies XSLT to modules loaded BEFORE yours
4. Then loads your mod's XML (additive)

## Basic Template

Every XSLT file needs this identity template to copy unchanged nodes:

```xml
<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output omit-xml-declaration="yes"/>
  
  <!-- Identity template - copies everything unchanged -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- Your modifications go here -->
  
</xsl:stylesheet>
```

## Common Operations

### Remove Element

```xml
<!-- Remove specific item -->
<xsl:template match="Item[@id='item_to_remove']"/>

<!-- Remove specific troop -->
<xsl:template match="NPCCharacter[@id='troop_to_remove']"/>

<!-- Remove multiple items -->
<xsl:template match="Item[@id='item1' or @id='item2' or @id='item3']"/>
```

### Modify Attribute

```xml
<!-- Change item value -->
<xsl:template match="Item[@id='iron_sword']/@value">
  <xsl:attribute name="value">500</xsl:attribute>
</xsl:template>

<!-- Change troop skill -->
<xsl:template match="NPCCharacter[@id='imperial_recruit']/skills/skill[@id='OneHanded']/@value">
  <xsl:attribute name="value">50</xsl:attribute>
</xsl:template>

<!-- Modify culture color -->
<xsl:template match="Culture[@id='empire']/@color">
  <xsl:attribute name="color">0xFF0000FF</xsl:attribute>
</xsl:template>
```

### Add Attribute

```xml
<!-- Add is_hidden_encyclopedia to troop -->
<xsl:template match="NPCCharacter[@id='aserai_recruit']">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="is_hidden_encyclopedia">true</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>
```

### Replace Child Element

```xml
<!-- Replace kingdom relationships -->
<xsl:template match="Kingdom[@id='aserai']/relationships">
  <relationships>
    <relationship kingdom="Kingdom.empire_s" value="-1" isAtWar="true"/>
    <relationship kingdom="Kingdom.vlandia" value="50" isAtWar="false"/>
  </relationships>
</xsl:template>
```

### Add Child Element

```xml
<!-- Add skill to troop -->
<xsl:template match="NPCCharacter[@id='my_troop']/skills">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
    <skill id="Athletics" value="100"/>
  </xsl:copy>
</xsl:template>

<!-- Add equipment item -->
<xsl:template match="NPCCharacter[@id='my_troop']/equipmentSet/equipment[1]">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
  <equipment slot="Item3" id="Item.throwing_axe"/>
</xsl:template>
```

## File Examples

### ModuleData/items.xslt

```xml
<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output omit-xml-declaration="yes"/>
  
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- Make iron sword more valuable -->
  <xsl:template match="Item[@id='iron_sword']/@value">
    <xsl:attribute name="value">1000</xsl:attribute>
  </xsl:template>

  <!-- Remove headscarf items -->
  <xsl:template match="Item[@id='headscarf_d']"/>
  <xsl:template match="Item[@id='open_head_scarf']"/>
  
</xsl:stylesheet>
```

### ModuleData/spnpccharacters.xslt

```xml
<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output omit-xml-declaration="yes"/>
  
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- Buff imperial recruit -->
  <xsl:template match="NPCCharacter[@id='imperial_recruit']/skills/skill[@id='OneHanded']/@value">
    <xsl:attribute name="value">60</xsl:attribute>
  </xsl:template>
  
  <xsl:template match="NPCCharacter[@id='imperial_recruit']/skills/skill[@id='Athletics']/@value">
    <xsl:attribute name="value">50</xsl:attribute>
  </xsl:template>

  <!-- Hide caravaneers from encyclopedia -->
  <xsl:template match="NPCCharacter[contains(@id,'caravan_master')]">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:attribute name="is_hidden_encyclopedia">true</xsl:attribute>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>
  
</xsl:stylesheet>
```

### ModuleData/settlements.xslt

```xml
<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output omit-xml-declaration="yes"/>
  
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- Increase town prosperity -->
  <xsl:template match="Settlement[@id='town_EN1']/Town/@prosperity">
    <xsl:attribute name="prosperity">5000</xsl:attribute>
  </xsl:template>

  <!-- Change village production -->
  <xsl:template match="Settlement[@id='village_EN1_1']/Village/@village_type">
    <xsl:attribute name="village_type">iron_mine</xsl:attribute>
  </xsl:template>
  
</xsl:stylesheet>
```

## SubModule.xml Setup

XSLT files use same XML entries. No separate registration needed:

```xml
<Xmls>
  <!-- This entry covers both items.xml AND items.xslt -->
  <XmlNode>
    <XmlName id="Items" path="items"/>
  </XmlNode>
  
  <XmlNode>
    <XmlName id="NPCCharacters" path="spnpccharacters"/>
  </XmlNode>
</Xmls>
```

## XPath Reference

| XPath | Meaning |
|-------|---------|
| `Item[@id='x']` | Item with id="x" |
| `NPCCharacter[contains(@id,'recruit')]` | NPCCharacter with "recruit" in id |
| `Culture[@id='empire']/basic_troop` | basic_troop child of empire culture |
| `//skill[@id='OneHanded']` | Any skill element with id="OneHanded" |
| `Item/@value` | value attribute of Item |
| `Settlement/Town/@prosperity` | prosperity attribute of Town child |

## Order of Application

1. Native → SandBoxCore → Sandbox → StoryMode (TW modules)
2. Your mod's XSLT applied to all above
3. Your mod's XML added (merged)

**Important**: XSLT only affects modules loaded BEFORE yours in load order.

## Debugging Tips

1. Use XML Editor from Modding Kit for XSLT editing
2. Validate XPath with online testers
3. Check game logs for XML parsing errors
4. Test with minimal changes first
5. Comments in XSLT are standard XML: `<!-- comment -->`
