import json
import os

from py_fumen.field import create_inner_field, Field, Mino, Operation
from py_fumen.page import Page
from py_fumen.encoder import encode


def rot_to_text(rot):
    if rot == 0:
        return 'spawn'
    elif rot == 1:
        return 'right'
    elif rot == 2:
        return 'reverse'
    elif rot == 3:
        return 'left'

def text_to_rot(text):
    if text == 'spawn':
        return 0
    elif text == 'right':
        return 1
    elif text == 'reverse':
        return 2
    elif text == 'left':
        return 3

def rot_convert(op: Operation) -> Operation:
    offsets = [[[(0, 1)], [(0, 1)], [(0, 1)], [(0, 1)]], [[(0, 1)], [(0, 1)], [(0, 1)], [(0, 1)]], [[(0, 1)], [(0, 2)], [(1, 2)], [(1, 1)]], [[(0, 1)], [(0, 1)], [(0, 1)], [(0, 1)]], [[(0, 1)], [(1, 1)], [(1, 0)], [(0, 0)]], [[(0, 1)], [(0, 1)], [(0, 1)], [(0, 1)]], [[(0, 1)], [(0, 1)], [(0, 1)], [(0, 1)]]]
    pieces = ['Z', 'L', 'O', 'S', 'I', 'J', 'T']
    return Operation(op.piece_type, op.rotation, op.x + offsets[pieces.index(op.piece_type)][text_to_rot(op.rotation)][0][0], op.y + offsets[pieces.index(op.piece_type)][text_to_rot(op.rotation)][0][1])



def json_to_fumen(json_path, output_path, additional_comment=False):
    if output_path[-1] not in ['/', '\\']:
        output_path += '/'
    with open(json_path, 'r') as f:
        data = json.load(f)

    for game in range(len(data)):
        for player in range(len(data[game])):
            d = data[game][player][:]
            pages = []
            for a in range(len(d)):
                if a != 0:
                    f = d[a - 1]['data']['board'][-20:]
                    board_str = ''.join([''.join([str(x) for x in row]) for row in f]).replace(' ', '_').replace('G', 'X')
                else:
                    board_str = '__________' * 20

                comment = ''
                if additional_comment:
                    if d[a]['data']['beforeMino']['lines'] != 0:
                        if d[a]['data']['backToBack'] > 1:
                            comment += f'{d[a]["data"]["backToBack"]-1}x B2B '
                        if d[a]['data']['combo'] > 1:
                            comment = f'{d[a]["data"]["combo"]-1} combo '
                        if d[a]['data']['beforeMino']['spin'] == 'Normal':
                            comment += 'T-Spin '
                        elif d[a]['data']['beforeMino']['spin'] == 'Mini':
                            comment += 'T-Spin Mini '
                        if d[a]['data']['beforeMino']['lines'] == 1:
                            comment += 'Single'
                        elif d[a]['data']['beforeMino']['lines'] == 2:
                            comment += 'Double'
                        elif d[a]['data']['beforeMino']['lines'] == 3:
                            comment += 'Triple'
                        elif d[a]['data']['beforeMino']['lines'] == 4:
                            comment += 'Quad'

                op = Operation(d[a]['data']['beforeMino']['minoType'], rot_to_text(d[a]['data']['beforeMino']['rotation']),
                               d[a]['data']['beforeMino']['x'], 37 - d[a]['data']['beforeMino']['y'])
                op = rot_convert(op)
                field = Field.create(board_str, '__________')
                pages.append(Page(field=create_inner_field(field), operation=op, comment=comment))

            os.makedirs(output_path + 'game' + str(game), exist_ok=True)
            # print(game, player, len(pages))
            with open(output_path + 'game' + str(game) + '/' + data[game][player][0]['data']['username'] + '.tetfu', 'w') as f:
                f.write(encode(pages))
