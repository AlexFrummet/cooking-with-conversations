import collections
import json
import pprint as pp


def load_conv(path):
    with open(path) as f:
        return json.loads(f.read())


def load_recipe(path, recipe_id):
    with open(path) as f:
        for line in f:
            json_obj = json.loads(line)
            if json_obj["id"] == recipe_id:
                return json_obj
            
def load_conversations(condition, start_number, end_number):
    results = []
    for i in range(start_number, end_number + 1):
        with open(f'../data/{condition}/conversation_{i}.json') as f:
            conversation_dict = json.loads(f.read(),
                                           object_pairs_hook=collections.OrderedDict)

            if conversation_dict['keep_conversation']:
                results.append(conversation_dict)

    return results


def clean_text(s):
    return s.replace("\t","").replace("\n","")

class RecipeNavigator:
    def __init__(self, recipes_file, recipe_id) -> None:
        self.steps = self.generate_recipe_steps_list(recipes_file, recipe_id)
        self.current_step = 0
        self.total_steps = len(self.steps)
        self.past_step = 0

    def load_recipe(self, path, recipe_id):
        with open(path) as f:
            for line in f:
                json_obj = json.loads(line)
                if json_obj["id"] == recipe_id:
                    return json_obj

    def generate_recipe_steps_list(self, path, recipe_id):
        recipe = self.load_recipe(path, recipe_id)
        ingredients = clean_text(" ".join(recipe["required_ingredient"]))
        equipment = clean_text(" ".join(recipe["required_equipment"]))
        ingredients_and_equipment = ingredients + " " + equipment
        steps = recipe["steps"]
        steps.insert(0, ingredients_and_equipment)
        return steps

    def next_step(self):
        if self.current_step < self.total_steps - 1:
            self.past_step = self.current_step
            self.current_step += 1

    def previous_step(self):
        if self.current_step > 0:
            self.past_step = self.current_step
            self.current_step -= 1

    def get_current_step_text(self):
        return self.steps[self.current_step]

if __name__ == "__main__":

    active_conversations = load_conversations('active', 0, 24)
    passive_conversations = load_conversations('passive', 0, 29)

    all_convs = active_conversations+passive_conversations

    with open("timeline.tsv", "w") as f:
        f.write("conv_id\tcondition\trecipe_id\tstep_n\tstep_text\tn_agent_utterances\tn_user_utterances\tknowledge\tamount\tcooking_technique\tequipment\tingredient\tmeal\tpreparation\trecipe\ttemperature\ttime\tmisc\ttotal_images_sent\ttotal_sources_used\twikipedia\tseriousEats\tstackExchangeCooking\texcel\n")
        for conv in all_convs:
            conv_id = conv['conversation_id']
            condition = conv['condition'] 
            recipe_id = conv['recipe_id']
            recipe_navigator = RecipeNavigator("serious_eats_anserini_recipes_v1.json", conv["recipe_id"])

            # Populate the process graph
            process_graph = []
            for i in range(recipe_navigator.total_steps):
                process_graph.append(collections.OrderedDict({
                    "step_number": None,
                    "step_text": None,
                    "n_agent_utterances": 0,
                    "n_user_utterances": 0,
                    "information_need_type_count": {
                        "knowledge":0,
                        "amount":0,
                        "cooking_technique":0,
                        "equipment":0,
                        "ingredient":0,
                        "meal":0,
                        "preparation":0,
                        "recipe":0,
                        "temperature":0,
                        "time":0,
                        "misc":0
                    },
                    "total_images_sent": 0,
                    "sources": {
                        "total_sources_used": 0,
                        "wikipedia": 0,
                        "seriousEats": 0,
                        "stackExchangeCooking": 0,
                        "excel": 0
                    }
                }))

            for utterance in conv["conversation"]:
                if process_graph[recipe_navigator.current_step]["step_number"] is None:
                    process_graph[recipe_navigator.current_step]["step_number"] = recipe_navigator.current_step
                    process_graph[recipe_navigator.current_step]["step_text"] = recipe_navigator.get_current_step_text()
                if utterance["interaction_type"] == "action":
                    if utterance["actions"][0] == "next":
                        recipe_navigator.next_step()
                    else:
                        recipe_navigator.previous_step()
                    process_graph[recipe_navigator.current_step]["step_number"] = recipe_navigator.current_step
                    process_graph[recipe_navigator.current_step]["step_text"] = recipe_navigator.get_current_step_text()
                    

                if utterance["interaction_type"] == "text":
                    if utterance["participant"] == "user":
                        process_graph[recipe_navigator.current_step]['n_user_utterances'] += 1
                    else:
                        process_graph[recipe_navigator.current_step]['n_agent_utterances'] += 1
                        if utterance["utterance"].startswith("https") or utterance[
                            "utterance"
                        ].startswith("http"):
                            process_graph[recipe_navigator.current_step]['total_images_sent'] += 1
                        else:
                            sources_used = []
                            for source in utterance["provenance"]:
                                if source['paragraph_id'] not in sources_used:
                                    process_graph[recipe_navigator.current_step]['sources']['total_sources_used'] += 1
                                    process_graph[recipe_navigator.current_step]['sources'][source['page_origin']] += 1
                                    sources_used.append(source['paragraph_id'])

                    if utterance['information_need_type'].strip() != "":
                        print(conv_id)
                        process_graph[recipe_navigator.current_step]['information_need_type_count'][utterance['information_need_type']] += 1


            # Save the final csv file
            for node in process_graph:
                if node['step_number'] is not None:
                    f.write(f"{conv_id}\t{condition}\t{recipe_id}\t{node['step_number']}\t{node['step_text']}\t{node['n_agent_utterances']}\t{node['n_user_utterances']}\t{node['information_need_type_count']['knowledge']}\t{node['information_need_type_count']['amount']}\t{node['information_need_type_count']['cooking_technique']}\t{node['information_need_type_count']['equipment']}\t{node['information_need_type_count']['ingredient']}\t{node['information_need_type_count']['meal']}\t{node['information_need_type_count']['preparation']}\t{node['information_need_type_count']['recipe']}\t{node['information_need_type_count']['temperature']}\t{node['information_need_type_count']['time']}\t{node['information_need_type_count']['misc']}\t{node['total_images_sent']}\t{node['sources']['total_sources_used']}\t{node['sources']['wikipedia']}\t{node['sources']['seriousEats']}\t{node['sources']['stackExchangeCooking']}\t{node['sources']['excel']}\t\n")
                