import random
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from collections import deque


class DQNAgent:
    def __init__(self, state_size, action_size):
        # state_size - number of inputs
        # action_size - number of outputs
        self.state_size = state_size
        self.action_size = action_size

        # make the memory to keep the actions to make the
        self.memory = deque(maxlen=100000)

        # gamma - discount the reward for the next predicted state
        # epsilon - the number controlling random action
        # epsilon_decay - the number controlling exploitation and exploration
        # learning_rate - the learning rate
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self.build_model()
        self.target_model = self.build_model()

    '''
    the neural network with: input layer, 3 dense layer and output
    '''
    def build_model(self):
        model = Sequential()
        model.add(Input(shape=(self.state_size,)))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    '''
    update the target model
    '''
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    '''
    remember function to add state-choices for sampling for experience replay
    '''
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    '''
    choose the action: either random or by the model
    '''
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    '''
    See if the memory have enough sample and then sample. Set target if it's not a game ending move predict another 
    Q(s,a). 
    '''
    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target_action = np.argmax(self.model.predict(next_state, verbose=0)[0])
                target = reward + self.gamma * self.target_model.predict(next_state, verbose=0)[0][target_action]
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)
        self.update_target_model()

    def save(self, name):
        self.model.save_weights(name)
