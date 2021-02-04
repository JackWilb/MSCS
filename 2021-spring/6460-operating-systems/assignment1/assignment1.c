/**
 * Write your solutions here and turn in just this file.
 * Please keep in mind that your solution must compile and work with the basic
 * tester and tests. Feel free to extend them, but we will have our
 * own edits to them and your assignment1.c needs to work correctly with the
 * original tests/tester.
 */
#define _POSIX_C_SOURCE 200809L // for strdup; it won't be part of C until 2023.
#include <string.h>
#include <stdlib.h>

#include "assignment1.h"

#define CACHE_SIZE 16

typedef struct Entry {
    char *key;
    char *value;
} Entry;

static Entry lru_cache[CACHE_SIZE];
static int priority[CACHE_SIZE] = { 0 };

// Added handler for removing an entry
static void _remove_entry(int del_loc) {
    // Check if the key exists and delete it if it does, otherwise do nothing
    if (lru_cache[del_loc].key) {
        free(lru_cache[del_loc].key);
        lru_cache[del_loc].key = NULL;
    }

    // Check if the key exists and delete it if it does, otherwise do nothing
    if (lru_cache[del_loc].value) {
        free(lru_cache[del_loc].value);
        lru_cache[del_loc].value = NULL;
    }
}

// Move highest_priority to the front of the priority array
static void _update_priority(int highest_priority) {
    // If the new high priority index is in the array, remove (set to -1)
    for (int i = 0; i < CACHE_SIZE; i++) {
        if (priority[i] == highest_priority) {
            priority[i] = -1;
            break;
        }
    }

    // Move values right unless the value is -1
    for (int i = CACHE_SIZE - 2; i >= 0; i--) {
        if (priority[i] != -1) {
            priority[i + 1] = priority[i];
        }

    }

    // Set the first value as the high priority index
    priority[0] = highest_priority;
}

static int _find_entry(const char* key) {
    for (int i = 0; i < CACHE_SIZE; i++) {
        if (lru_cache[i].key && strcmp(lru_cache[i].key, key) == 0){
            return i;
        }
    }

    return -1;
}

char* cache_get(const char* key) {
    // Search for the key and return the value if we find a match
    int location = _find_entry(key);

    if (location >= 0) {
        char* output = (char*)malloc(strlen(lru_cache[location].value) * sizeof(char));
        strcpy(output, lru_cache[location].value);

        _update_priority(location);
        return output;
    }

    // Else return null
    return NULL;
}

void cache_set(const char* key, const char* value) {
    int nextPosition = -1;

    // See if the key is already there
    nextPosition = _find_entry(key);

    // If key is not there, check for open spot
    if (nextPosition < 0) {
        for (int i = 0; i < CACHE_SIZE && nextPosition < 0; i++) {
            if (!lru_cache[i].key) {
                nextPosition = i;
            }
        }
    }

    // If no open spot, use least accessed (back of array)
    if (nextPosition < 0) {
        nextPosition = priority[CACHE_SIZE - 1];
    }

    // Free memory if necessary
    _remove_entry(nextPosition);

    // Allocate memory for the new values coming in
    lru_cache[nextPosition].key = malloc(strlen(key) * sizeof(char));
    lru_cache[nextPosition].value = malloc(strlen(value) * sizeof(char));

    // Set the key, value
    strcpy(lru_cache[nextPosition].key, key);
    strcpy(lru_cache[nextPosition].value, value);

    _update_priority(nextPosition);
}

bool cache_del(const char* key) {
    // Search for the key and delete the key/value if we find a match
    int location = _find_entry(key);
    if (location >= 0) {
        _remove_entry(location);
        return true;
    }

    return false;
}

void cache_clear(void) {
    for (int i = 0; i < CACHE_SIZE; i++) {
        _remove_entry(i);
    }
}
