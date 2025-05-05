import subprocess
import json
from typing import Optional
import logging
from egg_counter_shared import helper

logger = logging.getLogger(__name__)


class EggCounterController:
    def __init__(self):
        self.script_path = helper.script_path()
        self.process: Optional[subprocess.Popen] = None

    def start(self, house_number: int, values: helper.SettingsUpdate) -> None:
        if self.process and self.process.poll() is None:
            logger.info("Counter already running.")
            return
        logger.info(f"Starting counter for house {house_number}.")
        config_json = json.dumps(values)
        self.process = subprocess.Popen(
            [
                "python",
                self.script_path,
                "--command",
                "run",
                "--house_number",
                str(house_number),
                "--config",
                config_json,
            ]
        )

    def stop(self) -> None:
        if self.process and self.process.poll() is None:
            logger.info("Stopping counter.")
            self.process.terminate()
            self.process.wait()


counter = EggCounterController()
