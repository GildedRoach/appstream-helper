from pathlib import Path
import xml.etree.ElementTree as ET
from copy import deepcopy
from typing import Tuple


def merge_xml(base_xml: ET.Element, additional_xml: ET.Element) -> ET.Element:
    """
    Merge two XML trees while keeping existing values from ``base_xml`` intact.

    - Elements that are missing in ``base_xml`` are appended.
    - Matching elements are merged recursively.
    - Attributes and text values already present in ``base_xml`` are not overwritten.
    """

    def element_signature(elem: ET.Element) -> Tuple[str, Tuple[Tuple[str, str], ...]]:
        """Return a signature comprising the element tag and sorted attribute pairs."""
        return elem.tag, tuple(sorted(elem.attrib.items()))

    def copy_text(target: ET.Element, source: ET.Element, attr_name: str) -> None:
        """Copy text/tail when the target currently has no value."""
        current = getattr(target, attr_name)
        if current is not None and current != "":
            return
        value = getattr(source, attr_name)
        if value is not None:
            setattr(target, attr_name, value)

    for key, value in additional_xml.attrib.items():
        base_xml.attrib.setdefault(key, value)

    copy_text(base_xml, additional_xml, "text")
    copy_text(base_xml, additional_xml, "tail")

    existing_children = list(base_xml)
    used_indexes = set()

    for additional_child in additional_xml:
        signature = element_signature(additional_child)
        match_index = None

        for idx, base_child in enumerate(existing_children):
            if idx in used_indexes:
                continue
            if element_signature(base_child) == signature:
                match_index = idx
                break

        if match_index is None:
            base_xml.append(deepcopy(additional_child))
        else:
            used_indexes.add(match_index)
            merge_xml(existing_children[match_index], additional_child)

    return base_xml



def load_xml_document(path: Path) -> ET.Element:
    """Load an XML document from disk and return the root element."""
    tree = ET.parse(path)
    return tree.getroot()
