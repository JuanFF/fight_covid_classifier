import sys
sys.path.append('../')
from annotator_pkg import annotator

# Test message
print(
	annotator.annotator('vacuna en EE.UU produjo anticuerpos contra el coronavirus', 'lang_data/nodes_defeat_virus.json')
)