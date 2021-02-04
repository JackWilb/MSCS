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

typedef struct Entry {
    char key[100];
    char value[100];
    int timesAccessed;
} Entry;

Entry lru_cache[16];

// Added function
void _remove_entry(int del_loc) {
    strcpy(lru_cache[del_loc].key, "");
    strcpy(lru_cache[del_loc].value, "");
    lru_cache[del_loc].timesAccessed = 0;
}

char* cache_get(const char* key) {
    // Search for the key and return the value if we find a match
    for (int i = 0; i < 16; i++) {
        if (strcmp(lru_cache[i].key, key) == 0) {
            lru_cache[i].timesAccessed++;

            char* output = (char*)malloc(20);
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
    for (int i = 0; i < 16 && nextPosition < 0; i++) {
        if (strcmp(lru_cache[i].key, "") == 0) {
            nextPosition = i;
        }
    }

    // If no open spot, use least accessed
    if (nextPosition < 0) {
        int minTimesAccessed = 1000000;
        int minTimesAccessedPosition = 0;

        for (int i = 0; i < 16; i++) {
            if (lru_cache[i].timesAccessed < minTimesAccessed) {
                minTimesAccessed = lru_cache[i].timesAccessed;
                minTimesAccessedPosition = i;
            }
        }

        nextPosition = minTimesAccessedPosition;
    }

    strcpy(lru_cache[nextPosition].key, key);
    strcpy(lru_cache[nextPosition].value, value);
    lru_cache[nextPosition].timesAccessed = 0;
}

bool cache_del(const char* key) {
    // Search for the key and delete the key/value if we find a match
    for (int i = 0; i < 16; i++) {
        if (strcmp(lru_cache[i].key, key) == 0) {
            _remove_entry(i);
            return true;
        }
    }

    return false;
}

void cache_clear(void) {
    for (int i = 0; i < 16; i++) {
        _remove_entry(i);
    }
}

