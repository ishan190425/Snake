from model import Model
import tensorflow as tf
from collections import deque

import random
from SnakeGameAI import GameAI

max_memory = 100000
batch_size = 1000
learning_rate = 0.001


class Train:
    def __init__(self) -> None:
        self.num_games = 0
        self.epsilon = 0
        self.gamma = 0.9  # discount rate
        # max memory (remove the orignal if over bounds)
        self.memory = deque(maxlen=max_memory)
        self.model = Model(12, 64, 4)

    def get_state(self, game: GameAI):
        return game.get_state()

    def get_move(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.num_games
        final_move = [0, 0, 0, 0]

        if random.randint(0, 200) > self.epsilon:  # random chance at random move
            move = random.randint(0, 3)
            final_move[move] = 1

        else:
            prediction = self.model.get_qs(state)
            move = tf.argmax(prediction)
            final_move[move] = 1
        return final_move

    def train_step(self, transition):
        self.model.train_model(transition)

    def update_replay(self, state):
        self.model.update_replay_memory(state)


def train():
    record = 0
    trainer = Train()
    game = GameAI(speed=3)
    while True:
        # get old state

        state_old = trainer.get_state(game)

        move = trainer.get_move(state_old)

        reward, done, score = game.play_move(move)
        state_new = trainer.get_state(game)

        if done:
            game.reset(trainer.num_games, record)
            trainer.num_games += 1
            trainer.train_step((state_old, move, reward, state_new, done))

            if score > record:
                record = score

        trainer.update_replay((state_old, move, reward, state_new, done))


if __name__ == '__main__':
    train()
