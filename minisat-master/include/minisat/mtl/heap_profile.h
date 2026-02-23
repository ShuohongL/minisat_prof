// heap_profile.h  — use this exact content (C++17 required)

#pragma once
#include <cstdint>
#include <atomic>
#include <cstdio>

#ifdef HEAP_PROFILE

// Serialized rdtsc read (cpuid + rdtsc)
static inline uint64_t rdtsc_serialized() {
    unsigned int hi, lo;
    asm volatile("cpuid\n\t" ::: "rax","rbx","rcx","rdx"); // serialize
    asm volatile("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

// Use inline variables so there is exactly one instance across all TUs (C++17).
inline std::atomic<uint64_t> heap_insert_cycles{0};
inline std::atomic<uint64_t> heap_decrease_cycles{0};
inline std::atomic<uint64_t> heap_remove_cycles{0};

inline std::atomic<uint64_t> heap_insert_calls{0};
inline std::atomic<uint64_t> heap_decrease_calls{0};
inline std::atomic<uint64_t> heap_remove_calls{0};

// Call at program end to print results
struct HeapProfilePrinter {
    ~HeapProfilePrinter() {
        uint64_t ins_cycles = heap_insert_cycles.load();
        uint64_t dec_cycles = heap_decrease_cycles.load();
        uint64_t rm_cycles  = heap_remove_cycles.load();

        uint64_t ins_calls = heap_insert_calls.load();
        uint64_t dec_calls = heap_decrease_calls.load();
        uint64_t rm_calls  = heap_remove_calls.load();

        printf("=== Heap profiling summary ===\n");
        if (ins_calls)
            printf("insert: calls=%llu total_cycles=%llu avg_cycles=%.2f\n",
                (unsigned long long)ins_calls,
                (unsigned long long)ins_cycles,
                (double)ins_cycles / ins_calls);
        else
            printf("insert: calls=0\n");

        if (dec_calls)
            printf("decrease: calls=%llu total_cycles=%llu avg_cycles=%.2f\n",
                (unsigned long long)dec_calls,
                (unsigned long long)dec_cycles,
                (double)dec_cycles / dec_calls);
        else
            printf("decrease: calls=0\n");

        if (rm_calls)
            printf("removeMin: calls=%llu total_cycles=%llu avg_cycles=%.2f\n",
                (unsigned long long)rm_calls,
                (unsigned long long)rm_cycles,
                (double)rm_cycles / rm_calls);
        else
            printf("removeMin: calls=0\n");

        printf("================================\n");
    }
};

// single global printer instance
inline HeapProfilePrinter _heapProfilePrinter;

#endif // HEAP_PROFILE
