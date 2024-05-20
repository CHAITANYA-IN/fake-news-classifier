import sys
import random
import numpy as np
import matplotlib.pyplot as plt


class Voter:
    def __init__(self, is_registered=False, is_malicious=0):
        self.trustworthiness = {}
        self.topic_votes = {}
        self.totalVotes = {'Politics': 0, 'Technology': 0}
        self.topicCorrectVotes = {'Politics': 0, 'Technology': 0}
        self.expertise_topics = []
        self.deposit = 0
        self.reputation = 0
        # This attribute may need further clarification or modification
        self.last_vote_timestamp = 0
        self.registered = is_registered
        self.is_malicious = is_malicious

    def check_malicious(self):
        return self.is_malicious


class FakeNewsDApp:
    def __init__(self, reputation_decay_rate, base_discount, min_reputation_threshold, voting_deposit):
        self.voters = {}
        self.news_votes = {}
        self.news_outcome = {}
        self.total_deposits = 0
        self.reputation_decay_rate = reputation_decay_rate
        self.base_discount = base_discount
        self.min_reputation_threshold = min_reputation_threshold
        self.voting_deposit = voting_deposit
        self.registered_fact_checkers = []
        self.all_topics = ['Politics', 'Technology']
        self.news_topics = {}
        self.reputation_points_on_voting = 10
        self.max_vote_on_scale = 10
        self.p = 0.7

    def register_fact_checker(self, user_address, is_malicious):
        voter = Voter(is_registered=True, is_malicious=is_malicious)
        voter.expertise_topics = self.get_user_expertise_topics_from_external_source(
            user_address)
        self.bootstrap_trustworthiness(voter)
        self.voters[user_address] = voter
        self.registered_fact_checkers.append(user_address)

    def bootstrap_trustworthiness(self, voter):
        for topic in self.all_topics:
            voter.trustworthiness[topic] = 0.5
        for topic in voter.expertise_topics:
            voter.trustworthiness[topic] = 0.67

    def get_user_expertise_topics_from_external_source(self, user_address):
        # Simulated logic to fetch expertise topics from an external source
        # expertise_topics = ['Politics', 'Technology']
        expertise_topics = ['Politics']
        return expertise_topics

    def vote_on_news(self, user_address, news_item_id):
        voter = self.voters[user_address]
        news_topic = self.get_topic_for_news(news_item_id)
        vote = self.get_vote(user_address, news_item_id)
        voter.topic_votes[news_item_id] = vote
        voter.totalVotes[news_topic] += 1
        voter.deposit += self.voting_deposit

    def get_vote(self, user_address, news_item_id):
        # Simulated function to fetch vote from the user
        voter = self.voters[user_address]
        if voter.check_malicious():
            return 0

        news_topic = self.get_topic_for_news(news_item_id)
        if user_address < self.p*100:
            if news_topic in voter.expertise_topics and random.random() < 0.9:
                # if voter.trustworthiness[news_topic] > 0.67 :
                return self.max_vote_on_scale
            else:
                return random.randint(0, self.max_vote_on_scale)
        if news_topic in voter.expertise_topics and random.random() < 0.7:
            return self.max_vote_on_scale
        return random.randint(3, self.max_vote_on_scale-3)

    def get_final_outcome(self, news_item_id):
        # Initialize variables for weighted sum of votes and total trustworthiness
        weighted_sum = 0
        total_trustworthiness = 0
        # Get the topic corresponding to the news
        news_topic = self.get_topic_for_news(news_item_id)
        # Loop through all registered fact-checkers
        for voter_address in self.registered_fact_checkers:
            voter = self.voters[voter_address]
            # Calculate the weighted vote of the current voter
            weighted_vote = voter.topic_votes.get(
                news_item_id, 0) * voter.trustworthiness.get(news_topic, 0)
            # Add the weighted vote to the weighted sum
            weighted_sum += weighted_vote

            # Add the trustworthiness of the current voter to the total trustworthiness
            total_trustworthiness += voter.trustworthiness.get(news_topic, 0)

        # Calculate final outcome
        if total_trustworthiness == 0:
            final_outcome = 0  # Avoid division by zero
        else:
            final_outcome = weighted_sum / total_trustworthiness
        return final_outcome > 0.5

    def evaluate_trustworthiness(self, user_address, news_item_id):
        outcome = self.news_outcome.get(news_item_id, 0)
        vote = self.voters[user_address].topic_votes[news_item_id]
        news_topic = self.get_topic_for_news(news_item_id)
        if (vote > 5 and outcome == 1) or (vote <= 5 and outcome == 0):
            self.voters[user_address].topicCorrectVotes[news_topic] += 1
            self.voters[user_address].reputation += self.reputation_points_on_voting * (
                1 - vote / self.max_vote_on_scale) if outcome == 0 else self.reputation_points_on_voting * vote / self.max_vote_on_scale
        else:
            self.voters[user_address].deposit -= self.voting_deposit
            self.voters[user_address].reputation -= self.reputation_points_on_voting * (
                1 - vote / self.max_vote_on_scale) if outcome == 0 else self.reputation_points_on_voting * vote / self.max_vote_on_scale

        self.voters[user_address].trustworthiness[news_topic] = self.voters[user_address].topicCorrectVotes[news_topic] / \
            self.voters[user_address].totalVotes[news_topic]

    def get_topic_for_news(self, news_item_id):
        # Simulated function to get the topic for a news item
        return self.news_topics[news_item_id]

    def set_topic_for_news(self, news_item_id):
        # self.news_topics[news_item_id] = random.choice(['Politics', 'Technology'])
        self.news_topics[news_item_id] = 'Politics'


