#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <fstream>
#include <cstring>
#include <sstream>
#include <bits/stdc++.h>
#include <math.h>
#include "experiment.h"
#include "experiment2.h"
#include "experiment3.h"
#include "heap.h"
#include "dinic.h"
using namespace std;




int fasterGreedypp(int V, int vertexNum, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[]){
    clock_t start, finish;
    double duration;
    int T = 1000;
    int cp=1;
    int heapSize=vertexNum;
    int optSize = vertexNum;
    float originTotalW = totalW;
    float optDen = totalW/heapSize;
    long double * l = new long double [V+1]{0};
    int* heapPos = new int[V+1]{0};
    int* originIndicateG = new int[V+1]{0};
    for (int i=1; i<=V; i++){
        originIndicateG[i] = indicateGraph[i];
    }
    pair <float, int>* heap = new pair <float, int>[heapSize+1];

    float tempS;
    float dmax = 0;
    float maxS=0;
    float densityMax = totalW/vertexNum;


    start = clock();

    for (int i=1; i<=V; i++) {
        if (indicateGraph[i] > 0){
            heap[cp] = make_pair(strength[i], i);
            heapPos[i] = cp;
            cp += 1;
        }
    }

    for (int i=heapSize/2; i>=1; i--){
        minHeapify(i, heap, heapSize, heapPos);
    }


    while (heapSize > 1){
        tempS = heapExtractMin(heap, heapSize, heapPos, adj, indicateGraph);
        totalW -= tempS;
        if (tempS > dmax) dmax = tempS;
        if (densityMax < totalW/heapSize) {
            densityMax = totalW/heapSize;
        }
    }


    float thres;
    if (densityMax < 0.5*dmax){
        thres = 0.5*dmax;
    } else {
        thres = densityMax;
    }



    delete [] heap;
    delete [] heapPos;
    heapPos = new int[V+1]{0};
    heapSize = vertexNum;
    heap = new pair <float, int>[heapSize+1];
    for (int i=0; i<=V; i++){
        indicateGraph[i] = originIndicateG[i];
    }
    cp = 1;
    for (int i=1; i<=V; i++) {
        if (indicateGraph[i] > 0){
            heap[cp] = make_pair(strength[i], i);
            heapPos[i] = cp;
            cp += 1;
        }
    }

    for (int i=heapSize/2; i>=1; i--){
        minHeapify(i, heap, heapSize, heapPos);
    }

    while (heap[1].first < thres){
        heapExtractMin(heap, heapSize, heapPos, adj, indicateGraph);
    }

//    cout << "Heap size " << heapSize << endl;
//    cout << "threshold " << thres << endl;
//    cout << "max strength " << maxS << endl;

    for (int i=0; i<=V; i++){
        strength[i] = vertexS[i];
    }

    float sum;
    originTotalW = 0;
    vector<pair<int, float>> tp1;
    for (int i=1; i<=heapSize; i++){
        sum = 0;
        tp1 = adj[heap[i].second];
        for (int j=0; j<int(tp1.size()); j++){
            if (indicateGraph[tp1[j].first] > 0){
                sum += tp1[j].second;
                if (heap[i].second < tp1[j].first) {
                    originTotalW += tp1[j].second; // loc
                }
            }
        }
        strength[heap[i].second] += sum;
    }


    vertexNum = 0;
    for (int i=1; i<=V; i++){
        originIndicateG[i] = indicateGraph[i];
        if (indicateGraph[i] > 0) vertexNum ++;
    } // loc
    cout << "remain #" << vertexNum << endl;
    cout << "remain weight " << originTotalW << endl;


    // iteration begins
    for (int t=1; t<=T; t++){
        cout << "iter " << t << endl;
        totalW = originTotalW;
        heapSize = vertexNum;
        optDen = totalW/heapSize;
        cp = 1;
        for (int i=1; i<=V; i++){
            indicateGraph[i] = originIndicateG[i];
        }

        for (int i=1; i<=V; i++) {
            if (indicateGraph[i] > 0){
                heap[cp] = make_pair(strength[i]+l[i], i);
                heapPos[i] = cp;
                cp += 1;
            }
        }

        for (int i=heapSize/2; i>=1; i--){
            minHeapify(i, heap, heapSize, heapPos);
        }


        float tempS;
        while (heapSize > 1){
            tempS = heapExtractMinl(heap, heapSize, heapPos, adj, indicateGraph, l);
            totalW -= tempS;
            if (optDen < totalW/heapSize) {
                optDen = totalW/heapSize;
                optSize = heapSize;
            }
        }
    }

    finish = clock();
    duration = (double)(finish - start) / CLOCKS_PER_SEC;
    cout << "Density: " << optDen << endl;
    cout << "Time of greedy++: " << duration << endl;


    return 0;
}





int fastUnweighted(string path, string dataset){

    string file;
    int startLine;
    int lineNum;
    int V;
    bool fromZero;

    // live journal parameter set
    if (dataset == "LJ") {
        file = path + "/com-lj.ungraph.txt";
        startLine = 5;
        lineNum = 34681193;
        V=4036538;
        fromZero = true;
    }

     // friendster parameter set
    if (dataset == "FT") {
        file = path + "/com-friendster.ungraph.txt";
        startLine = 5;
        lineNum = 1806067139;
        V=124836179;
        fromZero = false;
    }


    // orkut parameter set
    if (dataset == "OK") {
        file = path + "/com-orkut.ungraph.txt";
        startLine = 5;
        V = 3072626;
        lineNum = 117185087;
        fromZero = false;
    }


    // com-YouTube parameter set
    if (dataset == "YT") {
        file = path + "/com-youtube.ungraph.txt";
        startLine = 5;
        V = 1157827;
        lineNum = 2987628;
        fromZero = false;
    }


    // com-dblp parameter set
    if (dataset == "DP") {
        file = path + "/com-dblp.ungraph.txt";
        startLine = 5;
        lineNum = 1049866;
        V = 425957;
        fromZero = true;
    }


    // com-Amazon
    if (dataset == "AZ") {
        file = path + "/com-amazon.ungraph.txt";
        startLine = 5;
        lineNum = 925876;
        V=548551;
        fromZero = false;
    }



    int edgeNum;
    int vertexNum = 0;
    long double totalW = 0;
    int* indicateGraph = new int[V+1]{0};
    float* strength = new float[V+1]{0};
    float* vertexS = new float[V+1]{0};
    vector <pair <int, float>>* adj = new vector <pair <int, float>> [V+1];


    readtxtGraph(file, "	", fromZero, vertexNum, edgeNum, startLine, lineNum, totalW, indicateGraph, strength, vertexS, adj);


    fasterGreedypp(V, vertexNum, totalW, indicateGraph, strength, vertexS, adj);

    return 0;
}





// int main(int argc, char *argv[]){

//     // 1: path; 2: dataset

//     stringstream ss;
//     string path;
//     string mode;
//     string dataset;

//     ss << argv[1];
//     ss >> path;

//     ss.clear();
//     ss.str("");

//     ss << argv[2];
//     ss >> dataset;


//     fastUnweighted(path, dataset);
//     return 0;
// }





