from annotator_pkg import annotator
from classifier_pkg import classifier

message = 'vacuna contra virus dio resultado'

messageAnnResult = annotator.annotator(message, 'annotator_pkg/lang_data/defeatVirus_nodes.json')
message_model = classifier.loadModel('classifier_pkg/defeatVirus.train.txt')
messageLabel = classifier.classify(message_model, messageAnnResult[0])