from dataclasses import dataclass
from datetime import date


@dataclass
class StatisticsCounts:
    guests: int
    passive_member: int
    managers: int
    super_members: int


@dataclass
class StatisticsData:
    statistics_per_day: dict[date, StatisticsCounts]
