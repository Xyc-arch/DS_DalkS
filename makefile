CXX=g++
CXXFLAGS=-O2 -std=c++11
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


