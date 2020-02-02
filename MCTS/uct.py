"""
import math
import numpy as np

def UCT(total_visit, win_score, visit):
    return win_score / visit + math.sqrt(2) * math.sqrt(math.log(total_visit)/visit) if visit else np.inf

"""
