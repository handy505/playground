#!/usr/bin/env python3
import os


def main():

    machines = {}
    with open('file.csv', 'r', encoding='utf-8') as fr:
        for line in fr:
            machine_id = line.split(',')[0]

            if not machine_id.isnumeric():
                continue

            if machine_id not in machines:
                machines[machine_id] = [line]
            else:
                machines[machine_id].append(line)

    for k, v in machines.items():
        filename = 'pv{}.csv'.format(k)
        with open(filename, 'w', encoding='utf-8') as fw:
            fw.writelines(v)


if __name__ == '__main__':
    main()
