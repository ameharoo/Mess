#include <gtest/gtest.h>
#include <test_protocol.h>

TEST(TestReadWriteTypes, Int8) {
    using namespace Mess::Default;

    // Allocate buffer
    auto in_message_buf = new int8_t[TestInt8::get_alloc_size()] {0};
    TestInt8::Initialize(in_message_buf);

    // Assign field
    auto in_message = (TestInt8*) in_message_buf;
    in_message->int8() = 127;

    // Check size (hash + int8)
    ASSERT_EQ(in_message->get_size(), 8 + 1);

    // Allocate buffer
    auto out_message_buf = new int8_t[TestInt8::get_alloc_size()] {0};

    // Copy data from in_message_buf to out_message_buf
    std::memcpy(out_message_buf, in_message_buf, in_message->get_size());

    // Free buffer
    delete[] in_message_buf;

    auto out_message = (TestInt8*) out_message_buf;

    // Check size (hash + int8)
    ASSERT_EQ(out_message->get_size(), 8 + 1);

    // Check deserialized field value
    ASSERT_EQ(out_message->int8(), 127);

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);

    // Free buffer
    delete[] out_message;
}

TEST(TestReadWriteTypes, Uint8) {
    using namespace Mess::Default;

    // Allocate buffer
    auto in_message_buf = new int8_t[TestUint8::get_alloc_size()] {0};
    TestUint8::Initialize(in_message_buf);

    // Assign field
    auto in_message = (TestUint8*) in_message_buf;
    in_message->uint8() = 255;

    // Check size (hash + uint8)
    ASSERT_EQ(in_message->get_size(), 8 + 1);

    // Allocate buffer
    auto out_message_buf = new int8_t[TestUint8::get_alloc_size()] {0};

    // Copy data from in_message_buf to out_message_buf
    std::memcpy(out_message_buf, in_message_buf, in_message->get_size());

    // Free buffer
    delete[] in_message_buf;

    auto out_message = (TestUint8*) out_message_buf;

    // Check size (hash + uint8)
    ASSERT_EQ(out_message->get_size(), 8 + 1);

    // Check deserialized field value
    ASSERT_EQ(out_message->uint8(), 255);

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);

    // Free buffer
    delete[] out_message;
}

TEST(TestReadWriteTypes, Int16) {
    using namespace Mess::Default;

    // Allocate buffer
    auto in_message_buf = new int8_t[TestInt16::get_alloc_size()] {0};
    TestInt16::Initialize(in_message_buf);

    // Assign field
    auto in_message = (TestInt16*) in_message_buf;
    in_message->int16() = SHRT_MAX;

    // Check size (hash + int16)
    ASSERT_EQ(in_message->get_size(), 8 + 2);

    // Allocate buffer
    auto out_message_buf = new int8_t[TestInt16::get_alloc_size()] {0};

    // Copy data from in_message_buf to out_message_buf
    std::memcpy(out_message_buf, in_message_buf, in_message->get_size());

    // Free buffer
    delete[] in_message_buf;

    auto out_message = (TestInt16*) out_message_buf;

    // Check size (hash + int16)
    ASSERT_EQ(out_message->get_size(), 8 + 2);

    // Check deserialized field value
    ASSERT_EQ(out_message->int16(), SHRT_MAX);

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);

    // Free buffer
    delete[] out_message;
}

TEST(TestReadWriteTypes, Uint16) {
    using namespace Mess::Default;

    // Allocate buffer
    auto in_message_buf = new int8_t[TestUint16::get_alloc_size()] {0};
    TestUint16::Initialize(in_message_buf);

    // Assign field
    auto in_message = (TestUint16*) in_message_buf;
    in_message->uint16() = USHRT_MAX;

    // Check size (hash + int16)
    ASSERT_EQ(in_message->get_size(), 8 + 2);

    // Allocate buffer
    auto out_message_buf = new int8_t[TestUint16::get_alloc_size()] {0};

    // Copy data from in_message_buf to out_message_buf
    std::memcpy(out_message_buf, in_message_buf, in_message->get_size());

    // Free buffer
    delete[] in_message_buf;

    auto out_message = (TestUint16*) out_message_buf;

    // Check size (hash + int16)
    ASSERT_EQ(out_message->get_size(), 8 + 2);

    // Check deserialized field value
    ASSERT_EQ(out_message->uint16(), USHRT_MAX);

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);

    // Free buffer
    delete[] out_message;
}

