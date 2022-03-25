import yamldoc.entries
from datetime import date
import pdb


def parse_yaml(file_path, char = "#'", debug = False):
    '''
    Parse a YAML file and return a list of YAML classes. 

    Arguments:
        file_path: Path to the YAML file.
        char: A character string used to identify yamldoc blocks.
        debug: Print debug information

    Return:
        List of YAML blocks.
    '''
    # YAML files have key value pairings seperated by 
    # newlines. The most straightforward kind of things to parse will be
    # keyvalue pairs preceeded by comments with the Doxygen marker #'

    current_entry = None
    meta = ""
    things = []

    with open(file_path) as yaml:
        for line in [l for l in yaml.readlines() if l.rstrip()]:
            if debug: print(line.rstrip())
            
            # Either we haven't started yet
            # or we've just flushed the entry.
            if current_entry is None:
                # Find the number of leading spaces.
                # YAML only uses spaces.
                nspaces = len(line) - len(line.lstrip(' '))
                if debug: print("@\tFound " + str(nspaces) + " indent level.")
                        
                if nspaces == 0:
                    current_entry = None
                    if line.startswith(char):
                        meta = meta + line.lstrip(char).rstrip()
                    else:
                        key, value = line.rstrip().split(":", 1)
                        
                        # If there is no value, this is the beginning of a 
                        # base entry (i.e. there are subentries to follow)
                        if not value.lstrip():
                            current_entry = yamldoc.entries.MetaEntry(key, meta)
                            if debug: print("@\tFound a meta entry.")
                            continue

                        # Otherwise continue on.
                        else:
                            things.append(yamldoc.entries.Entry(key, value.lstrip(' '), meta.lstrip()))
                            if debug: print("@\tFound an entry.")
                            meta = ""

            if current_entry is not None:
                if current_entry.isBase:

                    # If we're back at 0 indentation, the
                    # block is done and we need to quit.
                    if len(line) - len(line.lstrip(' ')) == 0:
                        things.append(current_entry)
                        current_entry = None
                        continue

                    # If not, continue parsing the sub entries.
                    if line.lstrip(' ').startswith(char):
                        meta = meta + line.lstrip().lstrip(char).rstrip()
                    else:
                        key, value = line.lstrip().rstrip().split(":", 1)
                        current_entry.entries.append(yamldoc.entries.Entry(key, value.lstrip(' '), meta.lstrip()))
                        if debug: print("@\tFound an entry and deposited it in meta.")
                        meta = ""

        # The file might run out
        # before the final meta
        # entry is added.
        try:
            if current_entry.isBase:
                things.append(current_entry)
        except AttributeError:
            pass


    
    return things


def key_value(line):
    '''
    Extract a key value pair from a single YAML line.

    Arguments:
        line: A character string to be processed.

    Returns:
        Key value pairing; alternatively, if not value i present, just the key.
    '''
    try:
        key, value = line.rstrip().lstrip(' ').split(":", 1)
    except ValueError: 
        values = line.rstrip().lstrip(' ').split(":", 1)
        key = values[0]
        value = ''.join(values[1:])
    if not value: return (key)
    return (key, value.lstrip(" "))

def count_indent(line):
    '''
    Count indentation level.

    Arguments:
        line: A character string to be processed.
    '''
    return len(line) - len(line.lstrip(' '))

def parse_schema(path_to_file, debug = False):
    '''
    Parse a schema file to identify key value pairing of 
    values and their associated types.

    Arguments:
        path_to_file: Path to schema file.

    Returns: Tuple of (schema, specials) where specials are unique YAMLDOC strings for the title and description of the desired markdown. 
    '''
    name = "base"

    indent = [0, 0]

    specials = {}
    indents = {}
    current = {}

    extras = {}

    special_type_case = False

    with open(path_to_file) as schema:
        for line in [l for l in schema.readlines() if l.rstrip()]:
            if debug: print(line)
            indent = [indent[1], count_indent(line)]

            
            # The base level has to start with a special name
            # because it is not named in the schema.
            try:
                key, value = key_value(line)
            except ValueError:
                key = key_value(line)
                value = None

            # This is awkwardly placed but we have to deal
            # with a special case where lines 
            # start with a dash, and indicate that
            # variables have multiple types.
            # 
            # If this has been observed further inside the
            # loop, and the line does indeed start with a dash
            if special_type_case:
                # If the indent has decreased, then 
                # the list of types has finished.
                if indent[1] < indent[0]:
                    special_type_case = False
                    continue
                if line.lstrip(" ").startswith("-"):
                    value = line.lstrip(" ").lstrip("- ").rstrip()
                    current[parent][name].append(value)
                    continue
                else:
                    raise TypeError("You must specify a value for type.")

            # < Deal with top level specials.
            if key == "$schema":
                assert value is not None
                specials["schema"] = value

            if key == "_yamldoc_title": 
                assert value is not None
                specials[key] = value

            if key == "_yamldoc_description": 
                assert value is not None
                specials[key] = value

            
            if key == "description":
                assert value is not None
                specials["description"] = value
            # />

            # Top level properties option
            if value is None:
                if key == "properties":
                    current[name] = {} 
                    indents[name] = {}
                    extras[name] = {}
                    continue


            # Deal with increasing indent levels
            # The actual amount of indent is not
            # relevant (though it may be for 
            # parsing a valid YAML document.
            if indent[1] >= indent[0]:
                if value is None:
                    # If the key is properties
                    # then we are starting a new object
                    # definition.
                    if key == "properties":
                        current[name] = {} 
                        indents[name] = {} 
                        extras[name] = {}
                        continue
                    
                    # This is a special case where
                    # there can be multiple types
                    # given for a particular variable.
                    elif key == "type":
                        current[parent][name] = []
                        indents[parent][name] = []
                        special_type_case = True
                        continue
                        

                    # Otherwise, its the name of the
                    # actual object.
                    # Assign the key to be the "name"
                    # and relegate the previous name
                    # to the "parent".
                    else:
                        parent = name
                        name = key
                        continue
                
                # If it's giving the type of the object
                # then store that under the parent (meta)
                # object along with its indentation level. 
                if key == "type":
                    assert value is not None
                    if value != "object":
                        current[parent][name] = value
                        indents[parent][name] = indent[1]
                    continue
                elif key in ["plain_text", "enum"]:
                    assert value is not None
                    if name in extras[parent].keys():
                        extras[parent][name][key] = value
                        indents[parent][name] = indent[1]
                    else: 
                        extras[parent][name] = {key: value}
                        indents[parent][name] = indent[1]




                

            if indent[1] < indent[0]:
                # We're just adding another value 
                if indent[1] == indents[parent][name]:
                    if value is None:
                        name = key
                        continue
                elif indent[1] < indents[parent][name]:
                    if value is None:
                        name = key
                        continue
                
        return current, specials, extras

