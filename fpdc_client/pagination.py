# from urllib.parse import urlparse, parse_qs


class Paginator:
    def __init__(self, start_page=1):
        # self.page = start_page - 1
        self._results_left = True
        self.total = None

    @property
    def results_left(self):
        return self._results_left

    def read_results(self, results):
        self.total = results.get("count")
        if not results.get("next"):
            self._results_left = False
            # if self.page == 0:
            #    self.page = 1
            return
        self._results_left = True
        # next_page = parse_qs(urlparse(results["next"]).query)
        # next_page = next_page.get("page")[0]
        # next_page = int(next_page)
        # self.page = next_page - 1

    # @property
    # def next_page(self):
    #    return self.page + 1

    # @property
    # def previous_page(self):
    #    return self.page + 1