# Simulation parameters
num_voters = int(sys.argv[1])
p_honest = float(sys.argv[2])  # Fraction of honest voters who are trustworthy
q_malicious = float(sys.argv[3])  # Fraction of malicious voters
# Number of iterations for updating trustworthiness estimates
num_news_articles_to_be_fact_checked = int(sys.argv[4])

# Initialize the FakeNewsDApp
fake_news_dapp = FakeNewsDApp(
    reputation_decay_rate=0.1, base_discount=0.1, min_reputation_threshold=0.5, voting_deposit=1)

# Register voters
for i in range(num_voters):
    is_honest = i < p_honest*num_voters
    if is_honest:
        fake_news_dapp.register_fact_checker(i, is_malicious=0)  # "HonestUser"
    else:
        fake_news_dapp.register_fact_checker(
            i, is_malicious=1)  # MAlicious user

# Simulate voting
for _ in range(num_news_articles_to_be_fact_checked):
    news_item_id = "NewsItem" + str(random.randint(1, 100))
    fake_news_dapp.set_topic_for_news(news_item_id)
    for user_address in fake_news_dapp.voters:
        # news_item_id = "NewsItem" + str(random.randint(1, 100))
        fake_news_dapp.vote_on_news(user_address, news_item_id)
    # Calculate and set the outcome
    outcome = fake_news_dapp.get_final_outcome(news_item_id)
    fake_news_dapp.news_outcome[news_item_id] = outcome
    # print (outcome)
    for user_address in fake_news_dapp.voters:
        fake_news_dapp.evaluate_trustworthiness(user_address, news_item_id)

users = []
trustw = []

# Print trustworthiness estimates
for user_address, voter in fake_news_dapp.voters.items():
    print("Trustworthiness Estimates for",
          user_address, voter.check_malicious() == 1)
    users.append(user_address)
    for topic, trustworthiness in voter.trustworthiness.items():
        if (topic == 'Politics'):
            trustw.append(trustworthiness)
        print(f"Topic: {topic}, Trustworthiness: {trustworthiness}")


def plot_bar_graph(x_values, y_values):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set x-ticks from 0 to 1 with a step size of 0.01
    x_ticks = np.arange(0, 1.1, 0.1)
    ax.set_xticks(x_ticks)

    # Plot bars for each value in x_values and y_values
    ax.bar(x_values, y_values, color='skyblue', edgecolor='black', width=0.001)

    # Set labels and title
    ax.set_xlabel('Trustworthiness')
    ax.set_ylabel('NUmber of Users')
    ax.set_title('Bar Graph')

    plt.savefig(
        f'results/{num_voters}_Voters{p_honest}_T{q_malicious}_M{num_news_articles_to_be_fact_checked}_Articles.png')
    # Show the plot
    plt.show()


def plot_trustworthiness_distribution(users, trustworthiness):
    trustworthiness_counts = {}
    for element in trustworthiness:
        if element in trustworthiness_counts:
            trustworthiness_counts[element] += 1
        else:
            trustworthiness_counts[element] = 1

    print(trustworthiness_counts)

    x_values = []
    y_values = []

    x_values = sorted(trustworthiness_counts.keys())
    y_values = list(trustworthiness_counts.values())

    print(x_values)
    print(y_values)

    x_values_all = np.arange(0, 1.001, 0.001)

    # Initialize y_values for missing x_values with 0

    y_values_all = [y_values[x_values.index(
        x)] if x in x_values else 0 for x in x_values_all]

    print(y_values_all)
    # Plot the bar graph
    plot_bar_graph(x_values_all, y_values_all)


plot_trustworthiness_distribution(users, trustw)
