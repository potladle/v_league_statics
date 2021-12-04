from volleyball.stat.Chance import Chances
from volleyball.stat.StatMaker import *
from volleyball.scraper.LinkProcessor import LinkProcessor
import statistics


link_processor = LinkProcessor(
    [LinkProcessor.WOMEN], [LinkProcessor.REGULAR_SEASON, LinkProcessor.PLAY_OFF, LinkProcessor.SEMI_PLAY_OFF, LinkProcessor.CHAMP]
    , list(range(2020, 2021))
    , list(range(1, 3000)))
link_processor.make_round_number()
stat = Stat(link_processor.links)

stat.fill_games()
stat.fill_sets()
stat.fill_messages()
stat.fill_rallies()
stat.fill_chances()

direct_induce_EffCalc = EffCalc({})

receive_over_induce_EffCalc = EffCalc({})

accurate_receive_induce_EffCalc = EffCalc({})

serve_EffCalc = EffCalc({})

accurate_receive_chance_EffCalc = EffCalc({})

receive_chance_EffCalc = EffCalc({})

accurate_receive_rally_EffCalc = EffCalc({})

receive_rally_EffCalc = EffCalc({})

direct_effect = EffCalc({})

just_next = EffCalc({})


def make_effect(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: set):
    direct_chances = chances.select_direct_chance(messages)
    for chance in direct_chances:
        serve_chance = chances.select_near_chance(chance, True, 1)
        direct_induce_EffCalc.append_effect_calc(messages[serve_chance.side].slice_messages_with_chance(serve_chance), game, "서브종합")

    receive_over_chances = chances.select_receive_over_chance(messages)
    for chance in receive_over_chances:
        serve_chance = chances.select_near_chance(chance, True, 1)
        receive_over_induce_EffCalc.append_effect_calc(messages[serve_chance.side].slice_messages_with_chance(serve_chance), game, "서브종합")

    accurate_receive_chances = chances.select_accurate_receive_chance(messages)
    for chance in accurate_receive_chances:
        serve_chance = chances.select_near_chance(chance, True, 1)
        accurate_receive_induce_EffCalc.append_effect_calc(messages[serve_chance.side].slice_messages_with_chance(serve_chance), game, "서브종합")

    serve_EffCalc.append_effect_calc(messages[0], game, "서브종합")
    serve_EffCalc.append_effect_calc(messages[1], game, "서브종합")

    for chance in chances:
        messages_in_chance = messages[chance.side].slice_messages_with_chance(chance)
        for message in messages_in_chance:
            if isinstance(message, ReceiveMessage) and message.success_failure == Message.SUCCESS:
                accurate_receive_chance_EffCalc.append_effect_calc(messages_in_chance
                                                                   , game
                                                                   , "공격종합")
            if isinstance(message, ReceiveMessage):
                receive_chance_EffCalc.append_effect_calc(messages_in_chance, game, "공격종합")

    for rally in rallies:
        messages_in_rally = messages[0].slice_messages_with_rallies([rally])
        for message in messages_in_rally:
            if isinstance(message, ReceiveMessage) and message.success_failure == Message.SUCCESS:
                accurate_receive_rally_EffCalc.append_effect_calc(messages_in_rally, game, "공격종합")
            if isinstance(message, ReceiveMessage):
                receive_rally_EffCalc.append_effect_calc(messages_in_rally
                                                         , game
                                                         , "공격종합")

    for rally in rallies:
        messages_in_rally = messages[1].slice_messages_with_rallies([rally])
        for message in messages_in_rally:
            if isinstance(message, ReceiveMessage) and message.success_failure == Message.SUCCESS:
                accurate_receive_rally_EffCalc.append_effect_calc(messages_in_rally, game, "공격종합")
            if isinstance(message, ReceiveMessage):
                receive_rally_EffCalc.append_effect_calc(messages_in_rally
                                                         , game
                                                         , "공격종합")

    for index, chance in enumerate(chances):
        if index == len(chances) - 1:
            break
        if chance.message_index[0] == chance.message_index[1] \
            and isinstance(messages[chance.side][chance.message_index[0]], ReceiveMessage) \
            and isinstance(messages[chance.other_side()][chances[index + 1].message_index[0]], AttackMessage):
            direct_effect.append_effect_calc(
                Messages([messages[chance.other_side()][chances[index + 1].message_index[0]]])
                , game
                , "공격종합")

    for index, chance in enumerate(chances):
        if index == len(chances) - 1:
            break
        if chance.message_index[0] == chance.message_index[1] \
            and isinstance(messages[chance.side][chance.message_index[0]], ReceiveMessage) \
            and isinstance(messages[chance.other_side()][chances[index + 1].message_index[0]], DigMessage):
            just_next.append_effect_calc(
                messages[chance.other_side()][chances[index + 1].message_index[0]: chances[index + 1].message_index[1] + 1]
                , game
                , "공격종합")


