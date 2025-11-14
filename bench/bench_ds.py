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
    da = DynamicArray[int]()
    for i in range(n):
        da.append(i)

def da_pop_test(n):
    da = DynamicArray[int]()
    for i in range(n):
        da.append(i)
    for _ in range(n):
        da.pop()

# --- Stack benchmarks ----


# --- Queue benchmarks ----


# --- HashSet benchmarks ----

# --- Main ---
def run_benchmarks():

    print("DynamicArray")
    for n in SIZES:
        t_append = Timer(f"da_append_test({n})",
                         "from __main__ import da_append_test").timeit(number=1) # only need timeit to run once
        t_pop = Timer(f"da_pop_test({n})",
                      "from __main__ import da_pop_test").timeit(number=1)

        print("n =", n)
        print("  append time:", t_append, "seconds")
        print("  pop time:   ", t_pop, "seconds")
        print()
