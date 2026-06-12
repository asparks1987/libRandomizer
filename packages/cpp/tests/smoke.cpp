#include <librandom/random.hpp>

int main() {
    return librandom::randomInt(1, 1) == 1 ? 0 : 1;
}
