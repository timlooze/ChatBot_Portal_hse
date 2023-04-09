def save_levels_to_excel():
    from linkgraph import LinkGraph, get_on_depth
    sentence_embeddings = LinkGraph().get_link_text()
    level_1 = []
    level_2 = []
    level_3 = []
    level_4 = []
    level_5 = []
    for i in sentence_embeddings:
        level_1.append(get_on_depth(i, 1))
        level_2.append(get_on_depth(i, 2))
        level_3.append(get_on_depth(i, 3))
        level_4.append(get_on_depth(i, 4))
        level_5.append(get_on_depth(i, 5))
    t = 0
    for i in level_2:
        for j in i:
            t += 1
    print(t)
    t = 0
    for i in level_5:
        for j in i:
            for k in j:
                for p in k:
                    for m in p:
                        t += 1
    print(t)
    levels = [level_1, level_2, level_3, level_4, level_5]
    for i, level in enumerate(levels):
        pd.DataFrame(level).to_excel(f'../data_files/level_{i + 1}.xlsx')