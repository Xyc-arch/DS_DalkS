#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <fstream>
#include <cstring>
#include <sstream>
#include <vector>
#include <utility>
//#include <bits/stdc++.h>
#include <math.h>
#include "experiment.h"
#include "dinic.h"







int unWeightexp(string path, string mode, string dataset, double eps){

    string file;
    int startLine;
    int lineNum;
    int V;
    bool fromZero;

//    int vertexNum = 0;
//    long double totalW = 0;
//    int* indicateGraph = new int[V+1]{0};
//    float* strength = new float[4036538]{0};
//    float* vertexS = new float[4036538]{0};
//    vector <pair <int, float>>* adj = new vector <pair <int, float>> [V+1];
//    readtxtGraph(file, "	", vertexNum, startLine, lineNum, totalW, indicateGraph, strength, vertexS, adj);
//    DALKSexp(V, vertexNum, 500, 8, totalW, indicateGraph, strength, vertexS, adj);
//    berkleyexp(V, vertexNum, totalW, indicateGraph, strength, vertexS, adj);
//    soda22exp(V, vertexNum, totalW, indicateGraph, strength, vertexS, adj);

    // live journal parameter set
    if (dataset == "LJ") {
        file = path + "/LJ.txt";
        startLine = 5;
        lineNum = 34681193;
        V=4036538;
        fromZero = true;
    }

     // friendster parameter set
    if (dataset == "FT") {
        file = path + "/FT.txt";
        startLine = 5;
        lineNum = 1806067139;
        V=124836179;
        fromZero = false;
    }


    // orkut parameter set
    if (dataset == "OK") {
        file = path + "/OK.txt";
        startLine = 5;
        V = 3072626;
        lineNum = 117185087;
        fromZero = false;
    }


    // com-YouTube parameter set
    if (dataset == "YT") {
        file = path + "/YT.txt";
        startLine = 5;
        V = 1157827;
        lineNum = 2987628;
        fromZero = false;
    }


    // com-dblp parameter set
    if (dataset == "DP") {
        file = path + "/DP.txt";
        startLine = 5;
        lineNum = 1049866;
        V = 425957;
        fromZero = true;
    }


    // com-Amazon
    if (dataset == "AZ") {
        file = path + "/AZ.txt";
        startLine = 5;
        lineNum = 925876;
        V=548551;
        fromZero = false;
    }


    // program execution
    int edgeNum;
    int vertexNum = 0;
    long double totalW = 0;
    int* indicateGraph = new int[V+1]{0};
    float* strength = new float[V+1]{0};
    float* vertexS = new float[V+1]{0};
    vector <pair <int, float>>* adj = new vector <pair <int, float>> [V+1];


    readtxtGraph(file, "	", fromZero, vertexNum, edgeNum, startLine, lineNum, totalW, indicateGraph, strength, vertexS, adj);

    if (mode == "fastDalkS") DALKSexp(V, vertexNum, 11578, 8, totalW, indicateGraph, strength, vertexS, adj);
    if (mode == "cCoreExact") berkleyexp2(V, vertexNum, totalW, indicateGraph, strength, vertexS, adj, edgeNum);
    if (mode == "FlowExact") berkleyexp3(V, indicateGraph, strength, vertexS, adj);
    if (mode == "cCoreApp*") soda22exp2(V, vertexNum, totalW, indicateGraph, strength, vertexS, adj, eps);
    if (mode == "cCoreApp") soda22exp1(V, vertexNum, totalW, indicateGraph, strength, vertexS, adj, eps);
    if (mode == "FlowApp*") soda22exp3(V, totalW, indicateGraph, strength, vertexS, adj, eps);
    if (mode == "FlowApp") soda22exp4(V, totalW, indicateGraph, strength, vertexS, adj, eps);
    if (mode == "Greedypp") greedyPPexp(V, vertexNum, totalW, indicateGraph, strength, vertexS, adj, eps);
    if (mode == "cCoreGpp") fasterGreedypp(V, vertexNum, totalW, indicateGraph, strength, vertexS, adj, eps);


//    greedyPPexp(V, vertexNum, totalW, indicateGraph, strength, vertexS, adj);


    //program execution for weighted graph



    return 0;
}


int main(int argc, char *argv[]){

    // 1: path; 2: mode; 3: dataset

    stringstream ss;
    string path;
    string mode;
    string dataset;
    double eps=0.001;

    ss << argv[1];
    ss >> path;

    ss.clear();
    ss.str("");

    ss << argv[2];
    ss >> mode;

    ss.clear();
    ss.str("");

    ss << argv[3];
    ss >> dataset;

    if (argc == 5) {
        ss.clear();
        ss.str("");
        ss << argv[4];
        ss >> eps;
    }

    // cout << path << endl;
    // cout << mode << endl;
    // cout << dataset << endl;


    unWeightexp(path, mode, dataset, eps);
    return 0;
}





