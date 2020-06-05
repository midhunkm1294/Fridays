__all__ = ['friday']

import os
import sys
import asyncio
import importlib
from types import ModuleType
from typing import List

import psutil

from friday import logging, Config
from friday.plugins import get_all_plugins
from .methods import Methods

_LOG = logging.getLogger(__name__)
_LOG_STR = "<<<!  #####  %s  #####  !>>>"


class friday(Methods):
    """friday, the userbot"""
    def __init__(self) -> None:
        self._imported: List[ModuleType] = []
        _LOG.info(_LOG_STR, "Setting friday Configs")
        super().__init__(client=self,
                         session_name=Config.HU_STRING_SESSION,
                         api_id=Config.API_ID,
                         api_hash=Config.API_HASH)

    @staticmethod
    def getLogger(name: str) -> logging.Logger:
        """This returns new logger object"""
        _LOG.debug(_LOG_STR, f"Creating Logger => {name}")
        return logging.getLogger(name)

    def load_plugin(self, name: str) -> None:
        """Load plugin to friday"""
        _LOG.debug(_LOG_STR, f"Importing {name}")
        self._imported.append(
            importlib.import_module(f"friday.plugins.{name}"))
        _LOG.debug(_LOG_STR, f"Imported {self._imported[-1].__name__} Plugin Successfully")

    def load_plugins(self) -> None:
        """Load all Plugins"""
        self._imported.clear()
        _LOG.info(_LOG_STR, "Importing All Plugins")
        for name in get_all_plugins():
            try:
                self.load_plugin(name)
            except ImportError as i_e:
                _LOG.error(_LOG_STR, i_e)
        _LOG.info(_LOG_STR, f"Imported ({len(self._imported)}) Plugins => "
                  + str([i.__name__ for i in self._imported]))

    async def reload_plugins(self) -> int:
        """Reload all Plugins"""
        self.manager.clear_plugins()
        reloaded: List[str] = []
        _LOG.info(_LOG_STR, "Reloading All Plugins")
        for imported in self._imported:
            try:
                reloaded_ = importlib.reload(imported)
            except ImportError as i_e:
                _LOG.error(_LOG_STR, i_e)
            else:
                reloaded.append(reloaded_.__name__)
        _LOG.info(_LOG_STR, f"Reloaded {len(reloaded)} Plugins => {reloaded}")
        return len(reloaded)

    async def restart(self, update_req: bool = False) -> None:
        """Restart the friday"""
        _LOG.info(_LOG_STR, "Restarting friday")
        await self.stop()
        try:
            c_p = psutil.Process(os.getpid())
            for handler in c_p.open_files() + c_p.connections():
                os.close(handler.fd)
        except Exception as c_e:
            _LOG.error(_LOG_STR, c_e)
        if update_req:
            _LOG.info(_LOG_STR, "Installing Requirements...")
            os.system("pip3 install -U pip")
            os.system("pip3 install -r requirements.txt")
        os.execl(sys.executable, sys.executable, '-m', 'friday')
        sys.exit()

    def begin(self) -> None:
        """This will start the friday"""
        loop = asyncio.get_event_loop()
        run = loop.run_until_complete
        _LOG.info(_LOG_STR, "Starting friday")
        run(self.start())
        running_tasks: List[asyncio.Task] = []
        for task in self._tasks:
            running_tasks.append(loop.create_task(task()))
        _LOG.info(_LOG_STR, "Idling friday")
        run(friday.idle())
        _LOG.info(_LOG_STR, "Exiting friday")
        for task in running_tasks:
            task.cancel()
        run(self.stop())
        for task in asyncio.all_tasks():
            task.cancel()
        run(loop.shutdown_asyncgens())
        loop.close()
