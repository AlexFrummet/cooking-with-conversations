

from statistical_analyses.utils import load_conversations


if __name__ == '__main__':

    active_conversations = load_conversations('active', 24)
    passive_conversations = load_conversations('passive', 29)

    stats_dict = {
        "active": {
            "agent": [],
            "user": []
        },
        "passive": {
            "agent": [],
            "user": []
        }
    }

    for active_conv in active_conversations:
        utterances = active_conv['conversation']
        for u in utterances:
            if u['interaction_type'] == 'text':
                stats_dict['active'][u['participant']].append(
                    len(u['utterance']))

    for passive_conv in passive_conversations:
        utterances = passive_conv['conversation']
        for u in utterances:
            if u['interaction_type'] == 'text':
                stats_dict['passive'][u['participant']].append(
                    len(u['utterance']))

    max_length = max(len(stats_dict['active']['agent']),
                     len(stats_dict['active']['user']),
                     len(stats_dict['passive']['agent']),
                     len(stats_dict['passive']['user']))

    # Add padding zeros to match columns length 
    for key, value in stats_dict.items():
        for participant, inner_list in value.items():
            l = len(inner_list)
            if l < max_length:
                for i in range(max_length - l):
                    stats_dict[key][participant].append(0)


    active_agent = stats_dict['active']['agent']
    active_user = stats_dict['active']['user']
    passive_agent = stats_dict['passive']['agent']
    passive_user = stats_dict['passive']['user']
    with open("utterances_length_stats.tsv", 'w') as w:
        w.write("active_agent\tactive_user\tpassive_agent\tpassive_user\n")
        for a, b, c, d in zip(active_agent, active_user, passive_agent,
                              passive_user):
            w.write(f"{a}\t{b}\t{c}\t{d}\n")
