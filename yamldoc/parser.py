import yamldoc.entries
import pdb

def parse_yaml(file_path, char = "#'", debug = True):
    # YAML files have key value pairings seperated by 
    # newlines. The most straightforward kind of things to parse will be
    # keyvalue pairs preceeded by comments with the Doxygen marker #'

    current_entry = None
    meta = ""
    things = []
    base_entry_found = False

    with open(file_path) as yaml:
        for line in yaml.readlines():
            if debug: print(line.rstrip())
            
            # Either we haven't started yet
            # or we've just flushed the entry.
            if current_entry is None:
                # Find the number of leading spaces.
                # YAML only uses spaces.
                nspaces = len(line) - len(line.lstrip(' '))
                if debug: print("@\tFound " + str(nspaces) + " indent level.")
                        
                if nspaces == 0:
                    base_entry_found = True
                    if line.startswith(char):
                        meta = meta + line.lstrip(char).rstrip()
                    else:
                        key, value = line.rstrip().split(":")
                        current_entry = yamldoc.entries.Entry(key, value.lstrip(' '), meta.lstrip())
                        if debug: print("@\tFound an entry.")
                        meta = ""

                if nspaces > 0:
                    if base_entry_found:
                        pass
                    else:
                        raise SyntaxError("Indented block found out of place.")


            if current_entry is not None and line in ['\n', '\r\n']:
                things.append(current_entry)
                current_entry = None

        # Clean up at the end of the file
        # if possible.
        if current_entry is not None:
            things.append(current_entry)


    
    return things




            

