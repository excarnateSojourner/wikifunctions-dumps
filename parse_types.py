import argparse
import json

TYPE_TYPE = 'Z4'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('objects_file', help='The name of the JSON file containing objects (as produced by parse_objects) to parse.')
	parser.add_argument('output_file', help='The name of the JSON file to write the types to (as a JSON object). The file will be created if it does not exist, but any directories must already exist.')
	args = parser.parse_args()

	with open(args.objects_file, encoding='utf-8') as in_file:
		objects = json.load(in_file)

	ids_to_names = {}
	for id_, obj in objects.items():
		try:
			if obj['value']['Z1K1'] == TYPE_TYPE:
				ids_to_names[id_] = obj['label']
		# Pesky Strings
		except TypeError:
			pass

	names_to_ids = {v: k for k, v in ids_to_names.items()}
	types = {'ids to names': ids_to_names, 'names to ids': names_to_ids}

	with open(args.output_file, 'w', encoding='utf-8') as out_file:
		json.dump(types, out_file, indent='\t')

if __name__ == '__main__':
	main()
