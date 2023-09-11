import pprint as pp

from statistical_analyses.utils import load_conversations




if __name__ == '__main__':

    active_conversations = load_conversations('active', 24)
    passive_conversations = load_conversations('passive', 29)

    all_conversations = active_conversations + passive_conversations


    types = {}
    total_info_need = 0
    for conv in active_conversations:
        for u in conv['conversation']:
            info_need = u['information_need_type']
            info_need_sub = u['information_need_subtype']
            if info_need_sub != "":
                if info_need_sub not in types:
                    types[info_need_sub] = 1
                else:
                    types[info_need_sub] += 1
            if info_need != '':
                total_info_need += 1

    print("Active:")
    print(total_info_need)
    pp.pprint(types)
    print("="*20)

    types = {}
    total_info_need = 0
    for conv in passive_conversations:
        for u in conv['conversation']:
            info_need = u['information_need_type']
            info_need_sub = u['information_need_subtype']
            if info_need_sub != "":
                if info_need_sub not in types:
                    types[info_need_sub] = 1
                else:
                    types[info_need_sub] += 1
            if info_need != '':
                total_info_need += 1

    print("Passive:")
    print(total_info_need)
    pp.pprint(types)
    print("="*20)

    types = {}
    total_info_need = 0
    for conv in all_conversations:
        for u in conv['conversation']:
            info_need = u['information_need_type']
            info_need_sub = u['information_need_subtype']
            if info_need_sub != "":
                if info_need_sub not in types:
                    types[info_need_sub] = 1
                else:
                    types[info_need_sub] += 1
            if info_need != '':
                total_info_need += 1

    print("All Conversations:")
    print(total_info_need)
    pp.pprint(types)
    print("="*20)
