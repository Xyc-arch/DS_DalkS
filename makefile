unWExp:
	g++ -O2 experiment.cpp commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp fastGreedypp.cpp -o unWExp

WExp:
	g++ -O2 experiment2.cpp commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp fastGreedypp.cpp -o WExp

denoExp:
	g++ -O2 experiment3.cpp commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp -o denoExp

fastGreedypp:
	g++ -O2 fastGreedypp.cpp commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp -o fastGreedypp

formatData:
	g++ -O2 formatData.cpp commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp -o formatData

exactDF:
	g++ ./Density-Friendly/exactDF.cpp -fopenmp -fpermissive -o ./Density-Friendly/exactDF -O3


.PHONY: unWExp WExp denoExp fastGreedypp formatData exactDF
