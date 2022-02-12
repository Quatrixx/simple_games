with open('word_list.txt') as input:
    word_list = [line.strip() for line in input.readlines()]
print(f"sorting {len(word_list)} words...")
word_list.sort(key=len)
word_length_lists = []
word_length_lists.append([])
for l in word_list[-1]:
    word_length_lists.append([])
for word in word_list:
    word_length_lists[len(word)].append(word)
for word_length, list in enumerate(word_length_lists):
    print(f"found {len(list):3} words of length {word_length:2}", end=" ")
    if(len(list) > 100 and word_length < 10):
        with open(f'{word_length}_letter_words.txt', 'x') as output:
            for word_index, word in enumerate(list):
                output.write(word)
                if word_index < len(list)-1:
                    output.write('\n')
        print("and wrote list to file")
    else:
        print("")