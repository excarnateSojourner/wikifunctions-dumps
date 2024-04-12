# Wikifunctions Dumps

*See also: [wiktionary-dumps](https://github.com/excarnateSojourner/wiktionary-dumps/tree/master)*

This is a collection of Python scripts I have written to parse [database dumps](https://dumps.wikimedia.org/) of [Wikifunctions](https://www.wikifunctions.org/wiki/Wikifunctions:Main_Page), a free library of computer functions that nearly anyone can edit.

## `ns`
If you want to do anything with Wikifunction objects you'll want to start here. This script takes the raw XML from the database dump and selects only pages in the specified MediaWiki namespace(s).

This script reads all of the XML into memory to process it. For a version of this script that goes page by page, allowing it to work with XML files that are gigabytes in size, see [wiktionary-dumps/ns.py](https://github.com/excarnateSojourner/wiktionary-dumps/blob/master/ns.py).

### Inputs
#### Required
1. `pages_file`: The name of the XML file containing MediaWiki pages to filter. It's called `pages-meta-current.xml` in the database dumps.
1. `namespaces`: The index(es) of the namespace(s) to filter out. The main namespace has index 0.
1. `--output-path-prefix`: This string is prepended to the index of each namespace (with ".xml" appended) to create the name of the file to write the pages in that namespace to.

#### Output
Unless they already exist this script will create a new file for every namespace specified.

## `parse_objects`
This script extracts and modifies JSON from the raw database data. This JSON is then used by the other scripts. This script only keeps labels, descriptions, and aliases for one language.

### Inputs
#### Required
1. `pages_file`: The name of the XML file containing all MediaWiki pages in the main namepspace. This is produced by running [`ns`](#ns) and selecting namespace 0.
1. `output_file`: The name of the JSON file to write the parsed objects (as a JSON object) to.

#### Optional
1. `--language`: The Z code for the language to select labels, descriptions, and aliases for. Defaults to English.

### Output
A JSON object in which each key is an object's Z code and the corresponding value is a JSON object with the following keys:
* `type` (the value being the object's type's Z code, not any of its labels)
* `label`
* `description`
* `aliases`
* `value` (the structure of the value depends on the type)

Objects are skipped if they do not match the general form of functions, implementations, and test cases. More precisely, they are skipped if any of the following keys do not exist in `obj`, the original JSON object:
* `obj['Z2K2']`
* `obj['Z2K3']`
	* `obj['Z2K3']['Z12K1']`
* `obj['Z2K4']`
	* `obj['Z2K4']['Z32K1']`
* `obj['Z2K5']`
	* `obj['Z2K5']['Z12K1']`

## `parse_types`
This script generates a list of all the types (defined as objects of type `Z4`) defined on Wikifunctions. (As of 2024-04-10 there are 34 of them.) It allows other scripts to easily convert from the Z codes of types to their names (which this script [casefolds](https://docs.python.org/3/library/stdtypes.html#str.casefold)) and vice-versa.

### Inputs
#### Required
1. `objects_file`: The name of the JSON file containing the objects, as produced by [`parse_objects`](#parse_objects). The language which was specified when running `parse_objects` will determine the language in which the type labels are saved.
1. `output_file`: The name of the JSON file to write the types to (as a JSON object).

### Output
A JSON object containing two sub-objects:
* `codes to names`: Maps types' Z codes to their labels.
* `names to codes`: Maps types' labels to their Z codes.

## `lacking_lang`
This script generates lists of objects that lack labels, descriptions, or aliases in a given language.

This script can run stand-alone or be used from another script.

### Inputs
#### Required
1. `objects_file`: The name of the JSON file containing the objects to check, as produced by [`parse_objects`](#parse_objects). The language that was selected when running `parse_objects` will be the the language for which the chosen field will be checked.
1. `types_file`: The name of the JSON file describing types, as produced by [`parse_types`](#parse_types).
1. `output`: If `--type` is given, this is the MediaWiki markup file to write the list of object Z codes to. Otherwise this is prepended to the object types to generate the names of the MediaWiki markup files which the lists of object Z codes will be written to.

#### Optional
1. `--field`: The name of the field that may be missing. Must be `label`, `description`, or `aliases`. Defaults to `label`.
1. `--type`: If given only fields of objects of the specified type will be checked. Given as the name of the type, not the Z code.

## `search`
I have found MediaWiki's search engine to not work well on Wikifunctions, so I've implemented a very simple one here. Queries are case **in**sensitive. The script checks if the query is a substring of an object's label or aliases, so the order of the words in a query matters.

This script is **in**efficient, so it will probably be prohibitively slow if you try to use it to search through database dumps of much larger wikis.

### Inputs
#### Required
1. `objects_file`: The name of the file containing objects to search through, as produced by [`parse_objects`](#parse_objects).
1. `query`: The text to search for.

#### Optional
1. `--max-results`: The maximum number of results to show. Defaults to 10.

#### Output
Results are shown with their Z codes, labels, aliases, and descriptions (where these exist). The results with the sortest labels will be shown first.

## `unimpled_funcs`
This script generates a list of functions that have no implementations, or that have no implementations in a given language. It excludes functions which have relevant disconnected implementations.

### Inputs
#### Required
1. `objects_file`: The name of the JSON file containing functions and implementations to search through, as produced by [`parse_objects`](#parse_objects). If `--impl-lang` is given then this file must also contain programming languages.
1. `output_file`: The name of the MediaWiki markup file to write the list of relevant function Z codes to.

#### Optional
1. `--impl-lang`: The name of a programming language. If given, output functions that do not have an implementation in this language, even if they do have implementations in other languages.

## `impled_untested_funcs`
This script generates a list of functions that have one or more implementations, or that are implemented in a given language, but do not yet have any test cases. Disconnected implementations and test cases are treated as valid (just the same as connected ones).

### Inputs
#### Required
1. `objects_file`: The name of the JSON file containing functions, implementations, and test cases to search through, as produced by [`parse_objects`](#parse_objects). If `--impl-lang` is given then this file must also contain programming languages.
1. `output_file`: The name of the MediaWiki markup file to write the list of relevant function Z codes to.

#### Optional
1. `--impl-lang`: The name of a programming language. If given, output is restricted to functions that have an implementation in this language, regardless of implementations in other languages.
