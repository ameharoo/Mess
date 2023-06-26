import typing

from message_manager import global_message_manager


class TypeField:
    name: str
    generic_args: [str]
    type: str
    doc: str

    def __init__(self, _type: str, name: str, doc: str):
        self.name = name
        self.type = _type
        self.generic_args = []
        self.doc = doc

        generic_left = self.type.find("<")
        generic_right = self.type.rfind(">")
        if generic_left != -1 and generic_right != -1 and generic_left != generic_right:
            self.generic_args = list(map(lambda x: x.strip(), self.type[generic_left + 1:generic_right].split(",")))
            self.type = self.type[:generic_left]

    def fetch_types(self):
        if self.type == "VarArray":
            return self.generic_args

        return [self.type]

    def instantiate(self):
        obj = None
        if self.type == "VarArray":
            nested_type = global_message_manager.get(self.generic_args[0])
            obj = global_message_manager.get(self.type)(self.name, nested_type)
        elif self.generic_args:
            raise Exception(f"Unknown generic message {self.type} with args {self.generic_args}")
        else:
            obj = global_message_manager.get(self.type)(self.name)

        obj.docs = self.doc

        return obj


class CppType:
    fields: list["CppType"] = []
    load_fields: list["TypeField"] = []
    docs: str
    is_variative: bool
    is_builtin: bool
    field_count: int = 0

    def __init__(self, var_name: str | None):
        self.var_name = var_name
        self.fields = []
        self.is_variative = False
        self.docs = ""
        self.is_builtin = False

        # for field in self.load_fields:
        #    self.fields.append(field.instantiate())

    def render_type_name(self):
        return f"CppType"

    def render_field_name(self):
        return self.var_name

    def render_field_getter(self):
        return f"{self.var_name}()"

    def render_var_static_size(self):
        return f"{self.render_type_name().upper()}_STATIC_SIZE"

    def render_first_method(self):
        return f"std::int8_t* first() {{\n" \
               f"   return (std::int8_t*) &buffer[0];\n" \
               f"}}\n"

    def render_last_method(self):
        return f"std::int8_t* last() {{\n" \
               f"   auto& last = {self.fields[-1].render_field_name() if self.fields else '*first'}();\n" \
               f"   return (std::int8_t*) &last;\n" \
               f"}}\n"

    def render_end_method(self):
        return f"std::int8_t* end() {{\n" \
               f"     auto last_elem = (std::int8_t*) last();\n" \
               f"     return (std::int8_t*) last_elem + sizeof(last_elem);\n" \
               f"}}\n"

    def render_get_size_method(self):
        return f"std::uint16_t get_size() {{ \n" \
               f"    return (std::uint16_t) (end() - first()); \n" \
               f"}}\n"

    def render_doc_comment(self):
        gen_doc_string: typing.Callable[["CppType"], str] = lambda \
                _field: f"// {_field.render_field_name()}: {_field.render_type_name()}\n"
        doc_lines = list(map(gen_doc_string, self.fields))

        if len(self.docs) != 0:
            docs = list(map(lambda doc: f"// {doc.strip()}", self.docs.split("\n")))
            doc_lines.insert(0, "\n".join(docs) + "\n")

        return "".join(doc_lines)

    def render_initialize_fields(self):
        fields_definition = []
        for field in self.fields:
            if not field.is_variative:
                continue

            field_var_name = f"{field.render_field_name()}_field"
            field_size_var_name = f"size_{field.render_field_name()}"

            fields_definition.append(
                f"    // Initialize field \"{field.render_field_name()}\"\n"
                f"    auto {field_var_name} = &value->{field.render_field_name()}();\n"
                f"    ::new({field_var_name}) {field.render_type_name()}({field_size_var_name});\n"
            )

        return "\n".join(fields_definition)

    def render_initialize_arguments(self):
        fields_definition = []
        for field in self.fields:
            if not field.is_variative:
                continue
            fields_definition.append(f"std::uint16_t size_{field.render_field_name()}")

        return (", " + ", ".join(fields_definition)) if fields_definition else ""

    def render_initialize_method(self):
        return f"static void Initialize(std::int8_t* buf{self.render_initialize_arguments()})  {{ \n" \
               f"    auto value = ::new(buf) {self.render_type_name()}(); \n" \
               f"    // ...\n" \
               f"{self.render_initialize_fields()}" \
               f"}};\n"

    def render_get_alloc_size_method(self):
        return f"static constexpr size_t get_alloc_size() {{\n" \
               f"   return {self.render_var_static_size()};\n" \
               f"}}\n"

    def render_allocate_size_fields(self):
        fields_definition = []
        for field in self.fields:
            if not field.is_variative:
                continue
            fields_definition.append(f"size_{field.render_field_name()}")

        return (", " + ", ".join(fields_definition)) if fields_definition else ""

    def render_allocate_method(self):
        return f"static {self.render_type_name()}* Allocate({self.render_initialize_arguments()[2:]}) {{\n" \
               f"    auto alloc_size = get_alloc_size();\n" \
               f"\n" \
               f"    auto buf = new std::int8_t[alloc_size]{{0}};\n" \
               f"    {self.render_type_name()}::Initialize(buf{self.render_allocate_size_fields()});\n" \
               f"\n" \
               f"    return ({self.render_type_name()}*) buf;\n" \
               f"}}\n"

    def render_contructor_method(self):
        return f"{self.render_type_name()}() = default; \n" \
               f"{self.render_type_name()}(const {self.render_type_name()}&) = delete; \n" \
               f"{self.render_type_name()}({self.render_type_name()}&&) = delete;\n"

    def render_destroy_method(self):
        return f"void destroy() {{ \n" \
               f"    delete[] (char*) this; \n" \
               f"}}\n"

    def render_field_type(self, field: "CppType"):
        return field.render_type_name()  # f"FieldTypes::{self.render_type_name()}::{field.render_field_name().capitalize()}"

    def render_get_size(self, variable):
        return f"sizeof({variable})"

    def render_fields(self):
        fields_definition = []
        prev_field = None
        for field in self.fields:
            fields_definition.append(
                f"{field.render_doc_comment()}"
                f"{self.render_field_type(field)}& {field.render_field_name()}() {{\n"
                f"    auto& prev = {prev_field.render_field_name() if prev_field is not None else '*first'}();\n"
                f"    return *({self.render_field_type(field)}*) (((std::int8_t*) &prev) + {prev_field.render_get_size('prev') if prev_field is not None else '0'});\n"
                f"}}\n")
            prev_field = field

        return "\n".join(fields_definition)

    def render_static_size_definition(self):
        fields_sizes = []
        for field in self.fields:
            if field.is_variative:
                continue

            fields_sizes.append(field.render_get_size(field.render_type_name()))

        sizes_str = "+".join(fields_sizes)

        return f"constexpr size_t {self.render_type_name().upper()}_STATIC_SIZE = ({sizes_str});\n"

    def render_definition(self):
        return f"{self.render_static_size_definition()}\n" \
               f"#pragma pack(push, 1)\n" \
               f"{self.render_doc_comment()}" \
               f"struct {self.render_type_name()} {{\n" \
               f"std::int8_t buffer[{self.render_var_static_size()}];\n\n" \
               f"{self.render_fields()}\n" \
               f"{self.render_first_method()}\n" \
               f"{self.render_last_method()}\n" \
               f"{self.render_end_method()}\n" \
               f"{self.render_get_size_method()}\n" \
               f"{self.render_initialize_method()}\n" \
               f"{self.render_get_alloc_size_method()}\n" \
               f"{self.render_allocate_method()}\n" \
               f"{self.render_contructor_method()}\n" \
               f"{self.render_destroy_method()}\n" \
               f"}};\n" \
               f"#pragma pack(pop)\n"


