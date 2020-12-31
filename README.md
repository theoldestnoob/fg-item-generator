# fg-item-generator
```
Generate a Fantasy Grounds Module filled with procedurally-generated items based on a JSON File input which defines the items to be generated. Note that this process is not random - it will generate every possible item.

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    JSON file of definitions for the items. Default: ./item_defs.json
  --output OUTPUT  Name of the directory to output the XML files to. Default: ./itemdb/
  --id ID          Item ID number to start with. Default: 1
```

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

If you want to generate items to add to an existing module, you can pass it the `--id` option. By default, the script will generate items starting at id-00001. If given the --id option, it will generate items starting with whatever number is passed to it (e.g. `python fg-item-generator.py --id 327` will generate items starting at 'id-00327'). You can then open the resulting `db.xml` file and copy the items from it to paste into your module.

Here is an example of using all of the options, compiling the example reference defintions and outputting it to a directory named reference, and starting at item ID 350:

`python fg-item-generator.py --in examples/reference.json --out reference --id 350`
## Definition Files
This section coming soon...
## Known Bugs
- Sometimes items marked as unidentified will load into a campaign as identified