import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from itertools import product
import argparse
import sys
import os


class FGItem:
    def __init__(self, ident: int = 0, name: str = '-Item-', desc: str = None,
                 nonid_name: str = None, nonid_desc: str = None,
                 cost: str = None, weight: float = None,
                 item_type: str = None, subtype: str = None,
                 identified: int = 1, locked: int = 1):
        self.ident = ident
        self.name = name
        self.description = desc
        self.nonid_name = nonid_name
        self.nonid_desc = nonid_desc
        self.cost = cost
        self.weight = weight
        self.item_type = item_type
        self.subtype = subtype
        self.identified = identified
        self.locked = locked

    def gen_xml(self) -> ET.Element:
        # XML is generated on demand, not as part of the item build.
        # If there is no value for the XML entry, it doesn't get added.
        # Because Fantasy Grounds has different item formats for different
        # rulesets, we store a generic entry in the FGItem and output it
        # several times with different names in the XML.
        item_xml = ET.Element(f'id-{self.ident:05d}'.format(self.ident))
        if self.name is not None:
            name = ET.SubElement(item_xml, 'name',
                                 {'type': 'string'})
            name.text = self.name
        if self.description is not None:
            description = ET.SubElement(item_xml, 'description',
                                        {'type': 'formattedtext'})
            description.text = self.description
            flavor = ET.SubElement(item_xml, 'flavor',
                                   {'type': 'string'})
            flavor.text = self.description
            notes = ET.SubElement(item_xml, 'notes',
                                  {'type': 'formattedtext'})
            notes.text = self.description
            text = ET.SubElement(item_xml, 'text',
                                 {'type': 'formattedtext'})
            text.text = self.description
        if self.nonid_name is not None:
            nonid_name = ET.SubElement(item_xml, 'nonid_name',
                                       {'type': 'string'})
            nonid_name.text = self.nonid_name
        if self.nonid_desc is not None:
            notident = ET.SubElement(item_xml, 'nonidentified',
                                     {'type': 'string'})
            notident.text = self.nonid_desc
            nonid_notes = ET.SubElement(item_xml, 'nonid_notes',
                                        {'type': 'string'})
            nonid_notes.text = self.nonid_desc
        if self.item_type is not None:
            item_type = ET.SubElement(item_xml, 'type',
                                      {'type': 'string'})
            item_type.text = self.item_type
        if self.subtype is not None:
            subtype = ET.SubElement(item_xml, 'subtype',
                                    {'type': 'string'})
            subtype.text = self.subtype
        if self.cost is not None:
            cost = ET.SubElement(item_xml, 'cost',
                                 {'type': 'string'})
            cost.text = self.cost
        if self.weight is not None:
            nonid_weight = ET.SubElement(item_xml, 'weight',
                                         {'type': 'number'})
            nonid_weight.text = f'{self.weight}'
        if self.identified is not None:
            identified = ET.SubElement(item_xml, 'isidentified',
                                       {'type': 'number'})
            identified.text = f'{self.identified}'
        if self.locked is not None:
            locked = ET.SubElement(item_xml, 'locked',
                                   {'type': 'number'})
            locked.text = f'{self.locked}'
        return item_xml


def read_definitions(filename: str) -> dict:
    try:
        with open(filename, 'r', encoding='utf-8') as defs_file:
            try:
                definitions = json.load(defs_file)
            except json.decoder.JSONDecodeError as json_err:
                raise json_err
    except FileNotFoundError:
        print(f"Error! {filename} can not be found! Exiting...")
        sys.exit()
    except PermissionError:
        print(f"Error! {filename} can not be opened! Exiting...")
        sys.exit()
    except json.decoder.JSONDecodeError as json_err:
        msg = (
            f'Error! Problem reading JSON file "{filename}": '
            f'{json_err}'
        )
        print(msg)
        sys.exit()
    return definitions


