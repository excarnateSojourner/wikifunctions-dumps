import argparse
import json

import parse_objects

def main():
	parser = argparse.ArgumentParser(description='Generate a list of funtions that lack implementations')
	parser.add_argument('objects_file', help='The JSON file to read the functions and implementations from, as produced by parse_objects.')
	parser.add_argument('output_file', help='The MediaWiki markup file to write the Z codes of functions missing implementations to.')
	parser.add_argument('-l', '--impl-lang', help='The programming language to look for implementations in. By default only functions which do not have any implementations in any language will be output.')
	args = parser.parse_args()
	if args.impl_lang:
		args.impl_lang = args.impl_lang.casefold()

	objects = parse_objects.load(args.objects_file)

	with open(args.output_file, 'w', encoding='utf-8') as out_file:
		for func_code, func_obj in objects.items():
			if func_obj['type'] == 'Z8':
				if not func_has_imp(func_code, func_obj, objects, impl_lang):
					print(f'* [[{func_code}]]', file=out_file)

def func_has_impl(func_code: str, func_obj: dict, objects: str, impl_lang: str | None = None):
	# See if the function knows it has implementations
	for impl_code in parse_objects.skip_first(func_obj['value']['Z8K4']):
		try:
			if impl_is_relevant_lang(objects[impl_code], args.impl_lang, objects):
				return True
		# Built-in or otherwise fundamental implementations may not have all keys.
		# See for example Z201.
		except KeyError:
			pass

	# Check for disconnected implementations
	for impl_obj in objects.values():
		if impl_obj['type'] == 'Z14' and impl_obj['value']['Z14K1'] == func_code and impl_is_relevant_lang(impl_obj, args.impl_lang, objects):
			return True

	return False

def impl_is_relevant_lang(impl_obj: dict, impl_lang: str, objects: dict[str, dict]) -> bool:
	try:
		lang: dict | str = impl_obj['value']['Z14K3']['Z16K1']
		# If lang is a Z code
		if isinstance(lang, str):
			lang: dict = objects[lang]['value']
		return not impl_lang or lang['Z61K1'].casefold() == impl_lang
	# Built-in or otherwise fundamental implementations may not have all keys
	# See for example Z201
	except KeyError:
		return not impl_lang

if __name__ == '__main__':
	main()
