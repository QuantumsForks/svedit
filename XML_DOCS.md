# XML structure documentation
If you're here, it's likely you want to contribute with a new save file format!\
First of all, **thank you**!

The goal of this document is to hopefully make the structure intuitive, if it isn't already.\
(Seriously, it's not that bad!)

## The root tag (`svedit`)
The file's root tag, that contains everything `svedit` needs to successfully read from and write
to a PSX memory card block.

### Attributes
1. `pattern` (`str`): Regex pattern that maps a specific format ID (like `DRAX02`) to a "generic"
ID (like `DRAX`)
2. `generic` (`str`): Value that specific IDs get mapped to. File name should be `<generic>.xml`
3. `contributor` (`str`, optional): If you want, set this to your GitHub name, etc... (no links!)

> [!important]
> Please remind yourself that whatever you put in `contributor` will appear throughout `svedit`,
> both in the terminal, and the interface!\
> Due to that fact, ensure it is appropriate, and that you don't include any sensitive information.
> 
> Thank you!

### Contains
1. `enums`: A list of enum definitions (`enumdef`). Fully optional.
2. `checksum`: One or many checksums that need to be recalculated on file save.
3. `file`: The actual file structure.

### Examples
```xml
<!-- From: DRAX.xml -->
<svedit pattern="DRAX.." generic="DRAX" contributor="QuantumsSources">
	<!-- ... -->
</svedit>
```

## Enum definitions (`enumdef`)
Optionally, you can define custom "enums" to use around your file, if you have certain entries that can only
take a set list of values, like `0x00` for `locked` and `0x01` for `unlocked`, for example.

### Attributes
1. `id` (`str`): The ID of the `enum` you're defining.

### Contains
1. `...`  (`int`): A list of `int` values that the `enum` can assume.

> [!important]
> If an `enum` resolves to a value not contained in its referenced `enumdef`,
> an `InvalidEnumItemError` is raised.

### Examples
```xml
<!-- From: DRAX.xml -->
<enumdef id="relic">
    <int name="in-use">3</int>
    <int name="unlocked">1</int>
    <int name="locked">0</int>
    <!-- You could add more values! -->
</enumdef>
```

## Structure definitions (`structdef`)
Optionally, you can also define custom "structs" to use around your file, if you have certain entries that are
structured the exact same, like an item that has a `str` for name, `int` for damage, etc...

### Attributes
1. `id` (`str`): The ID of the `struct` you're defining.
2. `type` (`str`, optional: `list`): How `svedit` should display this `struct`. Can be `list` or `dict`.

### Contains:
1. `...` (`Any supported`): The structure to be assumed wherever this `structdef` is referenced.

### Examples
```xml
<structdef id="item" type="list">
    <str name="name" length="8" encoding="ascii" display="Name"/>
    <int name="damage" length="4" order="little" display="Damage"/>
</structdef>
```

## File checksums (`checksum`)
Seeing as some PSX games use checksums to verify data integrity, `svedit` must support their use
to calculate them on the fly.

You can use multiple `checksum` tags, if the game has multiple checksum values.\
Currently supported checksum types are:
- `sum`: Simple byte-summing checksum;
- `xor`: XOR checksum;

If your game uses a type not available, open an issue about it, and we'll work on it.\
Alternatively, you could add it yourself and open a pull request to have it added.

### Attributes
1. `type` (`str`, optional: `xor`): Checksum type.
2. `range` (`str`, optional: `0x00:0x1FFE`): What byte range to use for the checksum digest,
in format `0x<start>:0x<end>`.
3. `offset` (`int`, optional: `0x1FFF`): At what offset (relative to start of block)
4. `length` (`int`, optional: `0x01`): How many bytes long the checksum is.
5. `order` (`str`, optional: `big`): What byte order to use when writing. Can be `big` or `little`.

> [!note]
> `start`, `end`, and `offset` are relative to the start of the block.\
> The formula for absolute offsets is `0x2000 * (<block_id> + 1) + <value>`.

### Examples
```xml
<!-- Range and offset values should go from 0x0 to 0x1FFF, as 0x2000 would be out of the block stream. -->
<checksum type="xor" range="0x0:0x1FFE" offset="0x1FFF" length="1"/>
```

