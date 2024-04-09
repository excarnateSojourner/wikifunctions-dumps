import argparse
import collections
import json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('input_path')
	parser.add_argument('output_path_prefix')
	args = parser.parse_args()

	with open(args.input_path, encoding='utf-8') as in_file:
		objects = json.load(in_file)

	lackers = collections.defaultdict(list)
	for id_, obj in objects.items():
		if not obj['label']:
			lackers[obj['value']['Z1K1']].append(id_)

	for type_, ids in lackers.items():
		with open(f'{args.output_path_prefix}{type_}.wiki', 'w', encoding='utf-8') as out_file:
			for id_ in ids:
				print(f'* [[{id_}]]', file=out_file)

if __name__ == '__main__':
	main()
