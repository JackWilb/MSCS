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
#include <stdio.h>

#include "assignment1.h"

#define CACHE_SIZE 16

typedef struct Entry {
    char *key;
    char *value;
} Entry;

Entry lru_cache[CACHE_SIZE];

// Added handler for removing an entry
void _remove_entry(int del_loc) {
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

char* cache_get(const char* key) {
    // Search for the key and return the value if we find a match
    for (int i = 0; i < CACHE_SIZE; i++) {
        if (lru_cache[i].key && strcmp(lru_cache[i].key, key) == 0) {
            char* output = (char*)malloc(strlen(lru_cache[i].value) * sizeof(char));
            strcpy(output, lru_cache[i].value);

            return output;
        }
    }

    // Else return null
    return NULL;
}

void cache_set(const char* key, const char* value) {
    int nextPosition = -1;

    // Check for open spot
    for (int i = 0; i < CACHE_SIZE && nextPosition < 0; i++) {
        if (!lru_cache[i].key) {
            nextPosition = i;
        }
    }

    // If no open spot, use least accessed
    if (nextPosition < 0) {
        // clock_t leastRecentAccess = clock();
        // int leastRecentAccessPosition = 0;

        // for (int i = 0; i < CACHE_SIZE; i++) {
        //     printf("timediff %ld\n",timespec_get(NULL));
        //     if (lru_cache[i].timeAccessed && (leastRecentAccess - lru_cache[i].timeAccessed) < 0) {
        //         leastRecentAccess = lru_cache[i].timeAccessed;
        //         leastRecentAccessPosition = i;
        //     }
        // }

        // nextPosition = leastRecentAccessPosition;
        // printf("no empty, next pos to remove: %d\n", nextPosition);
    }


    _remove_entry(nextPosition);

    lru_cache[nextPosition].key = malloc(strlen(key) * sizeof(char));
    lru_cache[nextPosition].value = malloc(strlen(value) * sizeof(char));

    strcpy(lru_cache[nextPosition].key, key);
    strcpy(lru_cache[nextPosition].value, value);
}

bool cache_del(const char* key) {
    // Search for the key and delete the key/value if we find a match
    for (int i = 0; i < CACHE_SIZE; i++) {
        if (lru_cache[i].key && strcmp(lru_cache[i].key, key) == 0) {
            _remove_entry(i);
            return true;
        }
    }

    return false;
}

void cache_clear(void) {
    for (int i = 0; i < CACHE_SIZE; i++) {
        _remove_entry(i);
    }
}