def parse_mod_def(definitions: dict) -> dict:
    mod_def = {}
    if 'version' in definitions.keys():
        mod_def['version'] = definitions['version']
    else:
        mod_def['version'] = '4'
    if 'release' in definitions.keys():
        mod_def['release'] = definitions['release']
    else:
        mod_def['release'] = '8|CoreRPG:4'
    if 'name' in definitions.keys():
        mod_def['name'] = definitions['name']
    else:
        print('Error! Missing "name" in module definition! Exiting...')
        sys.exit()
    if 'category' in definitions.keys():
        mod_def['category'] = definitions['category']
    else:
        mod_def['category'] = 'Accessories'
    if 'author' in definitions.keys():
        mod_def['author'] = definitions['author']
    else:
        print('Error! Missing "author" in module definition! Exiting...')
        sys.exit()
    if 'ruleset' in definitions.keys():
        mod_def['ruleset'] = definitions['ruleset']
    else:
        mod_def['ruleset'] = 'Any'
    return mod_def


def generate_mod_def(mod_defs: dict) -> ET.Element:
    def_root = ET.Element('root', {'version': mod_defs['version'],
                                   'release': mod_defs['release']})
    elem_name = ET.SubElement(def_root, 'name')
    elem_name.text = mod_defs['name']
    elem_category = ET.SubElement(def_root, 'category')
    elem_category.text = mod_defs['category']
    elem_author = ET.SubElement(def_root, 'author')
    elem_author.text = mod_defs['author']
    elem_ruleset = ET.SubElement(def_root, 'ruleset')
    elem_ruleset.text = mod_defs['ruleset']
    return def_root


