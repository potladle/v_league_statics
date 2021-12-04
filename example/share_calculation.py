import matplotlib.pyplot as plt
from volleyball.stat.StatMaker import *
from volleyball.scraper.LinkProcessor import LinkProcessor


link_processor = LinkProcessor([LinkProcessor.WOMEN], [LinkProcessor.REGULAR_SEASON], list(range(2020, 2021)), list(range(1, 300)))
link_processor.make_round_number()
stat = Stat(link_processor.links)

stat.fill_games()
stat.fill_sets()
stat.fill_messages()
stat.fill_rallies()

# 공격 성공-실패 이후 점유율(외국인)

shares: Dict[str, ShareCalc] = {}
for women_team in women_teams:
    shares[women_team] = ShareCalc({})

shares_after_three_points: Dict[str, ShareCalc] = {}
for women_team in women_teams:
    shares_after_three_points[women_team] = ShareCalc({})

shares_after_three_opposite_points: Dict[str, ShareCalc] = {}
for women_team in women_teams:
    shares_after_three_opposite_points[women_team] = ShareCalc({})

shares_after_twenty : Dict[str, ShareCalc] = {}
for women_team in women_teams:
    shares_after_twenty[women_team] = ShareCalc({})

forward_shares = {}
for women_team in women_teams:
    forward_shares[women_team] = ShareCalc({})

backward_shares = {}
for women_team in women_teams:
    backward_shares[women_team] = ShareCalc({})


def make_share(messages: List[Messages], rallies: Rallies, game: Game, set_in_game: Set):
    shares[game.teams[0]].make_action_and_time(messages[0], game, "공격종합")
    shares[game.teams[1]].make_action_and_time(messages[1], game, "공격종합")

    rallies_after_three_points = rallies.select_rally_with_near_result([0, 0, 0], [])
    messages_after_three_points = messages[0].slice_messages_with_rallies(rallies_after_three_points)
    shares_after_three_points[game.teams[0]].make_action_and_time(messages_after_three_points, game, "공격종합")

    rallies_after_three_points = rallies.select_rally_with_near_result([1, 1, 1], [])
    messages_after_three_points = messages[1].slice_messages_with_rallies(rallies_after_three_points)
    shares_after_three_points[game.teams[1]].make_action_and_time(messages_after_three_points, game, "공격종합")

    rallies_after_three_opposite_point = rallies.select_rally_with_near_result([1, 1, 1], [])
    messages_after_three_opposite_points = messages[0].slice_messages_with_rallies(rallies_after_three_opposite_point)
    shares_after_three_opposite_points[game.teams[0]].make_action_and_time(messages_after_three_opposite_points, game, "공격종합")

    rallies_after_three_opposite_point = rallies.select_rally_with_near_result([0, 0, 0], [])
    messages_after_three_opposite_points = messages[1].slice_messages_with_rallies(rallies_after_three_opposite_point)
    shares_after_three_opposite_points[game.teams[1]].make_action_and_time(messages_after_three_opposite_points, game, "공격종합")

    after_twenty_rallies = rallies.select_rally_with_score([[20, 100, 0]], set_in_game)
    after_twenty_messages = messages[0].slice_messages_with_rallies(after_twenty_rallies)
    shares_after_twenty[game.teams[0]].make_action_and_time(after_twenty_messages, game, "공격종합")

    after_twenty_rallies = rallies.select_rally_with_score([[20, 100, 1]], set_in_game)
    after_twenty_messages = messages[1].slice_messages_with_rallies(after_twenty_rallies)
    shares_after_twenty[game.teams[1]].make_action_and_time(after_twenty_messages, game, "공격종합")

    foreigners = team_and_foreign_2020[game.teams[0]]
    foreign_forward_rallies = rallies.select_rally_with_rotation(foreigners, [True for _ in foreigners], Rally.LEFT, False)
    foreigner_forward_messages = messages[0].slice_messages_with_rallies(foreign_forward_rallies)
    forward_shares[game.teams[0]].make_action_and_time(foreigner_forward_messages, game, "공격종합")

    foreigners = team_and_foreign_2020[game.teams[1]]
    foreign_forward_rallies = rallies.select_rally_with_rotation(foreigners, [True for _ in foreigners], Rally.RIGHT, False)
    foreigner_forward_messages = messages[1].slice_messages_with_rallies(foreign_forward_rallies)
    forward_shares[game.teams[1]].make_action_and_time(foreigner_forward_messages, game, "공격종합")

    foreigners = team_and_foreign_2020[game.teams[0]]
    foreign_backward_rallies = rallies.select_rally_with_rotation(foreigners, [False for _ in foreigners], Rally.LEFT, False)
    foreigner_backward_messages = messages[0].slice_messages_with_rallies(foreign_backward_rallies)
    backward_shares[game.teams[0]].make_action_and_time(foreigner_backward_messages, game, "공격종합")

    foreigners = team_and_foreign_2020[game.teams[1]]
    foreign_backward_rallies = rallies.select_rally_with_rotation(foreigners, [False for _ in foreigners], Rally.RIGHT, False)
    foreigner_backward_messages = messages[1].slice_messages_with_rallies(foreign_backward_rallies)
    backward_shares[game.teams[1]].make_action_and_time(foreigner_backward_messages, game, "공격종합")


stat.process_in_set(make_share)

fig = plt.figure()
i = 0
for share in shares_after_three_points.items():
    i += 1
    print(share[1].sort_share().print_share("공격 정유율", limit=5))
    share[1].make_share_graph(fig, share[0], 320+i, limit=5)
    share[1].comparing_share_graph([shares_after_three_opposite_points[share[0]], shares[share[0]]], fig, ["3점 이상 연속 득점", "3점 이상 연속 실점", "전체"], share[0], 320 + i, limit=5)
fig.tight_layout()
plt.savefig("./3점 이상 연속 득점 - 3점 이상 연속 실점.png", dpi=300)

for share in shares_after_three_opposite_points.items():
    print(share[1].sort_share().print_share("공격 점유율", limit=5))

print("-" * 100)


fig = plt.figure()
i = 0
for share in shares_after_twenty.items():
    i += 1
    print(share[1].sort_share().print_share("공격 정유율", limit=5))
    share[1].make_share_graph(fig, share[0], 320+i, limit=5)
    share[1].comparing_share_graph([shares[share[0]]], fig, ["20점 이상", "전체"], share[0], 320 + i, limit=5)
fig.tight_layout()
plt.savefig("./20점 이상 - 전체.png", dpi=300)

print("-" * 100)

fig = plt.figure()
i = 0
for share in forward_shares.items():
    i += 1
    print(share[1].sort_share().print_share("공격 정유율", limit=5))
    share[1].make_share_graph(fig, share[0], 320+i, limit=5)
    share[1].comparing_share_graph([backward_shares[share[0]]], fig, ["외국인 선수 전위", "외국인 선수 후위"], share[0], 320 + i, limit=5)
fig.tight_layout()
plt.savefig("./외국인 선수 전위-후위 점유율.png", dpi=300)

for share in backward_shares.items():
    print(share[1].sort_share().print_share("공격 점유율", limit=5))

print("-" * 100)

for share in shares.items():
    print(share[1].sort_share().print_share("공격 점유율", limit=5))
