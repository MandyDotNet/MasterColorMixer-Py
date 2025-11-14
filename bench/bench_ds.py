# benchmarks for ds endpoints
# run with command: python -m bench.bench_ds

from timeit import Timer
from src.master_color_mixer.ds import DynamicArray, Stack, RingBufferQueue, HashSet

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
def stack_push_test(n):
    s = Stack[int]()
    for i in range(n):
        s.push(i)

def stack_pop_test(n):
    s = Stack[int]()
    for i in range(n):
        s.push(i)
    for _ in range(n):
        s.pop()

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

        print("\n=== Stack ===")
    for n in SIZES:
        t_push = Timer(f"stack_push_test({n})",
                       "from __main__ import stack_push_test").timeit(number=1)
        t_pop = Timer(f"stack_pop_test({n})",
                      "from __main__ import stack_pop_test").timeit(number=1)
        print(f"n={n:6d} | push:   {t_push:.6f}s | pop: {t_pop:.6f}s")



if __name__ == "__main__":
    run_benchmarks()