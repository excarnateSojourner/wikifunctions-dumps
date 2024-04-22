import argparse
import collections.abc
import re
import xml.etree.ElementTree as xmlet

def main():
	parser = argparse.ArgumentParser(description='Filter MediaWiki pages by MediaWiki namespace')
	parser.add_argument('pages_file', help='The name of the XML file containing pages to filter. This is called "pages-meta-current.xml" in the database dumps.')
	parser.add_argument('mw_namespaces', nargs='+', type=int, help='The index(es) of the MediaWiki namespace(s) to select.', metavar='namespaces')
	parser.add_argument('-o', '--output-path-prefix', default='pages-', help='This string is prepended to the index of each MediaWiki namespace (with ".xml" appended) to create the name of the file to write pages in that namespace to. If a file does not exist it will be created, but any directories must already exist.')
	args = parser.parse_args()

	doc = xmlet.parse(args.pages_file, parser=xmlet.XMLParser(encoding='utf-8'))
	# XML namespaces get in the way when trying to find elements by tag name, so remove them all
	rm_xml_nses(doc.getroot())
	ns_trees = {ns: xmlet.ElementTree(xmlet.Element('mediawiki')) for ns in args.mw_namespaces}
	for page in doc.findall('page'):
		actual_mw_ns = int(page.find('ns').text)
		try:
			ns_trees[actual_mw_ns].getroot().append(page)
		except KeyError:
			# Namespace was not among those selected
			pass

	for ns, tree in ns_trees.items():
		tree.write(f'{args.output_path_prefix}{ns}.xml', encoding='utf-8')

def rm_xml_nses(elem: xmlet.Element) -> xmlet.Element:
	'''Recursively remove all XML namespaces from the tag of this element and its children's tags.'''
	elem.tag = re.sub(r'^\{.+?\}', '', elem.tag)
	for child in elem:
		rm_xml_nses(child)
	return elem

if __name__ == '__main__':
	main()
