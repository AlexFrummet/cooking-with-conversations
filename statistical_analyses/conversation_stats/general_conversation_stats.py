import pprint as pp
import json
from collections import OrderedDict
import string

from statistical_analyses.utils import load_conversations



def total_conversation_utterances(conversations, participant=None):
    number_utterances = 0
    for conversation in conversations:
        for utterance in conversation['conversation']:
            if participant is None and utterance['interaction_type'] == 'text':
                number_utterances += 1
                continue

            if participant == utterance['participant'] and utterance[
                    'interaction_type'] == 'text':
                number_utterances += 1

    return number_utterances


def average_length_utterances_char(conversations, participant=None):
    number_utterances = 0
    total_utterance_length = 0

    for conversation in conversations:
        for utterance in conversation['conversation']:
            if participant is None and utterance['interaction_type'] == 'text':
                if not utterance['utterance'].startswith("http"):
                    number_utterances += 1
                    total_utterance_length += len(utterance['utterance'])
                    continue

            if participant == utterance['participant'] and utterance[
                    'interaction_type'] == 'text':
                if not utterance['utterance'].startswith("http"):
                    number_utterances += 1
                    total_utterance_length += len(utterance['utterance'])

    return total_utterance_length / number_utterances

def average_length_utterances_words(conversations, participant=None):
    number_utterances = 0
    total_utterance_length = 0

    for conversation in conversations:
        for utterance in conversation['conversation']:
            if participant is None and utterance['interaction_type'] == 'text':
                if not utterance['utterance'].startswith("http"):
                    number_utterances += 1
                    words_in_utterance = utterance['utterance'].translate(str.maketrans('', '', string.punctuation)).split()
                    total_utterance_length += len(words_in_utterance)
                    continue

            if participant == utterance['participant'] and utterance[
                    'interaction_type'] == 'text':
                if not utterance['utterance'].startswith("http"):
                    number_utterances += 1
                    words_in_utterance = utterance['utterance'].translate(str.maketrans('', '', string.punctuation)).split()
                    total_utterance_length += len(words_in_utterance)

    return total_utterance_length / number_utterances


def searches_per_conversation(conversations):
    number_searches = 0

    for conversation in conversations:
        for utterance in conversation['conversation']:
            if utterance['interaction_type'] == 'text':
                number_searches += len(utterance['query'])

    return number_searches


def sources_per_conversation(conversations):
    number_searches = 0

    for conversation in conversations:
        for utterance in conversation['conversation']:
            if utterance['interaction_type'] == 'text':
                number_searches += len(utterance['provenance'])

    return number_searches


def category_distribution(conversations, participant=None):
    categories_counter = {}

    for conversation in conversations:
        for utterance in conversation['conversation']:

            if utterance['information_need_type'] == "":
                continue
            if participant is None and utterance['interaction_type'] == 'text':
                if utterance[
                        'information_need_type'] not in categories_counter:
                    categories_counter[utterance['information_need_type']] = 1
                else:
                    categories_counter[utterance['information_need_type']] += 1
                continue

            if participant == utterance['participant'] and utterance[
                    'interaction_type'] == 'text':
                if utterance[
                        'information_need_type'] not in categories_counter:
                    categories_counter[utterance['information_need_type']] = 1
                else:
                    categories_counter[utterance['information_need_type']] += 1

    return categories_counter


def information_need_subtype_distribution(conversations, participant=None):
    categories_counter = {}

    for conversation in conversations:
        for utterance in conversation['conversation']:

            if utterance['information_need_subtype'] == "":
                continue
            if participant is None and utterance['interaction_type'] == 'text':
                if utterance[
                        'information_need_subtype'] not in categories_counter:
                    categories_counter[utterance['information_need_subtype']] = 1
                else:
                    categories_counter[utterance['information_need_subtype']] += 1
                continue

            if participant == utterance['participant'] and utterance[
                    'interaction_type'] == 'text':
                if utterance[
                        'information_need_subtype'] not in categories_counter:
                    categories_counter[utterance['information_need_subtype']] = 1
                else:
                    categories_counter[utterance['information_need_subtype']] += 1

    return categories_counter


def distribution_to_percentage(dist, n_conversations):
    for key in dist:
        dist[key] = dist[key] / n_conversations * 100
    return dist


def dialogue_act_distribution(conversations, participant=None):
    categories_counter = {}

    for conversation in conversations:
        for utterance in conversation['conversation']:

            if utterance['dialogue_act'] == "":
                continue
            if participant is None and utterance['interaction_type'] == 'text':
                if utterance[
                        'dialogue_act'] not in categories_counter:
                    categories_counter[utterance['dialogue_act']] = 1
                else:
                    categories_counter[utterance['dialogue_act']] += 1
                continue

            if participant == utterance['participant'] and utterance[
                    'interaction_type'] == 'text':
                if utterance[
                        'dialogue_act'] not in categories_counter:
                    categories_counter[utterance['dialogue_act']] = 1
                else:
                    categories_counter[utterance['dialogue_act']] += 1

    return categories_counter


