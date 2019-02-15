from xml.dom import minidom
from xml.dom.minidom import Element, Document


def get_element_text(elem: Element) -> str:
    return " ".join(t.nodeValue for t in elem.childNodes if t.nodeType == t.TEXT_NODE)


def get_child_text(elem: Element, nodeName: str) -> str:
    children = elem.getElementsByTagName(nodeName)
    if len(children) > 0:
        return get_element_text(children[0])
    return None


def elements_dictionary(elem: Element) -> dict:
    ret = {}
    for node in elem.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            n = node.nodeName
            if n in ret:
                ret[n] += 1
            else:
                ret[n] = 0

    for k, v in ret.items():
        if v > 1:
            ret[k] = []
        else:
            ret[k] = None

    return ret


def get_dictionary_from_children(elem: Element):

    ret = elements_dictionary(elem)

    for node in elem.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            n = node.nodeName
            if ret[n] is None:
                ret[n] = get_dictionary_from_children(node)
            elif isinstance(ret[n], list):
                ret[n].append(get_dictionary_from_children(node))
            else:
                ret[n] = get_dictionary_from_children(node)

    if len(ret) == 0:
        ret = get_element_text(elem)

    return ret


def parse_xml_string(xmlString: str) -> Document:
    return minidom.parseString(xmlString)

class DictToXML(object):

    def __init__(self, structure, list_mappings={}):
        self.doc = Document()

        if len(structure) == 1:
            rootName = str(list(structure.keys())[0])
            self.root = self.doc.createElement(rootName)

            self.list_mappings = list_mappings

            self.doc.appendChild(self.root)
            self.build(self.root, structure[rootName])

    def build(self, father, structure):
        if type(structure) == dict:
            for k in structure:
                tag = self.doc.createElement(k)
                father.appendChild(tag)
                self.build(tag, structure[k])
        elif type(structure) == list:
            tag_name = self.default_list_item_name

            if father.tagName in self.list_mappings:
                tag_name = self.list_mappings[father.tagName]

            for l in structure:
                tag = self.doc.createElement(tag_name)
                self.build(tag, l)
                father.appendChild(tag)
        else:
            data = str(structure)
            tag = self.doc.createTextNode(data)
            father.appendChild(tag)

    def display(self):
        print(self.doc.toprettyxml(indent="  "))

    def get_string(self):
        return self.doc.toprettyxml(indent="  ")


def dict_to_xml(data: dict) -> str:
    if not data:
        return ''

    def add_children(doc, parent, input_data):
        if isinstance(input_data, dict):
            for k, v in input_data.items():
                child = doc.createElement(k)
                parent.appendChild(child)
                add_children(doc, child, v)
        elif isinstance(input_data, (list, tuple)):
            for item in input_data:
                # child = doc.createElement(parent.tagName)
                # parent.appendChild(child)
                add_children(doc, parent, item)
        else:
            child = doc.createTextNode(str(input_data))
            parent.appendChild(child)

    document = Document()
    key = list(data.keys())[0]
    root = document.createElement(key)
    document.appendChild(root)
    add_children(document, root, data[key])
    return document.toxml(encoding='utf8')
