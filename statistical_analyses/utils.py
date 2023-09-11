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

def load_dataset(path):
    with open(path) as f:
        result = set()
        for line in f:
            line = line.strip()
            line_json = json.loads(line)
            if line_json['page_id'] not in result:
                result.add(line_json['page_id'])
    return result
