from collections import OrderedDict
import json
from tabulate import tabulate


def load_conversations(condition, number_conversations):
    results = []
    for i in range(number_conversations):
        with open(f'../../data/{condition}/conversation_{i}.json') as f:
            conversation_dict = json.loads(f.read(),
                                           object_pairs_hook=OrderedDict)

            results.append(conversation_dict)

    return results


def length_utterances(conversation, participant=None):
    number_utterances = 0
    total_utterance_length = 0

    for utterance in conversation['conversation']:
        if participant is None and utterance['interaction_type'] == 'text':
            number_utterances += 1
            total_utterance_length += len(utterance['utterance'])
            continue

        if participant == utterance['participant'] and utterance[
                'interaction_type'] == 'text':
            number_utterances += 1
            total_utterance_length += len(utterance['utterance'])

    return (total_utterance_length, number_utterances)


if __name__ == '__main__':

    active_conversations = load_conversations('active', 24)
    passive_conversations = load_conversations('passive', 29)

    total_active = 0
    total_passive = 0

    print("=============== Active Conversations ===============")
    for index, conv in enumerate(active_conversations):
        print(f"conversation_{index}")
        u_total_utterance_length, u_number_utterances = length_utterances(
            conv, 'user')
        a_total_utterance_length, a_number_utterances = length_utterances(
            conv, 'agent')

        total_active += (u_number_utterances + a_number_utterances)

        data = [[
            'Agent', a_number_utterances,
            round(a_total_utterance_length / a_number_utterances, 2)
        ],
                [
                    'User', u_number_utterances,
                    round(u_total_utterance_length / u_number_utterances, 2)
                ]]
        print(
            tabulate(data,
                     headers=['Participant', 'N. Utterances', 'Avg. Length'],
                     tablefmt="fancy_grid"))

    print("\n=============== Passive Conversations ===============\n")
    for index, conv in enumerate(passive_conversations):
        print(f"conversation_{index}")
        u_total_utterance_length, u_number_utterances = length_utterances(
            conv, 'user')
        a_total_utterance_length, a_number_utterances = length_utterances(
            conv, 'agent')

        total_passive += (u_number_utterances + a_number_utterances)

        data = [[
            'Agent', a_number_utterances,
            round(a_total_utterance_length / a_number_utterances, 2)
        ],
                [
                    'User', u_number_utterances,
                    round(u_total_utterance_length / u_number_utterances, 2)
                ]]
        print(
            tabulate(data,
                     headers=['Participant', 'N. Utterances', 'Avg. Length'],
                     tablefmt="fancy_grid"))

print(
    f"Avg. number of utterances for Active condition across all {len(active_conversations)} conversations: {total_active/len(active_conversations)}"
)

print(
    f"Avg. number of utterances for Passive condition across all {len(passive_conversations)} conversations: {total_passive/len(active_conversations)}"
)
