void fail(const char* file, int line, const char* fmt, ...);
void tester_check_pair(const char* file, int line, const char* key, const char* value);
void tester_for_pairs(int n, void (*f)(const char*, const char*));
void tester_fill_pairs(int n);

#define FAIL(fmt, ...) fail(__FILE__, __LINE__, fmt, __VA_ARGS__)
#define CHECK_PAIR(key, value) tester_check_pair(__FILE__, __LINE__, key, value)

struct test {
    void (*f)(void);
    const char* name;
};