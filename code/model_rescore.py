from linkgraph import save_levels_to_excel
from model import Model

levels, levels_tokenize, links = save_levels_to_excel()
model = Model(False, levels, levels_tokenize, links)
X, y = model.getXY()
model.fit(X, y)
model.save()
