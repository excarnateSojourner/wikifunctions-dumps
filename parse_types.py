import argparse
import json

TYPE_Z_CODE = 'Z4'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('objects_file', help='The name of the JSON file containing objects (as produced by parse_objects) to parse.')
	parser.add_argument('output_file', help='The name of the JSON file to write the types to (as a JSON object). The file will be created if it does not exist, but any directories must already exist.')
	args = parser.parse_args()

	with open(args.objects_file, encoding='utf-8') as in_file:
		objects = json.load(in_file)

	codes_to_names = {}
	for z_code, obj in objects.items():
		if obj['type'] == TYPE_Z_CODE:
			codes_to_names[z_code] = obj['label'].casefold()

	names_to_codes = {v: k for k, v in codes_to_names.items()}
	types = {'codes to names': codes_to_names, 'names to codes': names_to_codes}

	with open(args.output_file, 'w', encoding='utf-8') as out_file:
		json.dump(types, out_file, indent='\t')

if __name__ == '__main__':
	main()
