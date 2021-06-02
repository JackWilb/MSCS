// DO NOT MODIFY THIS FILE.
//
// Forward declarations for the declarations below.
// You should define these functions however you like in assignment4.c.
// But leave these here so that code that includes assignment4.h
// can compile and link against the functions in assignment4.c

#ifndef ASSIGNMENT4_H
#define ASSIGNMENT4_H

#include <stdatomic.h>
#include <stdbool.h>

typedef struct cas_lock {
  atomic_bool locked;
} cas_lock_t;

void cas_lock_init(cas_lock_t* lock);
void cas_lock_acquire(cas_lock_t* lock);
void cas_lock_release(cas_lock_t* lock);

typedef struct ticket_lock {
  atomic_int turn;
  atomic_int ticket;
} ticket_lock_t;

void ticket_lock_init(ticket_lock_t* lock);
void ticket_lock_acquire(ticket_lock_t* lock);
void ticket_lock_release(ticket_lock_t* lock);

typedef struct node {
  int key;
  struct node* next;
} node_t;

typedef struct list {
  node_t* head;
  cas_lock_t lock;
} list_t;

void list_init(list_t* head);
void list_insert(list_t* head, int key);
bool list_find(list_t* head, int key);

#endif
