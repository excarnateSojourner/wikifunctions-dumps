import argparse
import xml.etree.ElementTree as xmlet

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('input_path')
	parser.add_argument('namespaces', nargs='+', type=int, help='The index(es) of the namespace(s) to select.')
	parser.add_argument('-o', '--output-path-prefix', default='pages-')
	args = parser.parse_args()

	doc_root = xmlet.parse(args.input_path).getroot()
	ns_trees = {ns: xmlet.ElementTree(xmlet.Element('mediawiki')) for ns in args.namespaces}
	for page in doc_root.findall('page'):
		actual_ns = int(page.find('ns').text)
		try:
			ns_trees[actual_ns].getroot().append(page)
		except KeyError:
			pass

	for ns, tree in ns_trees.items():
		tree.write(f'{args.output_path_prefix}{ns}.xml', encoding='utf-8')

if __name__ == '__main__':
	main()
