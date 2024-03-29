import os
import subprocess
import sys

import ttrm_to_fumen

if __name__ == '__main__':
    tetr_to_json = './bin/Fumen.exe'
    tetr_path = './example/example.ttrm'
    output_path = './example/fumen'

    if len(sys.argv) < 2:
        print('Usage: python main.py <tetr_path> <output_path: Optional>')
        exit(1)

    if len(sys.argv) > 3:
        print('Usage: python main.py <tetr_path> <output_path: Optional>')
        exit(1)

    if len(sys.argv) == 3:
        tetr_path = sys.argv[1]
        output_path = sys.argv[2]
    else:
        tetr_path = sys.argv[1]
        output_path = tetr_path + '_fumens/'
        i = 1
        while os.path.exists(output_path):
            output_path = tetr_path + f'_fumens ({i})/'
            i += 1

    process = subprocess.Popen(f'{tetr_to_json} {tetr_path}', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 실행이 끝날 때까지 기다림
    stdout, stderr = process.communicate()

    if not os.path.exists('example/example.ttrm.json'):
        print('tetr to json conversion failed!')
        exit(1)

    print('tetr to json conversion done!')
    if stdout.decode() != '':
        print(stdout.decode())
    if stderr.decode() != '':
        print(stderr.decode())

    ttrm_to_fumen.json_to_fumen(tetr_path + '.json', output_path)
