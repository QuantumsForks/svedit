# XML structure documentation
If you're here, it's likely you want to contribute with a new save file format!\
First of all, **thank you**!

The goal of this document is to hopefully make the structure intuitive, if it isn't already.\
(Seriously, it's not that bad!)

## The root tag (`svedit`)
The file's root tag, that contains everything `svedit` needs to successfully read from and write
to a PSX memory card block.

### Attributes
1. `pattern` (`str`): Regex pattern that maps a specific format ID (like `DRAX02`) to a "generic" ID (like `DRAX`)
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

### Example
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
1. `id` (`str`): The ID of the enum you're defining.

### Contains
1. `...`  (`int`): A list of values that the enum can assume.

### Example:
```xml
<!-- From: DRAX.xml -->
<enumdef id="relic">
    <int name="in-use">3</int>
    <int name="unlocked">1</int>
    <int name="locked">0</int>
    <!-- You could add more values! -->
</enumdef>
```

## File checksums (`checksum`)
Seeing as some PSX games use checksums to verify data integrity, `svedit` must support their use
to calculate them on the fly.

You can use multiple `checksum` tags, if the game has multiple checksum values.\
Currently supported checksum types are:
- `xor`

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

### Example
```xml
<!-- Range and offset values should go from 0x0 to 0x1FFF, as 0x2000 would be out of the block stream. -->
<checksum type="xor" range="0x0:0x1FFE" offset="0x1FFF" length="1"/>
```

## File definition (`file`)
### Attributes
1. `unfinished` (`bool`, optional: `False`): Lets the user know not every single option may be available
in this version of the format file.

### Contains
1. `...` (`Any supported`, see list below.): A list of every value in the save file.

# Supported types
`svedit`, currently, supports and parses the following Python types:

## `blank`
While not a Python type, you can use the `blank` tag to skip forward a set of bytes.

### Attributes
1. `length` (`int`): How many bytes to skip.

### Example
```xml
<blank length="4"/>
```

## `str`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read.
4. `encoding` (`str`, optional: `ascii`): What encoding to use.

### Example
```xml
<str name="name" length="8" encoding="ascii" display="Name"/>
```

## `int`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read.
4. `order` (`str`, optional: `big`): What byte order to use when parsing. Can be `big` or `little`.
5. `signed` (`bool`, optional: `False`): Whether this is a signed or unsigned integer.

### Example
```xml
<int name="level" length="4" order="little" display="Level"/>
```

## `float`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read. Can be `4` or `8` (for a double)
4. `order` (`str`, optional: `big`): What byte order to use when parsing. Can be `big` or `little`.

### Example
```xml
<float name="x" length="4" order="little" display="X"/>
```

## `bool`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read.

### Example
```xml
<bool name="unlocked_door" display="Door Unlocked" length="1"/>
```

## `tuple` / `list` / `dict`
### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.\
   In the case of `dict`, a child's `name` is also used as the key of the key-value pair.\
   In the case of `tuple` / `dict`, a child's `name` does not appear.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.

### Contains
1. `...` (`Any supported`): A list of every value inside the `tuple` / `list`

### Example (tuple)
```xml
<!-- From: DRAX.xml -->
<tuple name="playtime" display="Playtime">
    <int name="hours" length="4" order="little" display="Hours"/>
    <int name="minutes" length="4" order="little" display="Minutes"/>
    <int name="seconds" length="4" order="little" display="Seconds"/>
</tuple>
```

## `enum`
While also not a (regular) Python type, you can use enums defined by `enumdef` in the `enums` tag. 

### Attributes
1. `name` (`str`): A name that identifies the entry in the save file. Must be unique on that level.
2. `display` (`str`, optional): An optional, "human-friendly" name to display on the TUI.
3. `length` (`int`): How many bytes to read.
4. `id` (`str`): The ID of the enumdef this enum references.
### Example
```xml
<!-- From: DRAX.xml -->
<enum id="relic" name="holy_snorkel" display="Holy Symbol" length="1"/>
```
