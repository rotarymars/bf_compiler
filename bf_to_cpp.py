#!/usr/bin/env python3
"""
Brainfuck to C++ Transcompiler
Generates C++ code with expandable tape that doubles in length when insufficient.
Does not use std::vector as requested.
"""

import sys
import os

class BrainfuckTranscompiler:
    def __init__(self):
        self.indent_level = 0
        self.loop_counter = 0
        
    def indent(self):
        return "    " * self.indent_level
    
    def generate_cpp_header(self):
        """Generate the C++ header with necessary includes and tape structure."""
        return """#include <iostream>
#include <cstdlib>
#include <cstring>

class BrainfuckTape {
private:
    unsigned char* tape;
    int ptr;
    int capacity;
    int min_ptr;
    int max_ptr;
    
    void expand_tape_left() {
        int new_capacity = capacity * 2;
        unsigned char* new_tape = new unsigned char[new_capacity];
        
        // Copy existing data to the right half of new tape
        memcpy(new_tape + capacity, tape, capacity);
        
        // Initialize left half with zeros
        memset(new_tape, 0, capacity);
        
        // Update pointers
        delete[] tape;
        tape = new_tape;
        
        // Adjust position and bounds
        min_ptr += capacity;
        max_ptr += capacity;
        capacity = new_capacity;
    }
    
    void expand_tape_right() {
        int new_capacity = capacity * 2;
        unsigned char* new_tape = new unsigned char[new_capacity];
        
        // Copy existing data to the left half of new tape
        memcpy(new_tape, tape, capacity);
        
        // Initialize right half with zeros
        memset(new_tape + capacity, 0, capacity);
        
        // Update pointers
        delete[] tape;
        tape = new_tape;
        
        capacity = new_capacity;
    }
    
public:
    BrainfuckTape() {
        capacity = 30000;  // Initial capacity
        tape = new unsigned char[capacity];
        memset(tape, 0, capacity);
        ptr = 0;
        min_ptr = 0;
        max_ptr = capacity - 1;
    }
    
    ~BrainfuckTape() {
        delete[] tape;
    }
    
    unsigned char& get_current() {
        return tape[ptr];
    }
    
    void move_left() {
        ptr--;
        if (ptr < min_ptr) {
            expand_tape_left();
        }
    }
    
    void move_right() {
        ptr++;
        if (ptr > max_ptr) {
            expand_tape_right();
        }
    }
    
    void increment() {
        get_current()++;
    }
    
    void decrement() {
        get_current()--;
    }
    
    unsigned char read() {
        return get_current();
    }
    
    void write(unsigned char value) {
        get_current() = value;
    }
    
    void input() {
        std::cin >> get_current();
    }
    
    void output() {
        std::cout << static_cast<char>(get_current());
    }
};

int main() {
    BrainfuckTape tape;
"""
    
    def generate_cpp_footer(self):
        """Generate the C++ footer."""
        return """
    return 0;
}
"""
    
    def compile_instruction(self, instruction):
        """Compile a single Brainfuck instruction to C++."""
        if instruction == '>':
            return f"{self.indent()}tape.move_right();"
        elif instruction == '<':
            return f"{self.indent()}tape.move_left();"
        elif instruction == '+':
            return f"{self.indent()}tape.increment();"
        elif instruction == '-':
            return f"{self.indent()}tape.decrement();"
        elif instruction == '.':
            return f"{self.indent()}tape.output();"
        elif instruction == ',':
            return f"{self.indent()}tape.input();"
        elif instruction == '[':
            self.loop_counter += 1
            loop_id = self.loop_counter
            self.indent_level += 1
            return f"{self.indent()}while (tape.read() != 0) {{"
        elif instruction == ']':
            self.indent_level -= 1
            return f"{self.indent()}}}"
        else:
            return ""  # Ignore non-Brainfuck characters
    
    def compile_brainfuck(self, brainfuck_code):
        """Compile Brainfuck code to C++."""
        cpp_code = self.generate_cpp_header()
        
        for char in brainfuck_code:
            if char in '><+-.,[]':
                cpp_line = self.compile_instruction(char)
                if cpp_line:
                    cpp_code += cpp_line + "\n"
        
        cpp_code += self.generate_cpp_footer()
        return cpp_code
    
    def optimize_loops(self, brainfuck_code):
        """Basic optimization: combine consecutive operations."""
        optimized = []
        i = 0
        
        while i < len(brainfuck_code):
            char = brainfuck_code[i]
            
            if char in '+-<>':
                # Count consecutive operations
                count = 1
                while i + count < len(brainfuck_code) and brainfuck_code[i + count] == char:
                    count += 1
                
                if count > 1:
                    # Replace multiple operations with a single optimized one
                    if char in '+-':
                        optimized.append(f"{char}{count}")
                    else:  # <> operations
                        optimized.append(f"{char}{count}")
                    i += count
                else:
                    optimized.append(char)
                    i += 1
            else:
                optimized.append(char)
                i += 1
        
        return ''.join(optimized)
    
    def compile_optimized_instruction(self, instruction):
        """Compile optimized instructions (like +5, -3, >10, etc.)."""
        if len(instruction) > 1 and instruction[0] in '+-<>':
            op = instruction[0]
            try:
                count = int(instruction[1:])
                if op == '+':
                    return f"{self.indent()}tape.get_current() += {count};"
                elif op == '-':
                    return f"{self.indent()}tape.get_current() -= {count};"
                elif op == '>':
                    return f"{self.indent()}for (int i = 0; i < {count}; i++) tape.move_right();"
                elif op == '<':
                    return f"{self.indent()}for (int i = 0; i < {count}; i++) tape.move_left();"
            except ValueError:
                pass
        
        # Fall back to single instruction
        return self.compile_instruction(instruction[0])
    
    def compile_optimized_brainfuck(self, brainfuck_code):
        """Compile optimized Brainfuck code to C++."""
        optimized_code = self.optimize_loops(brainfuck_code)
        cpp_code = self.generate_cpp_header()
        
        i = 0
        while i < len(optimized_code):
            char = optimized_code[i]
            
            if char in '+-<>':
                # Check if this is an optimized instruction (followed by digits)
                instruction = char
                j = i + 1
                while j < len(optimized_code) and optimized_code[j].isdigit():
                    instruction += optimized_code[j]
                    j += 1
                
                if len(instruction) > 1:
                    # This is an optimized instruction
                    cpp_line = self.compile_optimized_instruction(instruction)
                    if cpp_line:
                        cpp_code += cpp_line + "\n"
                    i = j
                else:
                    # This is a single instruction
                    cpp_line = self.compile_instruction(char)
                    if cpp_line:
                        cpp_code += cpp_line + "\n"
                    i += 1
            elif char in '.,[]':
                cpp_line = self.compile_instruction(char)
                if cpp_line:
                    cpp_code += cpp_line + "\n"
                i += 1
            else:
                i += 1
        
        cpp_code += self.generate_cpp_footer()
        return cpp_code

def main():
    if len(sys.argv) != 2:
        print("Usage: python bf_to_cpp.py <brainfuck_file>")
        print("   or: python bf_to_cpp.py -")
        print("       (use '-' to read from stdin)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Read Brainfuck code
    if input_file == '-':
        brainfuck_code = sys.stdin.read()
    else:
        try:
            with open(input_file, 'r') as f:
                brainfuck_code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    
    # Filter out non-Brainfuck characters
    brainfuck_code = ''.join(c for c in brainfuck_code if c in '><+-.,[]')
    
    # Compile to C++
    transcompiler = BrainfuckTranscompiler()
    cpp_code = transcompiler.compile_optimized_brainfuck(brainfuck_code)
    
    # Generate output filename
    if input_file == '-':
        output_file = 'brainfuck_output.cpp'
    else:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.cpp"
    
    # Write C++ code to file
    try:
        with open(output_file, 'w') as f:
            f.write(cpp_code)
        print(f"Successfully compiled Brainfuck to C++: {output_file}")
        print(f"Compile with: g++ -O2 {output_file} -o {os.path.splitext(output_file)[0]}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()