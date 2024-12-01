class LRUCache:
    def __init__(self, capacity: int):
        self.struct = OrderedDict()
        self.cap = capacity

    def get(self, key: int) -> int:
        return self.struct.get(key, -1)

    def put(self, key: int, value: int) -> None:
        if key in self.struct:
            self.struct.move_to_end(key)

        if len(self.struct) >= self.cap:
            self.struct.popitem(last=False)
        self.struct[key] = value
