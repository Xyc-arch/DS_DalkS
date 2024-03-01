#unWExp:
#	g++ -O2 experiment.cpp commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp fastGreedypp.cpp -o unWExp
#
#WExp:
#	g++ -O2 experiment2.cpp commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp fastGreedypp.cpp -o WExp
#
#denoExp:
#	g++ -O2 experiment3.cpp commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp -o denoExp
#
#formatData:
#	g++ -O2 formatData.cpp commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp -o formatData
#
#exactDF:
#	g++ ./Density-Friendly/exactDF.cpp -fopenmp -fpermissive -o ./Density-Friendly/exactDF -O3
#
#all:
#	make unWExp
#	make WExp
#	make denoExp
#	make formatData
#	make exactDF
#
#clear:
#	rm -f unWExp WExp denoExp formatData exactDF
#
#.PHONY: unWExp WExp denoExp formatData exactDF

#CXX=g++
#CXXFLAGS=-O2
#LDFLAGS=
#COMMON_OBJS=commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp fastGreedypp.cpp
#EXECS=unWExp WExp denoExp formatData exactDF
#
#all: $(EXECS)
#
#unWExp: experiment.cpp $(COMMON_OBJS)
#
#	$(CXX) $(CXXFLAGS) $^ -o $@
#
#WExp: experiment2.cpp $(COMMON_OBJS)
#	$(CXX) $(CXXFLAGS) $^ -o $@
#
#denoExp: experiment3.cpp $(COMMON_OBJS)
#	$(CXX) $(CXXFLAGS) $^ -o $@
#
#formatData: formatData.cpp $(COMMON_OBJS)
#	$(CXX) $(CXXFLAGS) $^ -o $@
#
#exactDF: Density-Friendly/exactDF.cpp
#	$(CXX) $(CXXFLAGS) -fopenmp -fpermissive $^ -o ./Density-Friendly/exactDF
#
#clear:
#	rm -f $(EXECS) *.o ./Density-Friendly/*.o
#
#.PHONY: all clear $(EXECS)

CXX=g++
CXXFLAGS=-O2
OBJDIR := obj
COMMON_SRCS := commonExp.cpp berkley.cpp DALKS.cpp dinic.cpp soda22.cpp fastGreedypp.cpp
COMMON_OBJS := $(COMMON_SRCS:%.cpp=$(OBJDIR)/%.o)
EXECS := unWExp WExp denoExp formatData

all: $(EXECS)

$(OBJDIR)/%.o: %.cpp
	@mkdir -p $(OBJDIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

unWExp: $(OBJDIR)/experiment.o $(COMMON_OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

WExp: $(OBJDIR)/experiment2.o $(COMMON_OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

denoExp: $(OBJDIR)/experiment3.o $(COMMON_OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

formatData: $(OBJDIR)/formatData.o $(COMMON_OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

clear:
	rm -rf $(OBJDIR) $(EXECS)

.PHONY: all clear $(EXECS)


