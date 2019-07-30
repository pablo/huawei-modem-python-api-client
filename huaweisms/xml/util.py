import six
from typing import Union
from xml.dom import minidom
from xml.dom.minidom import Element, Document


def get_element_text(elem):
    # type: (Element) -> str
    return " ".join(t.nodeValue for t in elem.childNodes if t.nodeType == t.TEXT_NODE)


def get_child_text(elem, node_name):
    # type: (Element, str) -> Union[str, None]
    children = elem.getElementsByTagName(node_name)
    if children:
        return get_element_text(children[0])
    return None


def elements_dictionary(elem):
    # type: (Element) -> dict
    ret = {}
    for node in elem.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            n = node.nodeName
            if n in ret:
                ret[n] += 1
            else:
                ret[n] = 0

    ret = {k: [] if v > 1 else None for k, v in ret.items()}
    return ret


def get_dictionary_from_children(elem):
    # type: (Element) -> ...

    ret = elements_dictionary(elem)

    for node in elem.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            n = node.nodeName
            if ret[n] is None:
                ret[n] = get_dictionary_from_children(node)
            elif isinstance(ret[n], list):
                ret[n].append(get_dictionary_from_children(node))
            elif isinstance(ret[n], dict):
                previous_val = ret[n]
                ret[n] = [previous_val, get_dictionary_from_children(node)]
            else:
                ret[n] = get_dictionary_from_children(node)

    if not ret:
        ret = get_element_text(elem)
    return ret


def parse_xml_string(xml_string):
    # type: (str) -> Document
    parseable_xml_string = six.ensure_str(xml_string)
    return minidom.parseString(parseable_xml_string)


def dict_to_xml(data):
    # type: (dict) -> str
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
