# fg-item-generator
```
Generate a Fantasy Grounds Module filled with procedurally-generated items based on a JSON File input which defines the items to be generated. Note that this process is not random - it will generate every possible item.

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    JSON file of definitions for the items. Default: ./item_defs.json
  --output OUTPUT  Name of the directory to output the XML files to. Default: ./itemdb/
  --id ID          Item ID number to start with. Default: 1
```
https://github.com/theoldestnoob/fg-item-generator

- [Introduction](#introduction) 
  - [What It Does](#what-it-does)
  - [What It Doesn't Do](#what-it-doesnt-do)
  - [Why I Wrote It](#why-i-wrote-it)
- [Basic Usage](#basic-usage) 
- [Definition Files](#definition-files)
  - [Examples](#examples)
  - [File Format](#file-format)
    - [Schema](#schema-optional)
    - [Module](#module-mandatory)
    - [Items](#items-mandatory)
      - [Modifiers](#modifiers-mandatory)
      - [Bases](#bases-mandatory)
      - [Varieties](#varieties-optional)
## Introduction
### What It Does
This script reads in a JSON file (schema defined in 'fg-parametric-items-schema.json'), procedurally generates items based on that file, generates a Fantasy Grounds module containing those items, and outputs the resulting files (`definition.xml` and `db.xml`) into a directory ready to be dropped into your Fantasy Grounds modules folder. I recommend also adding an image named 'thumbnail.png' to the directory, to make finding the module in the module list and library easier.

The modules that this script creates contain:
- items
- a Library entry
- a Library page named Documentation listing the author and contributors
- a Library page named Items listing all the items alphabetically
- a Library page named Items By Cost listing all the items grouped by cost

The items that this script creates may have any or all of the below (but do not have to have all of them):
- procedurally generated name
- procedurally generated description
- procedurally generated name for players when not identified
- procedurally generated description for players when not identified
- procedurally generated cost/price
- procedurally generated weight
- type
- subtype

Items may be generated such that when first loaded they are:
- identified / not identified
- locked / not locked

In order to run this script, you will need Python installed. All libraries used are standard, so you should not need to install anything else. You should be able to simply download the script, create an item definition .json file, and run it. You can see the command line arguments above, or by using the command `python fg-item-generator.py --help`.

The modules that result have been tested and will work in the following rulesets:
- Core RPG, MoreCore, D&D 2E, D&D 3.5E, D&D 4E, D&D 5E, Pathfinder 1E, Pathfinder 2E, Starfinder, Fate Core, Cypher System, Numenera, The Strange
### What It Doesn't Do
- This script does not create anything other than a basic module with items in it.
- This script does not create items which interact with rulesets outside of weight and cost. No AC for procedurally generated armor, or damage and properties for procedurally generated weapons, etc.
- This script does not allow HTML or XML in any field, including the description fields - it will escape any such information and will display it as entered when the module is loaded. E.g. if you put in `<b>Description</b>` as a description in the definition file, that will appear in the item's description as `<b>Description</b>`, not as the word "**Description**" in bold text.
- This script does not generate any documentation other than a simple library page listing the author and contributors and two lists of the items. Manual editing of the db.xml file (or the use of another tool) will be required to make changes or updates to the library entry / documentation.
- This script will for the most part silently ignore any bad data passed to it. You may get warnings on the command line for certain errors in the definitions file, but can not count on it.
### Why I Wrote It
I found a module on the Fantasy Grounds forums that contained a large number of gemstones (made by forums user Lord Entrails), and spent several hours of time adding tables to it. I then decided I would like to add a greater variety of gemstones, and update the existing ones to include a name and description for when they weren't identified. After digging in to how that would be done, I discovered that manually editing all of the item definitions in Fantasy Grounds, or even in the raw xml, would have been an extremely time-intensive proces. Since each gem was just a combination of a base name and size, with the size modifying the cost, that sounded like something I could script fairly easily. After putting together a script to do that, I realized I could extend it to a more generic form and give it a lot more flexibility. The result is this project. My primary use case and almost all of my testing during development has been with generating gemstone items, but I could see it being used for Jewerly, Art Objects, or other flavor items for use in just about any game. Just define a set of materials, motifs, qualities, etc, and run the script to generate hundreds of items that will work across many rulesets.
## Basic Usage
The most basic usage is to put together an item definition file named 'item_defs.json' and then simply run the script in the same directory as that file: `python fg-item-generator.py`. This will output the resulting module to a subdirectory named 'itemdb/' in that directory.

If you want to use a different file for input, you can pass that file's name in as the `--input` option.

If you want to use a different directory for output, you can pass that directory's name in as the `--output` option. The script will use an existing directory, or create one if no directory of that name exists. The script will overwrite any files named 'definition.xml' and 'db.xml' present in the directory, so I recommend always outputting to a temporary directory and then copying it elsewhere for modification or use. 

You can copy the output directory into your Fantasy Grounds module folder as-is, or zip the contents and change the file extension to '.mod' for a single file module. To have a thumbnail image in the Module list and Library, you can add a PNG image named `thumbnail.png` to the directory.

If you want to generate items to add to an existing module, you can pass it the `--id` option. By default, the script will generate items starting at id-00001. If given the --id option, it will generate items starting with whatever number is passed to it (e.g. `python fg-item-generator.py --id 327` will generate items starting at 'id-00327'). You can then open the resulting `db.xml` file and copy the items from it to paste into your module.

Here is an example of using all of the options, compiling the example reference defintions and outputting it to a directory named reference, and starting at item ID 350:

`python fg-item-generator.py --in examples/reference.json --out reference --id 350`
## Definition Files
### Examples
There are several example definition files and their output available in the repository in the examples/ directory.
- `candelabras.json`: This is the primary example used in this documentation.
- `reference.json`: This is used for testing the script, and contains definitions that trigger most of the script's possible behavior. It should contain every possible field, and may be useful as a reference when producing your own definition files.
- `lord_entrails_gems.json`: This is a practical example. It generates a copy of LordEntrails' Gemstones module (without the proper Library pages). This reflects the way that this script was originally intended to be used, but it is much longer and more complicated than the compact version, which produces the same output. It may serve as a useful reference, but given the simplicity of the module (one modifier, simple name and description strings) I would recommend actually using something more like the compact version as the basis for similar modules.
- `lord_entrails_compact.json`: This generates a copy of LordEntrails' Gemstones module, but the definition is just over 1/6 the size and is much more readable.
- `gemstones_complex.json`: This generates gemstones as well, but is much more complex. It includes modifiers for size, quality, cut, and optical phenomenon (asterism, chatoyancy, etc), and several varations on each defined stone type. It is very far from complete, as only four gemstones have been defined: Agate, Moss Agate, Azurite, and Citrine. However, those four basic types generate 604 unique items when combined with *some* of the defined modifiers. Cominatorial math is a heck of a thing.
- `malformed_defs.json`: This is used for testing the script, and may contain several malformed modifiers and definitions with bad or nonsensical values. It will still run and generate a valid module.

Each example's output is also included in the repository, in the examples/ directory.

I recommend looking at the examples to get a starting point when creating your own definition file.
### File Format
The script takes as input a JSON-formatted file containing the following objects. Most of the examples below are taken from [examples/candelabras.json](https://github.com/theoldestnoob/fg-item-generator/blob/main/examples/candelabras.json).
#### Schema - Optional
A schema defines how a JSON file should be formatted, and validates that it has been correctly constructed. It is ignored by the script, but may be useful while building the definition file.

A schema is not required. The schema is available as part of the project, and you can link either a local copy or the one hosted on github at: https://raw.githubusercontent.com/theoldestnoob/fg-item-generator/main/fg-parametric-items-schema.json

If you have downloaded the entire git repository, your local copy of the schema will match the script. The copy hosted on github may change as the project is updated, so it is possible that older definition files may not conform to it in the future.
##### Examples
```
"$schema": "../fg-parametric-items-schema.json"
```
```
"$schema": "https://raw.githubusercontent.com/theoldestnoob/fg-item-generator/main/fg-parametric-items-schema.json"
```
#### Module - Mandatory
The `module` section defines several module-level attributes. The name and author are mandatory. All other values, if not present, will either have the default used or omit the relevant section from the module's contents. 
##### Examples
```
"module" : {
		"version" : "3.1",
		"release" : "7|CoreRPG:3",
		"name" : "FG Item Generator Reference",
		"category" : "Accessories",
		"author" : "theoldestnoob",
		"contributors" : [ "Contributor1", "Contributor2" ],
		"ruleset" : "Any"
	}
```
```
"module" : {
		"name" : "Noob's Candelabras",
		"author" : "theoldestnoob"
	}
```
##### Parameters
- `name`
  - Type: String
  - Mandatory: This must be included in the module definition.
  - Default: None. If not present, the script will display an error and exit.
  - This is the module name. It will appear in the Module list and Library. Inserted in the definition.xml file in the `<name>` tag.
- `author`
  - Type: String
  - Mandatory: This must be included in the module definition.
  - Default: None. If not present, the script will display an error and exit.
  - This is the module author. It will appear in the Module list and the Documentation reference page. Inserted in the definition.xml file in the `<author>` tag.
- `version`
  - Type: String
  - Optional: If not included in the JSON definition, the default value will be used.
  - Default: 4
  - Inserted in the definition.xml file in the `<root>` tag as the property `"version"`.
- `release`
  - Type: String
  - Optional: If not included in the JSON definition, the default value will be used.
  - Default: 8|CoreRPG:4
  - Inserted in the definition.xml file in the `<root>` tag as the property `"release"`
- `category`
  - Type: String
  - Optional: If not included in the JSON definition, the default value will be used.
  - Default: Accessories
  - This is the module category. It will categorize the Module in the Library when loaded. Inserted in the definition.xml file in the `<category>` tag.
- `contributors`
  - Type: Array of Strings
  - Optional: If not included in the JSON definition, no contributors will be listed.
  - Default: None
  - This is a list of the contributors. It will appear in the Documentaiton reference page.
- `ruleset`
  - Type: String
  - Optional: If not included in the JSON definition, the default value will be used.
  - Default: Any
  - This is the ruleset for which the module is intended. It will determine which rulesets the module can be loaded into. Inserted in the definition.xml file in the `<ruleset>` tag.
#### Items - Mandatory
The `items` section is composed of two mandatory subsections, `modifiers` and `bases`. They are discussed below.
##### Example
```
	"items" : {
		"modifiers" : {
            "modifier_1" : [
                { ... },
                { ... }
            ],
            "modifier_2" : [
                { ... },
                { ... }
            ]
        },
        "bases" : [ 
            { ... },
            { ... } 
        ]
    }
```
#### Modifiers - Mandatory
The `modifiers` section is composed of one or more arrays of objects. The objects' names can be anything - they will be matched with entries in the `bases` definition. Each object inside the top level array must contain an array of one or more objects. Each of these arrays defines a set of modifiers which can be applied to the `bases` to adjust one or more of the base item's: weight, cost, name, description, nonidentified name, or nonidentified description.
##### Examples
```
"modifiers" : {
    "size" : [
        {
            "key" : "S",
            "name" : "Small",
            "desc" : "small",
            "mod_weight" : 0.8
        },
        {
            "key" : "M",
            "name" : "Medium",
            "desc" : "medium"
        },
        {
            "key" : "L",
            "name" : "Large",
            "desc" : "large",
            "mod_weight" : 1.2
        }
    ],
    "material" : [
        {
            "key" : "Fe",
            "name" : "Iron",
            "desc" : "iron",
            "nonid_name" : "Black Metal",
            "nonid_desc" : "a dull dark metal",
            "mod_cost" : 0.5,
            "mod_weight" : 0.8
        },
        {
            "key" : "Ag",
            "name" : "Silver",
            "desc" : "silver",
            "nonid_name" : "Grey Metal",
            "nonid_desc" : "a shiny grey metal"
        },
        {
            "key" : "Au",
            "name" : "Gold",
            "desc" : "golden",
            "nonid_name" : "Yellow Metal",
            "nonid_desc" : "a shiny yellow metal",
            "mod_cost" : 2,
            "mod_weight" : 1.9
        }
    ]
}
```
##### Parameters
The individual modifier objects contained in the objects that `modifiers` contains (`"size"` and `"material"` in the example above) may have the following parameters.
- `key`
  - Type: String
  - Mandatory: This must be included in the module definition.
  - Default: None. If not present, the script will display a warning and continue, ignoring the invalid modifier entry.
  - This is the key by which a base item refers to an individual modifier entry in a modifier list.
- `mod_cost`
  - Type: Number or String ("x#", "+#", or "-#")
  - Optional: If not included, modifier will not modify the item's cost.
  - Default: None
  - This is an option which may be used to alter the item's base_cost. If a number is given, base_cost will be multiplied by this number. Division can be accomplished by using a number less than one (e.g. 0.5 will divide the cost in half). If a string is given, its behavior will depend on the first character: "x" is multiplication, identical to just providing a number; "+" will add the following number to the cost (e.g. "+100"); "-" will subtract the following number from the cost (e.g. "-100"). All modifiers with mod_cost present will modify the base_cost, so if one modifier is 0.5 and another modifier is 3 the end result will be the base cost multiplied by 1.5 (0.5 * 3). Order of operations is not guaranteed, although it *should* occur in order that the modifiers are listed in the base item's modifiers section; be sure to double check that the results are as intended if mixing multiplication and addition or subtraction.
- `mod_weight`
  - Type: Number or String
  - Optional: If not included, modifier will not modify the item's weight.
  - Default: None
  - This is an option which may be used to alter the item's base_weight. If a number is given, base_weight will be multiplied by this number. Division can be accomplished by using a number less than one (e.g. 0.5 will divide the cost in half). If a string is given, its behavior will depend on the first character: "x" is multiplication, identical to just providing a number; "+" will add the following number to the weight (e.g. "+100"); "-" will subtract the following number from the weight (e.g. "-100"). All modifiers with mod_weight present will modify the base_weight, so if one modifier is 0.5 and another modifier is 3 the end result will be the base weight multiplied by 1.5 (0.5 * 3). Order of operations is not guaranteed, although it *should* occur in order that the modifiers are listed in the base item's modifiers section; be sure to double check that the results are as intended if mixing multiplication and addition or subtraction.
- `name`
  - Type: String
  - Optional
  - Default: None
  - This is a convention, not a defined parameter in the script. It is intended to be used to replace a token in the base item's name, if desired. It can be omitted with no issue.
- `desc`
  - Type: String
  - Optional
  - Default: None
  - This is a convention, not a defined parameter in the script. It is intended to be used to replace a token in the base item's description, if desired. It can be omitted with no issue.
- `nonid_name`
  - Type: String
  - Optional
  - Default: None
  - This is a convention, not a defined parameter in the script. It is intended to be used to replace a token in the base item's name, if desired. It can be omitted with no issue.
- `nonid_desc`
  - Type: String
  - Optional
  - Default: None
  - This is a convention, not a defined parameter in the script. It is intended to be used to replace a token in the base item's description, if desired. It can be omitted with no issue.
- anything else
  - Type: String
  - Optional
  - Default: None
  - Anything can be entered to be used to replace tokens in the base item's item_name, description, nonid_name, or nonid_desc.
#### Bases - Mandatory
The `bases` section is composed of one or more objects defining a base object to be modified.
##### Example
```
"bases" : [
    {
        "base_name" : "Candelabra",
        "item_name" : "|size#name| |varieties#name| |material#name| |base_name|",
        "description" : "This is a |size#desc| |material#desc| |base_name|. |varieties#desc|",
        "nonid_name" : "|size#name| |material#nonid_name| |base_name|",
        "nonid_description" : "This |base_name| is made of |material#nonid_desc|. |varieties#desc|",
        "base_cost" : 100,
        "cost_ceiling" : 200,
        "cost_floor" : 20,
        "cost_units" : "gp",
        "cost_whole_num": true,
        "base_weight": 3,
        "weight_ceiling": 5,
        "weight_floor": 1,
        "weight_whole_num": false,
        "item_type": "Treasure",
        "subtype": "Art Objects",
        "identified": 0,
        "locked": 1,
        "varieties": [
            { ... }
        ],
        "modifiers": {
            "size" : [ "S", "L" ],
            "material" : [ "Fe", "Au", "Ag" ]
        }
    }
]
```
##### Parameters
- `item_name`
  - Type: String
  - Optional: If not included, generated items will not have a name.
  - Default: None
  - Inserted into a db.xml item entry in the `<name>` tag. This is a string defining what the generated item's name will be. It may include *tokens*, strings enclosed in the `|` character which will be replaced by the script. These tokens can include any parameter in the base item, or any parameter in the varieties or modifiers. To include a base parameter, simply put the name of the parameter inside a pair of | characters (e.g. `|base_name|`). To include a variety's parameter, put the name of the parameter inside a pair of | characters prepended with "varieties#" (e.g. `|varieties#name|`). To include a modifier's parameter, put the module's name and parameter name inside a pair of | characters, separated by the `#` character (e.g. `|size#name|`, `|material#name|`). As a result of the way these tokens are handled, you can not use the `|` or `#` character inside of item names.
- `description`
  - Type: String
  - Optional: If not included, generated items will not have a description.
  - Default: None
  - Inserted into a db.xml item entry in the `<description>`, `<flavor>`, `<notes>`, and `<text>` tags. This is a string defining what the generated item's description will be. It may include *tokens*, strings enclosed in the `|` character which will be replaced by the script. These tokens can include any parameter in the base item, or any parameter in the varieties or modifiers. To include a base parameter, simply put the name of the parameter inside a pair of | characters (e.g. `|base_name|`). To include a variety's parameter, put the name of the parameter inside a pair of | characters prepended with "varieties#" (e.g. `|varieties#name|`). To include a modifier's parameter, put the module's name and parameter name inside a pair of | characters, separated by the `#` character (e.g. `|size#name|`, `|material#name|`). As a result of the way these tokens are handled, you can not use the `|` or `#` character inside of item descriptions.
- `nonid_name`
  - Type: String
  - Optional: If not included, generated items will not have a different name when not indentified.
  - Default: None
  - Inserted into a db.xml item entry in the `<nonid_name>` tag. This is a string defining what the generated item's name will be when not identified. It may include *tokens*, strings enclosed in the `|` character which will be replaced by the script. These tokens can include any parameter in the base item, or any parameter in the varieties or modifiers. To include a base parameter, simply put the name of the parameter inside a pair of | characters (e.g. `|base_name|`). To include a variety's parameter, put the name of the parameter inside a pair of | characters prepended with "varieties#" (e.g. `|varieties#name|`). To include a modifier's parameter, put the module's name and parameter name inside a pair of | characters, separated by the `#` character (e.g. `|size#name|`, `|material#name|`). As a result of the way these tokens are handled, you can not use the `|` or `#` character inside of item names.
- `nonid_description`
  - Type: String
  - Optional: If not included, generated items will not have a description when not identified.
  - Default: None
  - Inserted into a db.xml item entry in the `<nonidentified>` and `<nonid_notes>` tags. This is a string defining what the generated item's description will be when not identified. It may include *tokens*, strings enclosed in the `|` character which will be replaced by the script. These tokens can include any parameter in the base item, or any parameter in the varieties or modifiers. To include a base parameter, simply put the name of the parameter inside a pair of | characters (e.g. `|base_name|`). To include a variety's parameter, put the name of the parameter inside a pair of | characters prepended with "varieties#" (e.g. `|varieties#name|`). To include a modifier's parameter, put the module's name and parameter name inside a pair of | characters, separated by the `#` character (e.g. `|size#name|`, `|material#name|`). As a result of the way these tokens are handled, you can not use the `|` or `#` character inside of item descriptions.
- `base_cost`
  - Type: Number
  - Optional: If not included, generated items will not have a cost or price.
  - Default: None
  - This is the base number which may be modified by varieties or modifiers to result in the generated item's cost, which will be inserted into a db.xml item entry in the `<cost>` and `<price>` tags.
- `cost_ceiling`
  - Type: Number
  - Optional
  - Default: None
  - This is the largest a cost may become after modification. Any final cost after modification which is larger than this number will be replaced with this number. Will be ignored if base_cost is not present.
- `cost_floor`
  - Type: Number
  - Optional
  - Default: 0
  - This is the smallest a cost may become after modification. Any final cost after modification which is smaller than this number will be replaced with this number. Will be ignored if base_cost is not present.
- `cost_units`
  - Type: String
  - Optional
  - Default: None
  - This is a string which will be appended to the final cost (e.g. "gp", "sp").
- `cost_whole_num`
  - Type: Boolean (true or false)
  - Optional
  - Default: true
  - This will determine whether a cost must be a whole number or may have a decimal portion. If true (or omitted), the final cost will be a whole number, dropping any decimal portion (flooring or rouding down the number to the nearest integer value).
- `base_weight`
  - Type: Number
  - Optional: If not included, generated items will not have a weight.
  - Default: None
  - This is the base number which may be modified by varieties or modifiers to result in the generated item's weight, which will be inserted into a db.xml item entry in the `<weight>` tag.
- `weight_ceiling`
  - Type: Number
  - Optional
  - Default: None
  - This is the largest a weight may become after modification. Any final weight after modification which is larger than this number will be replaced with this number. Will be ignored if base_weight is not present.
- `weight_floor`
  - Type: Number
  - Optional
  - Default: 0
  - This is the smallest a weight may become after modification. Any final weight after modification which are smaller than this number will be replaced with this number. Will be ignored if base_weight is not present.
- `weight_whole_num`
  - Type: Boolean (true or false)
  - Optional: If not included, default value will be used.
  - Default: false
  - This will determine whether a weight must be a whole number or may have a decimal portion. If true, the final weight will be a whole number, dropping any decimal portion (flooring or rouding down the number to the nearest integer value).
- `item_type`
  - Type: String
  - Optional: If not included, item will not have a 'Type'.
  - Default: None
  - Inserted into the db.xml item entry in the `<type>` tag.
- `subtype`
  - Type: String
  - Optional: If not included, item will not have a 'Subtype'.
  - Default: None
  - Inserted into the db.xml item entry in the `<subtype>` tag.
- `identified`
  - Type: Number (value: 0 or 1)
  - Optional
  - Default: 1
  - Inserted into the db.xml item entry in the `<isidentified>` tag. If 1, the item will be identified when the module is loaded. If 0, the item will not be identified when the module is loaded.
- `locked`
  - Type: Number (value: 0 or 1)
  - Optional
  - Default: 1
  - Inserted into the db.xml item entry in the `<locked>` tag. If 1, the item will be locked when the module is loaded. If 0, the item will not be locked when the module is loaded.
- `modifiers`
  - Type: Object containing one or more Arrays of one or more Strings.
  - Optional: If not included, no modifiers will be used when generating items, only base items and varieties.
  - Default: None
  - Each Array has a key which must match a defined modifier (e.g. `"size'`, "`material`"), and contains one or more strings which correspond to `key` values in those modifiers (e.g. `[ "S", "M", "L" ]` for `size`). This array determines which specific modifiers will be applied to the base item to generate the items. This allows you to define lists of modifiers and then apply them selectively depending on base item. For a complex example of this functinoality, see the `cut` modifiers in the [examples/gemstones_complex.json](https://github.com/theoldestnoob/fg-item-generator/blob/main/examples/gemstones_complex.json) example. A large number of cuts are defined, and then individual gemstones only have a smaller subset of those cut modifiers applied to them depending on what type of cuts are appropriate for the type of gemstone (i.e. faceted or not faceted).
- `varieties`
  - Type: Array of Objects
  - Optional
  - Default: None
  - This is 
- anything else
  - Type: String
  - Optional
  - Default: None
  - Anything can be entered to be used to replace tokens in the item_name, description, nonid_name, or nonid_desc. In addition to the parameters listed above, there may be value in including a `name_nonid` and `desc_nonid` parameter or something similar, if you wish to include some hint at a modifier's nature in the item's nonidentified name and description. The reference definition modifier entries include `desc_nonid` used for this purpose.
#### Varieties - Optional
Each base item may contain a list of varieties. Varieties are special modifiers which can override most parameters from the base object.
##### Example
```
"varieties": [
    { 
        "name": "Functional",
        "desc" : "It is unornamented."
    },
    {
        "name" : "Luxury",
        "desc": "It is covered in intricate carvings.",
        "base_cost" : 1000,
        "cost_ceiling" : 10000,
        "cost_floor" : 500
    }
]
```
##### Parameters
Each variety may contain the same parameters as a base, and will override all except: 
- item_name
- description
- nonid_name
- nonid_description. 
If one of those four is present it will be treated as "anything else" and used solely to replace tokens in the base's name, description, nonid_name, or nonid_description.
## Known Bugs
- Sometimes items marked as unidentified will load into a campaign as identified