def generate_items(definitions: dict) -> list:
    all_items = []
    for base_item in definitions['bases']:
        # build 2d array of all colors and modifiers allowed by the base item
        mod_lists = []
        if 'colors' in base_item.keys():
            mod_lists.append(base_item['colors'])
            for color in mod_lists[0]:
                color['type'] = 'colors'
        if 'modifiers' in base_item.keys():
            base_mods = base_item['modifiers']
            for base_mod, val in zip(base_mods.keys(), base_mods.values()):
                mod_vals = []
                for entry in val:
                    mod_def = [x for x in definitions['modifiers'][base_mod]
                               if x['key'] == entry]
                    if mod_def == []:
                        msg = (
                                f'Warning! Base item '
                                f'"{base_item["base_name"]}" calls for '
                                f'nonexistent  entry "{entry}" from '
                                f'Modifier "{base_mod}"! Ignoring...'
                        )
                        print(msg)
                    else:
                        mod_def[0]['type'] = base_mod
                        mod_vals.extend(mod_def)
                if mod_vals:
                    mod_lists.append(mod_vals)
        # build a list of all unique permutations for this base item
        perms = product(*mod_lists)
        # parse each unique permutation to build an FGItem
        for mod_combo in perms:
            # name and description defintions are strings of tokens
            # so we substitute in defined words and phrases from the
            # base and modifier definitions
            if 'name' in base_item.keys():
                name = parse_string(base_item['name'], base_item, mod_combo)
            else:
                name = None
            if 'description' in base_item.keys():
                desc = parse_string(base_item['description'], base_item,
                                    mod_combo)
            else:
                desc = None
            if 'nonid_name' in base_item.keys():
                nonid_name = parse_string(base_item['nonid_name'],
                                          base_item, mod_combo)
            else:
                nonid_name = None
            if 'nonid_description' in base_item.keys():
                nonid_desc = parse_string(base_item['nonid_description'],
                                          base_item, mod_combo)
            else:
                nonid_desc = None
            # base cost, cost modifiers, cost ceiling, cost floor, cost unit,
            # cost whole numbers or fractional (default whole numbers)
            if 'base_cost' in base_item.keys():
                cost = base_item['base_cost']
            else:
                cost = None
            if 'cost_units' in base_item.keys():
                cost_units = base_item['cost_units']
            else:
                cost_units = None
            # modify cost as directed by colors and modifiers
            for mod in mod_combo:
                if 'base_cost' in mod.keys():
                    cost = mod['base_cost']
            if cost is not None:
                for mod in mod_combo:
                    if 'mod_cost' in mod.keys():
                        mod_cost_in = mod["mod_cost"]
                        mod_cost_str = str(mod_cost_in)
                        if (mod_cost_str[0] in 'x+-'
                                and mod_cost_str[1:].isdecimal()):
                            if mod_cost_str[0] == 'x':
                                cost = cost * float(mod_cost_str[1:])
                            elif mod_cost_str[0] == '+':
                                cost = cost + float(mod_cost_str[1:])
                            elif mod_cost_str[0] == '-':
                                cost = cost - float(mod_cost_str[1:])
                        elif str(mod_cost_str).replace('.', '1').isdecimal():
                            cost = cost * mod_cost_in
                        else:
                            msg = (
                                f'Warning! Bad mod_cost value "{mod_cost_in}" '
                                f'in Modifier "{mod}". Ignoring...'
                            )
                            print(msg)
            # cap cost at cost_ceiling and cost_floor
            if 'cost_ceiling' in base_item.keys():
                cost_ceiling = base_item['cost_ceiling']
            else:
                cost_ceiling = None
            for mod in mod_combo:
                if 'cost_ceiling' in mod.keys():
                    cost_ceiling = mod['cost_ceiling']
            if 'cost_floor' in base_item.keys():
                cost_floor = base_item['cost_floor']
            else:
                cost_floor = None
            for mod in mod_combo:
                if 'cost_floor' in mod.keys():
                    cost_floor = mod['cost_floor']
            if cost_ceiling is not None and cost > cost_ceiling:
                cost = cost_ceiling
            if cost_floor is not None and cost < cost_floor:
                cost = cost_floor
            # drop the decimal if it's supposed to be a wole number
            if 'cost_whole_num' in base_item.keys():
                cost_whole_num = base_item['cost_whole_num']
            else:
                cost_whole_num = True
            for mod in mod_combo:
                if 'cost_whole_num' in mod.keys():
                    cost_whole_num = mod['cost_whole_num']
            if cost is not None and cost_whole_num:
                cost = int(cost)
            if cost is not None:
                cost_str = f'{cost} {cost_units}'
            # base weight, weight modifiers, weight ceiling, weight floor,
            # weight whole numbers or fractional (default fractional)
            if 'base_weight' in base_item.keys():
                weight = base_item['base_weight']
            else:
                weight = None
            for mod in mod_combo:
                if 'base_weight' in mod.keys():
                    weight = mod['base_weight']
            # modify weight as directed by colors and modifiers
            if weight is not None:
                for mod in mod_combo:
                    if 'mod_weight' in mod.keys():
                        mod_wt_in = mod["mod_weight"]
                        mod_wt_str = str(mod_wt_in)
                        if (mod_wt_str[0] in 'x+-'
                                and mod_wt_str[1:].isdecimal()):
                            if mod_wt_str[0] == 'x':
                                weight = weight * float(mod_wt_str[1:])
                            elif mod_wt_str[0] == '+':
                                weight = weight + float(mod_wt_str[1:])
                            elif mod_wt_str[0] == '-':
                                weight = weight - float(mod_wt_str[1:])
                        elif str(mod_wt_str).replace('.', '1').isdecimal():
                            weight = weight * float(mod_wt_in)
                        else:
                            msg = (
                                f'Warning! Bad mod_weight value "{mod_wt_in}" '
                                f'in Modifier "{mod}". Ignoring...'
                            )
                            print(msg)
            # cap weight at weight_ceiling and weight_floor
            if 'weight_ceiling' in base_item.keys():
                weight_ceiling = base_item['weight_ceiling']
            else:
                weight_ceiling = None
            for mod in mod_combo:
                if 'weight_ceiling' in mod.keys():
                    weight_ceiling = mod['weight_ceiling']
            if 'weight_floor' in base_item.keys():
                weight_floor = base_item['weight_floor']
            else:
                weight_floor = None
            if weight_ceiling is not None and weight > weight_ceiling:
                weight = weight_ceiling
            if weight_floor is not None and weight < weight_floor:
                weight = weight_floor
            for mod in mod_combo:
                if 'weight_floor' in mod.keys():
                    weight_floor = mod['weight_floor']
            # drop the decimal if it's supposed to be a whole number
            if 'weight_whole_num' in base_item.keys():
                weight_whole_num = base_item['weight_whole_num']
            else:
                weight_whole_num = False
            for mod in mod_combo:
                if 'weight_whole_num' in mod.keys():
                    weight_whole_num = mod['weight_whole_num']
            if weight is not None and weight_whole_num:
                weight = int(weight)
            # item type, subtype, is it locked (default yes),
            # is it identified (default no)
            if 'type' in base_item.keys():
                item_type = base_item['type']
            else:
                item_type = None
            if 'subtype' in base_item.keys():
                subtype = base_item['subtype']
            else:
                subtype = None
            if 'locked' in base_item.keys():
                locked = base_item['locked']
            else:
                locked = 1
            if 'identified' in base_item.keys():
                identified = base_item['identified']
            else:
                identified = 1
            # create the item as an FGItem and add it to our list of items
            all_items.append(FGItem(0, name, desc, nonid_name, nonid_desc,
                             cost_str, weight, item_type, subtype,
                             identified, locked))

    return all_items


