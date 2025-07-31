# Brainfuck to C++ Transcompiler

A Python-based transcompiler that converts Brainfuck code to optimized C++ code with an expandable tape implementation.

## Features

- **Expandable Tape**: The tape automatically doubles in length when the pointer goes beyond the current bounds
- **No std::vector**: Uses raw arrays and manual memory management as requested
- **Optimization**: Combines consecutive operations (e.g., `+++++` becomes `+5`)
- **Memory Safety**: Proper memory allocation and deallocation with RAII
- **Cross-platform**: Generates standard C++ code that compiles on any platform

## Usage

### Basic Usage

```bash
# Compile a Brainfuck file
python bf_to_cpp.py hello_world.bf

# Read from stdin
echo "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++." | python bf_to_cpp.py -
```

### Compile the Generated C++ Code

```bash
# Compile with g++
g++ -O2 hello_world.cpp -o hello_world

# Run the program
./hello_world
```

## How It Works

### Tape Implementation

The generated C++ code uses a `BrainfuckTape` class that:

1. **Initial Capacity**: Starts with 30,000 cells
2. **Dynamic Expansion**: When the pointer goes beyond bounds, the tape doubles in size
3. **Memory Management**: Uses `new[]` and `delete[]` for dynamic allocation
4. **Zero Initialization**: All cells start with value 0

### Expansion Strategy

- **Left Expansion**: When `ptr < min_ptr`, the tape expands leftward
- **Right Expansion**: When `ptr > max_ptr`, the tape expands rightward
- **Doubling**: Each expansion doubles the current capacity

### Optimizations

The transcompiler performs basic optimizations:

- `+++++` → `+5` (combines 5 increments)
- `----` → `-4` (combines 4 decrements)
- `>>>>` → `>4` (combines 4 right moves)
- `<<<<` → `<4` (combines 4 left moves)

## Example

### Input (hello_world.bf)
```
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
```

### Generated C++ (hello_world.cpp)
The transcompiler generates a complete C++ program with:
- `BrainfuckTape` class implementation
- Optimized Brainfuck instructions
- Proper memory management
- Standard C++ main function

### Output
```
Hello World!
```

## Requirements

- Python 3.6+
- C++ compiler (g++, clang++, MSVC, etc.)

## License

This project is open source and available under the MIT License.