import os
import subprocess
import sys

import ttrm_to_fumen

if __name__ == '__main__':
    tetr_to_json = './bin/Fumen.exe'
    tetr_path = ''
    output_path = ''
    additional_comment = False
    argumnets_list = ['-i', '-o', '-h', '--help', '-a', '--additional_comment']

    # get arguments
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] not in argumnets_list:
            print(f'Invalid argument: {sys.argv[i]}')
            exit(1)
        if sys.argv[i] == '-i':
            if i + 1 >= len(sys.argv):
                print('Invalid argument: no input tetr file path provided!')
                exit(1)
            tetr_path = sys.argv[i + 1]
        elif sys.argv[i] == '-o':
            if i + 1 >= len(sys.argv):
                print('Invalid argument: no output path provided!')
                exit(1)
            output_path = sys.argv[i + 1]
        elif sys.argv[i] == '-h' or sys.argv[i] == '--help':
            print('Usage: python main.py -i <input_tetr_path> -o <output_path> [-a]')
            exit(0)
        elif sys.argv[i] == '-a' or sys.argv[i] == '--additional_comment':
            additional_comment = True

    if tetr_path == '':
        tetr_path = './replay.ttrm'
    if output_path == '':
        output_path = tetr_path + '_fumens/'
        i = 1
        while os.path.exists(output_path):
            output_path = tetr_path + f'_fumens ({i})/'
            i += 1



    process = subprocess.Popen(f'{tetr_to_json} {tetr_path}', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 실행이 끝날 때까지 기다림
    stdout, stderr = process.communicate()

    if not os.path.exists(tetr_path + '.json'):
        print('tetr to json conversion failed!')
        exit(1)

    print('tetr to json conversion done!')
    if stdout.decode() != '':
        print(stdout.decode())
    if stderr.decode() != '':
        print(stderr.decode())

    ttrm_to_fumen.json_to_fumen(tetr_path + '.json', output_path, additional_comment)
