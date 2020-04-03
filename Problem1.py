# Use a single array to implement three stacks
# The stacks must be flexible, meaning their storage capacities can change according to the needs of the other stacks

# ArrayStack class was largely made to have a static variable keep track of values in stack array,
# and it makes it easier to keep the stack ranges organized
import Chapter3.Errors


class ArrayStack:

    stack_array = []
    size_of_array = 0

    # Initialize array, also retain size of array for cleaner code
    @staticmethod
    def init_stack_array():
        size = get_array_size()
        ArrayStack.stack_array = [None] * size
        ArrayStack.size_of_array = size

    # each stack when initialized should be allocated a specific range to remain consistent for all array sizes
    # knowing where the top of each stack is will probably be useful. Same with determining if the stack is full
    def __init__(self, stack_number):
        self.range = init_stack_range(ArrayStack.size_of_array, stack_number)
        self.size = 0
        self.is_full = False
        self.capacity = (self.range[1] - self.range[0]) + 1

        if stack_number == 1:
            self.neighbors = [1, 2]
        elif stack_number == 2:
            self.neighbors = [2, 0]
        else:
            self.neighbors = [0, 1]


def push(stacks, stack_id, value):

    stack = stacks[stack_id]
    array_index = stack.range[0] + stack.size

    if array_index >= ArrayStack.size_of_array:
        array_index = (array_index - ArrayStack.size_of_array)

    if not stack.is_full:

        ArrayStack.stack_array[array_index] = value
        stack.size += 1

        if stack.size == (stack.range[1] - stack.range[0]) + 1:
            stack.is_full = True

    else:

        if stacks[0].is_full and stacks[1].is_full and stacks[2].is_full:

            print("All stacks are full, cannot push anything else to the stacks \n")
            return False  # unsuccessful push

        shift(stacks, stack.neighbors[0], stack_id)
        ArrayStack.stack_array[array_index] = value
        stack.size += 1
        stack.capacity += 1

        if stack.range[1] == ArrayStack.size_of_array - 1:

            stack.range[1] = 0

        else:

            stack.range[1] += 1
    # successful push
    return True


def wrap_vertex(stack, vertex):

    if vertex == len(ArrayStack.stack_array) - 1:

        return len(ArrayStack.stack_array)

    elif vertex < stack.range[0]:

        return len(ArrayStack.stack_array) + vertex + 1

    else:

        return vertex + 1


def shift(stacks, neighbor, stack_id):
    # since we check if all stacks are full before calling this function
    # it is guaranteed that the second stack will not be full
    if stacks[neighbor].is_full:

        shift(stacks, stacks[stack_id].neighbors[1], stack_id)
        # we are moving everything up, so the top of the stack is actually the second to top w new stack
        prev_vertex = stacks[neighbor].range[1]
        current_vertex = wrap_vertex(stacks[neighbor], prev_vertex)

        while current_vertex > stacks[neighbor].range[0]:

            if current_vertex > len(ArrayStack.stack_array) - 1:

                ArrayStack.stack_array[current_vertex - len(ArrayStack.stack_array)] = ArrayStack.stack_array[prev_vertex]
                current_vertex = prev_vertex
                prev_vertex -= 1

            else:

                ArrayStack.stack_array[current_vertex] = ArrayStack.stack_array[prev_vertex]
                current_vertex = prev_vertex
                prev_vertex -= 1

        if stacks[neighbor].range[1] == len(ArrayStack.stack_array) - 1:

            stacks[neighbor].range[1] = 0
            stacks[neighbor].range[0] += 1

        else:

            stacks[neighbor].range[1] += 1
            stacks[neighbor].range[0] += 1

    else:
        # shift a non-empty stack (essentially just delete the top element and move everything up)
        current_vertex = stacks[neighbor].range[1]
        prev_vertex = current_vertex - 1

        # start from top of stack, move backwards
        while current_vertex > stacks[neighbor].range[0]:

            ArrayStack.stack_array[current_vertex] = ArrayStack.stack_array[prev_vertex]
            current_vertex = prev_vertex
            prev_vertex -= 1

        # update range, capacity, and is_full
        stacks[neighbor].range[0] += 1
        stacks[neighbor].capacity -= 1

        if stacks[neighbor].size == stacks[neighbor].capacity:

            stacks[neighbor].is_full = True


# def pop(stack_id):
#
#
def peek(stack):

    if stack.range[0] > stack.range[1]:

        return ArrayStack.stack_array[stack.range[1]]

    elif ArrayStack.stack_array[stack.range[0]] is None:

        return None

    return ArrayStack.stack_array[stack.range[0] + stack.size - 1]