## File definition (`file`)
### Attributes
1. `unfinished` (`bool`, optional: `false`): Lets the user know not every single option may be available
in this version of the format file.

### Contains
1. `...` (`Any supported`, see list below.): A list of every value in the save file.

# Supported types
`svedit`, currently, supports and parses the following tags:

## `blank`
Using the `blank` tag, the reader will skip forward a set of bytes.

### Attributes
1. `length` (`int`): How many bytes to skip.

### Examples
```xml
<blank length="4"/>
```

## `str`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read.
4. `encoding` (`str`, optional: `ascii`): What encoding to use.

### Examples
```xml
<str name="name" length="8" encoding="ascii" display="Name"/>
```

## `int`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read.
4. `order` (`str`, optional: `big`): What byte order to use when parsing. Can be `big` or `little`.
5. `signed` (`bool`, optional: `false`): Whether this is a signed or unsigned integer.

### Examples
```xml
<int name="level" length="4" order="little" display="Level"/>
```

## `float`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read. Can be `4` or `8` (for a double)
4. `order` (`str`, optional: `big`): What byte order to use when parsing. Can be `big` or `little`.

### Examples
```xml
<float name="box_x" length="4" order="little" display="Box X position"/>
```

## `bool`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read.

### Examples
```xml
<bool name="unlocked_door" display="Door Unlocked" length="1"/>
```

> [!note]
> If a `bool` tag is 1 byte long, it assumes `0x00` as `False` and anything else as `True`.
> Else, also accepts `yes`, `true`, and `1` (`0x31`) as `True`.
> 
> If your game's structure disagrees, use an `enum` instead.\

## `list` / `dict`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
> [!note]
> In the case of `dict`, a child's `name` is also used as the key to the key-value pair.\
> In the case of `list`, a child's `name` only appears if `display` isn't set. Else, `display` is used and
> `name` is omitted.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.

### Contains
1. `...` (`Any supported`): A list of every value inside the `list` / `dict`

### Examples
```xml
<!-- From: DRAX.xml, represents a 'list' type -->
<list name="playtime" display="Playtime">
    <int name="hours" length="4" order="little" display="Hours"/>
    <int name="minutes" length="4" order="little" display="Minutes"/>
    <int name="seconds" length="4" order="little" display="Seconds"/>
</list>
```

```xml
<!-- From: DRAX.xml, represents a 'dict' type -->
<dict name="relics" display="Relics">
    <enum id="relic" name="bat_form" display="Soul of Bat" length="1"/>
    <enum id="relic" name="bat_fire" display="Fire of Bat" length="1"/>
    <enum id="relic" name="bat_echo" display="Echo of Bat" length="1"/>
    <!-- etc... -->
</dict>
```

## `enum`
While not a regular type, you can use `enums` defined by `enumdef`.

### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read.
4. `id` (`str`): The ID of the `enumdef` this `enum` references.

### Examples
```xml
<!-- From: DRAX.xml -->
<enum id="relic" name="holy_snorkel" display="Holy Symbol" length="1"/>
```

## `struct`
Similarly to `enum`, you can use `structs` defined by `structdef`.

### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `id` (`str`): The ID of the `structdef` this `struct` references.

### Examples
```xml
<list name="inventory" display="Inventory">
    <struct id="item" name="slot_0" display="Slot 0"/>
    <struct id="item" name="slot_1" display="Slot 1"/>
    <struct id="item" name="slot_2" display="Slot 2"/>
</list>
```

`struct` tags are completely interchangeable with their `type`.\
For example, as the `item` `structdef` has `type="list"`, the above example is the same as this:
```xml
<list name="inventory" display="Inventory">
    <list name="slot_0" display="Slot 0">
        <str name="name" length="8" encoding="ascii" display="Name"/>
        <int name="damage" length="4" order="little" display="Damage"/>
    </list>
    <list name="slot_1" display="Slot 1">
        <str name="name" length="8" encoding="ascii" display="Name"/>
        <int name="damage" length="4" order="little" display="Damage"/>
    </list>
    <list name="slot_2" display="Slot 2">
        <str name="name" length="8" encoding="ascii" display="Name"/>
        <int name="damage" length="4" order="little" display="Damage"/>
    </list>
</list>
```