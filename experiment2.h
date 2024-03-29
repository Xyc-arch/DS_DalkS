#ifndef EXPERIMENT2_H
#define EXPERIMENT2_H

#endif // EXPERIMENT2_H


#include <stdlib.h>
#include <time.h>
#include <fstream>
#include <cstring>
#include <sstream>
//#include <bits/stdc++.h>

using namespace std;

void readWeightGraph(string name, string split, bool fromZero, int& vertexNum, long & edgeNum, int startLine, int lineNum, long double & totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[]);

void readtxtGraph(string name, string split, bool fromZero, int& vertexNum, long& edgeNum, int startLine, int lineNum, long double & totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[]);

// heap-related function in DALKS.cpp
void printAdjacent(int id, vector <pair <int, int>> adj[]);

void printGraph(vector<pair<int,float> > adj[], int V);

void printStrength(float strength[], int V);

void minHeapify(int pos, pair <float, int> heap[], int heapSize, int heapPos[]);

void minHeapify(int pos, pair <float, int> heap[], int heapSize);

void heapDecreaseKey(pair <float, int> heap[], int heapPos[], int id, float value);

int heapExtractMin(pair <float, int> heap[], int &heapSize, int heapPos[], vector <pair <int, float>> adj[], int indicateGraph[]);

void maxHeapify(int pos, pair <float, int> heap[], int heapSize);

pair <int, int> heapExtractMax(pair <float, int> heap[], int &heapSize);


// max flow function in berkley.cpp
float BerkleyFlow(double l, double u, float eps, int V, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[]);

float BerkleyFlowAcc(double l, double u, float eps, int V, int & heapSize, int heapPos[], int indicateGraph[], float strength[], float vertexS[], pair <float, int> heap[], vector <pair <int, float>> adj[]);


// max flow approximation function in soda22.cpp
float soda22FlowApp(float l, float u, float eps, int V, int edgeNum, int indicateGraph[], float vertexS[], vector <pair <int, float>> adj[]);

float soda22FlowAcc(float l, float u, float eps, int V, int edgeNum, int & heapSize, int heapPos[], int indicateGraph[], float vertexS[], float strength[], pair <float, int> heap[], vector <pair <int, float>> adj[]);

// orginial max flow function in soda22.cpp
float soda22FlowOrigin(float l, float u, float eps, int V, int edgeNum, int indicateGraph[], float vertexS[], vector <pair <int, float>> adj[]);

float soda22FlowOriginAcc(float l, float u, float eps, int V, int edgeNum, int & heapSize, int heapPos[], int indicateGraph[], float vertexS[], float strength[], pair <float, int> heap[], vector <pair <int, float>> adj[]);


//greedy++
int fasterGreedypp(int V, int vertexNum, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[], double eps);

int heapExtractMinl(pair <float, int> heap[], int &heapSize, int heapPos[], vector <pair <int, float>> adj[], int indicateGraph[], long double l[]);

// from unweighted experiment
pair<double, double> DALKSexp(int V, int vertexNum, int k, int j, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[]);

float berkleyexp1(int V, int vertexNum, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[]);

float berkleyexp2(int V, int vertexNum, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[], long edgeNum);

float berkleyexp3(int V, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[]);

float greedyPPexp(int V, int vertexNum, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[], double eps);

float soda22exp1(int V, int vertexNum, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[], double eps);

float soda22exp2(int V, int vertexNum, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[], double eps);

float soda22exp3(int V, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[], double eps);

float soda22exp4(int V, long double totalW, int indicateGraph[], float strength[], float vertexS[], vector <pair <int, float>> adj[], double eps);

// maintain

void copyGraph(int* graphSrc, int* graphDst, int V);

void updateC(int V, int* C, float hatRho, vector <pair <int, float>> adj[]);

float cCoreUpdateIns(int V, int vertexNum, float& hatRhoPlus, long double totalW, int indicateGraph[], int* tildeS, int* C, float strength[], float vertexS[], vector <pair <int, float>> adj[]);

int graphSize(int* graph, int V);