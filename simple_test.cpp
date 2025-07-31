#include <iostream>
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
tape.get_current() += 65;
tape.output();

    return 0;
}
