# Widget brief: Binary search only works on sorted data

Cluster id: `binary-search-requires-sorted-data`  |  serves 4 lessons

## The one thing the widget must make concrete

The halving strategy of binary search depends on the list being sorted; on unsorted data it cannot reliably locate items.

## The lessons it will sit in

### 1. [computer-science-aqa] Searching Algorithms: Linear and Binary Search — `/lesson/computer-science-aqa/algorithms/3`
Triage: Students think binary search is always faster and should always be used, not understanding that the halving only works because the list is sorted, and that sorting cost + search cost must be weighed against a single linear pass.

> Why Search Algorithms Matter Searching is one of the most common operations in computing. Every time you look up a contact on your phone, find a product on a retail site, or ask a search engine a question, a search algorithm is at work. The specification requires you to know two: linear search and binary search. Crucially, you must be able to compare them &mdash; choosing the right algorithm for a given situation is a practical engineering skill. Linear Search Linear search is the simplest approach. Starting at the beginning of the list, it checks each item in turn: does this match the target? If yes, return its position. If no, move to the next item. If the end of the list is reached without a match, the target is not present. Linear search works on any list &mdash; sorted or unsorted. This makes it very flexible. You do not need to sort the data first, which saves time when you only ne...

### 2. [computer-science-edexcel] Standard Algorithms: Bubble Sort, Merge Sort, Linear and Binary Search — `/lesson/computer-science-edexcel/computational-thinking/4`
Triage: Students think binary search is always faster because it 'halves' the search space, without grasping that this only works because the data is already sorted, and that the sorting cost itself must be paid upfront.

> Why Standard Algorithms Matter Searching and sorting data are the most common operations in computing. Every time you look up a contact on your phone, find a track in a music library, or see a leaderboard ranked by score, a search algorithm or sorting algorithm is at work. Your specification requires you to know four standard algorithms: two for searching (linear search and binary search) and two for sorting (bubble sort and merge sort). Linear Search Linear search is the simplest approach. Starting at the beginning of the list, it checks each item in turn: does this match the target? If yes, return its position. If no, move to the next item. If the end of the list is reached without a match, the target is not present. Linear search works on any list &mdash; sorted or unsorted. This makes it very flexible. You do not need to sort the data first, which is a significant advantage when you ...

### 3. [computer-science-eduqas] Searching: Linear and Binary — `/lesson/computer-science-eduqas/algorithms-programming-software/3`
Triage: Students think binary search is always faster and better, without recognising that the repeated halving only works because the list is sorted—they may imagine it 'just works' on unsorted data by luck, or believe the speed gain is automatic rather than dependent on a precondition.

> Why Searching Matters Searching is one of the most fundamental operations in computing. Every time you look up a contact on your phone, query a database, or ask a search engine a question, a search algorithm is running in the background. Your exam covers two searching algorithms: linear search and binary search . Understanding when to use each one, and being able to trace them by hand, are core exam skills. Linear Search Linear search (also called sequential search) is the simplest possible search algorithm. It checks each item in the list from the first to the last, one at a time, until it either finds the target or runs out of items. It works on any list &mdash; sorted or unsorted. Below is a linear search in pseudocode. It searches a list called names for the value stored in target : SET found = FALSE SET i = 0 WHILE i &lt; LENGTH(names) AND found = FALSE IF names[i] = target THEN SET...

### 4. [computer-science] Searching Algorithms — `/lesson/computer-science/computational-thinking/3`
Triage: Students believe binary search is always faster and should always be used, not understanding that it requires sorted data and that the cost of sorting must be factored in; they also struggle to visualize why halving works exponentially better than linear checking.
