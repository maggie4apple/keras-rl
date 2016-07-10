import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten

from rl.agents.dqn import DQNAgent, AnnealedEpsGreedyQPolicy
from rl.memory import Memory


ENV_NAME = 'CartPole-v0'


# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
nb_actions = env.action_space.n

# Next, we build our model. We use the same model that was described by Mnih et al. (2015).
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = Memory(limit=10000)
policy = AnnealedEpsGreedyQPolicy(eps_max=1., eps_min=.05, eps_test=0., nb_steps_annealing=1000)
dqn = DQNAgent(model=model, policy=policy, nb_actions=nb_actions, window_length=1, memory=memory,
	nb_steps_warmup=10, target_model_update_interval=100)
dqn.compile('nadam', metrics=['mae'])

# Okay, now it's time to learn something! We capture the interrupt exception so that training
# can be prematurely aborted. Notice that you can the built-in Keras callbacks!
dqn.fit(env, nb_steps=10000, action_repetition=1, log_interval=1000, visualize=True)

# After training is done, we save the final weights one more time.
dqn.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=5, action_repetition=1, visualize=False)