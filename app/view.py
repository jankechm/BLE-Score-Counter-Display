# Author: Marek Jankech

import uasyncio as asyncio
import ujson as json
import app.constants as const
from app.adt import CircularList
from app.hw import display
from app.mx_data import MxRenderable, MxDate, MxTime
from app.data import Config

SPACE = 8

FIVE_MILLIS = 5
TEN_MILLIS = 10

NO_VIEW = 0

class BasicViewer:
    ONE_INFO_LEN = 32
    TWO_INFO = 2
    
    SCROLL_MODE = 1
    ALTERNATE_MODE = 2

    def __init__(self):
        self.config = self._load_cfg()
        
        self.score = None
        self._to_render = []

        self._set_rendering_options()

    def disable(self):
        self._view_mode = NO_VIEW

    async def view_info(self):
        self._set_rendering_options()

        if self._view_mode == self.SCROLL_MODE:
            await self._scroll()
        else:
            await self._alternate()

    def _load_cfg(self):
        config = Config(True, False, False, const.INITIAL_BRIGHTNESS)

        try:
            with open(const.DATA_DIR + "/" + const.CONFIG_FILE, "r") as f:
                cfg_str = f.readline()
                cfg_dict = json.loads(cfg_str)
                config = Config(**cfg_dict)
                print("Loaded config: {}".format(config))
        except (OSError, ValueError, TypeError):
            print("Unable to read persisted configuration!" + 
                  "Using default configuration: {}".format(config))
            
        return config
    
    def _set_rendering_options(self):
        self._to_render = []

        display.set_brightness(self.config.bright_lvl)

        if self.config.use_score and self.score is not None:
            self._to_render.append(self.score)
        if self.config.use_time:
            self._to_render.append(MxTime())
        
        if self.config.scroll:
            self._view_mode = self.SCROLL_MODE
        else:
            self._view_mode = self.ALTERNATE_MODE

    async def _alternate(self):
        """
        This couroutine can alternate multiple text information on the display
        based on loaded configuration from the memory.
        It loops through a circular list of renderable info, so unless 
        :func:`disable` is called, it never ends.
        """

        if self._to_render:
            circular_to_render = CircularList(self._to_render)

            while self._view_mode == self.ALTERNATE_MODE:
                circular_to_render.next().render()
                await asyncio.sleep_ms(2000)

    async def _scroll(self):
        """
        This couroutine can scroll multiple text information on the display
        based on loaded configuration from the memory.
        It loops through a circular list of renderable info, so unless 
        :func:`disable` is called, it never ends.
        """

        if self._to_render:
            circular_to_render = CircularList(self._to_render)

            obj1 = circular_to_render.next()
            await self._scroll_basic_info_1(obj1)

            while self._view_mode == self.SCROLL_MODE:
                obj2 = circular_to_render.next()
                await self._scroll_basic_info_2(obj1, obj2)

                obj1 = obj2

    async def _scroll_basic_info_1(self, obj: MxRenderable):
        """
        This couroutine is intended to be called once at the beginning
        of text scrolling, when there was no previous text displayed.
        Only one text info is displayed.
        """

        for x_shift in range(self.ONE_INFO_LEN, 0, -1):
            if self._view_mode != self.SCROLL_MODE:
                break
            
            obj.render(x_shift)

            await asyncio.sleep_ms(TEN_MILLIS)

    async def _scroll_basic_info_2(self, obj1: MxRenderable, obj2: MxRenderable):
        """
        This couroutine is intended to be called in a cycle, 
        if the :func:`_scroll_basic_info_1` was already called right before.
        It starts where the :func:`_scroll_basic_info_1` ended and
        ends with the second text info displayed.
        """

        for x_shift in range(0, -(SPACE + self.ONE_INFO_LEN), -1):
            if self._view_mode != self.SCROLL_MODE:
                break
            
            display.fill(0)

            obj1.render(x_shift, False, False)
            obj2.render(x_shift + SPACE + self.ONE_INFO_LEN, False, False)

            display.redraw_twice()

            await asyncio.sleep_ms(FIVE_MILLIS)
