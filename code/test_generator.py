import pandas as pd, re, ast, random
from tqdm import tqdm


class TestGeneration:
    def __init__(self):
        fl = pd.read_excel('../data_files/level_5.xlsx')

        self.test_list = []
        self.index_list = []

        for i in tqdm(range(fl.shape[0])):
            for j in range(fl.shape[1]):
                self.recursion_down(fl.iloc[i, j], [i, j])
        pd.DataFrame({'text': self.test_list,
                      'index': self.index_list}).to_excel(
            '../data_files/train_set.xlsx')
        # print(self.test_list)

    def recursion_down(self, element, indexes):
        try:
            list_element = ast.literal_eval(element)
            for i in range(len(list_element)):
                self.recursion_down(list_element[i], indexes + [i])
        finally:
            for i in range(1, 20, 2):
                words_list = re.sub('xa0', ' ', str(element))
                text_example1 = random.choices(re.split(r'\W+', words_list), k=len(words_list) // i)
                text_example = ''
                for i in text_example1:
                    if len(i) > 3:
                        text_example += ' ' + i
                self.test_list.append(text_example)
                self.index_list.append(indexes)
            return
