import argparse
import xml.etree.ElementTree as xmlet

def main():
	parser = argparse.ArgumentParser(description='Filter MediaWiki pages by namespace')
	parser.add_argument('pages_file', help='The name of the XML file containing pages to filter. This is called "pages-meta-current.xml" in the database dumps.')
	parser.add_argument('namespaces', nargs='+', type=int, help='The index(es) of the namespace(s) to select.')
	parser.add_argument('-o', '--output-path-prefix', default='pages-', help='This string is prepended to the index of each namespace (with ".xml" appended) to create the name of the file to write pages in that namespace to. If a file does not exist it will be created, but any directories must already exist.')
	args = parser.parse_args()

	doc_root = xmlet.parse(args.pages_file).getroot()
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
