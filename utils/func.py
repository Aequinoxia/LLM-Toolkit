import math
from typing import List


def paginate(items: List, page_size: int, page_index: int):
    """
    [Example]
        paginate(items=list(range(1, 6)), page_size=3, page_index=1)
        >>> ([1, 2, 3], 1, 2)
        paginate(items=list(range(1, 6)), page_size=3, page_index=2)
        >>> ([4, 5], 2, 2)
    """
    assert len(items) > 0 and page_size > 0
    total_pages = math.ceil(len(items) / page_size)
    revised_page_index = (page_index-1) % total_pages  # Assume `page_index` starts from 1
    return items[
        revised_page_index * page_size: 
        (revised_page_index + 1) * page_size
    ], revised_page_index + 1, total_pages