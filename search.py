import argparse
import json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('objects_file', help='The name of the JSON file containing the objects to search through, as produced by parse_objects.')
	parser.add_argument('query', help='The text to search for.')
	parser.add_argument('-m', '--max-results', default=10, type=int, help='The maximum number of results to display. Defaults to %(default)s.')
	args = parser.parse_args()

	with open(args.objects_file, encoding='utf-8') as in_file:
		objects = json.load(in_file)

	query = args.query.casefold()
	results = []
	for z_code, obj in objects.items():
		if (obj['label'] and query in obj['label'].casefold()) or (obj['aliases'] and any(query in alias.casefold() for alias in obj['aliases'])):
			results.append({'code': z_code, 'label': obj['label'], 'aliases': obj['aliases'], 'description': obj['description']})

	# I tend to search for fundamental objects more than specific implemenations or test cases, so as a heuristic show shortest results first
	results.sort(key=lambda res: len(res['label']))

	if len(results) > args.max_results:
		print(f'Showing {args.max_results} of {len(results)} results.')
	else:
		print('Showing all results.')
	print()
	for res in results[:args.max_results]:
		print(f'{res["code"]}: {res.get("label", "Untitled")}')
		if res['aliases']:
			print(', '.join(res['aliases']))
		if res['description']:
			print(res['description'])
		print(f'https://www.wikifunctions.org/view/en/{res["code"]}')
		print()

if __name__ == '__main__':
	main()
