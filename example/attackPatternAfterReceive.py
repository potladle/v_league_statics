from volleyball.stat.Chance import Chances
from volleyball.stat.StatMaker import *
from volleyball.scraper.LinkProcessor import LinkProcessor
from utills import make_percentage, take_key_by_value, zero_to_one_one_to_zero
from alive_progress import config_handler

config_handler.set_global(spinner="wait")

def fill_effects_women_teams(effects: Dict[str, EffCalc]):
    for women_team in women_teams:
        effects[women_team] = EffCalc({})


attacks_after_accurate_receive : List[Dict[str, EffCalc]] = []

attacks_after_receive : List[Dict[str, EffCalc]] = []

attacks_after_serve : List[Dict[str, EffCalc]] = []


def processor_in_set(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    for rally in rallies:
        receive_result = -1
        attack_message_index = 0
        receive_team_messages = messages[zero_to_one_one_to_zero(rally.serve)][rally.message_index[0]:rally.message_index[1] + 1]
        for receive_team_message in receive_team_messages:
            if isinstance(receive_team_message, ReceiveMessage):
                receive_result = receive_team_message.success_failure
            elif receive_result == 0 and isinstance(receive_team_message, AttackMessage) and attack_message_index < len(attacks_after_receive):
                try:
                    attacks_after_receive[attack_message_index][take_key_by_value(action_to_class, type(receive_team_message))]
                except KeyError:
                    attacks_after_receive[attack_message_index][take_key_by_value(action_to_class, type(receive_team_message))] = EffCalc({})
                attacks_after_receive[
                    attack_message_index][
                    take_key_by_value(
                        action_to_class
                        , type(receive_team_message))].append_effect_calc(Messages([receive_team_message]), game, "공격종합")
                attack_message_index += 1
            elif receive_result == 0 and isinstance(receive_team_message, AttackMessage):
                attacks_after_receive.append({})
                try:
                    attacks_after_receive[attack_message_index][take_key_by_value(action_to_class, type(receive_team_message))]
                except KeyError:
                    attacks_after_receive[attack_message_index][take_key_by_value(action_to_class, type(receive_team_message))] = EffCalc({})
                attacks_after_receive[
                    attack_message_index][
                    take_key_by_value(
                        action_to_class
                        , type(receive_team_message))].append_effect_calc(Messages([receive_team_message]), game, "공격종합")
                attack_message_index += 1
            elif receive_result == 1 and isinstance(receive_team_message, AttackMessage) and attack_message_index < len(attacks_after_accurate_receive):
                try:
                    attacks_after_accurate_receive[attack_message_index][take_key_by_value(action_to_class, type(receive_team_message))]
                except KeyError:
                    attacks_after_accurate_receive[attack_message_index][take_key_by_value(action_to_class, type(receive_team_message))] = EffCalc({})
                attacks_after_accurate_receive[
                    attack_message_index][
                    take_key_by_value(
                        action_to_class
                        , type(receive_team_message))].append_effect_calc(Messages([receive_team_message]), game, "공격종합")
                attack_message_index += 1
            elif receive_result == 1 and isinstance(receive_team_message, AttackMessage):
                attacks_after_accurate_receive.append({})
                try:
                    attacks_after_accurate_receive[attack_message_index][take_key_by_value(action_to_class, type(receive_team_message))]
                except KeyError:
                    attacks_after_accurate_receive[attack_message_index][take_key_by_value(action_to_class, type(receive_team_message))] = EffCalc({})
                attacks_after_accurate_receive[
                    attack_message_index][
                    take_key_by_value(
                        action_to_class
                        , type(receive_team_message))].append_effect_calc(Messages([receive_team_message]), game, "공격종합")
                attack_message_index += 1

        attack_message_index = 0
        serve_team_messages = messages[rally.serve][rally.message_index[0]:rally.message_index[1] + 1]
        if serve_team_messages[0].success_failure == 0:
            for serve_team_message in serve_team_messages:
                if isinstance(serve_team_message, AttackMessage):
                    if attack_message_index >= len(attacks_after_serve):
                        attacks_after_serve.append({})
                    try:
                        attacks_after_serve[attack_message_index][take_key_by_value(action_to_class, type(serve_team_message))]
                    except KeyError:
                        attacks_after_serve[attack_message_index][take_key_by_value(action_to_class, type(serve_team_message))] = EffCalc({})
                    attacks_after_serve[
                        attack_message_index
                    ][take_key_by_value(
                        action_to_class, type(serve_team_message)
                    )].append_effect_calc(Messages([serve_team_message]), game, "공격종합")
                    attack_message_index += 1


link_processor = LinkProcessor(
    [LinkProcessor.WOMEN],
    [LinkProcessor.REGULAR_SEASON, LinkProcessor.PLAY_OFF, LinkProcessor.SEMI_PLAY_OFF, LinkProcessor.CHAMP]
    , list(range(2018, 2021))
    , list(range(1, 3000)))
link_processor.make_round_number()
stat = Stat(link_processor.links)

stat.fill_games()
stat.fill_sets()
stat.fill_messages()
stat.fill_rallies()
stat.fill_chances()

stat.process_in_set(processor_in_set)


print("일반 리시브 이후")
for attack_number, attack_after_receive in enumerate(attacks_after_receive):
    whole_whole_trial = 0
    for eff_calc in attack_after_receive.values():
        whole_whole_trial += eff_calc.return_whole_trial()
    for action, eff_calc in attack_after_receive.items():
        eff_calc.print_overall_trial(prefix=f"{attack_number + 1}번째 공격 - {action} {make_percentage(whole_whole_trial, eff_calc.return_whole_trial())}% ")

    print("\n", "-" * 50, "\n")

print("리시브 성공 이후")

for attack_number, attack_after_receive in enumerate(attacks_after_accurate_receive):
    whole_whole_trial = 0
    for eff_calc in attack_after_receive.values():
        whole_whole_trial += eff_calc.return_whole_trial()
    for action, eff_calc in attack_after_receive.items():
        eff_calc.print_overall_trial(prefix=f"{attack_number + 1}번째 공격 - {action} {make_percentage(whole_whole_trial, eff_calc.return_whole_trial())}% ")

    print("\n", "-" * 50, "\n")

print("서브 이후")

for attack_number, attack_after_serve in enumerate(attacks_after_serve):
    whole_whole_trial = 0
    for eff_calc in attack_after_serve.values():
        whole_whole_trial += eff_calc.return_whole_trial()
    for action, eff_calc in attack_after_serve.items():
        eff_calc.print_overall_trial(prefix=f"{attack_number + 1}번째 공격 - {action} {make_percentage(whole_whole_trial, eff_calc.return_whole_trial())}% ")

    print("\n", "-" * 50, "\n")

print("일반 리시브 이후")

for attack_number, attack_after_receive in enumerate(attacks_after_receive):
    for action, eff_calc in attack_after_receive.items():
        eff_calc.print_overall_effect(prefix=f"{attack_number + 1}번째 공격 - {action} ")

    attack_numbers = [0, 0, 0]
    for eff_calc in attack_after_receive.values():
        for one_attack_numbers in eff_calc.values():
            for v, one_number in enumerate(one_attack_numbers):
                attack_numbers[v] += one_number

    print(f"\n{attack_number + 1}번째 공격 - {make_percentage(attack_numbers[0], attack_numbers[1] - attack_numbers[2])} {attack_numbers}")

    print("\n", "-" * 50, "\n")

whole_attack_numbers = [0, 0, 0]
for attack_after_receive in attacks_after_receive:
    for eff_calc in attack_after_receive.values():
        for one_attack_numbers in eff_calc.values():
            for v, one_number in enumerate(one_attack_numbers):
                whole_attack_numbers[v] += one_number

print(f"일반 리시브 이후 총 공격 {make_percentage(whole_attack_numbers[0], whole_attack_numbers[1] - whole_attack_numbers[2])} {whole_attack_numbers}")

print("리시브 성공 이후")

for attack_number, attack_after_receive in enumerate(attacks_after_accurate_receive):
    for action, eff_calc in attack_after_receive.items():
        eff_calc.print_overall_effect(prefix=f"{attack_number + 1}번째 공격 - {action} ")

    attack_numbers = [0, 0, 0]
    for eff_calc in attack_after_receive.values():
        for one_attack_numbers in eff_calc.values():
            for v, one_number in enumerate(one_attack_numbers):
                attack_numbers[v] += one_number

    print(f"\n{attack_number + 1}번째 공격 - {make_percentage(attack_numbers[0], attack_numbers[1] - attack_numbers[2])} {attack_numbers}")

    print("\n", "-" * 50, "\n")

whole_attack_numbers = [0, 0, 0]
for attack_after_receive in attacks_after_accurate_receive:
    for eff_calc in attack_after_receive.values():
        for one_attack_numbers in eff_calc.values():
            for v, one_number in enumerate(one_attack_numbers):
                whole_attack_numbers[v] += one_number

print(f"리시브 성공 이후 총 공격 {make_percentage(whole_attack_numbers[0], whole_attack_numbers[1] - whole_attack_numbers[2])} {whole_attack_numbers}")

print("서브 이후")

for attack_number, attack_after_receive in enumerate(attacks_after_serve):
    for action, eff_calc in attack_after_receive.items():
        eff_calc.print_overall_effect(prefix=f"{attack_number + 1}번째 공격 - {action} ")

    attack_numbers = [0, 0, 0]
    for eff_calc in attack_after_receive.values():
        for one_attack_numbers in eff_calc.values():
            for v, one_number in enumerate(one_attack_numbers):
                attack_numbers[v] += one_number

    print(f"\n{attack_number + 1}번째 공격 - {make_percentage(attack_numbers[0], attack_numbers[1] - attack_numbers[2])} {attack_numbers}")

    print("\n", "-" * 50, "\n")

whole_attack_numbers = [0, 0, 0]
for attack_after_receive in attacks_after_serve:
    for eff_calc in attack_after_receive.values():
        for one_attack_numbers in eff_calc.values():
            for v, one_number in enumerate(one_attack_numbers):
                whole_attack_numbers[v] += one_number

print(f"서브 이후 총 공격 {make_percentage(whole_attack_numbers[0], whole_attack_numbers[1] - whole_attack_numbers[2])} {whole_attack_numbers}")
