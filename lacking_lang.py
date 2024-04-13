import argparse
import collections
import json

import parse_objects

IMPLEMENTATION_Z_CODE = 'Z14'
TEST_CASE_Z_CODE = 'Z20'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('objects_file', help='The name of the JSON file containing the objects to check (produced by parse_objects).')
	parser.add_argument('types_file', help='The name of the JSON file describing types, as produced by parse_types.')
	parser.add_argument('output', help='If --type is given, this is the file to write the list of objects to. Otherwise this is prepended to the object types to generate the names of the files which the lists of objects will be written to. The output file(s) will be created if they do not exist, but any directories must already exist.')
	parser.add_argument('-f', '--field', default='label', choices=['label', 'description', 'aliases'], help='The name of the field to check. Defaults to "%(default)s".')
	parser.add_argument('-t', '--type', help='If given only fields of objects of the specified type will be checked. Given as the name of the type, not the Z code. Requires --types-file.')
	args = parser.parse_args()

	lackers = objects_lacking_lang(args.objects_file, args.types_file, args.field)

	if args.type:
		with open(args.output, 'w', encoding='utf-8') as out_file:
			for lacker_code in lackers[args.type.casefold()]:
				print(f'* [[{lacker_code}]]', file=out_file)

	# no type specified
	else:
		for type_name, lacker_codes in lackers.items():
			with open(f'{args.output}{type_name.replace(" ", "_")}.wiki', 'w', encoding='utf-8') as out_file:
				for lacker_code in lacker_codes:
					print(f'* [[{lacker_code}]]', file=out_file)

def objects_lacking_lang(objects_file: str, types_file: str, field: str = 'label') -> dict[str, list[str]]:
	objects = parse_objects.load(objects_file)

	with open(types_file, encoding='utf-8') as in_file:
		type_codes_to_names: dict[str, str] = json.load(in_file)['codes to names']

	lackers = collections.defaultdict(list)
	for z_code, obj in objects.items():
		if not obj[field]:
			# If implementation or test case and associated function does not have a label, skip
			try:
				if (obj['type'] == IMPLEMENTATION_Z_CODE and not objects[obj['value']['Z14K1']]['label']) or (obj['type'] == TEST_CASE_Z_CODE and not objects[obj['value']['Z20K1']]['label']):
					continue
			# Some built-in functions do not have the usual fields, meaning they do not appear in parsed objects and their implementations and test cases won't be able to look them up here.
			# We assume these functions are labelled.
			except KeyError:
				pass
			lackers[type_codes_to_names[obj['type']]].append(z_code)
	return lackers

if __name__ == '__main__':
	main()
