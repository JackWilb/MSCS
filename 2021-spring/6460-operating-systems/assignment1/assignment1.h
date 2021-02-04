#ifndef ASSIGNMENT1_H
#define ASSIGNMENT1_H

#include <stdbool.h>

/**
 * cache_set stores a copy of the C string pointed to by `value` in the cache
 * associated with the C string pointed to by `key`. If `key` matches a key
 * already stored in the cache (via strcmp), then the value associated with it
 * in the cache then a copy of the C string pointed to by `value` replaces the
 * current value in the cache for that key.
 * 
 * The cache holds up to 16 key-value pairs at a time. If the cache is
 * full, then the key-value pair that was least recently accessed (via
 * cache_get()) or updated (via cache_set()) is evicted from the cache before
 * the new key-value pair is inserted into the cache.
 * 
 * All memory allocated during cache_set calls is freed when the corresponding
 * key-value pair is deleted (via cache_del() or cache_clear()) or evicted.
 * 
 * @param key Must be a non-NULL pointer to a nul-terminated C string that is
 *  to be associated to the stored value. Note: this function makes its
 *  own copy of this C string that it stores internally; the caller
 *  retains ownership for the C string `key` refers to and can use it, modify
 *  it, or free it as it sees fit.
 * 
 * @param value Must be a non-NULL pointer to a nul-terminated C string that is
 *  to be stored in the cache associated with the above key. Note: this function
 *  makes its own copy of this C string that it stores internally; the caller
 *  retains ownership for the C string `value` refers to and can use it, modify
 *  it, or free it as it sees fit.
 */
void cache_set(const char* key, const char* value);

/**
 * cache_get returns a copy of the C string value associated with a key that
 * matches `key` (via strcmp) that was stored by an earlier call to
 * `cache_set()` if that key-value pair hasn't been deleted (via cache_del() or
 * cache_clear()) or evicted since.
 * 
 * If cache_get returns non-NULL, then it counts the most recent access for the
 * purposes of cache eviction.
 * 
 * @param key Must be a non-NULL pointer to a nul-terminated C string that is
 *  used to match against existing keys associated with value stored in the
 *  cache.
 * 
 * @return NULL if `key` isn't associated with any value currently held in the
 *  key-pairs of the cache. Otherwise, a pointer to a copy of the C string
 *  associated with `key` in the cache. The caller is responsible for freeing
 *  the memory pointed to by the return value.
 */
char* cache_get(const char* key);

/**
 * cache_del searches the key-value pairs of the cache, and it removes
 * the key-value pair if one associated with a key matching `key` (via strcmp)
 * exists in the cache.
 * 
 * All memory used to hold the cached key-value pair, including its associated
 * key and its associated value, are freed.
 * 
 * @param key Must be a non-NULL pointer to a nul-terminated C string that is
 *  used to match against existing keys; any key-value pair with a matching key
 *  is removed from the cache.
 * 
 * @return True, if this results in the removal of a key-value pair from the
 *  cache. Returns false if no key-value pair in the cache matched `key`.
 */
bool cache_del(const char* key);

/**
 * cache_clear removes all key-value pairs from the cache, resetting it to an
 * empty state.
 * 
 * After cache_clear is called, there should be no key-value pairs stored in the
 * cache, and the cache should be ready for cache_set, cache_get, and cache_del
 * operations.
 * 
 * All memory used to hold key-value pairs including the C strings that hold
 * the stored keys and values is freed.
 */
void cache_clear(void);

#endif