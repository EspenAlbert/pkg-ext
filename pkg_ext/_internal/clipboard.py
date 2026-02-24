import logging
import subprocess
from shutil import which

logger = logging.getLogger(__name__)


def add_to_clipboard(content: str) -> None:
    if bin_path := which("pbcopy"):
        subprocess.run(bin_path, text=True, input=content, check=True)  # nosec
        logger.info("Copied to clipboard")
    else:
        logger.warning("pbcopy not found on $PATH")
        logger.info("Please copy the content manually")
