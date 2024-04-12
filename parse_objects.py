import argparse
# Just for type hints
import collections.abc
import json
import xml.etree.ElementTree as xmlet

STRING_Z_CODE = 'Z6'
TYPED_LIST_Z_CODE = 'Z881'
ENGLISH_Z_CODE = 'Z1002'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('pages_file', help='The name of the XML file to read the objects from. Called "pages-meta-current.xml" in the database dumps.')
	parser.add_argument('output_file', help='The name of the JSON file to write the modified objects to (as a JSON object). The file will be created if it does not exist, but any directories must already exist.')
	parser.add_argument('-l', '--language', default=ENGLISH_Z_CODE, help='The Z code of the language to select labels, descriptions, and aliases for. Defaults to English.')
	args = parser.parse_args()

	doc_root = xmlet.parse(args.pages_file).getroot()
	objects: dict[str, dict] = {}
	for page in doc_root.findall('page'):
		title = page.find('title').text
		text = page.find('revision').find('text').text
		obj_in = json.loads(text)
		obj_out = {}
		try:
			# The value of a String is the string itself, rather than a dict like other objects
			obj_value = obj_in['Z2K2']
			if isinstance(obj_value, dict):
				obj_out['type'] = obj_value['Z1K1']
			elif isinstance(obj_value, str):
				obj_out['type'] = STRING_Z_CODE
			elif isinstance(obj_value, list):
				obj_out['type'] = TYPED_LIST_Z_CODE
			obj_out['label']: str | None = search_multilingual_text(obj_in['Z2K3'], args.language)
			obj_out['aliases']: list[str] | None = search_multilingual_stringset(obj_in['Z2K4'], args.language)
			obj_out['description']: str | None = search_multilingual_text(obj_in['Z2K5'], args.language)
			obj_out['value'] = obj_in['Z2K2']
			objects[obj_in['Z2K1']['Z6K1']] = obj_out
		except KeyError:
			pass

	with open(args.output_file, 'w', encoding='utf-8') as out_file:
		json.dump(objects, out_file, ensure_ascii=False, indent='\t')

def load(objects_file: str) -> dict[str, dict]:
	with open(objects_file, encoding='utf-8') as in_file:
		return json.load(in_file)

def skip_first(able: collections.abc.Iterable) -> collections.abc.Iterator:
	'''
	Many lists in the JSON structure contain dicts except for their first element, which is a str indicating the type which each of the dicts describes.
	Rather than slicing such a list (expensive), create an iter and advance it past the first element.
	'''
	ator = iter(able)
	next(ator)
	return ator

def search_multilingual_text(texts: dict, language_code: str) -> str | None:
	'''
	A multilingual text (Z12) is a list of monolingual texts (Z11).
	Return the monolingual text for the target language code.
	'''

	try:
		return next(te['Z11K2'] for te in skip_first(texts['Z12K1']) if te['Z11K1'] == language_code)
	except StopIteration:
		return None

def search_multilingual_stringset(stringsets: dict, language_code: str) -> list[str] | None:
	'''
	A multilingual stringset (Z32) is a list of monolingual stringsets (Z31).
	Return the monolingual stringset for the target language.
	'''

	try:
		return next(ss['Z31K2'][1:] for ss in skip_first(stringsets['Z32K1']) if ss['Z31K1'] == language_code)
	except StopIteration:
		return None

if __name__ == '__main__':
	main()
