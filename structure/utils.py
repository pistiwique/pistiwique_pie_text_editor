'''
Copyright (C) 2017 Legigan Jeremy AKA Pistiwique

Created by Legigan Jeremy AKA Pistiwique

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re


EXCEPTIONS = ['bl_description', 'bl_idname', 'bl_label', 'bl_options',
             'bl_translation_context', 'bl_undo_group', 'bl_space_type',
             'bl_category', 'bl_context', 'bl_region_type'
             ]


def get_main_structure(current_text):
    """ Returns a dictionary containing the different classes, functions and variables.
        Each class, function or variable is declared by its name and take
        as value an identifier (C, F or V) and his line index statement.
        The "ORDER" key takes as a value the list of structures in the
        order in which they are declared.
        """

    structure = {'ORDER': []}

    for idx, line in enumerate(current_text.lines):
        if line.body.startswith("class "):
            name = line.body[6:-1]
            structure[name] = ["C", idx]
            structure['ORDER'].append(name)

        elif line.body.startswith("def "):
            name = line.body[4:-1]
            structure[name] = ["F", idx]
            structure['ORDER'].append(name)

        elif re.search('^\w(.)*=', line.body):
            name = line.body.split("=")[0].rstrip()
            structure[name] = ["V", idx]
            structure['ORDER'].append(name)

    return structure

def get_end_structure_line_index(current_text, start_index):
    """ Returns the index of the last line of the structure """

    start = start_index + 1 # to avoid starting on the statement line of
                            # the class or function

    for i, line in enumerate(current_text.lines[start:]):
        end = start + i
        text = line.body
        if re.search("^[\w]", text):
            break

    return end


def get_structure_methods(current_text, start_index, end_index):
    """ Return a dictionary containing the methods.
        Each methods is declared by its name and take as value his line
        index.
        The "ORDER" key takes as a value the list of methods in the order in
        which they are declared.
        """

    methods = {'ORDER': []}
    start = start_index + 1

    for idx, l in enumerate(current_text.lines[start:end_index]):
        if re.search("def (.)*:", l.body):
            start_def = re.search("def ", l.body).start()
            if start_def == l.body[:start_def].count(" "):
                name = l.body.split("def ")[-1][:-1]
                methods[name] = start + idx
                methods['ORDER'].append(name)

    return methods


def get_properties(current_text, start_index, end_index):
    """ Return a dictionary containing the properties.
        Each property is declared by its name and take as value his line
        index
        """

    properties = {}

    # loops on the different methods to extract the properties
    for idx, l in enumerate(current_text.lines[start_index:end_index]):
        if re.search("\s*self\.\w*(=|\s*=)", l.body):
            selecion = re.search("self\.\w*", l.body).span()
            prop_name = l.body[selecion[0]+5:selecion[1]]
            if not prop_name in properties:
                properties[prop_name] = start_index + idx

    is_docstring = False
    is_arguments = False
    # loop between the structure statement and the first method to extract
    # the properties
    for idx, l in enumerate(current_text.lines[start_index:end_index]):
        # stop the loop when we find the first method
        if "def " in l.body:
            break

        # don't take docstring into account
        if l.body.count('"""') == 2 or l.body.count("'''") == 2:
            pass
        if l.body.count('"""') == 1 or l.body.count("'''") == 1:
            is_docstring = not is_docstring

        if re.search("\s\w*(=|\s=)", l.body) and not is_docstring and not\
                is_arguments:
            prop_name = l.body.strip().split("=")[0].rstrip()
            if prop_name not in EXCEPTIONS and prop_name not in properties:
                properties[prop_name] = start_index + idx

            # don't take argument's properties into account
            if "(" and ")" in l.body:
                continue
            elif "(" in l.body:
                is_arguments = True

        if ")" in l.body:
            is_arguments = False

    return properties