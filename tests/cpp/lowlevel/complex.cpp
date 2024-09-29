#include <gtest/gtest.h>
#include <test_protocol.h>
#include <iomanip>

template<typename TInputIter>
std::string convert_bytes_to_string(TInputIter first, TInputIter last, bool use_uppercase = true, bool insert_spaces = false)
{
    std::ostringstream ss;
    ss << std::hex << std::setfill('0');
    if (use_uppercase)
        ss << std::uppercase;
    while (first != last)
    {
        std::uint8_t copied_char = std::int8_t(*first++);
        ss << std::setw(2) << static_cast<int>(copied_char);
        if (insert_spaces && first != last)
            ss << " ";
    }
    return ss.str();
}

TEST(TestReadWriteTypes, Complex) {
    using namespace Mess::Default;

    // Test data
    std::array<std::int32_t, 10> array_values { INT32_MAX, INT32_MIN, 0, 40, 50, 60, 70, 80, 90, 100};
    std::string string_values = "Hi GTest!";

    // Expected size: hash + (static_field_size) + (vararray_size_field + int32 * 10) + (vararray_size_field + string)
    auto expected_size_in_bytes = 8 + (1 + 1 + 2 + 2 + 4 + 4 + 4) + (2 + 4*array_values.size()) + (2 + string_values.size());
    auto expected_bytes = "1a 66 1d 21 e6 36 5d 66 01 02 03 00 04 00 05 00 00 00 06 00 00 00 66 66 f6 40 0a 00 ff ff ff 7f 00 00 00 80 00 00 00 00 28 00 00 00 32 00 00 00 3c 00 00 00 46 00 00 00 50 00 00 00 5a 00 00 00 64 00 00 00 09 00 48 69 20 47 54 65 73 74 21";

    // Create buffer
    std::vector<int8_t> in_message_buf(TestComplex::get_alloc_size(array_values.size(), string_values.size()));
    TestComplex::Initialize(in_message_buf.data(), array_values.size(), string_values.size());

    auto in_message = (TestComplex*) in_message_buf.data();

    // Copy values
    std::memcpy(in_message->array().values, array_values.data(), sizeof(std::int32_t) * array_values.size());
    std::memcpy(in_message->string().values, string_values.data(), string_values.size());

    // Set up static fields
    in_message->int8() = 1;
    in_message->uint8() = 2;
    in_message->int16() = 3;
    in_message->uint16() = 4;
    in_message->int32() = 5;
    in_message->uint32() = 6;
    in_message->ffloat() = 7.7;


    // Check size
    EXPECT_EQ(in_message->get_size(), expected_size_in_bytes);

    // Check size array field
    ASSERT_EQ(in_message->array().size, array_values.size());
    ASSERT_EQ(in_message->array().get_size(), 2 + 4*array_values.size());

    // Check size string field
    ASSERT_EQ(in_message->string().size, string_values.size());
    ASSERT_EQ(in_message->string().get_size(), 2 + string_values.size());

    // Check message all bytes
    ASSERT_STREQ(convert_bytes_to_string(in_message_buf.begin(), in_message_buf.end(), false, true).c_str(),
                 expected_bytes);

    // Copy data from in_message to out_message
    std::vector<int8_t> out_message_buf(in_message_buf);

    auto out_message = (TestComplex*) out_message_buf.data();

    // Check deserialized field value
    ASSERT_STREQ(convert_bytes_to_string(out_message_buf.begin(), out_message_buf.end(), false, true).c_str(),
                 expected_bytes);

}