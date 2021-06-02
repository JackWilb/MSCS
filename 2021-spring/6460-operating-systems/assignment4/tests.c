// A few basic tests for the cas_lock, ticket_lock, and list.
// Extend this code in whatever way you see fit to make sure
// your implementations work correctly.

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdatomic.h>
#include <unistd.h>
#include <pthread.h>

#include "assignment4.h"

// You can adjust this if you like. Keep in mind, that if you run with too many
// threads (>8 or so) the spinlocks will start to perform very poorly since
// sometimes the lock holding thread will get scheduled out.
const size_t nthreads = 4;
atomic_bool done;

cas_lock_t cas_lock;
ticket_lock_t ticket_lock;
list_t list;

int cas_counter = 0;
int ticket_counter = 0;

atomic_int iterations;

// A simple test that runs increments and list inserts in a few threads.
// If your locks provide mutual exclusion the counts should match
// at the end. Each item inserted into the list should also be
// found on future accesses.
void* thread_main(void* _) {
  const bool test_cas = true;
  const bool test_ticket = true;
  const bool test_list = true;

  while (!atomic_load(&done)) {
    if (test_cas) {
      cas_lock_acquire(&cas_lock);
      cas_counter++;
      cas_lock_release(&cas_lock);
    }

    if (test_ticket) {
      ticket_lock_acquire(&ticket_lock);
      ticket_counter++;
      ticket_lock_release(&ticket_lock);
    }

    int next = atomic_fetch_add(&iterations, 1);
    if (test_list) {
      list_insert(&list, next);
      bool found = list_find(&list, next);
      // Consider it a failure if the list element we just put into the list
      // doesn't seem to be there.
      if (!found) {
        fprintf(stderr, "list element missing %d\n", next);
        exit(-1);
      }
    }
  }

  return NULL;
}

int main(int argc, char* argv[]) {
  cas_lock_init(&cas_lock);
  ticket_lock_init(&ticket_lock);
  list_init(&list);

  atomic_store(&done, false);
  pthread_t threads[nthreads];
  // Start up several threads all running the same test loop code.
  for (size_t i = 0; i < nthreads; i++) {
    int r = pthread_create(&threads[i], NULL, thread_main, NULL);
    if (r < 0) {
      perror("pthread_create failed");
      exit(-1);
    }
  }

  sleep(1); // Let the threads run for a little bit.
  atomic_store(&done, true); // Then tell them all to quit.
 
  // Wait for all of the threads to exit and record their results.
  for (size_t i = 0; i < nthreads; i++) {
    int r = pthread_join(threads[i], NULL);
    if (r < 0) {
      perror("pthread_create failed");
      exit(-1);
    }
  }

  int i = atomic_load(&iterations);
  int c = atomic_load(&cas_counter);
  int t = atomic_load(&ticket_counter);
  printf("iterations: %d\n\n", i);

  printf("cas_counter: %d\n", c);
  if (i == c)
    printf("  cas_lock OK counts match\n\n");
  else
    printf("  cas_lock FAIL counts do not match\n\n");

  printf("ticket_counter: %d\n", t);
  if (i == t)
    printf("  ticket_lock OK counts match\n\n");
  else
    printf("  ticket_lock FAIL counts do not match\n\n");

  return 0;
}