class Int8(CppType):
    def __init__(self, var_name: str | None):
        super().__init__(var_name)
        self.is_builtin = True

    def render_type_name(self):
        return f"std::int8_t"

    def render_definition(self):
        return ""


class Int16(CppType):
    def __init__(self, var_name: str | None):
        super().__init__(var_name)
        self.is_builtin = True

    def render_type_name(self):
        return f"std::int16_t"

    def render_definition(self):
        return ""


class Int32(CppType):
    def __init__(self, var_name: str | None):
        super().__init__(var_name)
        self.is_builtin = True

    def render_type_name(self):
        return f"std::int32_t"

    def render_definition(self):
        return ""


class Int64(CppType):
    def __init__(self, var_name: str | None):
        super().__init__(var_name)
        self.is_builtin = True

    def render_type_name(self):
        return f"std::int64_t"

    def render_definition(self):
        return ""


class Float(CppType):
    def __init__(self, var_name: str | None):
        super().__init__(var_name)
        self.is_builtin = True

    def render_type_name(self):
        return f"float"

    def render_definition(self):
        return ""


class FixedN(CppType):
    def __init__(self, var_name: str, bitness):
        super().__init__(var_name)
        self.bitness = bitness

    def render_definition(self):
        return f"#pragma pack(push, 1)\n" \
               f"struct {self.render_type_name()} {{\n" \
               f"    std::int{self.bitness}_t raw;\n" \
               f"\n" \
               f"    {self.render_type_name()}(float fl) {{\n" \
               f"        this->set(fl);\n" \
               f"    }}\n" \
               f"\n" \
               f"    void set(float fl) {{\n" \
               f"        this->raw = fl * (1 << {int(self.bitness / 2)});\n" \
               f"    }}\n" \
               f"\n" \
               f"    float to_float() {{\n" \
               f"        return ((float)this->raw) / (1 << {int(self.bitness / 2)});\n" \
               f"    }}\n" \
               f"\n" \
               f"    {self.render_type_name()}& operator= (float source) {{\n" \
               f"        this->set(source);\n" \
               f"        return *this;\n" \
               f"    }}\n" \
               f"}};\n" \
               f"#pragma pack(pop)\n"

    def render_type_name(self):
        return f"Fixed{self.bitness}"


class Fixed16(FixedN):
    def __init__(self, var_name: str):
        super().__init__(var_name, 16)


class Fixed32(FixedN):
    def __init__(self, var_name: str):
        super().__init__(var_name, 32)


class VarArray(CppType):
    def __init__(self, var_name: str, cpp_type: typing.Type = CppType):
        super().__init__(var_name)

        self.is_variative = True
        self.is_builtin = True

        self.values_field = cpp_type("values")
        self.fields.append(self.values_field)

    def render_type_name(self):
        return f"VarArray<{self.values_field.render_type_name()}>"

    def render_var_static_size(self):
        return f"0"

    def render_definition(self):
        return f""

    def render_get_size(self, variable):
        return f"get_vararr_size({variable})"
