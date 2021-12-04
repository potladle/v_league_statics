from volleyball.stat.message.BlockingMessage import *
from volleyball.stat.message.AttackMessage import *
from volleyball.stat.message.SubstituteMessage import *
from volleyball.stat.message.TeamMessage import *
from volleyball.stat.message.SetMessage import *
from volleyball.stat.message.ServeMessage import *
from volleyball.stat.message.EtcMessage import *
from volleyball.stat.message.FaultMessage import *
from volleyball.stat.message.DefenseMessage import *
from volleyball.stat.message.Message import NoneMessage

action_with_name = ['투입', '세트', '스파이크서브', '세트퇴장', '디그', '벌칙', '서브'
                    , '시간차', '퀵오픈', '블로킹어시스트', '오픈', '리시브', '백어택', '유효블로킹'
                    , '블로킹', '속공', '교체', '이동', '포지션폴트', '기타범실', '경고']

action_with_result = ['세트', '스파이크서브', '디그', '서브'
                      , '시간차', '퀵오픈', '오픈', '리시브', '백어택'
                      , '블로킹', '속공', '이동']

action_with_lose_way = ['스파이크서브', '서브'
                        , '시간차', '퀵오픈', '오픈', '백어택'
                        , '속공', '이동']

message_end_all_rally = [AttackMessage, TeamMessage, ServeMessage]
message_end_lose_rally = [SetMessage]
message_end_lose_rally_after_opposite = [DefenseMessage, BlockMessage]

action_to_class = \
    {'투입': SubstituteInMessage
        , '세트': SetMessage
        , '스파이크서브': SpikeServeMessage
        , '세트퇴장': ExitMessage
        , '디그': DigMessage
        , '벌칙': PenaltyMessage
        , '서브': PlotterServeMessage
        , '경고': WarningMessage
        , '개인경고': PersonalWarningMessage
        , '팀 포지션폴트': PositionFaultMessage
        , '시간차': TimeLagMessage
        , '퀵오픈': QuickOpenMessage
        , '타임': TimeMessage
        , '블로킹어시스트': BlockAssistMessage
        , '오픈': OpenMessage
        , '팀실패': TeamMessage
        , '리시브': ReceiveMessage
        , '팀 기타범실': EtcFaultMessage
        , '백어택': BackAttackMessage
        , '팀득점': TeamMessage
        , '유효블로킹': EffectiveBlockMessage
        , '블로킹': BlockMessage
        , '속공': QuickMessage
        , '교체': SubstituteOutMessage
        , '이동': MoveMessage
        , '공격종합': AttackMessage
        , '수비종합': DefenseMessage
        , '범실종합': FaultMessage
        , '서브종합': ServeMessage
        , '': NoneMessage
        , '전체': Message}

error_to_num = \
    {'라인오버': Message.LINE_OVER,
     '더블컨텍트': Message.DOUBLE_CONTACT,
     '캐치볼': Message.CATCH_BALL,
     '오버네트': Message.OVER_NET,
     '포히트': Message.FOUR_HIT,
     '네트터치': Message.NET_TOUCH,
     '네트걸림' : Message.NET_CAUGHT,
     '아웃' : Message.OUT,
     '기타범실': Message.ETC_ERROR}

women_teams = ["한국도로공사", "현대건설", "GS칼텍스", "IBK기업은행", "흥국생명", "KGC인삼공사", "페퍼저축은행"]
team_and_foreign_2020 = {"한국도로공사": ["켈시"], "현대건설": ["루소"], "GS칼텍스": ["러츠"], "IBK기업은행": ["라자레바"], "흥국생명": ["루시아", "브루나"], "KGC인삼공사": ["디우프"]}
color = ["r", "g", "b", "c", "y", "w"]
attack_types = ["오픈", "백어택", "퀵오픈", "시간차", "속공", "이동"]