stat.process_in_set(make_effect)

direct_induce_EffCalc.print_effect_with_name(prefix="다이렉트 유도")
receive_over_induce_EffCalc.print_effect_with_name(prefix="리시브 넘어감")
accurate_receive_induce_EffCalc.print_effect_with_name(prefix="상대 리시브 정확")
serve_EffCalc.print_effect_with_name(prefix="서브 종합", at_least=250)
print("-" * 100)
direct_induce_EffCalc.print_overall_effect(prefix="다이렉트 유도")
receive_over_induce_EffCalc.print_overall_effect(prefix="리시브 넘어감")
accurate_receive_induce_EffCalc.print_overall_effect(prefix="상대 리시브 정확")
serve_EffCalc.print_overall_effect(prefix="서브 종합")
serve_Eff = []


def serve_eff_formula(player: Player, serve_stat: List[int]) -> str:
    if serve_stat[0] >= 200:
        serve_Eff.append(((serve_stat[1] - serve_stat[2] + serve_stat[3] * 0.6 + serve_stat[4] * 0.3 - serve_stat[5] * 0.35 - (serve_stat[0] - serve_stat[1] - serve_stat[2] - serve_stat[3] - serve_stat[4] - serve_stat[5]) * 0.25) / serve_stat[0] * 1000) / 10)
    return f"{int((serve_stat[1] - serve_stat[2] + serve_stat[3] * 0.6 + serve_stat[4] * 0.3 - serve_stat[5] * 0.35 - (serve_stat[0] - serve_stat[1] - serve_stat[2] - serve_stat[3] - serve_stat[4] - serve_stat[5]) * 0.25) / serve_stat[0] * 1000) / 10}%\
{serve_stat[0]}/{serve_stat[1]}/{serve_stat[2]}/{serve_stat[3]}/{serve_stat[4]}/{serve_stat[5]}/{serve_stat[0] - serve_stat[1] - serve_stat[2] - serve_stat[3] - serve_stat[4] - serve_stat[5]}"


serve_EffCalc.print_multiple_eff_calc(
    True, [direct_induce_EffCalc, receive_over_induce_EffCalc, accurate_receive_induce_EffCalc], serve_eff_formula, prefix="전체 서브 효율")

serve_EffCalc.print_multiple_eff_calc(
    False, [direct_induce_EffCalc, receive_over_induce_EffCalc, accurate_receive_induce_EffCalc], serve_eff_formula, prefix="전체 서브 효율"
)

print(statistics.median(serve_Eff), " 중앙값\n")

accurate_receive_chance_EffCalc.print_overall_effect(prefix="리시브 정확 찬스 공격 효율")
accurate_receive_rally_EffCalc.print_overall_effect(prefix="리시브 정확 랠리 공격 효율")

receive_chance_EffCalc.print_overall_effect(prefix="리시브 찬스 공격 효율")
receive_rally_EffCalc.print_overall_effect(prefix="리시브 랠리 공격 효율")

direct_effect.print_overall_effect(prefix="다이렉트 공격")
just_next.print_overall_effect(prefix="넘어온 공 공격")
