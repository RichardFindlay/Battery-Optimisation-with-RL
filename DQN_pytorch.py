import torch 
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# define model architecture
class QNet(nn.Module):
	""" Policy Model """
	def __init__(self, state_size, action_size, seed, fc1_units=64, fc2_units=64):
		super(QNet, self).__init__()
		self.seed = torch.manual_seed(seed)
		self.dense1 = nn.Linear(state_size, fc1_units)
		self.dense2 = nn.Linear(fc1_units, fc2_units)
		self.dense3 = nn.Linear(fc2_units, action_size)

	def forward(self, states):
		""" map state values to action values """
		x = F.relu(self.dense1(states))
		x = F.relue(self.dense2(x))
		return self.dense3(x)

# replay buffer object
class Replay():
	def __init__(self, action_size, buffer_size, batch_size, seed):
		self.action_size = action_size
		self.memory = deque(maxlen=buffer_size)
		self.batch_size = batch_size
		self.experiences = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
		self.seed = random.seed(seed)

	def add(self, state, action, reward, next_state, done):
		e = self.experiences(state, action, reward, next_state, done)
		self.memory.append(e)

	def sample(self):
		""" randomly sample experiences from memory """
		experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)

        return (states,actions,rewards,next_states,dones)

	def __len__(self):
		""" get current size of samples in memory """
		return len(self.memory)

# DQN Agent
class DQN_Agent()
	def __init__(self, state_size, action_size, seed):
		self.state_size = state_size
		self.action_size = action_size

		# Intialise q-networks
		self.qnet = QNet(state_size, action_size, seed).to(device)
		self.qnet_target = QNet(state_size, action_size, seed).to(device)

		# define optimiser
		self.optimizer = optim.Adam(self.qnetwork_local.parameters(), lr=learning_rate)

		# Replay Memory 
		self.memory = Replay(action_size, buffer_size, batch_size, seed)
		self.t_step = 0

	def step(self, state, action, reward, next_step, done):

		# save expereince in model
		self.memory.add(state, action, reward, next_step, done)

		# learn every 'x' time-steps
		self.t_step = (self.t_step+1) % '__UPDATE__'

		if self.t_step == 0:
			if len(self.memory) > batch_size:
				experience = self.memory.sample()
				self.learn(experience, GAMMA)


	def action(self, state, epsilion = 0):
		""" return action for given state given current policy """
		state = torch.from_numpy(state).float().unsqueeze(0).to(device)
		self.qnet.eval()

		with troch.no_grad():
			action_values = self.qnet(state)

		self.qnet.train()

		# action selection relative to greedy action selection
		if random.random() > epsilion:
			return np.argmax(action_values.cpu().data.numpy())
		else
			return random.choice(np.arange(self.action_size))


	def learn(self, experiences, gamma):
		states, actions, rewards, next_state, dones = experiences

		criterion = torch.nn.MSELoss()

		# local model used to train
		self.qnet.train()

		# target model used in eval mode
		self.qnet_target.eval()

		predicted_targets = self.qnet(next_states).gather(1,actions)

		with torch.no_grad():
			laebls_next = self.qnet_target(next_states).detach().max(1)[0].unsqueeze(1)

		labels = rewards + (gamma * labels_next * (1-dones))

		loss = criterion(predicted_targets, labels).to(device)
		self.optimizer.zero_grad()
		loss.backward()
		self.optimizer.step()

		# now update the target next weights
		self.soft_update(self.qnet, self.qnet_target, tau)


	def soft_updated(self, local_model, target_model, tau):

		"""Soft update model parameters.
        θ_target = τ*θ_local + (1 - τ)*θ_target """

		for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
			target.data.copy_(tau * local_param.data + (1 - tau) * target_param.data)








def main1():
	n_episodes = 200
	time_range = 168

	gamma = 1.0
	epsilon = 1.0

	dqn_agent = DQN_Agent()
	scores= [] #list of rewards from each episode
	

	for ep in range(n_episodes):
		episode_rew = 0
		cur_state = env.reset()

		for step in range(time_range):
			# print('step: %s' %(step)) 
			action = dqn_agent.action(cur_state, epsilon)
			new_state, reward, done, _ = env.step(action)

			dqn_agent.step(cur_state, action, reward, new_state, done)

			dqn_agent.replay()
			dqn_agent.target_train()

			cur_state = new_state
			episode_rew += reward 

			if done:
				break

		scores.append(episode_rew)
		# epsilon = epsilon - (2/episodes) if epsilon > 0.01 else 0.01
		epsilon = max(eps*eps_decay,eps_end)

		print("Episode:{}\n Reward:{}\n Epsilon:{}".format(ep, episode_rew, epsilon))

	torch.save(dqn_agent.qnet.state_dict(),'checkpoint.pth')

	fig, ax = plt.subplots()
	ax.plot(scores)
	ax.grid()
	plt.show()








