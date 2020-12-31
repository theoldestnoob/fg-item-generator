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
This script reads in a JSON file (schema defined in 'fg-parametric-items-schema.json'), procedurally generates items based on that file, generates a Fantasy Grounds module containing those items, and outputs the resulting files (`definition.xml` and `db.xml`) into a directory ready to be dropped into your Fantasy Grounds modules folder. I recommend also adding an image named 'thumbnail.png' to the directory, to make finding the module in the module list and library easier.

The modules that this script creates contain:
- items
- a Library entry
- a Library page named Documentation listing the author and contributors
- a Library page named Items listing all the items alphabetically
- a Library page named Items By Cost listing all the items grouped by cost

In order to run it, you will need Python installed. All libraries used are standard, so you should not need to install anything else. You should be able to simply download the script, create an item definition .json file, and run it. You can see the command line arguments above, or by using the command `python fg-item-generator.py --help`.

The modules that result have been tested and will work in the following rulesets:
- Core RPG, MoreCore, D&D 2E, D&D 3.5E, D&D 4E, D&D 5E, Pathfinder 1E, Pathfinder 2E, Starfinder, Fate Core, Cypher System, Numenera, The Strange
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