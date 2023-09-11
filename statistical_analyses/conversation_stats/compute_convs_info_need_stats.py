
from statistical_analyses.utils import load_conversations


if __name__ == '__main__':

    condition = 'active'
    active_conversations = load_conversations("active", 24)
    passive_conversations = load_conversations("passive", 29)

    if condition == "active":
        all_conversations = active_conversations
    elif condition == "passive":
        all_conversations = passive_conversations
    else:
        all_conversations = active_conversations + passive_conversations

    # Get all the utterances

    with open(f"{condition}_info_type.tsv", "w") as w:
        w.write(
            f"conversation_id\tparticipant_gender\tparticipant_age\tutterance_id\tinfo_need\tinfo_need_subtype\tutterance_text\n"
        )
        for conv in all_conversations:
            conv_id = conv['conversation_id']
            conv_gender = conv['participant_gender']
            conv_age = conv['participant_age']
            for u in conv['conversation']:
                if u['information_need_type'] != "":
                    utterance_id = u['id']
                    text = u['utterance'].replace("\t", "")
                    w.write(
                        f"{conv_id}\t{conv_gender}\t{conv_age}\t{utterance_id}\t{u['information_need_type']}\t{u['information_need_subtype']}\t{text}\n"
                    )
