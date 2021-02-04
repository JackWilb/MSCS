/**
 * @author Ryan Stutsman <stutsman@cs.utah.edu>
 * @brief Unit tester for CS5460 Assignment 1.
 * 
 * @copyright Copyright 2021 University of Utah. All rights reserved.
 * 
 * Providers the main test runner for the unit tests defined in tests.c.
 * See usage() and main() for more details on how to run it.
 */

#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <math.h>

#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#include "assignment1.h"
#include "tester.h"

/**
 * fail prints a message using a printf-format string and args and then
 * exits.
 * 
 * This is mainly meant to be used via the FAIL macro which injects the
 * filename and line number FAIL was called on to produce more meaningful
 * error messages on failure.
 * 
 * FAIL is used in tests.c to indicate the test reached an unexpected state.
 */
void fail(const char* file, int line, const char* fmt, ...) {
    va_list args;

    fprintf(stderr, "  !!! %s:%d ", file, line);
    va_start(args, fmt);
    vfprintf(stderr, fmt, args);
    va_end(args);
    fprintf(stderr, "\n-- FAIL\n\n");

    exit(-1);
}

/**
 * Asserts that the cache contains `key` and that `value` is stored under
 * that key. `value` can be NULL, which asserts that the cache does not
 * contain `key`. If the cache doesn't contain the expected value then
 * this function triggers and exit(-1).
 * 
 * This calls cache_get() to probe the cache; if any string is returned by
 * that call, this function handles freeing it.
 * 
 * This is a helper function for tests in test.c that is mainly intended to be
 * used via the CHECK_PAIR macro, which injects the filename and line number
 * CHECK_PAIR was called on to produce more meaningful error messages on
 * failure.
 */
void tester_check_pair(const char* file,
                       int line,
                       const char* key,
                       const char* value)
{
    char* r = cache_get(key);
    if (value == NULL) {
        if (r != NULL) {
            fail(file, line,
                 "cache_get(\"%.64s\") returned \"%.64s\", expected NULL", key, r);
        }
    } else {
        if (r == NULL) {
            fail(file, line,
                 "cache_get(\"%.64s\") returned NULL, expected \"%.64s\"",
                 key, value);
        } else if (strcmp(r, value) != 0) {
            fail(file, line,
                 "cache_get(\"%.64s\") returned \"%s\", expected \"%.64s\"",
                 key, r, value);
        }
        free(r);
    }
}

/// Tracks the number of allocs that have yet to be freed.
ssize_t mallocs = 0;

/** Fail test cases if mallocs/frees are not balanced over the course of the
 * test.
 */
bool use_mc = false;

/// The linker remaps libc malloc to this symbol due to -wrap=malloc.
void* __real_malloc(size_t n);
/// The linker maps calls to malloc() here due to -wrap=malloc.
void* __wrap_malloc(size_t n) {
    void* p = __real_malloc(n);
    if (p && use_mc)
        mallocs++;
    return p;
}

/// The linker remaps libc calloc to this symbol due to -wrap=calloc.
void* __real_calloc(size_t nemb, size_t size);
/// The linker maps calls to calloc() here due to -wrap=calloc.
void* __wrap_calloc(size_t nemb, size_t size) {
    void* p = __real_calloc(nemb, size);
    if (p && use_mc)
        mallocs++;
    return p;
}

/// The linker remaps libc realloc to this symbol due to -wrap=realloc.
void* __real_realloc(void* ptr , size_t size);
/// The linker maps calls to realloc() here due to -wrap=realloc.
void* __wrap_realloc(void* ptr, size_t size) {
    bool was_null = !ptr;
    void* p = __real_realloc(ptr, size);
    if (p && use_mc && was_null)
        mallocs++;
    return p;
}

/// The linker remaps libc free to this symbol due to -wrap=free.
void __real_free(void* p);
/// The linker maps calls to free() here due to -wrap=free.
void __wrap_free(void* p) {
    if (p && use_mc)
        mallocs--;
    __real_free(p);
}

/**
 * For x in `n` times, generate a C string "key-x" and "value-x" and trigger
 * `f` on them. Used to add or check several key-value pairs in the cache
 * quickly.
 */
