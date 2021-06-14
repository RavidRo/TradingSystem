from dataclasses import dataclass


@dataclass
class StatisticsCounts:
    guests: int
    passive_member: int
    managers: int
    owners: int
    super_members: int


@dataclass
class StatisticsData:
    statistics_per_day: dict[str, StatisticsCounts]
