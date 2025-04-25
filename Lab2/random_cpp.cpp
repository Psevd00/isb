#include <iostream>
#include <fstream>
#include <random>

int main() {
    std::ofstream file("sequence_cpp.txt");
    std::mt19937 gen(std::random_device{}());
    std::uniform_int_distribution<> dist(0, 1);

    for (int i = 0; i < 128; ++i) {
        file << dist(gen);
    }
    file.close();
    return 0;
}