def distribution_categories_over_conversations(conversations_distribution,
                                               n_conversations):
    for key, value in conversations_distribution.items():
        conversations_distribution[key] = value / n_conversations * 100

    return conversations_distribution


def sources_distribution(conversations):
    result = {}
    for conversation in conversations:
        for utterance in conversation['conversation']:
            if len(utterance['provenance']) != 0:
                processed_sources = []
                for provenance in utterance['provenance']:
                    if provenance['paragraph_id'] not in processed_sources:
                        if provenance['page_origin'] not in result:
                            result[provenance['page_origin']] = 1
                        else:
                            result[provenance['page_origin']] += 1
                        processed_sources.append(provenance['paragraph_id'])
    return result


def sources_distribution_percentage(sources_distribution):
    total = 0
    for value in sources_distribution.values():
        total += value
    for key, value in sources_distribution.items():
        sources_distribution[key] = value / total * 100
    return sources_distribution


def statistics_pipeline(conversations, condition):

    print(f"++++++++++ {condition} CONVS STATS ++++++++++")
    print("============ GENERAL STATS ============")
    print(f"Total Conversations: {len(conversations)}")

    # Compute total utterances
    total_utterances = total_conversation_utterances(conversations)
    print(f"Total Utterances: {total_utterances}")
    # Compute average length of all utterances in char
    avg_utterances_length = average_length_utterances_char(conversations)
    print(f"Average Utterances Char Length: {avg_utterances_length}")
    # Compute average length of all utterances in words
    avg_utterances_length_word = average_length_utterances_words(conversations)
    print(f"Average Utterances Words Length: {avg_utterances_length_word}")

    print("============ USER STATS ============")
    # Compute total user utterances
    total_user_utterances = total_conversation_utterances(
        conversations, 'user')
    print(f"Total User Utterances: {total_user_utterances}")
    # Compute total length per user utterances in char
    avg_user_utterances_length = average_length_utterances_char(
        conversations, 'user')
    print(f"Average User Utterances Char Length: {avg_user_utterances_length}")
    # Compute total length per user utterances in words
    avg_user_utterances_length_words = average_length_utterances_words(
        conversations, 'user')
    print(f"Average User Utterances Words Length: {avg_user_utterances_length_words}")
    # Compute number of user utterances split by category
    categories_user_distrib = category_distribution(conversations, 'user')
    print(f"Distribution of information need type for user utterances:")
    pp.pprint(categories_user_distrib)
    # Compute percentage of user utterances split by category
    categories_user_distrib_percentage = sources_distribution_percentage(
        categories_user_distrib)
    print(f"Distribution of information need type for user utterances:")
    pp.pprint(categories_user_distrib_percentage)
    # Compute number of user utterances split by category averaged over all conversations
    categories_user_distrib_averaged = distribution_categories_over_conversations(
        categories_user_distrib, len(conversations))
    print(
        f"Distribution of categories for user utterances averaged per conversation:"
    )
    pp.pprint(categories_user_distrib_averaged)
    subtype_user_distrib = information_need_subtype_distribution(conversations, 'user')
    print(f"Distribution of information need subtype for user utterances:")
    pp.pprint(subtype_user_distrib)
    # Compute percentage of user utterances split by category
    subtype_user_distrib_percentage = sources_distribution_percentage(
        subtype_user_distrib)
    print(f"Distribution of information need subtype for user utterances:")
    pp.pprint(subtype_user_distrib_percentage)
    # Compute number of user utterances split by dialogue act
    dialogue_act_categories_user_distrib = dialogue_act_distribution(conversations, 'user')
    print(f"Distribution of dialogue act categories for user utterances:")
    pp.pprint(dialogue_act_categories_user_distrib)

    # Compute percentage of user utterances split by dialogue act
    dialogue_act_categories_user_distrib_percentage = distribution_to_percentage(
        dialogue_act_categories_user_distrib, total_user_utterances)
    print(f"Distribution of  dialogue act categories for user utterances:")
    pp.pprint(dialogue_act_categories_user_distrib_percentage)

    print("============ AGENT STATS ============")
    # Compute total agent utterances
    total_agent_utterances = total_conversation_utterances(
        conversations, 'agent')
    print(f"Total Agent Utterances: {total_agent_utterances}")
    # Compute average length per agent utterance in char
    avg_agent_utterances_length = average_length_utterances_char(
        conversations, 'agent')
    print(f"Average Agent Utterances Char Length: {avg_agent_utterances_length}")
    # Compute average length per agent utterance in words
    avg_agent_utterances_length_words = average_length_utterances_words(
        conversations, 'agent')
    print(f"Average Agent Utterances Words Length: {avg_agent_utterances_length_words}")
    # Compute total number of searches
    total_searches = searches_per_conversation(conversations)
    print(f"Total searches performed by agent: {total_searches}")
    # Compute number of sources used by agent
    total_sources = sources_per_conversation(conversations)
    print(f"Total sources used by agent: {total_sources}")
    # Compute distribution of sources used by agent
    sources_dist = sources_distribution(conversations)
    print(f"Sources distribution used by agent:")
    pp.pprint(sources_dist)
    # Compute percentage of distribution of sources used by agent
    sources_dist_percentage = sources_distribution_percentage(sources_dist)
    print(f"Percentage of sources distribution used by agent:")
    pp.pprint(sources_dist_percentage)
    subtype_agent_distrib = information_need_subtype_distribution(conversations, 'agent')
    print(f"Distribution of information need subtype for agent utterances:")
    pp.pprint(subtype_agent_distrib)
    # Compute percentage of user utterances split by category
    subtype_agent_distrib_percentage = sources_distribution_percentage(
        subtype_agent_distrib)
    print(f"Distribution of information need subtype for agent utterances:")
    pp.pprint(subtype_agent_distrib_percentage)
    # Compute number of agent utterances split by dialogue act
    dialogue_act_categories_agent_distrib = dialogue_act_distribution(conversations, 'agent')
    print(f"Distribution of dialogue act categories for agent utterances:")
    pp.pprint(dialogue_act_categories_agent_distrib)
    # Compute percentage of agent utterances split by dialogue act
    dialogue_act_categories_agent_distrib_percentage = distribution_to_percentage(
        dialogue_act_categories_agent_distrib, total_agent_utterances)
    print(f"Distribution of  dialogue act categories for agent utterances:")
    pp.pprint(dialogue_act_categories_agent_distrib_percentage)