void tester_for_pairs(int n, void (*f)(const char*, const char*)) {
    char key[16];
    char value[16];
    for (int i = 0; i < n; i++) {
        snprintf(key, 16, "key-%d", i);
        snprintf(value, 16, "value-%d", i);
        f(key, value);
    }
}

/**
 * Fill the cache with `n` key-value pairs of the form
 * ("key-x", "value-x"). Used to quickly mock up cache contents.
 */
void tester_fill_pairs(int n) {
    tester_for_pairs(n, cache_set);
}

/**
 * Run a single test called `testname`.
 * Prints a banner, resets malloc counts, clears the cache, runs the test,
 * clear the cache, and then fails the test if a leak was detected.
 * Otherwise it prints "-- OK". Failed tests don't print OK since they
 * terminate mid-test.
 */
void run_test(void (*test)(void), const char* testname) {
    fprintf(stderr, "== %s\n", testname);

    mallocs = 0;
    cache_clear();
    test();
    cache_clear();

    if (use_mc && mallocs != 0) {
        fprintf(stderr, "!!! LEAKED %zd alloc(s)\n-- FAIL\n\n", mallocs);
        exit(-1);
    } else {
        fprintf(stderr, "-- OK\n\n");
    }
}

/// Break a test if it runs too long Only affects -f runs.
const int timeout_seconds = 100;

/// Signal handler for alarm(). Run when -f is used and a test takes too long.
void fail_test(int _) {
    fprintf(stderr, "!!! TIMEOUT\n-- FAIL\n\n");
    exit(-1);
}

/// Defined in tests.c; the array of tests and testnames to run.
extern struct test tests[];

/**
 * Prints instructions for running tester; run if arguments to main()
 * don't seem to make sense.
 */
void usage(const char* cmd) {
    fprintf(stderr,
            "Usage: %s [-f] [testname]\n"
            "  [-f]      fork before each test. This ensures that tests\n"
            "            complete even if a test crashes or segfault, and it\n"
            "            terminates tests that too long. This flag makes it\n"
            "            harder to use gdb, so don't use it when debugging a\n"
            "            single test.\n"
            "  [-m]      fail tests that seem to have memory leaks (malloc\n"
            "            without free). Some library calls (printf) allocate\n"
            "            and hold on to memory so this can cause false\n"
            "            positives. Only use this if you have removed\n"
            "            debugging print statements, etc, from your code\n"
            "            and tests.\n"
            " [testname] By default, the harness runs all tests. A single\n"
            "            test can be run by passing the test name e.g.\n"
            "            test_initially_empty.\n\n", cmd);
    exit(-1);
}

/**
 * Run tester and print out fraction of tests that passed.
 * See usage() for details on arguments.
 */
int main(int argc, char* argv[]) {
    const char* cmd = argv[0];

    bool use_fork = false;
    const char* testname = NULL;

    while (argc > 1 && argv[1][0] == '-') {
        if (strcmp(argv[1], "-f") == 0)
            use_fork = true;
        else if (strcmp(argv[1], "-m") == 0)
            use_mc = true;
        else
            break;
        argc--;
        argv++;
    }

    if (argc > 1)
        testname = argv[1];

    int ok = 0;
    int total = 0;

    for (int i = 0; tests[i].f != NULL; i++) {
        struct test* test = &tests[i];

        // Skip if a specific testname was specified.
        if (testname && strcmp(testname, test->name) != 0)
            continue;

        if (!use_fork) {
            run_test(test->f, test->name);
            ok++;
            total++;
            continue;
        }

        int pid = fork();
        assert(pid != -1);

        if (pid == 0) {
            signal(SIGALRM, fail_test);
            alarm(timeout_seconds);
            run_test(test->f, test->name);
            exit(0);
        } else {
            int status = 0;
            wait(&status);
            if (status == 0)
                ok++;
            total++;
        }
    }

    // No tests matched the given name.
    if (total == 0)
        usage(cmd);

    fprintf(stderr, "\n>> SCORE %d/%d %.0f%%\n\n", ok, total,
            round(((double)ok)/total * 100));

    return 0;
}
