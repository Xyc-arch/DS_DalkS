import requests
import os
import gzip
import zipfile
import subprocess
import numpy as np


# import pandas as pd
import matplotlib.pyplot as plt


def download_file(url, filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')
    except Exception as err:
        print(f'An error occurred: {err}')


def extract_file(in_file, short_name):
    # print(in_file.strip().split('.')[-1])
    # print(''.join(in_file.split('/')[:-1]) + '/' + short_name + '.txt')
    type = in_file.strip().split('.')[-1]
    out_file = '/'.join(in_file.split('/')[:-1]) + '/' + short_name
    if short_name != 'LB':
        out_file += '.txt'
    else:
        out_file += '.csv'
    # if not os.path.exists(out_file):
    if type == 'gz':
        with gzip.open(in_file, 'rb') as f_in:
            with open(out_file, 'wb') as f_out:
                f_out.write(f_in.read())
    elif type == 'zip':
        with zipfile.ZipFile(in_file, 'r') as zip_ref:
            zip_ref.extract('edges.csv', '/'.join(out_file.split('/')[:-1]))
        os.rename('/'.join(out_file.split('/')[:-1]) + '/edges.csv', out_file)
    elif type == 'txt':
        os.rename(in_file, out_file)
    if os.path.exists(in_file):
        os.remove(in_file)
    # print(short_name + ' has been extracted.')


def run(command, timeout=72 * 3600):
    command = command.strip().split(' ')
    # print(command)
    executable = command[-4]
    algorithm, dataset = command[-2], command[-1]
    # command = [executable, data_directory, algorithm, dataset]
    file_name = './outputs/' + executable + '_' + algorithm + '_' + dataset + '.txt'
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print(timeout)
        stdout, stderr = proc.communicate(timeout=timeout)

        with open(file_name, 'w') as file:
            file.write(stdout)

    except subprocess.TimeoutExpired:
        print(f"Process exceeded timeout of {timeout} seconds.")
        proc.kill()
        # stdout, stderr = proc.communicate()  #
        with open(file_name, 'w') as file:
            file.write(f'Process exceeded timeout of {timeout} seconds.')
        # return timeout
    except Exception as e:
        print(f"An error occurred: {e}")


def format_time(time):
    flag = time[0] == '>'
    if flag:
        time = float(time[1:])
    else:
        time = float(time)
    if time >= 60:
        time = round(time)
        min = time / 60
        if min >= 60:
            hour = int(min // 60)
            min = int(min % 60)
            time = f'{hour} h'
            if min >= 1:
                time += f' {min} m'
        else:
            min = int(time // 60)
            sec = int(time % 60)
            time = f'{min} m'
            if sec >= 1:
                time += f' {sec} s'
    else:
        time = f"{format(time, '.2f')} s"
    if flag:
        time = '>' + time
    return time


def table_4(unweighted_graphs, weighted_graphs, timeout=72 * 3600):
    # todo
    cols = ['Dataset', 'cCoreExact', 'FlowExact', 'cCoreApp*', 'FlowApp', 'FlowApp*', 'Greedy++', 'cCoreG++',
            r'$\frac{FlowExact}{cCoreExact}$', r'$\frac{FlowApp*}{cCoreApp*}$', r'$\frac{Greedy++}{cCoreExact}$']
    result = subprocess.run(['which', 'time'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time = result.stdout.strip()
    data = []
    for graph in unweighted_graphs:
        row = [f'{graph}']
        executable = './unWExp'
        for col in cols[1: 8]:
            if col[-2] == '+':
                col = col[:-2] + 'pp'
            file_name = './outputs/' + '_'.join([executable, col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph])
                if col == 'FlowExact' or col == 'cCoreExact':
                    command = time + ' -v ' + command
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if lines[0][:7] == 'Process':
                    row.append('>' + str(timeout))
                elif col == 'FlowExact':
                    row.append(lines[3].split(' ')[-1])
                elif col == 'cCoreExact':
                    row.append(lines[5].split(' ')[-1])
                else:
                    row.append(lines[-1].split(' ')[-1])
        if row[2][0] != '>':
            row.append(format(float(row[2]) / float(row[1]), '.2f'))
        else:
            row.append('>' + format(float(row[2][1:]) / float(row[1]), '.2f'))
        if row[5][0] != '>':
            row.append(format(float(row[5]) / float(row[3]), '.2f'))
        else:
            row.append('>' + format(float(row[5][1:]) / float(row[3]), '.2f'))
        if row[6][0] != '>':
            row.append(format(float(row[6]) / float(row[1]), '.2f'))
        else:
            row.append(format(float(row[6][1:]) / float(row[1]), '.2f'))
        for i in range(1, 8):
            row[i] = format_time(row[i])
        data.append(row)

    for graph in weighted_graphs:
        row = [f'{graph}']
        executable = './WExp'
        for col in cols[1: 8]:
            if col[-2] == '+':
                col = col[:-2] + 'pp'
            file_name = './outputs/' + '_'.join([executable, col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph])
                if col == 'FlowExact' or col == 'cCoreExact':
                    command = time + ' -v ' + command
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if lines[0][:7] == 'Process':
                    row.append('>' + str(timeout))
                elif col == 'FlowExact':
                    row.append(lines[6].split(' ')[-1])
                elif col == 'cCoreExact':
                    row.append(lines[8].split(' ')[-1])
                else:
                    row.append(lines[-1].split(' ')[-1])
        if row[2][0] != '>':
            row.append(format(float(row[2]) / float(row[1]), '.2f'))
        else:
            row.append('>' + format(float(row[2][1:]) / float(row[1]), '.2f'))
        if row[5][0] != '>':
            row.append(format(float(row[5]) / float(row[3]), '.2f'))
        else:
            row.append('>' + format(float(row[5][1:]) / float(row[3]), '.2f'))
        if row[6][0] != '>':
            row.append(format(float(row[6]) / float(row[1]), '.2f'))
        else:
            row.append(format(float(row[6][1:]) / float(row[1]), '.2f'))
        for i in range(1, 8):
            row[i] = format_time(row[i])
        data.append(row)
    print(data)
    plt.rcParams['text.usetex'] = True

    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data, colLabels=cols, loc='center', cellLoc='center', edges='horizontal')
    plt.savefig('./outputs/table_4.png')
    plt.show()


def figure_6(unweighted_graphs, weighted_graphs, timeout=72 * 3600):
    # todo
    labels = ['cCoreExact', 'FlowExact']
    result = subprocess.run(['which', 'time'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time = result.stdout.strip()
    data = [[], []]
    x_labels = []
    for graph in unweighted_graphs:
        executable = './unWExp'
        for i, label in enumerate(labels):
            file_name = './outputs/' + '_'.join([executable, label, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', label, graph])
                command = time + ' -v ' + command
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if lines[0][:7] == 'Process':
                    if len(data[0]) != len(data[1]):
                        data[0].pop()
                    break
                else:
                    data[i].append(float(lines[-14].split(' ')[-1]))
                    if i:
                        x_labels.append(graph)

    for graph in weighted_graphs:
        executable = './WExp'
        for i, label in enumerate(labels):
            file_name = './outputs/' + '_'.join([executable, label, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', label, graph])
                command = time + ' -v ' + command
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if lines[0][:7] == 'Process':
                    if len(data[0]) != len(data[1]):
                        data[0].pop()
                    break
                else:
                    data[i].append(float(lines[-14].split(' ')[-1]))
                    if i:
                        x_labels.append(graph)
    print(data)
    x = np.arange(len(data[0]))
    print(x)
    total_width, n = 0.8, 2
    width = total_width / n
    x = x - width / 2
    fig, ax = plt.subplots()
    plt.bar(x, data[0], width=width, label=labels[0])
    plt.bar(x + width, data[1], width=width, label=labels[1], color='y')
    # plt.xticks(np.arange(len(data[0])), labels=labels)
    plt.legend()
    ax.set_xticks(np.arange(3), x_labels)
    # plt.xlabel('Figure. 6. Memory cost of cCoreExact and FlowExact.')
    plt.xlabel('Datasets')
    plt.ylabel('memory cost (kB)')
    plt.yscale('log')
    plt.tick_params(which = 'both', direction='in', labelsize="large", top=True, right=True)
    plt.savefig('./outputs/figure_6.png')
    plt.show()


def table_5(graphs, timeout=72 * 3600):
    cols = ['Dataset', '\# vertices', '\# edges', r'$\rho(S^*)$', 'FlowExact', 'cCoreExact']
    executable = './denoExp'
    data = []
    for graph in graphs:
        row = [f'{graph}']
        with open(f'./data/{graph}.txt', 'r') as file:
            for _ in range(3):
                line = file.readline()
            line = line.strip().split(' ')
            row.append('{:,.0f}'.format(float(line[2])))
            row.append('{:,.0f}'.format(float(line[4])))
        for col in cols[-2:]:
            file_name = './outputs/' + '_'.join([executable, col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph])
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if len(row) < 4:
                    row.append(format(float(lines[1].split(' ')[-1]), '.2f'))
                row.append(lines[-1].split(' ')[-1])
        data.append(row)
    plt.rcParams['text.usetex'] = True

    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data, colLabels=cols, loc='center', cellLoc='center', edges='horizontal')
    plt.savefig('./outputs/table_5.png')
    plt.show()


def table_6(unweighted_graphs, weighted_graphs, timeout=72 * 3600):
    cols = ['Dataset', r'$\rho(S^*) by cCoreExact$', r'$\hat{\rho}(S^*) by Greedy++$']
    result = subprocess.run(['which', 'time'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time = result.stdout.strip()
    data = []
    for graph in unweighted_graphs:
        row = [f'{graph}']
        executable = './unWExp'
        for col in cols[1: 3]:
            col = col.split(' ')[-1][:-1]
            if col[-2] == '+':
                col = col[:-2] + 'pp'
            # print(col)
            file_name = './outputs/' + '_'.join([executable, col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph])
                if col == 'cCoreExact':
                    command = time + ' -v ' + command
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if col == 'cCoreExact':
                    row.append(format(float(lines[4].split(' ')[-1]), '.2f'))
                else:
                    row.append(format(float(lines[1].split(' ')[-1]), '.2f'))
        data.append(row)

    for graph in weighted_graphs:
        row = [f'{graph}']
        executable = './WExp'
        for col in cols[1: 3]:
            col = col.split(' ')[-1][:-1]
            if col[-2] == '+':
                col = col[:-2] + 'pp'
            file_name = './outputs/' + '_'.join([executable, col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph])
                if col == 'cCoreExact':
                    command = time + ' -v ' + command
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if col == 'cCoreExact':
                    row.append(format(float(lines[7].split(' ')[-1]), '.2f'))
                else:
                    row.append(format(float(lines[-2].split(' ')[-1]), '.2f'))
        data.append(row)

    plt.rcParams['text.usetex'] = True

    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data, colLabels=cols, loc='center', cellLoc='center', edges='horizontal')
    plt.savefig('./outputs/table_6.png')
    plt.show()

# todo
urls = [
    'https://snap.stanford.edu/data/bigdata/communities/com-friendster.ungraph.txt.gz',
    'https://snap.stanford.edu/data/bigdata/communities/com-orkut.ungraph.txt.gz',
    'https://snap.stanford.edu/data/bigdata/communities/com-lj.ungraph.txt.gz',
    'https://snap.stanford.edu/data/bigdata/communities/com-youtube.ungraph.txt.gz',
    'https://snap.stanford.edu/data/bigdata/communities/com-dblp.ungraph.txt.gz',
    'https://snap.stanford.edu/data/bigdata/communities/com-amazon.ungraph.txt.gz',
    'https://networks.skewed.de/net/libimseti/files/libimseti.csv.zip',
    'http://opsahl.co.uk/tnet/datasets/OF_one-mode_weightedmsg_sum.txt',
    'http://opsahl.co.uk/tnet/datasets/Newman-Cond_mat_95-99-co_occurrence.txt',
    'http://opsahl.co.uk/tnet/datasets/openflights.txt',
    'https://snap.stanford.edu/data/wiki-Vote.txt.gz',
    'https://snap.stanford.edu/data/web-Stanford.txt.gz',
    'https://snap.stanford.edu/data/web-NotreDame.txt.gz'
]
datasets = [
    'FT',
    'OK',
    'LJ',
    'YT',
    'DP',
    'AZ',
    'LB',
    'FF',
    'NM',
    'OF',
    'WV',
    'SF',
    'ND'
]

# # todo
# urls = [urls[4], urls[-5]]
# datasets = [datasets[4], datasets[-5]]

if not os.path.exists('./data'):
    os.mkdir('data')
files = []
for i, url in enumerate(urls):
    raw_file = './data/' + url.strip().split('/')[-1]
    file_name = './data/' + datasets[i]
    if datasets[i] != 'LB':
        file_name += '.txt'
    else:
        file_name += '.csv'
        if not os.path.exists(file_name):
            download_file(url, raw_file)
            extract_file(raw_file, datasets[i])
    print(datasets[i] + ' has been extracted.')

os.system('make all')
if not os.path.exists('./outputs'):
    os.mkdir('outputs')
table_4(['YT', 'DP', 'AZ', 'LJ', 'FT', 'OK'], ['LW', 'YW', 'LB', 'NM', 'OF', 'FF'])
figure_6(['YT', 'DP', 'AZ', 'LJ', 'FT', 'OK'], ['LW', 'YW', 'LB', 'NM', 'OF', 'FF'])
table_5(['WV', 'SF', 'ND'])
table_6(['YT', 'DP', 'AZ', 'LJ', 'FT', 'OK'], ['LW', 'YW', 'LB', 'NM', 'OF', 'FF'])
os.system('make clear')

