import requests
import os
import gzip
import zipfile
import subprocess
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


def run(command, timeout=72 * 3600, file_name=''):
    command = command.strip().split(' ')
    # print(command)
    executable = command[-5]
    algorithm, dataset = command[-3], command[-2]
    # command = [executable, data_directory, algorithm, dataset]
    if file_name == '':
        file_name = './outputs/' + executable[2:] + '_' + algorithm + '_' + dataset + '.txt'
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # print(timeout)
        stdout, stderr = proc.communicate(timeout=timeout)
        print(file_name)
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
    flag = time[1] == '>'
    if flag:
        time = float(time[3:])
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
        time = r'$>$' + time
    return time


def table_4(unweighted_graphs, weighted_graphs, timeout=72 * 3600):
    cols = ['Dataset', 'cCoreExact', 'FlowExact', 'cCoreApp*', 'FlowApp', 'FlowApp*', 'Greedy++', 'cCoreG++',
            r'$\frac{FlowExact}{cCoreExact}$', r'$\frac{FlowApp*}{cCoreApp*}$', r'$\frac{Greedy++}{cCoreExact}$']
    result = subprocess.run(['which', 'time'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time = result.stdout.strip()
    data = []
    for graph in unweighted_graphs:
        row = [f'{graph}']
        executable = './unWExp'
        for col in cols[1: 8]:
            eps = '0.001'
            if col[-2] == '+':
                col = col[:-2] + 'pp'
                eps = '0.0909'
            file_name = './outputs/' + '_'.join([executable[2:], col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph, eps])
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
                    row.append(lines[6].split(' ')[-1])
                else:
                    row.append(lines[-1].split(' ')[-1])
        if row[1][0] != '>':
            if row[2][0] != '>':
                row.append(format(float(row[2]) / float(row[1]), '.2f'))
            else:
                row.append(r'$>$' + format(float(row[2][1:]) / float(row[1]), '.2f'))
                row[2] = r'$>$' + row[2][1:]
        else:
            row.append('---')
        if row[3][0] != '>':
            if row[5][0] != '>':
                row.append(format(float(row[5]) / float(row[3]), '.2f'))
            else:
                row.append(r'$>$' + format(float(row[5][1:]) / float(row[3]), '.2f'))
                row[5] = r'$>$' + row[5][1:]
        else:
            row.append('---')
        if row[1][0] != '>':
            if row[6][0] != '>':
                row.append(format(float(row[6]) / float(row[1]), '.2f'))
            else:
                row.append(format(float(row[6][1:]) / float(row[1]), '.2f'))
                row[6] = r'$>$' + row[6][1:]
        else:
            row.append('---')
        # print(row)
        for i in range(1, 8):
            if row[i][0] == '>':
                row[i] = r'$>$' + row[i][1:]
            row[i] = format_time(row[i])
        data.append(row)

    for graph in weighted_graphs:
        row = [f'{graph}']
        executable = './WExp'
        for col in cols[1: 8]:
            eps = '0.001'
            if col[-2] == '+':
                col = col[:-2] + 'pp'
                eps = '0.0909'
            file_name = './outputs/' + '_'.join([executable[2:], col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph, eps])
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
                    row.append(lines[9].split(' ')[-1])
                else:
                    row.append(lines[-1].split(' ')[-1])
        if row[1][0] != '>':
            if row[2][0] != '>':
                row.append(format(float(row[2]) / float(row[1]), '.2f'))
            else:
                row.append(r'$>$' + format(float(row[2][1:]) / float(row[1]), '.2f'))
                row[2] = r'$>$' + row[2][1:]
        else:
            row.append('---')
        if row[3][0] != '>':
            if row[5][0] != '>':
                row.append(format(float(row[5]) / float(row[3]), '.2f'))
            else:
                row.append(r'$>$' + format(float(row[5][1:]) / float(row[3]), '.2f'))
                row[5] = r'$>$' + row[5][1:]
        else:
            row.append('---')
        if row[1][0] != '>':
            if row[6][0] != '>':
                row.append(format(float(row[6]) / float(row[1]), '.2f'))
            else:
                row.append(format(float(row[6][1:]) / float(row[1]), '.2f'))
                row[6] = r'$>$' + row[6][1:]
        else:
            row.append('---')
        # print(row)
        for i in range(1, 8):
            if row[i][0] == '>':
                row[i] = r'$>$' + row[i][1:]
            row[i] = format_time(row[i])
        data.append(row)
    # print(data)
    # plt.rcParams['text.usetex'] = True

    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data, colLabels=cols, loc='center', cellLoc='center', edges='horizontal')
    plt.savefig('./outputs/table_4.pdf')
    plt.show()


def figure_6(unweighted_graphs, weighted_graphs, timeout=72 * 3600):
    labels = [r'cCoreExact', r'FlowExact']
    result = subprocess.run(['which', 'time'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time = result.stdout.strip()
    data = [[], []]
    x_labels = []
    for graph in unweighted_graphs:
        executable = './unWExp'
        for i, label in enumerate(labels):
            file_name = './outputs/' + '_'.join([executable[2:], label, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', label, graph, '0.001'])
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
            file_name = './outputs/' + '_'.join([executable[2:], label, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', label, graph, '0.001'])
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
    # plt.rcParams['text.usetex'] = True
    # x = np.arange(len(data[0]))
    x = [_ for _ in range(len(data[0]))]
    # print(x)
    total_width, n = 0.8, 2
    width = total_width / n
    # x = x - width / 2
    x = [_ - width / 2 for _ in x]
    fig, ax = plt.subplots()
    plt.bar(x, data[0], width=width, label=labels[0])
    plt.bar([_ + width for _ in x], data[1], width=width, label=labels[1], color='y')
    # plt.xticks(np.arange(len(data[0])), labels=labels)
    plt.legend()
    ax.set_xticks([_ + width / 2 for _ in x], x_labels)
    # plt.xlabel('Figure. 6. Memory cost of cCoreExact and FlowExact.')
    plt.xlabel(r'Datasets')
    plt.ylabel(r'memory cost (kB)')
    plt.yscale('log')
    plt.grid(True)
    plt.tick_params(which='both', direction='in', labelsize="large", top=True, right=True)
    plt.savefig('./outputs/figure_6.pdf')
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
            file_name = './outputs/' + '_'.join([executable[2:], col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph, '0.001'])
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if lines[0][:7] == 'Process':
                    time = '$>$' + str(timeout)
                else:
                    time = lines[-1].split(' ')[-1]
                if len(row) < 4:
                    row.append('---')
                elif time[:3] != '$>$':
                    row[3] = format(float(lines[-2].split(' ')[-1]), '.2f')
                row.append(format_time(time))
        data.append(row)
    # plt.rcParams['text.usetex'] = True

    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data, colLabels=cols, loc='center', cellLoc='center', edges='horizontal')
    plt.savefig('./outputs/table_5.pdf')
    plt.show()


def table_6(unweighted_graphs, weighted_graphs, timeout=72 * 3600):
    cols = ['Dataset', r'$\rho(S^*)$ by cCoreExact', r'$\hat{\rho}(S^*)$ by Greedy++']
    result = subprocess.run(['which', 'time'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time = result.stdout.strip()
    data = []
    for graph in unweighted_graphs:
        row = [f'{graph}']
        executable = './unWExp'
        for col in cols[1: 3]:
            col = col.split(' ')[-1]
            eps = '0.001'
            if col[-2] == '+':
                col = col[:-2] + 'pp'
                eps = '0.0909'
            # print(col)
            file_name = './outputs/' + '_'.join([executable[2:], col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph, eps])
                if col == 'cCoreExact':
                    command = time + ' -v ' + command
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                try:
                    if col == 'cCoreExact':
                        row.append(format(float(lines[5].split(' ')[-1]), '.2f'))
                    else:
                        row.append(format(float(lines[1].split(' ')[-1]), '.2f'))
                except IndexError:
                    row.append('---')
        data.append(row)

    for graph in weighted_graphs:
        row = [f'{graph}']
        executable = './WExp'
        for col in cols[1: 3]:
            col = col.split(' ')[-1]
            eps = '0.001'
            if col[-2] == '+':
                col = col[:-2] + 'pp'
                eps = '0.0909'
            file_name = './outputs/' + '_'.join([executable[2:], col, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', col, graph, eps])
                if col == 'cCoreExact':
                    command = time + ' -v ' + command
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                try:
                    if col == 'cCoreExact':
                        row.append(format(float(lines[8].split(' ')[-1]), '.2f'))
                    else:
                        row.append(format(float(lines[-2].split(' ')[-1]), '.2f'))
                except IndexError:
                    row.append('---')
        data.append(row)
    # plt.rcParams['text.usetex'] = True

    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data, colLabels=cols, loc='center', cellLoc='center', edges='horizontal')
    plt.savefig('./outputs/table_6.pdf')
    plt.show()


def figure_7(unweighted_graphs, weighted_graphs, timeout=72 * 3600):
    result = subprocess.run(['which', 'time'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time = result.stdout.strip()
    x, y1, y2 = [], [], []
    for graph in unweighted_graphs:
        executable = './unWExp'
        algorithm = 'cCoreExact'
        # print(col)
        file_name = './outputs/' + '_'.join([executable[2:], algorithm, graph]) + '.txt'
        if not os.path.exists(file_name):
            command = ' '.join([executable, './data', algorithm, graph, '0.001'])
            command = time + ' -v ' + command
            print(command)
            run(command, timeout)
        with open(file_name, 'r') as file:
            lines = file.read().splitlines()
            try:
                x.append(lines[1].split(' ')[1])
            except:
                x.append('nan')
            try:
                y1.append(lines[1].split(' ')[3])
            except IndexError:
                y1.append('nan')
            try:
                y2.append(lines[2].split(' ')[2])
            except IndexError:
                y2.append('nan')

    for graph in weighted_graphs:
        executable = './WExp'
        algorithm = 'cCoreExact'
        # print(col)
        file_name = './outputs/' + '_'.join([executable[2:], algorithm, graph]) + '.txt'
        if not os.path.exists(file_name):
            command = ' '.join([executable, './data', algorithm, graph, '0.001'])
            command = time + ' -v ' + command
            print(command)
            run(command, timeout)
        with open(file_name, 'r') as file:
            lines = file.read().splitlines()
            try:
                x.append(lines[4].split(' ')[1])
            except IndexError:
                x.append('nan')
            try:
                y1.append(lines[4].split(' ')[3])
            except IndexError:
                y1.append('nan')
            try:
                y2.append(lines[5].split(' ')[2])
            except IndexError:
                y2.append('nan')

    # plt.rcParams['text.usetex'] = True
    fig, ax = plt.subplots()
    plt.grid(True)
    plt.tick_params(which='both', direction='in', labelsize="large", top=True, right=True)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel(r'\#edges')
    plt.ylabel(r'\#vertices')
    plt.xlim(1e2, 1e10)
    plt.ylim(1e0, 1e8)
    ax.set_xticks([1e2, 1e4, 1e6, 1e8, 1e10])
    ax.set_yticks([1e0, 1e2, 1e4, 1e6, 1e8])
    # x, y1, y2 = list(map(int, x)), list(map(int, y1)), list(map(int, y2))
    plt.loglog(x, y1, '^', label=r'\#vertices in whole graph')
    plt.loglog(x, y2, 'o', label=r'\#vertices in core')
    plt.legend()
    plt.savefig('./outputs/figure_7.pdf')
    plt.show()


def figure_8(unweighted_graphs, weighted_graphs, timeout=72 * 3600):
    algorithms = ['FlowApp', 'FlowApp*']
    speedup = []
    labels = []
    for graph in unweighted_graphs:
        executable = './unWExp'
        # print(col)
        time = 0
        for i, algorithm in enumerate(algorithms):
            file_name = './outputs/' + '_'.join([executable[2:], algorithm, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', algorithm, graph, '0.001'])
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if lines[0][:7] == 'Process':
                    break
                else:
                    if time == 0:
                        time = float(lines[-1].split(' ')[-1])
                    else:
                        time /= float(lines[-1].split(' ')[-1])
        if time:
            speedup.append(time)
            labels.append(graph)
    for graph in weighted_graphs:
        executable = './WExp'
        # print(col)
        time = 0
        for i, algorithm in enumerate(algorithms):
            file_name = './outputs/' + '_'.join([executable[2:], algorithm, graph]) + '.txt'
            if not os.path.exists(file_name):
                command = ' '.join([executable, './data', algorithm, graph, '0.001'])
                print(command)
                run(command, timeout)
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                if lines[0][:7] == 'Process':
                    break
                else:
                    if time == 0:
                        time = float(lines[-1].split(' ')[-1])
                    else:
                        time /= float(lines[-1].split(' ')[-1])
        if time:
            speedup.append(time)
            labels.append(graph)
    fig, ax = plt.subplots()
    x = [_ for _ in range(len(labels))]

    plt.bar(x, speedup, width=0.5)
    # plt.xticks(np.arange(len(data[0])), labels=labels)
    ax.set_xticks(x, labels)
    # plt.xlabel('Figure. 6. Memory cost of cCoreExact and FlowExact.')
    plt.xlabel(r'Datasets')
    plt.ylabel(r'Speed up')
    plt.grid(True)
    plt.tick_params(which='both', direction='in', labelsize="large", top=True, right=True)
    plt.savefig('./outputs/figure_8.pdf')
    plt.show()


def figure_9(unweighted_graphs, weighted_graphs, timeout=72 * 3600):
    algorithms = [r'cCoreApp*', r'Greedypp']
    speedup = []
    labels = []
    x = list(range(60, 100, 5))
    x = [_ / 100 for _ in x]
    fig, ax = plt.subplots(2, 2)
    fig.subplots_adjust(wspace=0.5, hspace=0.5)
    # plt.rcParams['text.usetex'] = True

    for j, graph in enumerate(unweighted_graphs):
        y = [[], []]
        executable = './unWExp'
        # print(col)
        for eps in x:
            for i, algorithm in enumerate(algorithms):
                file_name = './outputs/' + '_'.join([executable[2:], algorithm, graph, str(round(eps, 2))]) + '.txt'
                if not os.path.exists(file_name):
                    command = ' '.join([executable, './data', algorithm, graph, str(round(1 - eps, 2))])
                    print(command)
                    run(command, timeout, file_name)
                with open(file_name, 'r') as file:
                    lines = file.read().splitlines()
                    try:
                        y[i].append(float(lines[-1].split(' ')[-1]))
                    except IndexError:
                        y[i].append(timeout)
                    except ValueError:
                        y[i].append(timeout)
        ax[j // 2, j % 2].plot(x, y[0], '^-', linewidth=2, label=algorithms[0])
        ax[j // 2, j % 2].plot(x, y[1], 'o--', linewidth=2, label=algorithms[1])
        # ax[j // 2, j % 2].set_ylim(0, timeout)
        ax[j // 2, j % 2].set_xlabel(r'appro factor')
        ax[j // 2, j % 2].set_ylabel(r'time (s)')
        ax[j // 2, j % 2].set_yscale('log')
        ax[j // 2, j % 2].legend()
        ax[j // 2, j % 2].tick_params(which='both', direction='in', labelsize="large", top=True, right=True)
        if timeout in y[0] or timeout in y[1]:
            current_ticks = ax[j // 2, j % 2].get_yticks()
            current_labels = [item.get_text() for item in ax[j // 2, j % 2].get_yticklabels()]
            index_to_replace = 0
            for i, tick in enumerate(current_ticks.tolist()):
                try:
                    if tick <= timeout < current_ticks.tolist()[i + 1]:
                        index_to_replace = i + 1
                except IndexError:
                    index_to_replace = i
            current_labels[index_to_replace] = 'inf'
            current_ticks[index_to_replace] = timeout
            ax[j // 2, j % 2].set_yticks(current_ticks[:index_to_replace + 1])
            ax[j // 2, j % 2].set_yticklabels(current_labels[:index_to_replace + 1])
        ax[j // 2, j % 2].set_title(graph)

    for j, graph in enumerate(weighted_graphs):
        y = [[], []]
        executable = './WExp'
        # print(col)
        for eps in x:
            for i, algorithm in enumerate(algorithms):
                file_name = './outputs/' + '_'.join([executable[2:], algorithm, graph, str(round(eps, 2))]) + '.txt'
                if not os.path.exists(file_name):
                    command = ' '.join([executable, './data', algorithm, graph, str(round(1 - eps, 2))])
                    print(command)
                    run(command, timeout, file_name)
                with open(file_name, 'r') as file:
                    lines = file.read().splitlines()
                    try:
                        y[i].append(float(lines[-1].split(' ')[-1]))
                    except IndexError:
                        y[i].append(timeout)
                    except ValueError:
                        y[i].append(timeout)
        ax[1, j + 1].plot(x, y[0], '^-', linewidth=2, label=algorithms[0])
        ax[1, j + 1].plot(x, y[1], 'o--', linewidth=2, label=algorithms[1])
        # ax[1, j + 1].set_ylim(0, timeout)
        ax[1, j + 1].set_xlabel(r'appro factor')
        ax[1, j + 1].set_ylabel(r'time (s)')
        ax[1, j + 1].set_yscale('log')
        ax[1, j + 1].legend()
        ax[1, j + 1].tick_params(which='both', direction='in', labelsize="large", top=True, right=True)
        if timeout in y[0] or timeout in y[1]:
            current_ticks = ax[1, j + 1].get_yticks()
            current_labels = [item.get_text() for item in ax[1, j + 1].get_yticklabels()]
            index_to_replace = 0
            for i, tick in enumerate(current_ticks.tolist()):
                try:
                    if tick <= timeout < current_ticks.tolist()[i + 1]:
                        index_to_replace = i + 1
                except IndexError:
                    index_to_replace = i
            current_labels[index_to_replace] = 'inf'
            current_ticks[index_to_replace] = timeout
            ax[1, j + 1].set_yticks(current_ticks[:index_to_replace + 1])
            ax[1, j + 1].set_yticklabels(current_labels[:index_to_replace + 1])
        ax[1, j + 1].set_title(graph)

    plt.savefig('./outputs/figure_9.pdf')
    plt.show()


def read_txt(inputpath):
    pairs = []
    D_tilde_size = []
    temp_size = 0
    with open(inputpath, 'r', encoding='utf-8') as infile:
        for line in infile:
            data_line = line.strip("\n").split()
            pairs.append((int(data_line[0]), eval(data_line[1])))
    sorted_pairs = sorted(pairs, key=lambda x: x[1], reverse=True)
    for pair in sorted_pairs:
        temp_size += pair[0]
        D_tilde_size.append(temp_size)

    return D_tilde_size


def graph_one(inputpath, N):
    D_tilde_size = read_txt(inputpath)
    DS_size = D_tilde_size[0]
    approx = []
    size = []
    c_idx = 0
    n_50_80 = 0
    n_80_95 = 0
    n_95_99 = 0
    n_ge99 = 0
    n_33_50 = 0
    n_le33 = 0
    for n in range(1, N + 1):
        if n <= DS_size or n == N:
            approx.append(1)
            n_ge99 += 1
        else:
            if n >= D_tilde_size[c_idx]:
                c_idx += 1
            rate = n / D_tilde_size[c_idx]
            approx.append(rate)
            if rate >= 0.99:
                n_ge99 += 1
            elif 0.95 <= rate < 0.99:
                n_95_99 += 1
            elif 0.8 <= rate < 0.95:
                n_80_95 += 1
            elif 0.5 <= rate < 0.8:
                n_50_80 += 1
            elif 0.33 <= rate < 0.5:
                n_33_50 += 1
            elif rate < 0.33:
                n_le33 += 1
        size.append(n / N)
    return [(n_le33 + n_33_50 + n_50_80) / N, n_80_95 / N, n_95_99 / N, n_ge99 / N]


def figure_10():
    os.system('g++ ./Density-Friendly/exactDF.cpp -fopenmp -fpermissive -o ./Density-Friendly/exactDF -O3')
    datasets = ['NM', 'DP', 'AZ', 'LJ']
    proportions = {
        r'0-0.8': [],
        r'0.8-0.95': [],
        r'0.95-0.99': [],
        r'0.99-1': []
    }
    Ns = [16264, 317080, 334863, 3997962]
    for i, dataset in enumerate(datasets):
        file_name = f"./Density-Friendly/{dataset}_Exact.txt"
        if not os.path.exists(file_name):
            os.system(f'./formatData ./data {dataset}')
            os.system(
                f'./Density-Friendly/exactDF 4 1500 ./data/{dataset}_net.txt ./Density-Friendly/{dataset}_rates.txt ./Density-Friendly/{dataset}_pavafit.txt ./Density-Friendly/{dataset}_cuts.txt ./Density-Friendly/{dataset}_Exact.txt')
            os.system(
                f'rm ./data/{dataset}_net.txt ./Density-Friendly/{dataset}_rates.txt ./Density-Friendly/{dataset}_pavafit.txt ./Density-Friendly/{dataset}_cuts.txt')
        nums = graph_one(file_name, Ns[i])
        proportions[r'0-0.8'].append(nums[0])
        proportions[r'0.8-0.95'].append(nums[1])
        proportions[r'0.95-0.99'].append(nums[2])
        proportions[r'0.99-1'].append(nums[3])
    # with open(path, 'r') as file:
    #     lines = file.read().splitlines()
    #     for i in range(4):
    #         num1 = int(lines[i * 7 + 1].split(' ')[1]) + int(lines[i * 7 + 2].split(' ')[1]) + int(
    #             lines[i * 7 + 3].split(' ')[1])
    #         num2 = int(lines[i * 7 + 4].split(' ')[1])
    #         num3 = int(lines[i * 7 + 5].split(' ')[1])
    #         num4 = int(lines[i * 7 + 6].split(' ')[1])
    #         total = num1 + num2 + num3 + num4
    #         proportions[r'0-0.8'].append(num1 / total)
    #         proportions[r'0.8-0.95'].append(num2 / total)
    #         proportions[r'0.95-0.99'].append(num3 / total)
    #         proportions[r'0.99-1'].append(num4 / total)

    fig, ax = plt.subplots()

    # Stacked bar chart
    bottoms = [0] * len(datasets)
    for name, values in proportions.items():
        ax.barh(datasets, values, left=bottoms, label=name)
        bottoms = [left + value for left, value in zip(bottoms, values)]

    ax.set_xlabel('Proportion')
    ax.set_title('Datasets')
    ax.legend()
    plt.savefig('./outputs/figure_10.pdf')
    plt.show()


timeout = 60
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
if not os.path.exists('outputs'):
    os.mkdir('outputs')
table_4(['YT', 'DP', 'AZ', 'LJ', 'FT', 'OK'], ['LW', 'YW', 'LB', 'NM', 'OF', 'FF'], timeout)
figure_6(['YT', 'DP', 'AZ', 'LJ', 'FT', 'OK'], ['LW', 'YW', 'LB', 'NM', 'OF', 'FF'], timeout)
table_5(['WV', 'SF', 'ND'], timeout)
table_6(['YT', 'DP', 'AZ', 'LJ', 'FT', 'OK'], ['LW', 'YW', 'LB', 'NM', 'OF', 'FF'], timeout)
figure_7(['YT', 'DP', 'AZ', 'LJ', 'FT', 'OK'], ['LW', 'YW', 'LB', 'NM', 'OF', 'FF'], timeout)
figure_8(['YT', 'DP', 'AZ', 'LJ', 'FT', 'OK'], ['LW', 'YW', 'LB', 'NM', 'OF', 'FF'], timeout)
figure_9(['DP', 'YT', 'LJ'], ['LB'], timeout)
figure_10()

os.system('make clear')
