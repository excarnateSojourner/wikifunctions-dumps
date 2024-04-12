import argparse

import funcs_lacking_impls
import parse_objects

def main():
	parser = argparse.ArgumentParser(description='Generate a list of functions that have implementations but not test cases')
	parser.add_argument('objects_file', help='The name of the JSON file containing functions, implementations, and test cases, as produced by parse_objects.')
	parser.add_argument('output_file', help='The name of the MediaWiki markup file to write the relevant functions to.')
	parser.add_argument('-l', '--impl-lang', help='The programming language to look for implementations in. By default a function needs at least one implementation in any language to be output.')
	args = parser.parse_args()
	if args.impl_lang:
		args.impl_lang = args.impl_lang.casefold()

	objects = parse_objects.load(args.objects_file)

	with open(args.output_file, 'w', encoding='utf-8') as out_file:
		for func_code, func_obj in objects.items():
			if func_obj['type'] == 'Z8' and funcs_lacking_impls.func_has_impl(func_code, objects, args.impl_lang) and not func_has_test(func_code, objects):
				print(f'* [[{func_code}]]', file=out_file)

def func_has_test(func_code: str, objects: dict[str, dict]) -> bool:
	if len(objects[func_code]['value']['Z8K3']) > 1:
		return True
	else:
		for test_obj in objects.values():
			if test_obj['type'] == 'Z20' and test_obj['value']['Z20K1'] == func_code:
				return True
	return False

if __name__ == '__main__':
	main()
