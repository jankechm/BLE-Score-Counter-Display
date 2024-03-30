# Author: Marek Jankech

import app.font as mx_font
import app.constants as const
import uasyncio as asyncio
from app.data import Score
from app.hw import display, rtc
from app.decorator import singleton

class MxRenderable:
    """
    Abstract class represents information that could be directly rendered
    on the matrix display.
    """

    def render(self, x_shift=0, pre_clear=True, redraw=True):
        pass

class MxNumeric(MxRenderable):
    """
    Represents a numeric information that could be directly rendered
    on the matrix display.
    """

    def __init__(self):
        self._matrix = display

    def _render_2_digit_num(self, num, x_shift=0):
        (tens, ones) = divmod(num, 10)
        ft = mx_font.Medium()

        for digit in [tens, ones]:
            char = ft.get(str(digit))
            char.x_shift(x_shift)
            char.render(self._matrix.fb)

            x_shift += const.COLS_IN_MATRIX

class MxScore(MxNumeric):
    """
    Represents the whole score of both teams that could be rendered 
    on a display.
    """

    ZERO_TENS_DIGIT = 0
    ONE_TENS_DIGIT = 1

    MIN_SCORE = 0
    MAX_SCORE = 99

    class SingleOneDigit(MxRenderable):
        """
        Represents 1 part (left or right) of one-digit-only score (0 - 9).
        """

        X_OFFSET = 4
        X_OFFSET_FOR_1 = 7

        def __init__(self, digit, side):
            self._digit = digit
            self._side = side
            self._matrix = display

        def render(self, x_shift=0):
            offset = x_shift

            if self._digit == 1:
                offset += self.X_OFFSET_FOR_1
            else:
                offset += self.X_OFFSET

            if self._side == const.RIGHT:
                offset += const.RIGHT_SIDE_X_OFFSET

            font = mx_font.BigDigit()

            renderable = font.get(self._digit)
            renderable.x_shift(offset)
            renderable.render(self._matrix.fb)

    class SingleTwoDigit(MxRenderable):
        """
        Represents 1 part (left or right) of two-digit score,
        where digit 1 is on the place of tens (score 10 - 19).
        """

        TENS_X_OFFSET = 2
        ONES_X_OFFSET = 6
        ONES_X_OFFSET_FOR_1 = 12

        def __init__(self, tens, ones, side):
            self._tens = tens
            self._ones = ones
            self._side = side
            self._matrix = display

        def render(self, x_shift=0):
            tens_offset = x_shift
            ones_offset = x_shift

            tens_offset += self.TENS_X_OFFSET

            if self._ones == 1:
                ones_offset += self.ONES_X_OFFSET_FOR_1
            else:
                ones_offset += self.ONES_X_OFFSET

            if self._side == const.RIGHT:
                tens_offset += const.RIGHT_SIDE_X_OFFSET
                ones_offset += const.RIGHT_SIDE_X_OFFSET

            font = mx_font.BigDigit()

            renderable_ones = font.get(self._tens)
            renderable_ones.x_shift(tens_offset)
            renderable_ones.render(self._matrix.fb)

            renderable_ones = font.get(self._ones)
            renderable_ones.x_shift(ones_offset)
            renderable_ones.render(self._matrix.fb)

    class SingleHigherTwoDigit(MxNumeric):
        """
        Represents 1 part (left or right) of two-digit score,
        where digit higher than 1 is on the place of tens (score 20 - 99).
        The main difference is in the used font, which is smaller
        than the font used in classes represting score lower than 20.
        The reason for that is that the digits of tens and ones would blend
        on the display if a bigger font would be used.
        """

        RIGHT_SCORE_X_SHIFT = 18

        def __init__(self, single_score, side):
            super().__init__()

            self._single_score = single_score
            self._side = side

        def render(self, x_shift=0):
            if self._side == const.RIGHT:
                x_shift += self.RIGHT_SCORE_X_SHIFT

            self._render_2_digit_num(self._single_score, x_shift)
    
    
    def __init__(self) -> None:
        super().__init__()

        self._score = Score(0,0)

    def set_score(self, l_val, r_val):
        self.set_left(l_val)
        self.set_right(r_val)

    def set_left(self, val):
        if val > self.MAX_SCORE:
            self._score.left = self.MAX_SCORE
        elif val < self.MIN_SCORE:
            self._score.left = self.MIN_SCORE
        else:
            self._score.left = val

    def set_right(self, val):
        if val > self.MAX_SCORE:
            self._score.right = self.MAX_SCORE
        elif val < self.MIN_SCORE:
            self._score.right = self.MIN_SCORE
        else:
            self._score.right = val

    def render(self, x_shift=0, pre_clear=True, redraw=True, render_delim=True):
        if pre_clear:
            self._matrix.fill(0)

        (l_tens, l_ones) = divmod(self._score.left, 10)
        (r_tens, r_ones) = divmod(self._score.right, 10)

        if l_tens > self.ONE_TENS_DIGIT or r_tens > self.ONE_TENS_DIGIT:
            l_score = self.SingleHigherTwoDigit(self._score.left, const.LEFT)
            r_score = self.SingleHigherTwoDigit(self._score.right, const.RIGHT)
        else:
            if l_tens == self.ZERO_TENS_DIGIT:
                l_score = self.SingleOneDigit(l_ones, const.LEFT)
            else:
                l_score = self.SingleTwoDigit(l_tens, l_ones, const.LEFT)

            if r_tens == self.ZERO_TENS_DIGIT:
                r_score = self.SingleOneDigit(r_ones, const.RIGHT)
            else:
                r_score = self.SingleTwoDigit(r_tens, r_ones, const.RIGHT)

        l_score.render(x_shift)
        if render_delim:
            self._render_score_delimiter(x_shift)
        r_score.render(x_shift)

        if redraw:
            self._matrix.redraw_twice()

    def _render_score_delimiter(self, x_shift):
        self._matrix.hline(15 + x_shift, 7, 2, 1)
        self._matrix.hline(15 + x_shift, 8, 2, 1)

    async def render_change(self, l_val: int, r_val: int):
        """
        Indicate new score being set.
        If both sides are being changed, blink with the whole display.
        If one side is being changed, blink just with that score part.
        If the both values are the same, blink just with the delimiter.
        """

        self.render()
        await asyncio.sleep_ms(300)

        if self._score.left != l_val:
            if self._score.right != r_val:
                self._matrix.fill(0)
                self._matrix.redraw_twice()
            else:
                self._matrix.clear_half(const.LEFT)
        elif self._score.right != r_val:
            self._matrix.clear_half(const.RIGHT)
        else:
            self.render(render_delim=False)
        
        self.set_score(l_val, r_val)
        await asyncio.sleep_ms(400)
        self.render()

