from collections import deque
import random
from keras import callbacks
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.callbacks import TensorBoard
from collections import deque
import numpy as np
import time
import os

REPLAY_MEMORY_SIZE = 100_000
MODEL_NAME = "12X4"
MIN_REPLAY_MEMORY_SIZE = 1_000
MINIBATCH_SIZE = 64
DISCOUNT = 0.99
UPDATE_TARGET_EVERY = 5


class ModifiedTensorBoard(TensorBoard):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self.writer = tf.summary.create_file_writer(self.log_dir)
        self._log_write_dir = self.log_dir

    def set_model(self, model):
        self.model = model

        self._train_dir = os.path.join(self._log_write_dir, 'train')
        self._train_step = self.model._train_counter

        self._val_dir = os.path.join(self._log_write_dir, 'validation')
        self._val_step = self.model._test_counter

        self._should_write_train_graph = False

    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    def on_batch_end(self, batch, logs=None):
        pass

    def on_train_end(self, _):
        pass

    def update_stats(self, **stats):
        with self.writer.as_default():
            for key, value in stats.items():
                tf.summary.scalar(key, value, step=self.step)
                self.writer.flush()


class Model:
    def __init__(self, input_size, hidden_size, output_size) -> None:
        # main -> gets trained every step
        self.model = self.create_model(input_size, hidden_size, output_size)

        # target -> using .predict against
        self.target = self.create_model(input_size, hidden_size, output_size)
        self.target.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        self.tensorboard = ModifiedTensorBoard(
            log_dir=f"logs/{MODEL_NAME}-{int(time.time())}")

        self.target_update_counter = 0

    def create_model(self, input_size, hidden_size, output_size):
        model = Sequential()
        model.add(Dense(units=input_size, activation='relu', input_dim=input_size))
        model.add(Dense(units=hidden_size, activation='relu'))
        model.add(Dense(units=output_size, activation='linear'))
        model.compile(loss="mse", optimizer='adam', metrics=['accuracy'])
        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape))[0]

    def train_model(self, terminal_state):
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE) #random sample


        #get current actions and current states
        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_list = self.model.predict(current_states)

        #get new current states
        new_current_states = np.array(
            [transition[3] for transition in minibatch])
        future_qs_list = self.target.predict(new_current_states)

        X = []
        y = []

        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + (DISCOUNT * max_future_q)
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            #append all current state and current qs
            X.append(current_state)
            y.append(current_qs)

        #fit if a terminal state
        self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, verbose=0,
                       shuffle=False, callbacks=[self.tensorboard] if terminal_state else None)

        # if we want to update target model
        if terminal_state:
            self.target_update_counter += 1

        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target.set_weights(self.model.get_weights())
            self.target_update_counter = 0
