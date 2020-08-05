from gym.spaces import Space
from typing import Union, Optional

from ray.rllib.env.base_env import BaseEnv
from ray.rllib.models.action_dist import ActionDistribution
from ray.rllib.models.modelv2 import ModelV2
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.utils.annotations import DeveloperAPI
from ray.rllib.utils.framework import try_import_torch, TensorType


torch, nn = try_import_torch()


@DeveloperAPI
class Exploration:
    """Implements an exploration strategy for Policies.

    An Exploration takes model outputs, a distribution, and a timestep from
    the agent and computes an action to apply to the environment using an
    implemented exploration schema.
    """

    def __init__(self, action_space: Space, *, framework: str,
                 policy_config: dict, model: ModelV2, num_workers: int,
                 worker_index: int):
        """
        Args:
            action_space (Space): The action space in which to explore.
            framework (str): One of "tf" or "torch".
            policy_config (dict): The Policy's config dict.
            model (ModelV2): The Policy's model.
            num_workers (int): The overall number of workers used.
            worker_index (int): The index of the worker using this class.
        """
        self.action_space = action_space
        self.policy_config = policy_config
        self.model = model
        self.num_workers = num_workers
        self.worker_index = worker_index
        self.framework = framework
        # The device on which the Model has been placed.
        # This Exploration will be on the same device.
        self.device = None
        if isinstance(self.model, nn.Module):
            params = list(self.model.parameters())
            if params:
                self.device = params[0].device

    @DeveloperAPI
    def before_compute_actions(self,
                               *,
                               timestep: Optional[int] = None,
                               explore: bool = False,
                               tf_sess: Optional["tf.Session"] = None,
                               **kwargs):
        """Hook for preparations before policy.compute_actions() is called.

        Args:
            timestep (Optional[int]): An optional timestep tensor.
            explore (bool): An optional explore boolean flag.
            tf_sess (Optional[tf.Session]): The tf-session object to use.
            **kwargs: Forward compatibility kwargs.
        """
        pass

    @DeveloperAPI
    def get_exploration_action(self,
                               *,
                               action_distribution: ActionDistribution,
                               timestep: Union[int, TensorType],
                               explore: bool = True):
        """Returns a (possibly) exploratory action and its log-likelihood.

        Given the Model's logits outputs and action distribution, returns an
        exploratory action.

        Args:
            action_distribution (ActionDistribution): The instantiated
                ActionDistribution object to work with when creating
                exploration actions.
            timestep (int|TensorType): The current sampling time step. It can
                be a tensor for TF graph mode, otherwise an integer.
            explore (bool): True: "Normal" exploration behavior.
                False: Suppress all exploratory behavior and return
                    a deterministic action.

        Returns:
            Tuple:
            - The chosen exploration action or a tf-op to fetch the exploration
              action from the graph.
            - The log-likelihood of the exploration action.
        """
        pass

    @DeveloperAPI
    def on_episode_start(self,
                         policy: "Policy",
                         *,
                         environment: BaseEnv = None,
                         episode: int = None,
                         tf_sess: Optional["tf.Session"] = None):
        """Handles necessary exploration logic at the beginning of an episode.

        Args:
            policy (Policy): The Policy object that holds this Exploration.
            environment (BaseEnv): The environment object we are acting in.
            episode (int): The number of the episode that is starting.
            tf_sess (Optional[tf.Session]): In case of tf, the session object.
        """
        pass

    @DeveloperAPI
    def on_episode_end(self,
                       policy: "Policy",
                       *,
                       environment: BaseEnv = None,
                       episode: int = None,
                       tf_sess: Optional["tf.Session"] = None):
        """Handles necessary exploration logic at the end of an episode.

        Args:
            policy (Policy): The Policy object that holds this Exploration.
            environment (BaseEnv): The environment object we are acting in.
            episode (int): The number of the episode that is starting.
            tf_sess (Optional[tf.Session]): In case of tf, the session object.
        """
        pass

    @DeveloperAPI
    def postprocess_trajectory(self,
                               policy: "Policy",
                               sample_batch: SampleBatch,
                               tf_sess: Optional["tf.Session"] = None):
        """Handles post-processing of done episode trajectories.

        Changes the given batch in place. This callback is invoked by the
        sampler after policy.postprocess_trajectory() is called.

        Args:
            policy (Policy): The owning policy object.
            sample_batch (SampleBatch): The SampleBatch object to post-process.
            tf_sess (Optional[tf.Session]): An optional tf.Session object.
        """
        return sample_batch

    @DeveloperAPI
    def get_info(self, sess: Optional["tf.Session"] = None):
        """Returns a description of the current exploration state.

        This is not necessarily the state itself (and cannot be used in
        set_state!), but rather useful (e.g. debugging) information.

        Args:
            sess (Optional[tf.Session]): An optional tf Session object to use.

        Returns:
            dict: A description of the Exploration (not necessarily its state).
                This may include tf.ops as values in graph mode.
        """
        return {}
