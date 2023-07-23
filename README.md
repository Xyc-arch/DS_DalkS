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
```

## Setup

A Linux machine equipped with two Intel(R) Xeon(R) Silver 4210R CPU @ 2.40GHz processors with 10 cores.

gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1).

Python 3.8.10 with numpy and matplotlib installed.


## Dataset preparation

|  Dataset  |  Short  |  weblink  |  download file  | 
| --------- | ------- | --------- | --------------- | 
| Friendster | FT | [link](https://snap.stanford.edu/data/com-Friendster.html) | com-friendster.ungraph.txt.gz | 
| Orkut | OK | [link](https://snap.stanford.edu/data/com-Orkut.html) | com-orkut.ungraph.txt.gz |
| LiveJournal | LJ | [link](https://snap.stanford.edu/data/com-LiveJournal.html) | com-lj.ungraph.txt.gz |
| YouTube | YT | [link](https://snap.stanford.edu/data/com-Youtube.html) | com-youtube.ungraph.txt.gz |
| DBLP | DP | [link](https://snap.stanford.edu/data/com-DBLP.html) | com-dblp.ungraph.txt.gz |
| Amazon | AZ | [link](https://snap.stanford.edu/data/com-Amazon.html) | com-amazon.ungraph.txt.gz |
| Libimseti | LB | [link](https://networks.skewed.de/net/libimseti) | libimseti (network.csv.zip) |
| FacebookForum | FF | [link](https://toreopsahl.com/datasets/) | Network 2 Weighted static one-mode network (weighted by number of messages; sum): tnet-format |
| Newman | NM | [link](https://toreopsahl.com/datasets/) | Network 12 Weighted static one-mode network (sum of joint papers): tnet-format (1.21mb) |
| Open-Flights| OF | [link](https://toreopsahl.com/datasets/) | Network 14 third dataset tnet-format |
| WikiVote | N/A | [link](https://snap.stanford.edu/data/wiki-Vote.html) | Wiki-Vote.txt.gz |
| Standford | N/A | [link](https://snap.stanford.edu/data/web-Stanford.html) | web-Stanford.txt.gz |
| NotreDame | N/A | [link](https://snap.stanford.edu/data/web-NotreDame.html) | web-NotreDame.txt.gz |

You need to place text files in the directory `data`. Follow the steps:

- `gz files`: decompress gz files and extract txt files. (e.g. web-NotreDame.txt from web-NotreDame.txt.gz)
- `tnet`: press `command/ctr` + `s` to download txt files.
- `zip files`: unzip `network.csv.zip` and extract `edges.csv` out.
- Place all text files in `data` directory.
- Rename `Newman-Cond_mat_95-99-co_occurrence.txt` (`NM`) as `test.txt`.

Check the `data` directory:


 * data
    * data/com-friendster.ungraph.txt
    * data/com-orkut.ungraph.txt
    * data/com-lj.ungraph.txt
    * data/com-youtube.ungraph.txt
    * data/com-dblp.ungraph.txt
    * data/com-amazon.ungraph.txt
    * data/edges.csv
    * data/OF_one-mode_weightedmsg_sum.txt
    * data/test.txt
    * data/open-flight.txt
    * data/Wiki-Vote.txt
    * data/web-Stanford.txt
    * data/web-NotreDame.txt



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
./WExp /mnt/data/yichen/data cCoreExact NM
```

`cCoreApp*`:

```sh
./WExp /mnt/data/yichen/data cCoreApp* NM
```

`cCoreG++`:

```sh
./WExp /mnt/data/yichen/data cCoreGpp NM
```

`dalksDecomp`:

```sh
./formatData /mnt/data/yichen/data NM
./Density-Friendly/exactDF 4 1500 /mnt/data/yichen/data/testnet.txt ./Density-Friendly/rates.txt ./Density-Friendly/pavafit.txt ./Density-Friendly/cuts.txt ./Density-Friendly/testExact.txt
```

The generated file `./Density-Friendly/testExact` contains the info about decomposition. Further, you can use `./Density-Friendly/dalksDecomp.py` to report (visualize) the result.


## Full Reproduction

Here, we provide the instruction for reproducing all of results. Note that the most time costly experiment using our novel algorithms may take around 1 day, while baselines may not finish within 3 days.

Components in following cmd are like:

```sh
./executable /path/to/data/dirctory algorithm dataset
```
In the following, we use `/mnt/data/yichen/data` as the path to our `data` directory containing all data. You should replace it with yours.


### Table 4, Table 6, Figure 7, Figure 8, Figure 9

For unweighted graphs: `YT`, `DP`, `AZ`, `LJ`, `FT`, `OK`. Replace `YouTube` (`YT`) in the end of the cmd with other datasets.
```sh

make unWExp
./unWExp /mnt/data/yichen/data cCoreExact YT
./unWExp /mnt/data/yichen/data fastDalkS YT
./unWExp /mnt/data/yichen/data cCoreApp* YT
./unWExp /mnt/data/yichen/data greedypp YT
./unWExp /mnt/data/yichen/data cCoreGpp YT
./unWExp /mnt/data/yichen/data FlowExact YT
./unWExp /mnt/data/yichen/data cCoreApp YT
./unWExp /mnt/data/yichen/data FlowApp YT
./unWExp /mnt/data/yichen/data FlowApp* YT
```

For weighted graphs: `LW`, `YW`, `LB`, `NM`, `OF`, `FF`.

```sh
make WExp
./WExp /mnt/data/yichen/data cCoreExact NM
./WExp /mnt/data/yichen/data fastDalkS NM
./WExp /mnt/data/yichen/data cCoreApp* NM
./WExp /mnt/data/yichen/data greedypp NM
./WExp /mnt/data/yichen/data cCoreGpp NM
./WExp /mnt/data/yichen/data FlowExact NM
./WExp /mnt/data/yichen/data cCoreApp NM
./WExp /mnt/data/yichen/data FlowApp NM
./WExp /mnt/data/yichen/data FlowApp* NM
```


### Figure 6

Replace `./unWExp` and `./WExp` in `Table 4` with `/usr/bin/time -v ./unWExp` and `/usr/bin/time -v ./WExp`.


### Table 5

For weighted graphs: `WV`, `SF`, `ND`.

```sh
make denoExp
./denoExp /mnt/data/yichen/data cCoreExact WV
./denoExp /mnt/data/yichen/data FlowExact WV
```


### Figure 10

First preprocess datasets: `LJ`, `AZ`, `DP`, `NM`.

```sh
make formatData
./formatData /mnt/data/yichen/data NM
```

In your `data` directory, you observe a processed file `data/*net.txt`. For instance, `data/testnet.txt`.

Then we run the decomposition (our DalkS algorithm is based on decomposition) in processed file.

```sh
make exactDF
./Density-Friendly/exactDF 4 1500 /mnt/data/yichen/data/testnet.txt ./Density-Friendly/rates.txt ./Density-Friendly/pavafit.txt ./Density-Friendly/cuts.txt ./Density-Friendly/testExact.txt
```

You will observe the file containing information about decomposition in the form of `./Density-Friendly/*Exact.txt`. Then obtain the proportion of approximation ratio by:

```sh
python3 ./Density-Friendly/dalksDecomp.py
```