TEST(TestReadWriteTypes, Int32) {
    using namespace Mess::Default;

    // Allocate buffer
    auto in_message_buf = new int8_t[TestInt32::get_alloc_size()] {0};
    TestInt32::Initialize(in_message_buf);

    // Assign field
    auto in_message = (TestInt32*) in_message_buf;
    in_message->int32() =   INT32_MAX;

    // Check size (hash + int32)
    ASSERT_EQ(in_message->get_size(), 8 + 4);

    // Allocate buffer
    auto out_message_buf = new int8_t[TestInt32::get_alloc_size()] {0};

    // Copy data from in_message_buf to out_message_buf
    std::memcpy(out_message_buf, in_message_buf, in_message->get_size());

    // Free buffer
    delete[] in_message_buf;

    auto out_message = (TestInt32*) out_message_buf;

    // Check size (hash + int32)
    ASSERT_EQ(out_message->get_size(), 8 + 4);

    // Check deserialized field value
    ASSERT_EQ(out_message->int32(), INT32_MAX);

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);

    // Free buffer
    delete[] out_message;
}

TEST(TestReadWriteTypes, Uint32) {
    using namespace Mess::Default;

    // Allocate buffer
    auto in_message_buf = new int8_t[TestUint32::get_alloc_size()] {0};
    TestUint32::Initialize(in_message_buf);

    // Assign field
    auto in_message = (TestUint32*) in_message_buf;
    in_message->uint32() = UINT32_MAX;

    // Check size (hash + int32)
    ASSERT_EQ(in_message->get_size(), 8 + 4);

    // Allocate buffer
    auto out_message_buf = new int8_t[TestUint32::get_alloc_size()] {0};

    // Copy data from in_message_buf to out_message_buf
    std::memcpy(out_message_buf, in_message_buf, in_message->get_size());

    // Free buffer
    delete[] in_message_buf;

    auto out_message = (TestUint32*) out_message_buf;

    // Check size (hash + int32)
    ASSERT_EQ(out_message->get_size(), 8 + 4);

    // Check deserialized field value
    ASSERT_EQ(out_message->uint32(), UINT32_MAX);

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);

    // Free buffer
    delete[] out_message;
}

TEST(TestReadWriteTypes, Float) {
    using namespace Mess::Default;

    // Allocate buffer
    auto in_message_buf = new int8_t[TestFloat::get_alloc_size()] {0};
    TestFloat::Initialize(in_message_buf);

    // Assign field
    auto in_message = (TestFloat*) in_message_buf;
    in_message->ffloat() = FLT_MAX;

    // Check size (hash + float)
    ASSERT_EQ(in_message->get_size(), 8 + 4);

    // Allocate buffer
    auto out_message_buf = new int8_t[TestFloat::get_alloc_size()] {0};

    // Copy data from in_message_buf to out_message_buf
    std::memcpy(out_message_buf, in_message_buf, in_message->get_size());

    // Free buffer
    delete[] in_message_buf;

    auto out_message = (TestFloat*) out_message_buf;

    // Check size (hash + float)
    ASSERT_EQ(out_message->get_size(), 8 + 4);

    // Check deserialized field value
    ASSERT_EQ(out_message->ffloat(), FLT_MAX);

    // Check deserialized message protocol hash
    ASSERT_EQ(out_message->protocol_hash, _HASH);

    // Free buffer
    delete[] out_message;
}