def generate_similar_permutations_of_string(word):
        list_of_new_names = []
        counter = 0
        for each_character_of_word in word:
                new_name = word[:counter]
                new_name += (each_character_of_word)
                new_name += (word[counter:])
                list_of_new_names.append(new_name)
                counter += 1
        return list_of_new_names

data_list = ['MATTEO FABBRI', 'DILIP HARISH']
list_of_new_names = []
for name in data_list:
    list_of_new_names += generate_similar_permutations_of_string(name)
for full_name in data_list:
    for each_word_of_name in full_name.split(' '):
        list_of_new_names += generate_similar_permutations_of_string(each_word_of_name)       
print(list_of_new_names)