from math import ceil


class Paginator:
    def __init__(self, array: list | tuple | set, page: int = 1, per_page: int = 1):
        self.array = array
        self.page = page
        self.per_page = per_page
        self.len = len(array)
        self.total_pages = ceil(self.len / self.per_page)

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.total_pages:
            return self.page + 1
        return False

    def has_prev(self):
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self):
        if next_page := self.has_next():
            self.page = next_page
            return self.get_page()
        return None

    def get_previous(self):
        if prev_page := self.has_prev():
            self.page = prev_page
            return self.get_page()
        return None
