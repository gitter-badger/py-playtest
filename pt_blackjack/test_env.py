import pytest

import numpy as np
import gym.spaces as spaces

from playtest.env import GameWrapperEnvironment
from playtest.action import InvalidActionError, ActionWait, ActionWaitRange


from .constant import Reward, Param
from .game import Blackjack
from .action import (
    ActionBetRange,
    ActionHit,
    ActionBet,
    ActionHitRange,
    ActionSkipRange,
)


AGENT_COUNT = 2


@pytest.fixture
def env() -> GameWrapperEnvironment:
    env = GameWrapperEnvironment(Blackjack(Param(number_of_players=2)))
    return env


def test_reset(env):
    array = env.reset()
    assert isinstance(array, list)
    assert isinstance(array[0], np.ndarray)


def test_obs_space(env):
    space = env.observation_space
    assert isinstance(space, spaces.Tuple)
    assert len(space) == 2, "Observe space contains both action and observation"
    assert space[0]["wait"], "Action space contains wait"
    assert space[1]["self"]["hand"], "You can see your own hand"
    assert "hand" not in space[1]["others"][0], "You cannot see other hands"

    assert spaces.flatdim(space[1]) == (
        52
        + 52  # discarded
        + 2  # player hand
        # player bank + bet  # other player hands
        + (1 + 1) * (AGENT_COUNT - 1)
    ), "Observation space is of right shape"


def test_action_space(env):
    space = env.action_space
    assert space
    assert spaces.flatdim(space) == 23


def test_reward(env: GameWrapperEnvironment):
    assert env.reward_range[0] < 0
    assert env.reward_range[1] > 0


def test_step_needs_action(env: GameWrapperEnvironment):
    env.reset()
    corrupt_input = -99
    with pytest.raises(InvalidActionError):
        _, _, _, _ = env.step([corrupt_input, corrupt_input])


def test_invalid_action(env: GameWrapperEnvironment):
    """Ensure that invalid action will get punished

    And also observation should represent the accepted action
    """
    env.reset()
    state = env.game.s
    assert env.next_accepted_action == [ActionBetRange(state, player_id=0)]
    assert env.next_player == 0

    hit_numpy_value = env.action_factory.to_int(ActionHit())
    bet3_numpy_value = env.action_factory.to_int(ActionBet(3))
    wait_numpy_value = env.action_factory.to_int(ActionWait())

    obs, reward, _, _ = env.step([hit_numpy_value, bet3_numpy_value])

    assert reward[0] < 0
    assert reward[1] < 0
    _, reward, _, _ = env.step([wait_numpy_value, wait_numpy_value])
    assert reward[0] < 0
    assert reward[1] == Reward.VALID_ACTION
    _, reward, _, _ = env.step([bet3_numpy_value, bet3_numpy_value])
    assert reward[0] == Reward.BETTED
    assert reward[1] < 0


def test_continuous_invalid_action(env: GameWrapperEnvironment):
    """Given continous invalid action, this will eventually pick a
    random valida action
    """
    env.reset()
    state = env.game.s
    assert env.next_accepted_action == [ActionBetRange(state, player_id=0)]
    assert env.next_player == 0

    bet3_numpy_value = env.action_factory.to_int(ActionBet(3))
    wait_numpy_value = env.action_factory.to_int(ActionWait())

    # Move one step forward in the bet
    obs, reward, _, _ = env.step([bet3_numpy_value, wait_numpy_value])
    assert env.next_accepted_action == [
        ActionHitRange(state, player_id=0),
        ActionSkipRange(state, player_id=0),
    ]
    assert env.next_player == 0

    # Now let's keep giving the player bad action
    for _ in range(env.max_continuous_invalid_inputs + 1):
        obs, reward, _, _ = env.step([bet3_numpy_value, wait_numpy_value])
        assert reward[0] < 0, "Player is punished"

    games_moved = env.next_player == 1 or len(env.game.s.get_player_state(0).hand) == 3
    assert games_moved, "Automatically moved on"


def test_step(env: GameWrapperEnvironment):
    env.reset()

    action_factory = env.action_factory
    state = env.game.s

    # Note round 1: only one agent we care about!
    assert env.next_player == 0
    assert env.next_accepted_action == [ActionBetRange(state, player_id=0)]

    hit_numpy_value = env.action_factory.to_int(ActionHit())
    bet1_numpy_value = env.action_factory.to_int(ActionBet(1))
    wait_numpy_value = env.action_factory.to_int(ActionWait())

    obs, reward, terminal, info = env.step([bet1_numpy_value, wait_numpy_value])
    assert len(obs) == AGENT_COUNT
    assert len(reward) == AGENT_COUNT
    assert len(terminal) == AGENT_COUNT
    assert all([r >= 0 for r in reward]), f"not contain negative {reward}"

    # given the observation, we should be able to flatten it
    # and obtain reasonable result
    obs_space = env.observation_space
    flatten_data = obs[0]
    assert flatten_data.size == spaces.flatdim(obs_space)

    # Now we need to action again
    assert env.next_player == 0
    assert env.next_accepted_action == [
        ActionHitRange(state, 0),
        ActionSkipRange(state, 0),
    ]
    obs, reward, terminal, info = env.step([hit_numpy_value, wait_numpy_value,])
    assert len(obs) == AGENT_COUNT
    assert len(reward) == AGENT_COUNT
    assert reward[0] == Reward.HITTED
    assert len(terminal) == AGENT_COUNT
    assert all([r >= 0 for r in reward]), f"contain negative {reward}"
