#include <iostream>
#include <fstream>
#include <cstring>
#include "test_message.cpp"

#define BUF_SIZE 512
#define ARR_SIZE 5
int main() {
    // Allocate buffer
    static auto* static_buf = new std::int8_t[BUF_SIZE];

    // Example string
    const char* string = "Hello world!";

    // Initialize all nested variable-size arrays
    // ARR_SIZE - is arr.size
    // strlen(string) - is string.size
    Test::Initialize(static_buf, ARR_SIZE, strlen(string));

    // Cast to our message
    auto test_message = (Test*) static_buf;

    // Setting field arr element
    for (int i = 0; i < test_message->arr().size; ++i) {
        test_message->arr()[i] = i;
    }

    // Setting field "string" without null-terminate symbol
    std::memcpy(&test_message->string().values[0], string, strlen(string));

    // Setting common fields
    test_message->foo() = 0x0529BB;
    test_message->bar() = 1;
    test_message->kek() = 0.3;

    // Print "arr" elements
    std::cout << "arr.size = " << test_message->arr().size << std::endl;

    for(int i=0; i<test_message->arr().size; ++i)
        std::cout << "arr[" << i << "] = " << test_message->arr()[i] << std::endl;

    // Print "string" field like a string
    std::cout << "\nstring.size = " << test_message->string().size << std::endl;

    auto tmp_string = new char[test_message->string().size + 1];
    tmp_string[test_message->string().size] = '\0';

    std::memcpy(tmp_string, &test_message->string().values[0], test_message->string().size);

    std::cout << "string = " << tmp_string << std::endl;

    // Print common fields
    std::cout << "\nfoo = " << test_message->foo()
              << "\nbar = " << test_message->bar()
              << "\nkek = " << test_message->kek()
              << std::endl;

    // Just save data to "out.bin"
    std::cout << "\ntest_message total size = " << test_message->get_size() << " bytes" << std::endl;

    std::ofstream f("out.bin", std::ios::binary);
    f.write((char*) test_message, test_message->get_size());
    f.close();

    delete[] static_buf;

    return 0;
}