# @singleton
# class MxDate(MxNumeric):
#     DAY_X_SHIFT = 18
#     DAY_ORDINAL_DOT_X_SHIFT = 18

#     def __init__(self) -> None:
#         super().__init__()

#         self._rtc = rtc
#         self.pull()

#     def pull(self):
#         """
#         Fetch the date from the Real Time Clock module.
#         """

#         datetime = self._rtc.get_time()

#         self._day = datetime.date
#         self._month = datetime.month
#         self._year = datetime.year

#     def render(self, x_shift=0, pre_clear=True, redraw=True):
#         """
#         Render the day and month with their ordinal dots. No year rendering.
#         This is intended for rendering during basic operation mode.
#         """

#         self.pull()

#         if pre_clear:
#             self._matrix.fill(0)

#         self._render_2_digit_num(self._day, x_shift)
#         self._render_ordinal_dot(x_shift)
#         self._render_2_digit_num(self._month, x_shift + self.DAY_X_SHIFT)
#         self._render_ordinal_dot(x_shift + self.DAY_ORDINAL_DOT_X_SHIFT)

#         if redraw:
#             self._matrix.redraw_twice()

#     def _render_ordinal_dot(self, x_shift=0):
#         self._matrix.hline(15 + x_shift, 13, 2, 1)
#         self._matrix.hline(15 + x_shift, 14, 2, 1)

@singleton
class MxTime(MxNumeric):
    MINUTES_X_SHIFT = 18

    def __init__(self) -> None:
        super().__init__()
        
        self.pull()

    def pull(self):
        """
        Fetch the time from the Real Time Clock module.
        """

        datetime = rtc.datetime()

        self._hours = datetime[const.RTC_HOURS_IDX]
        self._minutes = datetime[const.RTC_MINUTES_IDX]

    def render(self, x_shift=0, pre_clear=True, redraw=True):
        """
        This method pulls the actual time from the RTC module before rendering.
        """

        self.pull()

        self._matrix.fill(0)

        self._render_2_digit_num(self._hours, x_shift)
        self._render_time_delimiter(x_shift)
        self._render_2_digit_num(self._minutes, x_shift + self.MINUTES_X_SHIFT)

        self._matrix.redraw_twice()

    def _render_time_delimiter(self, x_shift=0):
        self._matrix.hline(15 + x_shift, 4, 2, 1)
        self._matrix.hline(15 + x_shift, 5, 2, 1)
        self._matrix.hline(15 + x_shift, 10, 2, 1)
        self._matrix.hline(15 + x_shift, 11, 2, 1)

