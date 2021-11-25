def guess(beginning, ending, counter):
    # Solving the case where the numbers are interval boundaries
    global start, end
    if ending == start + 1:
        print(f"Liar! No number smaller than {ending} and larger than {ending}!")
        return
    if beginning == end - 1:
        print(f"Liar! No number smaller than {beginning} and larger than {beginning}!")
        return

    # Dealing with an inconsistency/lie
    if ending - beginning == 1:
        print(f"Liar! No number smaller than {ending} and larger than {beginning}!")
        return

    # Dealing with common situation
    average = (beginning + ending) // 2
    print(f"Is your number greater (>), equal (=), or less (<) than {average} ?")
    clue = input("Please answer <, = or >! ")
    if clue != "<" and clue != "=" and clue != ">":
        print("Relational Operator ERROR!!! Please answer <, = or > CORRECTLY!!!")
        guess(beginning, ending, counter)
    elif clue == "<":
        ending = average
        counter += 1
        guess(beginning, ending, counter)
    elif clue == ">":
        beginning = average
        counter += 1
        guess(beginning, ending, counter)
    elif clue == "=":
        counter += 1
        print("I have guessed it!")
        print(f"I needed {counter} steps!")
        # Show the number of steps
        

start, end = 0, 101
# It can be straightforward to modify for a different interval[start + 1, end - 1].
counting = 0

print(f"Think of a number between {start + 1} and {end - 1}!")
guess(start, end, counting)
