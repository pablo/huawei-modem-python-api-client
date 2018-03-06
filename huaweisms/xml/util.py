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
            #if
            if ret[n] == None:
                ret[n] = get_dictionary_from_children(node)
            else:
                ret[n].append(get_dictionary_from_children(node))

    if len(ret) == 0:
        ret = get_element_text(elem)

    return ret

def parse_xml_string(xmlString: str) -> Document:
    return minidom.parseString(xmlString)
