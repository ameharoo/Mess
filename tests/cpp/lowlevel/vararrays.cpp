#include <gtest/gtest.h>
#include <test_protocol.h>

template<size_t SIZE>
std::string to_string(std::array<std::int32_t, SIZE> data) {
    std::stringstream ss;
    for(int i=0; i<data.size(); ++i)
        ss << std::hex << data[i] << " ";
    return ss.str();
}

std::string to_string(Mess::Default::TestArray* data) {
    std::stringstream ss;
    for(int i=0; i<data->array().size; ++i)
        ss << std::hex << data->array()[i] << " ";
    return ss.str();
}

TEST(TestReadWriteTypes, VarArrayInt32) {
    using namespace Mess::Default;

    // Test data
    std::array<std::int32_t, 10> values { INT32_MAX, INT32_MIN, 0, 40, 50, 60, 70, 80, 90, 100};

    // Create buffer
    std::vector<int8_t> in_message_buf(TestArray::get_alloc_size(10));
    TestArray::Initialize(in_message_buf.data(), 10);

    auto in_message = (TestArray*) in_message_buf.data();

    ASSERT_TRUE((std::int8_t*)in_message->array().values + sizeof(values) <=  (std::int8_t*)in_message_buf.end().base());

    // Copy values
    std::memcpy(in_message->array().values, values.data(), sizeof(std::int32_t) * values.size());

    // Check size (hash + vararray_size_field + int32 * 10)
    ASSERT_EQ(in_message->get_size(), 8 + 2 + 4*10);
    ASSERT_EQ(in_message->array().size, 10);
    ASSERT_EQ(in_message->array().get_size(), 2 + 4*10);


    // Check field value
    ASSERT_STREQ(to_string(in_message).c_str(),
                 to_string(values).c_str());

    // Copy data from in_message to out_message
    std::vector<int8_t> out_message_buf(in_message_buf);

    auto out_message = (TestArray*) out_message_buf.data();

    // Check size (hash + vararray_size_field + int32 * 10)
    ASSERT_EQ(out_message->get_size(), 8 + 2 + 4*10);
    ASSERT_EQ(out_message->array().size, 10);
    ASSERT_EQ(out_message->array().get_size(), 2 + 4*10);

    // Check deserialized field value
    ASSERT_STREQ(to_string(out_message).c_str(),
                 to_string(values).c_str());

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);
}

TEST(TestReadWriteTypes, VarArrayString) {
    using namespace Mess::Default;

    // Test data
    auto test_string = "Hello world from GTest! 1234567890";

    // Allocate buffer
    std::vector<std::int8_t> in_message_buf(TestString::get_alloc_size(strlen(test_string)));
    TestString::Initialize(in_message_buf.data(), strlen(test_string));

    auto in_message = (TestString*) in_message_buf.data();

    // Copy values
    std::memcpy(in_message->string().values, test_string, strlen(test_string));

    // Check size (hash + vararray_size_field + string)
    ASSERT_EQ(in_message->get_size(), 8 + 2 + strlen(test_string));
    ASSERT_EQ(in_message->string().size, strlen(test_string));
    ASSERT_EQ(in_message->string().get_size(), 2 + strlen(test_string));

    // Check field value
    ASSERT_STREQ(std::string(in_message->string().values, in_message->string().values + in_message->string().size).c_str(),
            std::string(test_string).c_str());

    // Copy data from in_message to out_message
    std::vector<std::int8_t> out_message_buf(in_message_buf);

    auto out_message = (TestString*) out_message_buf.data();

    // Check size (hash + vararray_size_field + string)
    ASSERT_EQ(out_message->get_size(), 8 + 2 + strlen(test_string));
    ASSERT_EQ(out_message->string().size, strlen(test_string));
    ASSERT_EQ(out_message->string().get_size(), 2 + strlen(test_string));

    // Check deserialized field value
    ASSERT_STREQ(std::string(out_message->string().values, out_message->string().values + out_message->string().size).c_str(),
            std::string(test_string).c_str());

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);
}

#pragma pack(push, 1)
struct Entry {
    std::int8_t int8;
    std::uint32_t uint32;
};
#pragma pack(pop)


template<size_t SIZE>
inline std::string to_string(std::array<Entry, SIZE> data) {
    std::stringstream ss;
    for (int i = 0; i < data.size(); ++i)
        ss << std::hex << "(" << data[i].int8 << ", " << data[i].uint32 << ") ";
    return ss.str();
}

inline std::string to_string(Mess::Default::TestArrayNested* data) {
    std::stringstream ss;
    for (int i = 0; i < data->array_nested().size; ++i)
        ss << std::hex << "(" << data->array_nested()[i].int8() << ", " << data->array_nested()[i].uint32() << ") ";
    auto s = ss.str();
    return s;
}

TEST(TestReadWriteTypes, VarArrayNested) {
    using namespace Mess::Default;

    std::array<Entry, 10> test_entries {{
            {INT8_MAX, UINT32_MAX},
            {INT8_MIN, 0},
            {INT8_MIN, UINT32_MAX},
            {INT8_MAX, 0},
            {123, 854},
            {55, 12312},
            {10, 10},
            {0, 643},
            {10, 4733},
            {-10, 10},
    }};

    // Allocate buffer
    std::vector<int8_t> in_message_buf(TestArrayNested::get_alloc_size(10));
    TestArrayNested::Initialize(in_message_buf.data(), 10);

    auto in_message = (TestArrayNested*) in_message_buf.data();

#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wstringop-overflow"
#elif defined(__GNUC__) || defined(__GNUG__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wstringop-overflow"
#elif defined(_MSC_VER)
#endif
    // Copy values
    for(int i=0; i < in_message->array_nested().size; ++i) {
        in_message->array_nested().values[i].int8() = test_entries[i].int8;
        in_message->array_nested(). values[i].uint32() = test_entries[i].uint32;
    }
#if defined(__clang__)
#pragma clang diagnostic pop
#elif defined(__GNUC__) || defined(__GNUG__)
#pragma GCC diagnostic pop
#elif defined(_MSC_VER)
#endif
    // Check size (hash + vararray_size_field + (entry with hash) * 10)
    ASSERT_EQ(in_message->get_size(), 8 + 2 + 10 * (8 + sizeof(Entry)));
    ASSERT_EQ(in_message->array_nested().size, 10);
    ASSERT_EQ(in_message->array_nested().get_size(), 2 + 10 * (8 + sizeof(Entry)));

    // Check field value
    ASSERT_STREQ(to_string(in_message).c_str(),
                 to_string(test_entries).c_str());

    // Copy data from in_message to out_message
    std::vector<std::int8_t> out_message_buf(in_message_buf);

    auto out_message = (TestArrayNested*) out_message_buf.data();

    // Check size (hash + vararray_size_field + (entry with hash) * 10)
    ASSERT_EQ(out_message->get_size(), 8 + 2 + 10 * (8 + sizeof(Entry)));
    ASSERT_EQ(out_message->array_nested().size, 10);
    ASSERT_EQ(out_message->array_nested().get_size(), 2 + 10 * (8 + sizeof(Entry)));

    // Check deserialized field value
    ASSERT_STREQ(to_string(out_message).c_str(),
                 to_string(test_entries  ).c_str());

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);
}