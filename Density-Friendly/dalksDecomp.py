
# import matplotlib.pyplot as plt
# import numpy as np


# def read_txt(inputpath):
#     D_tilde_size = []
#     temp_size = 0
#     with open(inputpath, 'r', encoding='utf-8') as infile:
#         for line in infile:
#             data_line = line.strip("\n").split() 
#             temp_size += int(data_line[0])
#             D_tilde_size.append(temp_size)
#     return D_tilde_size


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



def graph_one(inputpath, name, N, c):
    
    # if inputpath == "./Density-Friendly/NM_Exact.txt":
    #     print(32*"*")
    #     print("dalkSDecomp on NM:")
    # elif inputpath == "./Density-Friendly/LJ_Exact.txt":
    #     print(32*"*")
    #     print("dalkSDecomp on LJ:")
    # elif inputpath == "./Density-Friendly/DP_Exact.txt":
    #     print(32*"*")
    #     print("dalkSDecomp on DP:")
    # elif inputpath == "./Density-Friendly/AZ_Exact.txt":
    #     print(32*"*")
    #     print("dalkSDecomp on AZ:")
        
    
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
    for n in range(1, N+1):
        if n <= DS_size or n==N:
            approx.append(1)
            n_ge99 += 1
        else:
            if n >= D_tilde_size[c_idx]:
                c_idx += 1
            rate = n/D_tilde_size[c_idx]
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
        size.append(n/N) 
    print("statistics of file {}".format(inputpath.split("\\")[-1]))
    print("<0.33: {} {}".format(n_le33, n_le33/N))
    print("0.33~0.5: {} {}".format(n_33_50, n_33_50/N))
    print("0.5~0.8: {} {}".format(n_50_80, n_50_80/N))
    print("0.8~0.95: {} {}".format(n_80_95, n_80_95/N))
    print("0.95~0.99: {} {}".format(n_95_99, n_95_99/N))
    print(">0.99: {} {}".format(n_ge99, n_ge99/N))
    # plt.plot(size, approx, linewidth=1, color=c, marker=",", label = name)



def find_near_subgraph(inputpath, q, graph_num=5):
    D_tilde_size = read_txt(inputpath)
    pivot_index = next((i for i, x in enumerate(D_tilde_size) if x >= q), None)
    if pivot_index is None:
        pivot_index = len(D_tilde_size) - 1
    
    closest_smaller_than_q = []
    closest_larger_than_or_equal_to_q = []
    
    if pivot_index > 0:  
        start_index = max(0, pivot_index - graph_num)  
        closest_smaller_than_q = D_tilde_size[start_index:pivot_index]
    
    end_index = min(len(D_tilde_size), pivot_index + graph_num)  
    closest_larger_than_or_equal_to_q = D_tilde_size[pivot_index:end_index]
    
    return closest_smaller_than_q + closest_larger_than_or_equal_to_q
    




if __name__ == "__main__":
    # print()
    # inputpath = "D:\\research\\2020-6-12\\data\\testexact.txt"
    # D_tilde_size = read_txt(inputpath)
    # DS_size = D_tilde_size[0]
    # approx = []
    # size = []
    # N = 16264
    # c_idx = 0
    # n_le80 = 0
    # n_80_95 = 0
    # n_95_99 = 0
    # n_ge99 = 0
    # for n in range(1, N+1):
    #     if n <= DS_size or n==N:
    #         approx.append(1)
    #         n_ge99 += 1
    #     else:
    #         if n >= D_tilde_size[c_idx]:
    #             c_idx += 1
    #         rate = n/D_tilde_size[c_idx]
    #         approx.append(rate)
    #         if rate >= 0.99:
    #             n_ge99 += 1
    #         elif 0.95 <= rate < 0.99:
    #             n_95_99 += 1
    #         elif 0.8 <= rate < 0.95:
    #             n_80_95 += 1
    #         else:
    #             n_le80 += 1
    #     size.append(n/N) 
    # print("statistics of file {}".format(inputpath.split("\\")[-1]))
    # print("<0.8: {}".format(n_le80))
    # print("0.8~0.95: {}".format(n_80_95))
    # print("0.95~0.99: {}".format(n_95_99))
    # print(">0.99: {}".format(n_ge99))
    # plt.plot(size, approx, linewidth=1, color="orange", marker=",", label = 'NM')
    # plt.legend()
    # plt.show()

    graph_one("./NM_Exact.txt", "NM", 16264, "orange")
    graph_one("./DP_Exact.txt", "DP", 317080, "blue")
    graph_one("./AZ_Exact.txt", "AZ", 334863, "green")
    graph_one("./LJ_Exact.txt", "LJ", 3997962, "purple")
    
    closest = find_near_subgraph("./comljExact.txt", 50000)
    print(closest)
    # plt.legend()
    # plt.ylabel("approximation")
    # plt.xlabel("k/(# vertices in whole graph)")
    # plt.show()




