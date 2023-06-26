#pragma pack(push, 1)

template<typename T>
struct VarArray {
    uint16_t size;
    T values[1];

    static VarArray* Allocate(uint16_t size) {
        auto alloc_size = sizeof(VarArray) + (size - 1) * sizeof(T);
        auto buf = new std::int8_t[alloc_size]{0};
        return ::new(buf) VarArray(size);
    }

    explicit VarArray(uint16_t _size) : size(_size) {}

    VarArray(const VarArray&) = delete;

    VarArray(VarArray&&) = delete;

    [[nodiscard]] T* get(int i) const {
        return &((T*) ((std::int8_t*) values))[i];
    }

    T& operator[](int i) const {
        return *get(i);
    }

    uint16_t get_size() { return sizeof(VarArray) + (size - 1) * sizeof(T); }

    void destroy() {
        delete[] (std::int8_t*) this;
    }
};

template<typename T>
std::int32_t get_vararr_size(VarArray<T>& arr) {
    return sizeof(VarArray<T>) + (arr.size - 1) * sizeof(T);
}

template<typename T>
constexpr std::int32_t get_vararr_size(std::uint16_t size) {
    return sizeof(VarArray<T>) + (size - 1) * sizeof(T);
}