def generate_convs_lenth_chart(output, convs):
    with open(output, "w") as f:
        f.write('conv_id\tcondition\tavg_length_char\tavg_length_words\n')
        for conv in convs:
            conv_id = conv['conversation_id']
            conv_condition = conv['condition']
            utterances = conv['conversation']

            number_utterances = 0
            total_utterance_length = 0
            
            for utterance in utterances:
                if utterance['interaction_type'] == 'text':
                    if not utterance['utterance'].startswith("http"):
                        number_utterances += 1
                        total_utterance_length += len(utterance['utterance'])

            avg_conv_length_char = total_utterance_length / number_utterances

            number_utterances = 0
            total_utterance_length = 0
            
            for utterance in utterances:
                if utterance['interaction_type'] == 'text':
                    if not utterance['utterance'].startswith("http"):
                        number_utterances += 1
                        words_in_utterance = utterance['utterance'].translate(str.maketrans('', '', string.punctuation)).split()
                        total_utterance_length += len(words_in_utterance)

            
            avg_conv_length_words = total_utterance_length / number_utterances

            f.write(f"{conv_id}\t{conv_condition}\t{avg_conv_length_char}\t{avg_conv_length_words}\t\n")

def generate_conv_n_utterances(output, convs):
    with open(output, "w") as f:
        f.write('conv_id\tcondition\tn_user_utterances\tn_agent_utterances\n')
        for conv in convs:
            conv_id = conv['conversation_id']
            conv_condition = conv['condition']
            utterances = conv['conversation']

            user_utterances = 0
            agent_utterances = 0
            
            for utterance in utterances:
                if utterance['interaction_type'] == 'text':
                    if utterance['participant'] == 'user':
                        user_utterances += 1
                    if utterance['participant'] == 'agent':
                        agent_utterances += 1

            f.write(f"{conv_id}\t{conv_condition}\t{user_utterances}\t{agent_utterances}\t\n")


def generate_convs_lenth_full(output, convs):
    with open(output, "w") as f:
        f.write('conv_id\tcondition\tutterance_id\tparticipant\tlength_char\tlength_words\tutterance\n')
        for conv in convs:
            conv_id = conv['conversation_id']
            conv_condition = conv['condition']
            utterances = conv['conversation']
            
            for utterance in utterances:
                utterance_id = utterance['id']
                utterance_participant = utterance['participant']
                utterance_text = utterance['utterance'].replace("\t","").replace("\n", "")
                if utterance['interaction_type'] == 'text':
                    if not utterance_text.startswith("http"):
                        total_utterance_length = len(utterance_text)
                        words_in_utterance = len(utterance_text.translate(str.maketrans('', '', string.punctuation)).split())

                        f.write(f"{conv_id}\t{conv_condition}\t{utterance_id}\t{utterance_participant}\t{total_utterance_length}\t{words_in_utterance}\t{utterance_text}\n")


if __name__ == '__main__':

    active_conversations = load_conversations('active', 0, 24)
    passive_conversations = load_conversations('passive', 0, 29)

    statistics_pipeline(active_conversations, 'active')
    statistics_pipeline(passive_conversations, 'passive')

    generate_convs_lenth_chart("avg_convs_length_stats.tsv", active_conversations+passive_conversations)
    generate_conv_n_utterances("convs_n_utterances_stats.tsv", active_conversations+passive_conversations)
    generate_convs_lenth_full("avg_convs_length_full.tsv", active_conversations+passive_conversations)


    
