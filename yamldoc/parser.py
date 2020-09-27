import yamldoc.entries
import pdb

def parse_yaml(file_path, char, debug):
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
                        key, value = line.rstrip().split(":")
                        
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
                        key, value = line.lstrip().rstrip().split(":")
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
    try:
        key, value = line.rstrip().lstrip(' ').split(":")
    except ValueError: 
        values = line.rstrip().lstrip(' ').split(":")
        key = values[0]
        value = ''.join(values[1:])
    if not value: return (key)
    return (key, value.lstrip(" "))

def count_indent(line):
    return len(line) - len(line.lstrip(' '))

def schema_parser(path_to_file, debug = True):
    name = "base"

    indent = [0, 0]

    specials = {}
    current = {}

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

            # Deal with top level specials.
            if key == "$schema":
                assert value is not None
                specials["schema"] = value
            
            if key == "description":
                assert value is not None
                specials["description"] = value


            if indent[1] > indent[0]:
                if value is None:
                    if key == "properties":
                        current[name] = {} 
                        indents[name] = {} 
                        continue
                    else:
                        parent = name
                        name = key
                        continue

                if key == "type":
                    assert value is not None
                    current[parent][name] = value
                    indents[parent][name] = indent[1]
                    continue

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
                
        return current 



def main(path_to_file, char = "#'", debug = True, title = "Configuration Parameters Reference", description = "Any information about this page goes here."):
    print("# " + title + "\n\n" + description + "\n")

    values = parse_yaml(path_to_file, char, debug)
    # Build the table with top level values
    print("| Key | Value | Information |")
    print("| :-: | :-: | :-- |") 
    for value in values:
        if not value.isBase:
            print(value.to_markdown())

    print("\n\n")

    for value in values:
        if value.isBase:
            print(value.to_markdown())
