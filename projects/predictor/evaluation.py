import numpy as np

class Evaluator(object):
    def __init__(self, labels):
        self.confusion_matrix = np.zeros((len(labels), len(labels)), dtype=np.int16)
        self.labels = labels
    
    def record(self, predictions, true_label):
        row_index = self.labels.index(true_label)
        for p in predictions:
            col_index = self.labels.index(p[0])
            self.confusion_matrix[row_index][col_index] += 1
    
    def _f_score(self, precision, recall):
        return 2 * precision * recall / (precision + recall)

    def precision(self):
        precisions = np.diag(self.confusion_matrix) / np.sum(self.confusion_matrix, axis=0)
        mean_p = np.mean(precisions)
        return precisions, mean_p

    def recall(self):
        recalls = np.diag(self.confusion_matrix) / np.sum(self.confusion_matrix, axis=1)
        mean_r = np.mean(recalls)
        return recalls, mean_r

    def print_eval(self):
        print('Confusion Matrix:')
        print(self.confusion_matrix)
        
        precisons, mean_p = self.precision()
        recalls, mean_r = self.recall()

        for i, label in enumerate(self.labels):
            print('{}: precision={}, recall={}'.format(label, precisons[i], recalls[i]))
        print('Mean: precision={}, recall={}'.format(mean_p, mean_r))
        print('F1 score={}'.format(self._f_score(mean_p, mean_r)))
