from statistical_analyses.utils import load_conversations, load_dataset


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

    how_tos_ids = load_dataset(
        'serious_eats_anserini_v1.json'
    )
    recipes_ids = load_dataset(
        'serious_eats_anserini_recipes_v1.json'
    )

    

    info_nuggets = {}
    with open("cooking-with-conversations/statistical_analyses/woz_data_analysis_files/information_nuggets_final_cleaned.tsv") as f:
        for line in f:
            line = line.strip()
            line = line.split("\t")
            id = line[0]
            nuggets = line[6:9]
            info_nuggets[id] = nuggets

    utterances = {}
    # Get all the utterances

    for conv in all_conversations:
        for u in conv['conversation']:
            id = u['id']
            u['conv_id'] = conv['conversation_id']
            u['conv_gender'] = conv['participant_gender']
            u['conv_age'] = conv['participant_age']
            utterances[id] = u

    with open(f"{condition}_info_nuggets_parent_children.tsv", "w") as w:
        w.write(
            f"conversation_id\tparticipant_gender\tparticipant_age\tutterance_id\tparent_id\tparent_info_need\tparent_info_need_subtype\tparent_text\tutterance_text\tnugget_1\tnugget_2\tnugget_3\tavg\texcel_how_to\texcel_recipe\twikipedia\tserious_eats\tstack_excahnge\ttot_sources\n"
        )
        for key, value in utterances.items():
            parents = [utterances[p] for p in value['parent']]

            for parent in parents:
                info_need_type = parent['information_need_type']
                parent_info_need_subtype = parent['information_need_subtype']
                if info_need_type != "":

                    conversation_id = value['conv_id']
                    participant_gender = value['conv_gender']
                    participant_age = value['conv_age']
                    try:
                        nuggets = [int(n) for n in info_nuggets[value['id']]]
                    except:
                        continue
                    avg = sum(nuggets) / 3
                    nuggets = [str(n) for n in nuggets]
                    nuggets = "\t".join(nuggets)
                    parent_u = parent['utterance'].replace("\n", "")
                    child_u = value['utterance'].replace("\n", "")
                    tot_source = len(value['provenance'])
                    sources_split = [0, 0, 0, 0, 0]
                    for source in value['provenance']:
                        if source['page_origin'] == 'excel':
                            # Find whether the origin comes from how-tos or recipes
                            if source['page_id'] in how_tos_ids:
                                sources_split[0] += 1
                            if source['page_id'] in recipes_ids:
                                sources_split[1] += 1
                        if source['page_origin'] == 'wikipedia':
                            sources_split[2] += 1
                        if source['page_origin'] == 'seriousEats':
                            sources_split[3] += 1
                        if source['page_origin'] == 'stackExchangeCooking':
                            sources_split[4] += 1
                    sources_split = "\t".join([str(s) for s in sources_split])
                    w.write(
                        f"{conversation_id}\t{participant_gender}\t{participant_age}\t{key}\t{parent['id']}\t{info_need_type}\t{parent_info_need_subtype}\t{parent_u}\t{child_u}\t{nuggets}\t{avg}\t{sources_split}\t{tot_source}\n"
                    )
