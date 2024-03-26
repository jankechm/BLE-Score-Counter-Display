# Author: Marek Jankech

class Score:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Datetime:
    def __init__(self, year, month, date, hours, minutes, seconds, weekday):
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.weekday = weekday
        self.date = date
        self.month = month
        self.year = year

class Config:
    def __init__(self, use_score: bool, use_date: bool, use_time: bool,
        scroll: bool, bright_lvl: int) -> None:
        self.use_score = use_score
        self.use_date = use_date
        self.use_time = use_time
        self.scroll = scroll
        self.bright_lvl = bright_lvl

