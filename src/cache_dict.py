import os
import shelve

from cachetools import LRUCache


class CacheDict:
    """
    Dictionary wrapper that creates a dictionary that
    frequently saves to file but has an in memory
    read cache.
    """

    __slots__ = ['_file_dict', '_cache']

    def __len__(self):
        return len(self._file_dict)

    def _prepare_path(self, directory, rank, t="stats"):
        """
        Helper function. Takes a directory and makes sure
        the directory plays nice with the other functions
        that require it.
        """
        if directory is None:
            directory = ''
        else:
            if directory[-1] != '/':
                directory = directory + '/'
        directory = directory + t + '/' + str(rank) + '/'
        try:
            os.makedirs(directory)
        except OSError:  # File exists.
            pass

        return directory

    def __init__(self, name, directory, rank, max_size=100, t="stats"):
        self._file_dict = shelve.open(
            self._prepare_path(directory, rank, t=t) + name
        )
        self._cache = LRUCache(maxsize=max_size)

    def __getitem__(self, key):
        try:
            # Need the additional step in case of KeyError
            if isinstance(key, int):
                return self._cache[str(key)]
            else:
                return self._cache[key]
        except KeyError:
            # Need the additional step in case of KeyError
            if isinstance(key, int):
                item = self._file_dict[str(key)]
                self._cache[str(key)] = item
                return item
            else:
                item = self._file_dict[key]
                self._cache[key] = item
                return item

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._file_dict[str(key)] = value
            self._cache[str(key)] = value
        else:
            self._file_dict[key] = value
            self._cache[key] = value

    def __delitem__(self, key):
        if isinstance(key, int):
            del self._file_dict[str(key)]
            del self._cache[str(key)]
        else:
            del self._file_dict[str(key)]
            del self._cache[str(key)]

    def __contains__(self, item):
        return item in self._file_dict
