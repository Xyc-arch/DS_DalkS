# DS and DalkS code

This is the code for SIGMOD 2023 paper `Efficient and Effective Algorithms for Generalized Densest Subgraph Discovery`. Our novel algorithms mainly include:

- `cCoreExact`
- `cCoreApp*`
- `cCoreG++`
- `dalksDecomp`

All relevant data is expected to be in the directory `data`.

```sh
git clone https://github.com/Xyc-arch/DS_DalkS.git
cd DS_DalkS
mkdir data
```

## Setup

A Linux machine equipped with two Intel(R) Xeon(R) Silver 4210R CPU @ 2.40GHz processors with 10 cores.

gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1).

Python3.

To equip with the necessary python package, run

```sh
pip install -r requirements.txt
```


## Dataset preparation

|  Dataset  | Short |  weblink  | download file                                                                                 | 
| --------- |-------| --------- |-----------------------------------------------------------------------------------------------| 
| Friendster | FT    | [link](https://snap.stanford.edu/data/com-Friendster.html) | com-friendster.ungraph.txt.gz                                                                 | 
| Orkut | OK    | [link](https://snap.stanford.edu/data/com-Orkut.html) | com-orkut.ungraph.txt.gz                                                                      |
| LiveJournal | LJ    | [link](https://snap.stanford.edu/data/com-LiveJournal.html) | com-lj.ungraph.txt.gz                                                                         |
| YouTube | YT    | [link](https://snap.stanford.edu/data/com-Youtube.html) | com-youtube.ungraph.txt.gz                                                                    |
| DBLP | DP    | [link](https://snap.stanford.edu/data/com-DBLP.html) | com-dblp.ungraph.txt.gz                                                                       |
| Amazon | AZ    | [link](https://snap.stanford.edu/data/com-Amazon.html) | com-amazon.ungraph.txt.gz                                                                     |
| Libimseti | LB    | [link](https://networks.skewed.de/net/libimseti) | libimseti (network.csv.zip)                                                                   |
| FacebookForum | FF    | [link](https://toreopsahl.com/datasets/) | Network 2 Weighted static one-mode network (weighted by number of messages; sum): tnet-format |
| Newman | NM    | [link](https://toreopsahl.com/datasets/) | Network 12 Weighted static one-mode network (sum of joint papers): tnet-format (1.21mb)       |
| Open-Flights| OF    | [link](https://toreopsahl.com/datasets/) | Network 14 third dataset tnet-format                                                          |
| WikiVote | WV    | [link](https://snap.stanford.edu/data/wiki-Vote.html) | wiki-Vote.txt.gz                                                                              |
| Standford | SF    | [link](https://snap.stanford.edu/data/web-Stanford.html) | web-Stanford.txt.gz                                                                           |
| NotreDame | ND     | [link](https://snap.stanford.edu/data/web-NotreDame.html) | web-NotreDame.txt.gz                                                                          |

You need to place text files in the directory `data`. Follow the steps:

- `gz files`: decompress gz files and extract txt files. (e.g. `web-NotreDame.txt` from `web-NotreDame.txt.gz`)
- `tnet`: press `command/ctr` + `s` to download txt files.
- `zip files`: unzip `network.csv.zip` and extract `edges.csv` out.
- Place all text files in `data` directory.
- Rename all text files as their corresponding short name. (e.g. `web-NotreDame.txt` as `ND.txt`)

[//]: # (- Rename `wiki-Vote.txt` &#40;`WV`&#41; as `Wiki-Vote`)

Check the `data` directory:


 * data
    * data/FT.txt
    * data/OK.txt
    * data/LJ.txt
    * data/YT.txt
    * data/DP.txt
    * data/AZ.txt
    * data/LB.csv
    * data/OF.txt
    * data/NM.txt
    * data/OF.txt
    * data/WV.txt
    * data/SF.txt
    * data/ND.txt



## Compilation

You can compile all executables by

```sh
make all
```

You can clear all by

```sh
make clear
```

If you want to do experiemt about c-core-based acceleration with original edge density on unweighted graphs, you can enter:

```sh
make unWExp
```

If you want to do experiemt about `c-core-based acceleration` with `weighted density` on `weighted graphs`, you can enter:

```sh
make WExp
```

If you want to do experiemt about `c-core-based acceleration` with `denominator weighted density` on `weighted graphs`, you can enter:

```sh
make denoExp
```

## Test 

This is a simple and efficient test of our algorithms. We use the dataset `Newman` (`NM`).The instruction about time-costly full version can be found below this test version.

```sh
make all
```

`cCoreExact`:

```sh
./WExp ./data cCoreExact NM
```

`cCoreApp*`:

```sh
./WExp ./data cCoreApp* NM
```

`cCoreG++`:

```sh
./WExp ./data cCoreGpp NM
```

`dalksDecomp`:

```sh
./formatData ./data NM
./Density-Friendly/exactDF 4 1500 ./data/testnet.txt ./Density-Friendly/rates.txt ./Density-Friendly/pavafit.txt ./Density-Friendly/cuts.txt ./Density-Friendly/testExact.txt
```

The generated file `./Density-Friendly/testExact` contains the info about decomposition. Further, you can use `./Density-Friendly/dalksDecomp.py` to report (visualize) the result.


## Full Reproduction

Here, we provide the instruction for reproducing all of results. Note that the most time costly experiment using our novel algorithms may take around 1 day, while baselines may not finish within 3 days.

You can directly get the full reproduction by

```sh
python3 reproduce.py
```

Components in following cmd are like:

```sh
./executable /path/to/data/directory algorithm dataset epsilon
```

*Note*: If you omit `epsilon`, it will be set to `0.001` by default.

In the following, we use `./data` as the path to our `data` directory containing all data. You should replace it with yours.


### Table 4, Table 6, Figure 7, Figure 8, Figure 9

For unweighted graphs: `YT`, `DP`, `AZ`, `LJ`, `FT`, `OK`. Replace `YouTube` (`YT`) in the end of the cmd with other datasets.
```sh

make unWExp
./unWExp ./data cCoreExact YT
./unWExp ./data fastDalkS YT
./unWExp ./data cCoreApp* YT
./unWExp ./data Greedypp YT 0.0909
./unWExp ./data cCoreGpp YT 0.0909
./unWExp ./data FlowExact YT
./unWExp ./data cCoreApp YT
./unWExp ./data FlowApp YT
./unWExp ./data FlowApp* YT
```

For weighted graphs: `LW`, `YW`, `LB`, `NM`, `OF`, `FF`.

```sh
make WExp
./WExp ./data cCoreExact NM
./WExp ./data fastDalkS NM
./WExp ./data cCoreApp* NM
./WExp ./data Greedypp NM 0.0909
./WExp ./data cCoreGpp NM 0.0909
./WExp ./data FlowExact NM
./WExp ./data cCoreApp NM
./WExp ./data FlowApp NM
./WExp ./data FlowApp* NM
```


### Figure 6

Before running the experiments to reproduce `Figure 6`, please ensure the `time` utility is installed on your system. This utility is used to measure the execution time of the experiments. You can verify the installation and locate the executable path of `time` by running the following command in your terminal:

```bash
which time
```

After confirming the installation of time, replace the commands in `Table 4` as follows:

- Replace `./unWExp` with the full path to `time` followed by `-v ./unWExp`.
- Replace `./WExp` with the full path to `time` followed by `-v ./WExp`.
For example, if `which time` returns `/usr/bin/time`, you should modify the commands in `Table 4` to `/usr/bin/time -v ./unWExp` and `/usr/bin/time -v ./WExp` respectively.

[//]: # (Replace `./unWExp` and `./WExp` in `Table 4` with `/usr/bin/time -v ./unWExp` and `/usr/bin/time -v ./WExp`.)


### Table 5

For weighted graphs: `WV`, `SF`, `ND`.

```sh
make denoExp
./denoExp ./data cCoreExact WV
./denoExp ./data FlowExact WV
```


### Figure 10

First preprocess datasets: `LJ`, `AZ`, `DP`, `NM`.

```sh
make formatData
./formatData ./data NM
```

In your `data` directory, you observe a processed file `data/*net.txt`. For instance, `data/testnet.txt`.

Then we run the decomposition (our DalkS algorithm is based on decomposition) in processed file.

```sh
g++ ./Density-Friendly/exactDF.cpp -fopenmp -fpermissive -o ./Density-Friendly/exactDF -O3
./Density-Friendly/exactDF 4 1500 ./data/NM_net.txt ./Density-Friendly/NM_rates.txt ./Density-Friendly/NM_pavafit.txt ./Density-Friendly/NM_cuts.txt ./Density-Friendly/NM_Exact.txt
```

You will observe the file containing information about decomposition in the form of `./Density-Friendly/*_Exact.txt`. Then obtain the proportion of approximation ratio by:

```sh
python3 ./Density-Friendly/dalksDecomp.py
```




