`yamldoc` now supports arbitrary levels of nesting for hierarchical representations of `data`. For examples, see `test/yaml/two_level.yaml` and `test/schema/two_level.schema`. The program is run the same way.

### Example of Deeper Nesting

Here is an example of a YAML file with deeper nesting:

```yaml
#' This is a flat entry.
flat: "yes"

#' But this is a two level thing.
two:
        #' These can have documentation too.
        entry: "hi"

#' This is a three level thing.
three:
        #' This is the second level.
        level_two:
                #' This is the third level.
                level_three: "hello"
```

The corresponding schema file:

```yaml
$schema: "http://json-schema.org/draft-04/schema#"

type: object

properties:
        flat:
                type: string
        two:
                type: object
                properties:
                        entry:
                                type: 
                                        - string
                                        - number
        three:
                type: object
                properties:
                        level_two:
                                type: object
                                properties:
                                        level_three:
                                                type: string
```

The output will include all levels of nesting.
