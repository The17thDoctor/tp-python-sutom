from importlib.abc import Traversable
import importlib.resources

package_directory: Traversable = importlib.resources.files()
DICTIONARY_PATH: str = str(package_directory) + "\\dictionary.txt"