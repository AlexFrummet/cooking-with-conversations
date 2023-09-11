from collections import OrderedDict
import json


def load_conversations(condition, number_conversations):
    results = []
    for i in range(number_conversations):
        with open(f'../../data/{condition}/conversation_{i}.json') as f:
            conversation_dict = json.loads(f.read(),
                                           object_pairs_hook=OrderedDict)
            if conversation_dict['keep_conversation']:
                results.append(conversation_dict)

    return results


if __name__ == '__main__':

    active_conversations = load_conversations('active', 24)
    passive_conversations = load_conversations('passive', 29)

    all_conversations = active_conversations + passive_conversations

    ages_dict = {}
    for conv in all_conversations:
        age_bracked = conv['participant_age']

        if age_bracked not in ages_dict:
            ages_dict[age_bracked] = 1
        else:
            ages_dict[age_bracked] += 1

    for key, value in ages_dict.items():
        print(f"{key}: {value}")
