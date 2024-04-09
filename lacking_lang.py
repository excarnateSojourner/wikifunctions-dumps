import argparse
import collections
import json

TYPE_STRING = 'Z6'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('input_path')
	parser.add_argument('output_path_prefix')
	parser.add_argument('-p', '--property', default='label')
	args = parser.parse_args()

	with open(args.input_path, encoding='utf-8') as in_file:
		objects = json.load(in_file)

	lackers = collections.defaultdict(list)
	for id_, obj in objects.items():
		if not obj[args.property]:
			try:
				lackers[obj['value']['Z1K1']].append(id_)
			# The value of a String is just the string itself (not a dict)
			except TypeError:
				lackers[TYPE_STRING].append(id_)

	for type_, ids in lackers.items():
		with open(f'{args.output_path_prefix}{type_}.wiki', 'w', encoding='utf-8') as out_file:
			for id_ in ids:
				print(f'* [[{id_}]]', file=out_file)

if __name__ == '__main__':
	main()
