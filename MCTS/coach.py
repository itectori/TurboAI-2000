from MCTS import ai
import numpy as np
from copy import deepcopy
from MCTS import validation
from keras.models import load_model

class Coach():
    """
    This class executes the self-play + learning. It uses the functions defined
    in Game and NeuralNet. args are specified in main.py.
    """
    def __init__(self, ai):
        #self.pnet = self.nnet.__class__(self.game)  # the competitor network
        self.ai = ai
        self.batch_size = 500
        self.trainExamplesHistoryX = [[]]
        self.trainExamplesHistoryY = [[],[]]

    def executeEpisode(self):
        states = []
        policy = []
        rewards = []
        
        episodeStep = 0

        while True:
            episodeStep += 1
            #temp = int(episodeStep < self.args.tempThreshold)
            pi = self.ai.mcts.get_proba(self.ai.board, self.ai, self.ai.config['play_simulation'], False)
            #sym = self.game.getSymmetries(canonicalBoard, pi)
            
            """
            X = [[game_module.encode_input()]]
            Y = [ [[0, 0, 0, 0, 1, 0, 0, 0, 0]], [-1] ]
            """

            states.append(self.ai.board.encode_input())
            policy.append(pi)                   
            
            
            action = np.random.choice(len(pi), p=pi)
            self.ai.notify_move(action)
            game_result = self.ai.board.end()

            if game_result!=0:
                reward = 0 if game_result==3 else (-1)**(game_result==2)
                for i in range(len(states)):
                    rewards.append(reward)
                    reward *=-1
                return states, policy, rewards
    
    def _check_len_insert(self, l, data):
        while len(l)+len(data) > self.batch_size:
            l.pop(0)
        l += data

    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximum length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(25):
            print('------ITER ' + str(i) + '------')
            # examples of the iteration
            
            for eps in range(15): #number of game
                #print(f"play eps nb {eps}")
                self.ai.reset()
                states,policy,rewards = self.executeEpisode()
                self._check_len_insert(self.trainExamplesHistoryX[0], states)
                self._check_len_insert(self.trainExamplesHistoryY[0], policy)
                self._check_len_insert(self.trainExamplesHistoryY[1], rewards)

        
            path = f"temp/model_{i}"
            self.ai.rdn.save(path)
            self.ai.rdn.fit(self.trainExamplesHistoryX, self.trainExamplesHistoryY, epochs=100, verbose=0)
            
            opponent = ai.AI(load_model(path, custom_objects={"loss_eval":ai.loss_eval, "loss_p": ai.loss_p}), self.ai.game, self.ai.config, 2)
            temp_tau = opponent.tau
            
            new_tau = 0.2
            opponent.tau = new_tau
            self.ai.tau = new_tau

            nb_game = 50
            nwins, pwins, draws = validation.score(self.ai.game, self.ai, opponent, nb_game)
            ratio = nwins+draws*1/2
            
            opponent.tau = temp_tau
            self.ai.tau = temp_tau
            print('NEW/PREV WINS : %f / %f ; DRAWS : %f , ratio %f' % (nwins, pwins, draws, ratio))
            if  ratio < 0.55:
                print('REJECTING NEW MODEL')
                self.ai.rdn = opponent.rdn  
            else:
                print('ACCEPTING NEW MODEL')
            

