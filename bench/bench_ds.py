# benchmarks for ds endpoints
# run with command: python -m bench.bench_ds

from timeit import Timer
from src.mastercolormixer.ds import DynamicArray, Stack, RingBufferQueue, HashSet

# input sizes
SIZES = [1_000, 10_000, 100_000]

# when it comes to timing performance, I'm used to stopwatch in C#
#    var sw = Stopwatch.StartNew();
#    DoAppends();
#    sw.Stop();

# for this week's task, I've made simple tests like shown in the text
# https://runestone.academy/ns/books/published/pythonds/AlgorithmAnalysis/Lists.html

# --- DynamicArray benchmarks ----
def da_append_test(n):
    theDA = DynamicArray[int]()
    for i in range(n):
        theDA.append(i)

def da_pop_test(n):
    theDA = DynamicArray[int]()
    for i in range(n):
        theDA.append(i)
    for _ in range(n):
        theDA.pop()

# --- Stack benchmarks ----


# --- Queue benchmarks ----


# --- HashSet benchmarks ----
