import numpy as np
import math

class BanditAlgorithms:
    """
    A class that encapsulates different bandit algorithms including LinUCB, UCB,
    epsilon-greedy, and pure-greedy.
    """

    def __init__(self, alpha, pd_feature_input, pd_reward_input, n_trial, n_feature, n_arms):
        self.alpha = alpha
        self.pd_feature_input = pd_feature_input
        self.pd_reward_input = pd_reward_input
        self.n_trial = n_trial
        self.n_feature = n_feature
        self.n_arms = n_arms

    def linUCB_disjoint(self):
        # 1. Initialize object
        # 1.1. Output object
        arm_choice_output = np.empty(self.n_trial)  # store arm choice (integer) for each trial
        r_payoff = np.empty(self.n_trial)  # store payoff (float) for each trial
        theta = np.empty(shape=(self.n_trial, self.n_arms, self.n_feature))  # record theta over each trial (n_arms, n_feature) per trial
        p = np.empty(shape=(self.n_trial, self.n_arms))  # predictions for reward of each arm for each trial

        # 1.2 Intermediate object
        A = np.array([np.diag(np.ones(shape=self.n_feature)) for _ in np.arange(self.n_arms)])
        b = np.array([np.zeros(shape=self.n_feature) for _ in np.arange(self.n_arms)])

        # 2. Algo
        for t in np.arange(self.n_trial):
            # Compute estimates (theta) and prediction (p) for all arms
            for a in np.arange(self.n_arms):
                inv_A = np.linalg.inv(A[a])
                theta[t, a] = inv_A.dot(b[a])
                p[t, a] = theta[t, a].dot(self.pd_feature_input[t, a]) + self.alpha * np.sqrt(self.pd_feature_input[t, a].dot(inv_A).dot(self.pd_feature_input[t, a]))

            # Choosing best arms
            chosen_arm = np.argmax(p[t])
            x_chosen_arm = self.pd_feature_input[t, chosen_arm]
            r_payoff[t] = self.pd_feature_input[chosen_arm, t]

            arm_choice_output[t] = chosen_arm

            # update intermediate objects (A and b)
            A[chosen_arm] += np.outer(x_chosen_arm, x_chosen_arm.T)
            b[chosen_arm] += r_payoff[t] * x_chosen_arm
            # update_alpha(alpha_input, t, 3)
        return dict(theta=theta, p=p, arm_choice=arm_choice_output, r_payoff=r_payoff, name = "linucb")


    # different modes to update alpha
    def update_alpha(alpha_input, t, mode=1):
        if t > 0:
            if mode == 1:
                alpha_input = alpha_input / t
            elif mode == 2:
                    alpha_input = 1 / t
            elif mode == 3:
                    alpha_input = alpha_input / 2
        return alpha_input

    def tcp_ucb_algorithm(alpha, pd_feature_input, pd_reward_input, n_trail, n_feature, n_arms):
        arm_choice_output = np.empty(n_trail)  # store arm choice (integer) for each trial
        arm_choice_num = np.ones(shape=(n_trail, n_arms))
        reward_arm = np.empty(shape=(n_trail, n_arms))
        average_reward_arm = np.empty(shape=(n_trail, n_arms))
        confidence_arm = np.empty(shape=(n_trail, n_arms))
        ucb_arm = np.empty(shape=(n_trail, n_arms))  # predictions for reward of each arm for each trial
        chosen_arm = 0
        cumulative_reward = np.empty(n_trail)
        # 2. Algo
        for t in np.arange(n_trail):
            if t == 0:
                continue

            reward_arm[t][chosen_arm] = reward_arm[t][chosen_arm] + pd_reward_input[chosen_arm][t]
            arm_choice_num[t][chosen_arm] = arm_choice_num[t][chosen_arm] + 1
            # calculate profit for chosen arm
            average_reward_arm[t][chosen_arm] = (reward_arm[t][chosen_arm] / arm_choice_num[t][chosen_arm])

            confidence_arm[t][chosen_arm] = (2 * math.log(t) / (1 * arm_choice_num[t][chosen_arm])) ** 0.5
            ucb_arm[t][chosen_arm] = average_reward_arm[t][chosen_arm] + alpha * confidence_arm[t][chosen_arm]

            # Choosing best arms
            chosen_arm = np.argmax(ucb_arm[t])
            arm_choice_output[t] = chosen_arm
            cumulative_reward[t] += cumulative_reward[t - 1] + pd_reward_input[chosen_arm][t]

        total_reward = np.sum(pd_reward_input.T * (arm_choice_output[:, np.newaxis] == np.arange(n_arms)),
                              axis=(0, 1))
        return dict(arm_choice=arm_choice_output, ucb_arm=ucb_arm, name=__name__, param="alpha",
                    total_reward=total_reward,
                    cumulative_reward=cumulative_reward)

    def epsilon_greedy(self, epsilon):
        chosen_arms = np.empty(self.n_trail)  # Store chosen arm for each trial
        arm_rewards = np.empty(shape=(self.n_trail, self.n_arms))  # Store rewards for each arm for each trial

        q_values = np.zeros(self.n_actions)  # Initialize Q-values for each action
        action_counts = np.zeros(self.n_actions)  # Track the number of times each action is chosen
        cumulative_reward = np.zeros(self.n_trail)
        total_reward = 0  # Cumulative total reward

        for t in range(self.n_trail):
            # Explore or exploit
            if np.random.random() < epsilon:
                # Explore: Choose a random action
                action = np.random.choice(np.arange(self.n_actions))
            else:
                # Exploit: Choose the action with the highest Q-value
                action = np.argmax(q_values)

            # Execute the chosen action and observe the reward
            reward = self.pd_reward_input[action][t]

            # Update the Q-value of the chosen action
            action_counts[action] += 1
            n = action_counts[action]
            q_values[action] = ((n - 1) / n) * q_values[action] + 1 / n * reward

            chosen_arms[t] = action
            arm_rewards[t] = self.pd_reward_input[:, t]
            if t > 0:
                cumulative_reward[t] = cumulative_reward[t - 1] + reward
            total_reward += reward

        return {
            'chosen_arms': chosen_arms,
            'arm_rewards': arm_rewards,
            'total_reward': total_reward,
            'cumulative_reward': cumulative_reward,
            'name': 'epsilon-greedy',
            'param': epsilon
        }

    def pure_greedy(self):


        chosen_arms = np.empty(self.n_trail)  # Store chosen arm for each trial
        arm_rewards = np.empty(shape=(self.n_trail, self.n_arms))  # Store rewards for each arm for each trial
        cumulative_reward = np.zeros(self.n_trail)
        q_values = np.zeros(self.n_actions)  # Initialize Q-values for each action

        total_reward = 0  # Cumulative total reward

        for t in range(self.n_trail):
            # Choose the action with the highest Q-value
            action = np.argmax(q_values)

            # Execute the chosen action and observe the reward
            reward = self.pd_reward_input[action][t]

            # Update the Q-value of the chosen action
            q_values[action] += (1 / (t + 1)) * (reward - q_values[action])

            chosen_arms[t] = action
            arm_rewards[t] = self.pd_reward_input[:, t]
            if t > 0:
                cumulative_reward[t] = cumulative_reward[t - 1] + reward
            total_reward += reward

        return {
            'chosen_arms': chosen_arms,
            'arm_rewards': arm_rewards,
            'total_reward': total_reward,
            'cumulative_reward': cumulative_reward,
            'name': 'pure-greedy',
            'param': None
        }



