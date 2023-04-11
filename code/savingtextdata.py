import pandas as pd
from linkgraph import LinkGraph, get_on_depth


def save_levels_to_excel():
    links, sentence_embeddings = LinkGraph().get_link_text()
    levels = []
    levels_tokenize = []
    for j in range(1, 6):
        levels.append([])
        levels_tokenize.append([])
        for i in sentence_embeddings:
            levels[j - 1].append(get_on_depth(i, j))
            levels_tokenize[j - 1].append(get_on_depth(i, j, True))

    for i, level in enumerate(levels):
        pd.DataFrame(level).to_excel(f'../data_files/level_{i + 1}.xlsx')
    for i, level in enumerate(levels_tokenize):
        pd.DataFrame(level).to_excel(f'../data_files/levels_tokenize_{i + 1}.xlsx')
    return levels, levels_tokenize, links
