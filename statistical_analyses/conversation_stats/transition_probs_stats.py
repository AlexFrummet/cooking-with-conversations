import json
import pprint as pp


REMOVE_EDGE_PERCENTAGE = 1
RECURSIVE_REMOVE_PERCENTAGE = 1


def load_conv(path):
    with open(path) as f:
        conv = json.loads(f.read())
        if conv["keep_conversation"]:
            return conv


if __name__ == "__main__":
    active_conv = []
    passive_conv = []
    for i in range(0, 25):
        conv = load_conv(f"../../data/active/conversation_{i}.json")
        if conv is not None and conv["keep_conversation"] is True:
            active_conv.append(conv)

    for i in range(0, 30):
        conv = load_conv(f"../../data/passive/conversation_{i}.json")
        if conv is not None and conv["keep_conversation"] is True:
            passive_conv.append(conv)

    print(f"Active Conversations: {len(active_conv)}")
    print(f"Passive Conversations: {len(passive_conv)}")

    interaction_map_active = {
        "agent_question_agent_question": 0,
        "agent_question_agent_answer": 0,
        "agent_question_agent_other": 0,
        "agent_answer_agent_question": 0,
        "agent_answer_agent_answer": 0,
        "agent_answer_agent_other": 0,
        "agent_other_agent_question": 0,
        "agent_other_agent_answer": 0,
        "agent_other_agent_other": 0,
        "user_question_user_question": 0,
        "user_question_user_answer": 0,
        "user_question_user_other": 0,
        "user_answer_user_question": 0,
        "user_answer_user_answer": 0,
        "user_answer_user_other": 0,
        "user_other_user_question": 0,
        "user_other_user_answer": 0,
        "user_other_user_other": 0,
        "agent_question_user_question": 0,
        "agent_question_user_answer": 0,
        "agent_question_user_other": 0,
        "agent_answer_user_question": 0,
        "agent_answer_user_answer": 0,
        "agent_answer_user_other": 0,
        "agent_other_user_question": 0,
        "agent_other_user_answer": 0,
        "agent_other_user_other": 0,
        "user_question_agent_question": 0,
        "user_question_agent_answer": 0,
        "user_question_agent_other": 0,
        "user_answer_agent_question": 0,
        "user_answer_agent_answer": 0,
        "user_answer_agent_other": 0,
        "user_other_agent_question": 0,
        "user_other_agent_answer": 0,
        "user_other_agent_other": 0,
    }

    interaction_map_passive = {
        "agent_question_agent_question": 0,
        "agent_question_agent_answer": 0,
        "agent_question_agent_other": 0,
        "agent_answer_agent_question": 0,
        "agent_answer_agent_answer": 0,
        "agent_answer_agent_other": 0,
        "agent_other_agent_question": 0,
        "agent_other_agent_answer": 0,
        "agent_other_agent_other": 0,
        "user_question_user_question": 0,
        "user_question_user_answer": 0,
        "user_question_user_other": 0,
        "user_answer_user_question": 0,
        "user_answer_user_answer": 0,
        "user_answer_user_other": 0,
        "user_other_user_question": 0,
        "user_other_user_answer": 0,
        "user_other_user_other": 0,
        "agent_question_user_question": 0,
        "agent_question_user_answer": 0,
        "agent_question_user_other": 0,
        "agent_answer_user_question": 0,
        "agent_answer_user_answer": 0,
        "agent_answer_user_other": 0,
        "agent_other_user_question": 0,
        "agent_other_user_answer": 0,
        "agent_other_user_other": 0,
        "user_question_agent_question": 0,
        "user_question_agent_answer": 0,
        "user_question_agent_other": 0,
        "user_answer_agent_question": 0,
        "user_answer_agent_answer": 0,
        "user_answer_agent_other": 0,
        "user_other_agent_question": 0,
        "user_other_agent_answer": 0,
        "user_other_agent_other": 0,
    }

    # Notice that in the interaction agent has rows and user has columns

    for conv in active_conv:
        current_key = ""
        for utterance in conv["conversation"]:
            if utterance["dialogue_act"] != "":
                if current_key == "":
                    current_key = (
                        f'{utterance["participant"]}_{utterance["dialogue_act"]}_'
                    )
                    continue
                else:
                    current_key = f'{current_key}{utterance["participant"]}_{utterance["dialogue_act"]}'
                    interaction_map_active[current_key] += 1
                    current_key = (
                        f'{utterance["participant"]}_{utterance["dialogue_act"]}_'
                    )
    active_total = sum([value for value in interaction_map_active.values()])
    for key, value in interaction_map_active.items():
        interaction_map_active[key] = round(value / active_total * 100, 2)

    for conv in passive_conv:
        current_key = ""
        for utterance in conv["conversation"]:
            if utterance["dialogue_act"] != "":
                if current_key == "":
                    current_key = (
                        f'{utterance["participant"]}_{utterance["dialogue_act"]}_'
                    )
                    continue
                else:
                    current_key = f'{current_key}{utterance["participant"]}_{utterance["dialogue_act"]}'
                    interaction_map_passive[current_key] += 1
                    current_key = (
                        f'{utterance["participant"]}_{utterance["dialogue_act"]}_'
                    )
    passive_total = sum([value for value in interaction_map_passive.values()])
    for key, value in interaction_map_passive.items():
        interaction_map_passive[key] = round(value / passive_total * 100, 2)

    print("Interaction Map Active")
    pp.pprint(interaction_map_active)
    print("Interaction Map Passive")
    pp.pprint(interaction_map_passive)
    # cols_rows = [
    #     ("agent_question", 0),
    #     ("agent_answer", 1),
    #     ("agent_other", 2),
    #     ("user_question", 3),
    #     ("user_answer", 4),
    #     ("user_other", 5),
    # ]
    # result_matrix = [
    #     [0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0],
    # ]
    # print(len(interaction_map_active.keys()))
    # combinations = []
    # for col, row in itertools.product(cols_rows, cols_rows):
    #     combinations.append((col, row))

    # for col, row in combinations:
    #     result_matrix[col[1]][row[1]] = interaction_map_active[f"{col[0]}_{row[0]}"]

    # with open("active_transition_prob_chart.tsv", "w") as w:
    #     title = "\t".join([" "] + [col[0] for col in cols_rows])
    #     w.write(f"{title}\n")
    #     for index, line in enumerate(result_matrix):
    #         line = [str(el) for el in line]
    #         to_write_line = [cols_rows[index][0]] + line
    #         to_write_line = "\t".join(to_write_line)
    #         w.write(f"{to_write_line}\n")