def pop(stack):

    vertex = get_stack_vertex(stack)
    pop_val = ArrayStack.stack_array[vertex]
    ArrayStack.stack_array[vertex] = None
    stack.size -= 1
    stack.is_full = False
    return pop_val


def get_stack_vertex(stack):

    if stack.range[0] > stack.range[1]:

        return stack.range[1]

    return stack.range[0] + stack.size - 1


def get_array_size():

    # get the user's input so that array is more flexible. Handle invalid input errors and input < 3 errors
    # (you can split an array in three sections if it has less than three elements
    while True:
        try:

            array_size = int(input("How large should the array be? "))
            print()

            if array_size < 3:
                raise Chapter3.Errors.InvalidArraySizeError
            break

        except ValueError:
            print("Please enter a valid value. \n")

        except Chapter3.Errors.InvalidArraySizeError:
            print("Array size cannot be less than 3. \n")

    return array_size


def init_stack_range(size, stack_number):

    # if the array size is evenly divisible by 3, split initial stack capacities into three equal parts
    if size % 3 == 0:
        if stack_number == 1:
            return [0, int(size/3) - 1]
        elif stack_number == 2:
            return [int(size/3), int(size * .66)]
        else:
            return [int(size * .66) + 1, size - 1]

    # if array size mod 3 == 1, two stack capacities need to be one less than the other
    elif size % 3 == 1:

        if stack_number == 1:
            return [0, int(size/3)]
        elif stack_number == 2:
            return [int(size/3) + 1, int(size * .66)]
        else:
            return [int(size * .66) + 1, size - 1]

    # if array size mod 3 == 2, one stack capacity needs to be one smaller than the others.
    # these checks make it so stack capacities are initially as even as possible.
    else:

        if stack_number == 1:
            return [0, int(size/3)]
        elif stack_number == 2:
            return [int(size/3) + 1, int(size * .66)]
        else:
            return [int(size * .66) + 1, size - 1]


def get_user_input():

    while True:  # This loop continues until user has entered valid input for all fields.
        try:

            data = ""
            operation = input("What would you like to do? ")
            print()

            if operation != "push" and operation != "pop" and operation != "peek" and operation != "exit":
                raise Chapter3.Errors.InvalidOperationError

            elif operation == "exit":
                stack_id = ""  # fill stack ID so error is not thrown and array can be returned safely
                break

            elif operation == "push":
                data = int(input("What value would you like to push? (integers only): "))
                print()

            stack_id = int(input("Which stack would you like to " + operation + "? "))
            print()

            if stack_id < 1 or stack_id > 3:
                raise Chapter3.Errors.InvalidStackError

            break

        except ValueError:
            print("You can only enter an integer here. Now you get to start over. \n")

        except Chapter3.Errors.InvalidStackError:
            print("That's not a valid stack. There's 3 stacks, and they're number 1, 2, 3. Start over. \n")

        except Chapter3.Errors.InvalidOperationError:
            print("Can't perform that operation. Start over \n")

    return [operation, stack_id, data]


def main():

    # Greet the user, give instruction on how to use app
    print("\nWelcome to stack array simulation. You can perform push, pop, and peek operations on the stacks.")
    print("To perform these operations, type 'push', 'pop', or 'peek.")
    print("Type 'exit' when prompted to enter an operation to exit. \n")

    print("First, you need to initialize the array \n")
    ArrayStack.init_stack_array()

    # Make three StackArray objects
    s1 = ArrayStack(1)
    s2 = ArrayStack(2)
    s3 = ArrayStack(3)

    stack_holder = [s1, s2, s3]

    while True:  # This loop continues until user wishes to exit

        user_input = get_user_input()

        # if user enters 'exit' at any time, exit outer loop and quit program.
        if user_input[0] == "exit" or user_input[1] == "exit" or user_input[2] == "exit":
            break

        if user_input[0] == "push":

            flag = push(stack_holder, user_input[1] - 1, user_input[2])  # user_input - 1 because arrays are zero indexed
            if not flag:
                continue
            print("Push successful \n")                           # but 1 indexing is user friendly
            print(ArrayStack.stack_array)
            print("Current stack ranges: " + str(s1.range[0]) + "," + str(s1.range[1]) + " " + str(s2.range[0]) + "," + str(s2.range[1]) +
                  " " + str(s3.range[0]) + "," + str(s3.range[1]) + "\n")

        elif user_input[0] == "peek":

            print("The value at the top of stack " + str(user_input[1]) + " is: " +
                  str(peek(stack_holder[user_input[1] - 1])) + "\n")

        else:

            print("Value popped: " + str(pop(stack_holder[user_input[1] - 1])))
            print(ArrayStack.stack_array)
            print()


if __name__ == '__main__':
    main()
