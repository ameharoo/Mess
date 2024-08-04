#include <iostream>
#include <fstream>
#include <cstring>
#include "test_message.h"

#define BUF_SIZE 1024
#define ARR_SIZE 5
#define COLORS_SIZE 100

using Mess::TestProto::Test;

int main() {
    // Allocate buffer
    static std::int8_t static_buf[BUF_SIZE] {0};

    // Example string
    const char* string = "Hello world!";

    // Initialize all nested variable-size arrays
    // ARR_SIZE - is arr.size
    // strlen(string) - is string.size
    Test::Initialize(static_buf, ARR_SIZE, strlen(string), COLORS_SIZE);

    // Cast to our message
    auto test_message = (Test*) static_buf;

    // Setting field arr element
    for (int i = 0; i < test_message->arr().size; ++i) {
        test_message->arr()[i] = i;
    }

    // Setting field "string" without null-terminate symbol
    std::memcpy(&test_message->string().values[0], string, strlen(string));

    // Setting Array of User messages
    for (int i = 0; i < test_message->colors().size; ++i) {
        test_message->colors()[i].r() = i;
        test_message->colors()[i].g() = i+1;
        test_message->colors()[i].b() = i+2;
    }

    // Setting common fields
    test_message->fixed() = 0.81;
    test_message->foo() = 0x0529BB;
    test_message->bar() = 0x41;
    test_message->f() = 0.3;

    // Print "arr" elements
    std::cout << "arr.size = " << test_message->arr().size << std::endl;

    for(int i=0; i<test_message->arr().size; ++i)
        std::cout << "arr[" << i << "] = " << test_message->arr()[i] << std::endl;

    // Print "string" field like a string
    std::cout << "\nstring.size = " << test_message->string().size << std::endl;

    char tmp_string[test_message->string().size + 1] {0};

    std::memcpy(tmp_string, &test_message->string().values[0], test_message->string().size);

    std::cout << "string = " << tmp_string << std::endl;

    // Print common fields
    std::cout << "\nfixed = " << test_message->fixed().to_float()
              << "\nfoo = " << test_message->foo()
              << "\nbar = " << test_message->bar()
              << "\nf = " << test_message->f()
              << std::endl;

    // Just save data to "out.bin"
    std::cout << "\ntest_message total size = " << test_message->get_size() << " bytes\n" 
              << "hash = " << (std::uint64_t) test_message->protocol_hash
              << std::endl;

    std::ofstream f("out.bin", std::ios::binary);
    f.write((char*) test_message, test_message->get_size());
    f.close();

    return 0;
}
