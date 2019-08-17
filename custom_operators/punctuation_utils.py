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

from . utils import *


def frame_the_selection(current_text, line_begin, line_end, start_idx,
                        end_idx, punctuation):

    end_line = current_text.lines[line_end].body

    current_text.lines[line_end].body = "{}{}{}".format(
            end_line[:end_idx],
            punctuation[1],
            end_line[end_idx:]
            )

    start_line = current_text.lines[line_begin].body

    current_text.lines[line_begin].body = "{}{}{}".format(
            start_line[:start_idx],
            punctuation[0],
            start_line[start_idx:]
            )

    bpy.ops.text.move(type='NEXT_CHARACTER')
    bpy.ops.text.move(type='NEXT_CHARACTER')

    if line_begin == line_end:
        bpy.ops.text.move(type='NEXT_CHARACTER')


def insert_ponctuation(punctuation, start_idx, end_idx, text):

    base = text.current_line.body

    text.current_line.body = "{}{}{}".format(
            base[:start_idx],
            punctuation,
            base[end_idx:],
            )

    bpy.ops.text.move(type='NEXT_CHARACTER')


def smart_punctuation(punctuation):
    current_text = get_current_text()
    start_idx, end_idx = get_selection(current_text)
    line_begin, line_end = get_lines_selection(current_text)

    if line_begin > line_end:
        line_begin, line_end = remap_line_index(line_begin, line_end)
    if start_idx > end_idx:
        start_idx, end_idx = remap_selection(start_idx, end_idx)

    clean_end_lines(current_text, line_begin, line_end)

    if start_idx != end_idx or line_begin != line_end:
        frame_the_selection(current_text, line_begin,
                            line_end, start_idx,
                            end_idx, punctuation
                            )

    else:
        base = current_text.current_line.body

        if "#" in base[:start_idx]:
            current_text.current_line.body = "{}{}{}".format(
                    base[:start_idx],
                    punctuation[0],
                    base[start_idx:],
                    )
            bpy.ops.text.move(type='NEXT_CHARACTER')

        else:
            if start_idx < len(base):
                if punctuation in ["''", '""']:
                    if base[start_idx] == " ":
                        if start_idx >= 2 and\
                                base[start_idx - 2:start_idx] == punctuation:
                                current_text.current_line.body =\
                                base[:start_idx] + punctuation * 2 + \
                                base[start_idx:]
                                bpy.ops.text.move(type='NEXT_CHARACTER')


                        else:
                            insert_ponctuation(punctuation, start_idx,
                                               end_idx, current_text
                                               )

                    else:
                        if base[start_idx - 1:start_idx + 1] == punctuation:

                            bpy.ops.text.move(type='NEXT_CHARACTER')

                        elif base[start_idx] in ["]", "}", ")"]:
                            insert_ponctuation(punctuation, start_idx,
                                               end_idx, current_text
                                               )
                        # elif base[start_idx - 1:start_idx + 1] in\
                        #         ["[]", "{}", "()"]:
                        #     insert_ponctuation(punctuation, start_idx,
                        #                        end_idx, current_text
                        #                        )

                        else:
                            insert_ponctuation(punctuation[0], start_idx,
                                               end_idx, current_text
                                               )

                else:
                    if base[start_idx] not in ["]", "}", ")", " "]:
                        insert_ponctuation(punctuation[0], start_idx,
                                           end_idx, current_text
                                           )

                    else:
                        insert_ponctuation(punctuation, start_idx,
                                           end_idx, current_text
                                           )

            else:
                if start_idx >= 2 and punctuation in ['""', "''"]:
                    if base[start_idx - 2:] == punctuation:
                        current_text.current_line.body += punctuation * 2
                        bpy.ops.text.move(type='NEXT_CHARACTER')

                    else:
                        insert_ponctuation(punctuation, start_idx, end_idx,
                                           current_text)

                else:
                    insert_ponctuation(punctuation, start_idx, end_idx,
                                       current_text)