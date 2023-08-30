from collections import OrderedDict
import json
from tabulate import tabulate


def load_conversations(condition, number_conversations):
    results = []
    for i in range(number_conversations):
        with open(f'../../data/{condition}/conversation_{i}.json') as f:
            conversation_dict = json.loads(f.read(),
                                           object_pairs_hook=OrderedDict)

            if conversation_dict['keep_conversation']:
                results.append(conversation_dict)

    return results


def compute_duration_in_minutes(previous_timestamp, current_timestamp):
    return (current_timestamp - previous_timestamp) / 60 / 1000


def compute_conversation_duration(conversation):

    conversation = conversation['conversation']
    previous_timestamp = conversation[0]['timestamp']
    current_timestamp = conversation[-1]['timestamp']

    return compute_duration_in_minutes(previous_timestamp, current_timestamp)


if __name__ == '__main__':

    active_conversations = load_conversations('active', 24)
    passive_conversations = load_conversations('passive', 29)

    active_durations = []
    passive_durations = []

    print("=============== Active Conversations ===============")
    for index, conv in enumerate(active_conversations):
        print(f"conversation_{index}")

        duration_in_minutes = compute_conversation_duration(conv)

        data = [[duration_in_minutes]]
        active_durations.append(duration_in_minutes)
        print(
            tabulate(data,
                     headers=['Duration in minutes'],
                     tablefmt="fancy_grid"))

    print(f"Active longest conversation in minutes: {max(active_durations)}")
    print(
        f"Active average duration in minutes: {sum(active_durations) / len(active_conversations)}"
    )
    print("\n=============== Passive Conversations ===============\n")
    for index, conv in enumerate(passive_conversations):
        print(f"conversation_{index}")

        duration_in_minutes = compute_conversation_duration(conv)

        data = [[duration_in_minutes]]
        passive_durations.append(duration_in_minutes)
        print(
            tabulate(data,
                     headers=['Duration in minutes'],
                     tablefmt="fancy_grid"))

    print(f"Passive longest conversation in minutes: {max(passive_durations)}")
    print(
        f"Passive average duration in minutes: {sum(passive_durations)/ len(passive_conversations)}"
    )
