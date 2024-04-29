from typing import List, Any, Tuple


def run_process(process: Any, arguments: Tuple = None) -> List:
    """
    Starts the process.

    Parameters:
    - process [any]: Class object.
    - arguments [tuple]: Tuple of arguments for process.

    Returns:
    - List: List of collected files.
    """
    if not arguments:
        return process.run()

    return process(*arguments).run()