def add_type_metadata(schema, yaml, debug = False):
    '''
    Modified a list of yaml entries in place to add type information
    from a parsed schema.

    Arguments:
        schema: List of schema representations from parse_schema.
        yaml: List of yaml representations from parse_yaml.
        debug: Print debug information
    
    Returns: 
        Nothing.
    '''
    # Loop over each value of the schema 
    for name, variables in schema.items():
        # Find the corresponding entry in the YAML.
        
        # Special case: if the name is base in the schema
        # these are top level variables
        # which need to be dealt with seperately.
        if name == "base": 
            # Look for top level entries
            for var, var_type in variables.items(): 
                for value in yaml:
                    if not value.isBase:
                        if var == value.key:
                            value.type = var_type
        else:
            for value in yaml:
                if value.isBase:
                    if name == value.name:
                        for var, var_type in variables.items():
                            for entry in value.entries:
                                if var == entry.key:
                                    if debug: print(f"Setting type of {var}")
                                    entry.type = var_type
                                    # If we find at least one
                                    # then we can say that
                                    # there's a schema.
                                    value.has_schema = True
                                    entry.has_schema = True

            
def add_extra_metadata(extras, yaml, debug = False):
    '''
    Modified a list of yaml entries in place to add extra type information
    from a parsed schema.

    Arguments:
        schema: List of schema representations from parse_schema.
        yaml: List of yaml representations from parse_yaml.
        debug: Print debug information
    
    Returns: 
        Nothing.
    '''
    # Loop over each value of the schema 
    for name, variables in extras.items():
        # Find the corresponding entry in the YAML.
        
        # Special case: if the name is base in the schema
        # these are top level variables
        # which need to be dealt with seperately.
        if name == "base": 
            # Look for top level entries
            for var, meta in variables.items(): 
                for value in yaml:
                    if not value.isBase:
                        if var == value.key:
                            for key, v in meta.items(): 
                                value.key = value
        else:
            for value in yaml:
                if value.isBase:
                    if name == value.name:
                        for var, meta in variables.items():
                            for entry in value.entries:
                                if var == entry.key:
                                    if debug: print(f"Setting type of {var}")
                                    for key, v in meta.items(): 
                                        setattr(entry, key, v)



        

def main(yaml_path, char = "#'", debug = False, schema_path = None, title = "Configuration Parameters Reference", description = "Any information about this page goes here."):
    '''
    Takes a given YAML file and optionally an associated schema, parsing each for their key value pairings and reports the results as a markdown document.

    Arguments:
        yaml_path: Path to YAML file.
        schema_path: Path to schema file. 
        char: Special character to identify comments to be included in YAMLDOC documentation.
        debug: Print debug information
        title: Title of markdown generated.
        description: Description given below the title in markdown.

    Returns: 
        Nothing, prints to stdout.
    '''
    # If a schema has been specified, add the
    # type information to the rest of the 
    # variables.
    if schema_path is not None:
        schema, specials, extras = parse_schema(schema_path, debug)
        yaml = parse_yaml(yaml_path, char, debug)

        # Edit the yaml in place with type information.
        add_type_metadata(schema, yaml, debug)

        if "_yamldoc_title" in specials:
            title = specials["_yamldoc_title"]

        if "_yamldoc_description" in specials:
            description = specials["_yamldoc_description"]
            

        # And do the printing
        print("# " + title + "\n\n" + description + "\n")

        # Build the table with top level yaml
        print("| Key | Value | Type | Information |")
        print("| :-: | :-: | :-: | :-- |") 
        for value in yaml:
            if not value.isBase:
                print(value.to_markdown(schema = True))

        print("\n\n")

        for value in yaml:
            if value.isBase:
                print(value.to_markdown(schema = True))

        print(f"---\nGenerated by [yamldoc](https://github.com/chris1221/yaml.doc) v{yamldoc.__version__} on {date.today()}")

    else: 
        print("# " + title + "\n\n" + description + "\n")

        yaml = parse_yaml(yaml_path, char, debug)
        # Build the table with top level yaml
        print("| Key | Value | Information |")
        print("| :-: | :-: | :-- |") 
        for value in yaml:
            if not value.isBase:
                print(value.to_markdown())

        print("\n\n")

        for value in yaml:
            if value.isBase:
                print(value.to_markdown())

        print(f"---\nGenerated by [yamldoc](https://github.com/chris1221/yaml.doc) v{yamldoc.__version__} on {date.today()}")

