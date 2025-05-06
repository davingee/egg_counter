import subprocess
import json
from typing import Optional
import logging
from shared import helper

logger = logging.getLogger(__name__)
import os
env = os.environ.copy()
env["PYTHONPATH"] = "."

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
            ],
        cwd="../",  # IMPORTANT: this should be where app/, counter/, shared/ live
        env=env,
        start_new_session=False
        )


    def stop(self) -> None:
        if self.process and self.process.poll() is None:
            logger.info("Stopping counter.")
            # self.process.terminate()
            # self.process.wait()

            self.process.terminate()

            try:
                self.process.wait(timeout=2)  # seconds to wait for graceful exit
            except subprocess.TimeoutExpired:
                print("Process did not terminate in time; killing it.")
                self.process.kill()  # force kill
                self.process.wait() #sdfdasdf

counter = EggCounterController()
