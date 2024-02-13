using Int16 = std::int16_t;
using Int8 = std::int8_t;



constexpr size_t TEST_STATIC_SIZE = (sizeof(Color) + sizeof(Color));

#pragma pack(push, 1)

// 


struct Test {
    std::int8_t buffer[TEST_STATIC_SIZE];

    //  My 8bit color
// 

    Color& color8() {
        auto& prev = *first();
        return *(Color) (((std::int8_t*) &prev));
    }
    //  My 16bit color
// 

    Color& color16() {
        auto& prev = color8();
        return *(Color) (((std::int8_t*) &prev) + sizeof(Color));
    }

    std::int8_t* first() {
       return (std::int8_t*) &buffer[0];
    }

    std::int8_t* last() {
        auto& last = color16();
        return (std::int8_t*) &last;
    }

    std::int8_t* end() {
        auto last_elem = (std::int8_t*) last();
        return (std::int8_t*) last_elem + sizeof(last_elem);
    }

    std::uint16_t get_size() {
        return (std::uint16_t) (end() - first());
    }

    static void Initialize(std::int8_t* buf)  {
        // ...
    };

    static constexpr size_t get_alloc_size() {
        return TEST_STATIC_SIZE;
    }

    static Test* Allocate() {
        auto alloc_size = get_alloc_size();

        auto buf = new std::int8_t[alloc_size]{0};
        Test::Initialize(buf);

        return (Test*) buf;
    }

    Test() = default;
    Test(const Test&) = delete;
    Test(Test&&) = delete;

    void destroy() {
        delete[] (char*) this;
    }
}


#pragma pack(pop)

