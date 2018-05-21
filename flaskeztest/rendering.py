
import re

# Stores the number of times a test id has been subsituted in so that the currect index can be included
#   in eztestid attribute
id_iterations = dict()


def render_eztestids(source):

    def sub_func(match_obj):
        """
        Matches against _eztestid(testid)
        returns _eztestid=testid(with row index in test id)
        """
        match = match_obj.group(0)
        testid_match = re.search(r'(?<=\().*(?>=\))', match).group(0)
        table_name = testid_match.split('.')[0]
        if table_name not in id_iterations:
            id_iterations[table_name] = 1
        else:
            id_iterations[table_name] += 1
        testid_match = testid_match.split('.')
        testid_match[0] += '[%s]' % id_iterations[testid_match]
        testid_match = '.'.join(testid_match)

    re.sub(
        r"_eztestid\(.*\)",
        sub_func,
        source
    )