def parse_string(string: str, base: dict, mods: list) -> str:
    # split a token string apart and substitute in words and phrases
    tokens = string.split('|')
    output_raw = ''
    for token in tokens:
        if token in base.keys():
            output_raw = output_raw + base[token]
        elif '#' in token:
            mod_type, key = token.split('#')
            for mod in mods:
                if mod['type'] == mod_type and key in mod.keys():
                    output_raw = output_raw + mod[key]
        else:
            output_raw = output_raw + token
    # strip extra whitespace
    output_fewer_spaces = ' '.join(output_raw.split())
    # strip leading and trailing commas and spaces
    output_strip_comma = output_fewer_spaces.strip(', ')
    # strip orphaned commas and periods
    output_clean_commas = output_strip_comma.replace(', ,', ',')
    output_cleaned = output_clean_commas.replace('. .', '.')
    return output_cleaned


def xml_prettify(xml_root: ET.ElementTree) -> str:
    # the ElementTree library doesn't use whitespace
    # so we run it through minidom to make it human readable
    string = ET.tostring(xml_root)
    parsed = minidom.parseString(string)
    return parsed.toprettyxml()


if __name__ == "__main__":
    # build our command line and parse any arguments we get
    help_desc = (
        'Generate a Fantasy Grounds Module filled with procedurally-generated '
        'items based on a JSON File input which defines the items to be '
        'generated. Note that this process is not random - it will generate '
        'every possible item.'
    )
    parser = argparse.ArgumentParser(description=help_desc)
    parser.add_argument('--input', default='item_defs.json',
                        help='''JSON file of definitions for the items.
                                 Default: ./item_defs.json''')
    parser.add_argument('--output', default='itemdb',
                        help='''Name of the directory to output the XML files to.
                                 Default: ./itemdb/''')
    parser.add_argument('--id', default=1,
                        help='''Item ID number to start with. Default: 1''')
    args = parser.parse_args()
    infile = args.input
    outfile = args.output
    id_num = int(args.id)
    # check to make sure our output argument isn't an existing file
    if os.path.isfile(outfile):
        msg = (
            f'Error! Output argument "{outfile}" is an existing file, '
            'not a directory!'
        )
        print(msg)
        sys.exit()
    print(f'Generating items based on {infile} and outputting to {outfile}...')
    # read in the module definitions file
    defs = read_definitions(infile)
    # generate the definition.xml file
    mod_defs = parse_mod_def(defs['module'])
    mod_def_root = generate_mod_def(mod_defs)
    mod_def_out = xml_prettify(mod_def_root)
    # generate the items
    items = generate_items(defs['items'])
    print(f'Generated {len(items)} items!')
    # set up our db.xml root
    db_root = ET.Element('root', {'version': mod_defs['version'],
                                  'release': mod_defs['release']})
    # set up our item element and tree
    item_element = ET.Element('item')
    db_root.append(item_element)
    # add all our items, and give them unique IDs
    for item in items:
        item.ident = id_num
        item_element.append(item.gen_xml())
        id_num = id_num + 1
    # prettify our database XML tree
    db_xml_out = xml_prettify(db_root)
    # create a directory for our module if it does not exist
    try:
        os.makedirs(outfile, exist_ok=True)
    except Exception as e:
        msg = (
            f'Error! Could not create directory {outfile}! {e}'
        )
        print(msg)
    # write our definition.xml module definitions to a file
    out_db = outfile + '/definition.xml'
    with open(out_db, 'w') as outfh:
        outfh.write(mod_def_out)
    # write our db.xml database tree to a file
    out_db = outfile + '/db.xml'
    with open(out_db, 'w') as outfh:
        outfh.write(db_xml_out)
    print(f'Module XML files written to {outfile}. Done!')
