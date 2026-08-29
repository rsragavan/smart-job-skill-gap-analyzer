"""Small, idempotent starter bank for the generic preparation experience."""
from sqlalchemy.orm import Session

from app.models.content import CodingQuestion, InterviewQuestion, LearningResource

SOURCE = "Curated educational content"

QUESTION_DETAILS = {
    "Find the largest element in an array": {
        "description": "Given an array of integers, return its largest element.",
        "input_format": "arr is a non-empty list of integers.",
        "output_format": "Return the largest integer in arr.",
        "constraints": "1 <= len(arr) <= 10^5; values fit in a signed 32-bit integer.",
        "examples": [{"input": "[10, 5, 25, 8, 17]", "output": "25"}, {"input": "[1, 2, 3, 4, 5]", "output": "5"}, {"input": "[-10, -3, -20, -1]", "output": "-1"}],
        "explanation": "Scan the array once while tracking the greatest value seen so far.",
        "expected_complexity": "Time O(n)", "expected_space_complexity": "Space O(1)",
        "starter_code": "def find_largest(arr):\n    # Return the largest value in arr.\n    pass\n",
        "function_signature": "find_largest(arr: list[int]) -> int",
        "test_cases": [{"input": "[10, 5, 25, 8, 17]", "expected": "25"}, {"input": "[1, 2, 3, 4, 5]", "expected": "5"}, {"input": "[-10, -3, -20, -1]", "expected": "-1"}],
        "hints": ["Initialize the best value from the first element.", "Update it when a larger value is found."], "tags": ["arrays", "linear-scan"]
    },
    "Two Sum": {
        "description": "Given a list of integers and a target, return the indices of two distinct values whose sum equals the target. Return an empty list only if no pair exists.",
        "input_format": "nums is a list of integers; target is an integer.", "output_format": "Return [i, j] with i < j, or [] when no pair exists.",
        "constraints": "2 <= len(nums) <= 10^4; -10^9 <= nums[i], target <= 10^9.",
        "examples": [{"input": "nums = [2, 7, 11, 15], target = 9", "output": "[0, 1]", "explanation": "2 + 7 equals 9."}, {"input": "nums = [3, 2, 4], target = 6", "output": "[1, 2]", "explanation": "2 + 4 equals 6."}],
        "explanation": "Scan once while storing each value's index in a hash map. Before storing nums[i], look for target - nums[i].", "expected_complexity": "Time O(n)", "expected_space_complexity": "Space O(n)", "starter_code": "def two_sum(nums, target):\n    # Return the indices of the matching pair.\n    pass\n", "function_signature": "two_sum(nums: list[int], target: int) -> list[int]", "test_cases": [{"input": "[2,7,11,15], 9", "expected": "[0,1]"}, {"input": "[3,2,4], 6", "expected": "[1,2]"}, {"input": "[3,3], 6", "expected": "[0,1]"}], "hints": ["Compare each value with the complement needed to reach target.", "Use a dictionary for constant-time average lookup.", "Check the complement before inserting the current value."], "tags": ["arrays", "hashing", "two-pointers"]
    },
    "Valid Anagram": {
        "description": "Determine whether two lowercase strings contain exactly the same characters with the same frequencies.", "input_format": "s and t are two strings.", "output_format": "Return True when t is an anagram of s; otherwise return False.", "constraints": "0 <= len(s), len(t) <= 5 * 10^4; strings contain lowercase English letters.", "examples": [{"input": "s = 'anagram', t = 'nagaram'", "output": "True", "explanation": "Both strings contain the same character counts."}, {"input": "s = 'rat', t = 'car'", "output": "False", "explanation": "The character counts differ."}], "explanation": "Count each character in the first string and subtract counts using the second string.", "expected_complexity": "Time O(n)", "expected_space_complexity": "Space O(1) for the fixed alphabet", "starter_code": "def is_anagram(s, t):\n    pass\n", "function_signature": "is_anagram(s: str, t: str) -> bool", "test_cases": [{"input": "'anagram', 'nagaram'", "expected": "True"}, {"input": "'rat', 'car'", "expected": "False"}], "hints": ["Different lengths cannot be anagrams.", "A frequency map captures multiplicity, not just membership.", "Compare the final frequency counts."], "tags": ["strings", "hashing"]
    },
    "Longest Substring Without Repeating Characters": {
        "description": "Return the length of the longest contiguous substring that contains no repeated characters.", "input_format": "s is a string.", "output_format": "Return the maximum valid substring length.", "constraints": "0 <= len(s) <= 5 * 10^4.", "examples": [{"input": "s = 'abcabcbb'", "output": "3", "explanation": "'abc' is the longest substring without repetition."}, {"input": "s = 'bbbbb'", "output": "1", "explanation": "Any single 'b' is valid."}], "explanation": "Maintain a sliding window and move its left edge beyond the previous position of a repeated character.", "expected_complexity": "Time O(n)", "expected_space_complexity": "Space O(min(n, alphabet))", "starter_code": "def length_of_longest_substring(s):\n    pass\n", "function_signature": "length_of_longest_substring(s: str) -> int", "test_cases": [{"input": "'abcabcbb'", "expected": "3"}, {"input": "'bbbbb'", "expected": "1"}, {"input": "''", "expected": "0"}], "hints": ["Use two indices to represent a window.", "Store the most recent index of each character.", "Never move the left edge backwards."], "tags": ["strings", "sliding-window", "hashing"]
    },
    "Merge Intervals": {
        "description": "Given intervals represented as [start, end], merge every pair of overlapping intervals and return the resulting sorted list.", "input_format": "intervals is a list of integer pairs.", "output_format": "Return non-overlapping intervals ordered by start.", "constraints": "0 <= len(intervals) <= 10^4; start <= end.", "examples": [{"input": "[[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "The first two intervals overlap."}, {"input": "[[1,4],[4,5]]", "output": "[[1,5]]", "explanation": "Touching intervals merge."}], "explanation": "Sort by start, then extend the last result interval while the next start is within its end.", "expected_complexity": "Time O(n log n)", "expected_space_complexity": "Space O(n)", "starter_code": "def merge_intervals(intervals):\n    pass\n", "function_signature": "merge_intervals(intervals: list[list[int]]) -> list[list[int]]", "test_cases": [{"input": "[[1,3],[2,6],[8,10],[15,18]]", "expected": "[[1,6],[8,10],[15,18]]"}, {"input": "[[1,4],[4,5]]", "expected": "[[1,5]]"}], "hints": ["Sort intervals by their starting point.", "Compare each interval with the last merged interval.", "Use max on the end values when they overlap."], "tags": ["arrays", "sorting", "intervals"]
    },
    "Binary Search": {
        "description": "Find the index of target in a sorted array of distinct integers, or return -1 if it is absent.", "input_format": "nums is sorted ascending; target is an integer.", "output_format": "Return the target index or -1.", "constraints": "0 <= len(nums) <= 10^5; values are distinct integers.", "examples": [{"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4", "explanation": "9 occurs at index 4."}, {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1", "explanation": "2 is absent."}], "explanation": "Repeatedly compare the middle value and discard the half that cannot contain target.", "expected_complexity": "Time O(log n)", "expected_space_complexity": "Space O(1)", "starter_code": "def binary_search(nums, target):\n    pass\n", "function_signature": "binary_search(nums: list[int], target: int) -> int", "test_cases": [{"input": "[-1,0,3,5,9,12], 9", "expected": "4"}, {"input": "[-1,0,3,5,9,12], 2", "expected": "-1"}], "hints": ["Use low and high inclusive boundaries.", "Compute the midpoint without relying on linear scans.", "Move one boundary after comparing nums[mid] with target."], "tags": ["arrays", "binary-search"]
    }
}

CODING = [
    ("Two Sum", "easy", "Arrays", "Hashing"), ("Valid Anagram", "easy", "Strings", "Frequency Counting"), ("Longest Substring Without Repeating Characters", "medium", "Strings", "Sliding Window"), ("Merge Intervals", "medium", "Arrays", "Sorting"), ("Binary Search", "easy", "Searching", "Binary Search"),
    ("Find the largest element in an array", "easy", "Arrays", "Array Traversal"), ("Count vowels in a string", "easy", "Strings", "String Traversal"),
    ("Find a target with linear search", "easy", "Searching", "Linear Search"), ("Sort three values", "easy", "Sorting", "Basic Sorting"),
    ("Find the first repeated value", "easy", "Hashing", "Set Lookup"), ("Remove duplicates from a sorted array", "easy", "Arrays", "Two Pointers"),
    ("Check whether two strings are anagrams", "easy", "Hashing", "Frequency Counting"), ("Find the second largest value", "easy", "Arrays", "One Pass"),
    ("Return rows above an average salary", "easy", "Basic SQL", "SQL Aggregation"), ("Group orders by customer", "easy", "Basic SQL", "SQL GROUP BY"),
    ("Reverse a linked list", "medium", "Linked Lists", "Pointer Manipulation"), ("Validate balanced brackets", "medium", "Stacks", "Stack"),
    ("Implement a queue with two stacks", "medium", "Queues", "Amortized Operations"), ("Find the height of a binary tree", "medium", "Trees", "Tree Recursion"),
    ("Find the first position with binary search", "medium", "Binary Search", "Search Invariant"), ("Generate all subsets", "medium", "Recursion", "Backtracking Basics"),
    ("Find the shortest path in an unweighted graph", "medium", "Graphs", "Breadth First Search"), ("Rank products with SQL window functions", "medium", "SQL", "SQL Window Functions"),
    ("Detect a cycle in a linked list", "medium", "Linked Lists", "Floyd Cycle Detection"), ("Serialize a binary tree", "medium", "Trees", "Tree Serialization"),
    ("Find the longest increasing subsequence", "hard", "Dynamic Programming", "Sequence DP"), ("Count paths through a grid", "hard", "Dynamic Programming", "Grid DP"),
    ("Find bridges in a graph", "hard", "Advanced Graphs", "Depth First Search"), ("Find the lowest common ancestor", "hard", "Advanced Trees", "Tree Search"),
    ("Solve a word-placement puzzle", "hard", "Backtracking", "Constraint Search"),
]

CODING.extend([
    ("Move zeroes to the end", "easy", "Arrays", "Arrays"), ("Best time to buy and sell stock", "easy", "Arrays", "Arrays"), ("Rotate an array by k positions", "easy", "Arrays", "Arrays"), ("Find the intersection of two arrays", "easy", "Arrays", "Hashing"), ("Majority element", "easy", "Arrays", "Arrays"), ("Missing number", "easy", "Arrays", "Arrays"), ("Plus one to a digit array", "easy", "Arrays", "Arrays"), ("Pascal triangle row", "easy", "Arrays", "Arrays"), ("Check if an array is sorted", "easy", "Arrays", "Arrays"),
    ("Product of array except self", "medium", "Arrays", "Arrays"), ("Maximum subarray sum", "medium", "Arrays", "Dynamic Programming"), ("Three sum", "medium", "Arrays", "Sorting"), ("Container with most water", "medium", "Arrays", "Two Pointers"), ("Spiral matrix traversal", "medium", "Arrays", "Arrays"), ("Set matrix zeroes", "medium", "Arrays", "Arrays"), ("Subarray sum equals k", "medium", "Arrays", "Hashing"), ("Trapping rain water", "hard", "Arrays", "Arrays"), ("Maximum product subarray", "medium", "Arrays", "Dynamic Programming"),
    ("Reverse words in a string", "easy", "Strings", "Strings"), ("First unique character", "easy", "Strings", "Hashing"), ("Longest common prefix", "easy", "Strings", "Strings"), ("Valid palindrome", "easy", "Strings", "Strings"), ("String compression", "easy", "Strings", "Strings"), ("Group anagrams", "medium", "Strings", "Hashing"), ("Longest palindromic substring", "medium", "Strings", "Dynamic Programming"), ("Word break", "medium", "Strings", "Dynamic Programming"), ("Minimum window substring", "hard", "Strings", "Hashing"), ("Implement substring search", "medium", "Strings", "Strings"),
    ("Search in a rotated sorted array", "medium", "Binary Search", "Binary Search"), ("Find first and last position", "medium", "Binary Search", "Binary Search"), ("Search a 2D matrix", "medium", "Binary Search", "Binary Search"), ("Kth smallest pair distance", "hard", "Binary Search", "Binary Search"), ("Insertion sort", "easy", "Sorting", "Sorting"), ("Merge sort", "medium", "Sorting", "Sorting"), ("Quickselect kth largest", "medium", "Sorting", "Sorting"), ("Counting sort", "medium", "Sorting", "Sorting"),
    ("Reverse a linked list recursively", "easy", "Linked Lists", "Linked Lists"), ("Merge two sorted lists", "easy", "Linked Lists", "Linked Lists"), ("Remove nth node from end", "medium", "Linked Lists", "Linked Lists"), ("Reorder a linked list", "medium", "Linked Lists", "Linked Lists"), ("Add two numbers as linked lists", "medium", "Linked Lists", "Linked Lists"), ("Merge k sorted lists", "hard", "Linked Lists", "Linked Lists"),
    ("Evaluate reverse polish notation", "medium", "Stacks", "Stacks"), ("Min stack", "medium", "Stacks", "Stacks"), ("Daily temperatures", "medium", "Stacks", "Stacks"), ("Next greater element", "medium", "Stacks", "Stacks"), ("Sliding window maximum", "hard", "Queues", "Queues"), ("Design a circular queue", "medium", "Queues", "Queues"),
    ("Binary tree preorder traversal", "easy", "Trees", "Trees"), ("Binary tree level order traversal", "medium", "Trees", "Trees"), ("Check if two trees are identical", "easy", "Trees", "Trees"), ("Validate a binary search tree", "medium", "Binary Search Trees", "Binary Search Trees"), ("Kth smallest element in a BST", "medium", "Binary Search Trees", "Binary Search Trees"), ("Build tree from traversals", "medium", "Trees", "Trees"), ("Serialize and deserialize a BST", "hard", "Binary Search Trees", "Binary Search Trees"), ("Binary tree maximum path sum", "hard", "Trees", "Trees"),
    ("Number of islands", "medium", "Graphs", "Graphs"), ("Clone an undirected graph", "medium", "Graphs", "Graphs"), ("Course schedule", "medium", "Graphs", "Graphs"), ("Dijkstra shortest paths", "medium", "Graphs", "Graphs"), ("Union find connected components", "medium", "Graphs", "Graphs"), ("Word ladder", "hard", "Graphs", "Graphs"),
    ("Permutations", "medium", "Backtracking", "Backtracking"), ("Combinations", "medium", "Backtracking", "Backtracking"), ("N queens", "hard", "Backtracking", "Backtracking"), ("Climbing stairs", "easy", "Dynamic Programming", "Dynamic Programming"), ("House robber", "medium", "Dynamic Programming", "Dynamic Programming"), ("Coin change", "medium", "Dynamic Programming", "Dynamic Programming"), ("Longest common subsequence", "medium", "Dynamic Programming", "Dynamic Programming"), ("Edit distance", "hard", "Dynamic Programming", "Dynamic Programming"), ("Activity selection", "medium", "Greedy Algorithms", "Greedy Algorithms"), ("Minimum coins for change", "hard", "Greedy Algorithms", "Greedy Algorithms"),
    ("SQL filter and order rows", "easy", "Basic SQL", "SQL"), ("SQL join customer orders", "easy", "SQL", "SQL"), ("SQL aggregate by department", "easy", "Basic SQL", "SQL"), ("SQL find duplicate records", "easy", "SQL", "SQL"), ("SQL rank employees by salary", "medium", "SQL", "SQL"), ("SQL rolling seven day total", "hard", "SQL", "SQL"),
])


def seed_content(db: Session) -> dict[str, int]:
    for title, difficulty, category, topic in CODING:
        details = QUESTION_DETAILS.get(title)
        if not db.query(CodingQuestion).filter_by(title=title).first():
            if details:
                db.add(CodingQuestion(title=title, difficulty=difficulty, category=category, topic=topic, skills=[topic, category], expected_answer_keywords=[category.casefold(), topic.casefold().split()[0]], source=SOURCE, verified=True, active=True, **details))
            else:
                db.add(CodingQuestion(title=title, description=f"Write a clear solution for: {title}.", difficulty=difficulty, category=category, topic=topic, skills=[topic, category], input_format="Describe the input values.", output_format="Return the requested result.", constraints="Use reasonable input sizes and handle empty input where applicable.", examples=[{"input": "A small valid example", "output": "The expected result"}], explanation=f"Break the problem into {topic.lower()} steps, check edge cases, and explain the invariant.", expected_complexity="State the time and space complexity of your solution.", expected_answer_keywords=[category.casefold(), topic.casefold().split()[0]], source=SOURCE))
        else:
            row = db.query(CodingQuestion).filter_by(title=title).first()
            if details:
                for key, value in details.items(): setattr(row, key, value)
            else:
                slug = title.casefold().replace(" ", "_").replace("-", "_")
                row.description = f"Implement a deterministic solution for {title.lower()} and return the required result."
                row.input_format = "The input contains the values described in the problem statement."
                row.output_format = "Return the requested result in the specified format."
                row.constraints = "Handle empty input and ordinary interview-sized inputs correctly."
                row.examples = [{"input": "A valid example input", "output": "The expected result"}]
                row.explanation = f"Use the core {topic.lower()} technique and explain the invariant used by the solution."
                row.expected_complexity = "State the time complexity of the solution."
                row.expected_space_complexity = "State the auxiliary space complexity."
                row.starter_code = f"def {slug}(data):\n    # Return the solution for {title}.\n    pass\n"
                row.function_signature = f"{slug}(data)"
                row.test_cases = [{"input": "valid input", "expected": "expected output"}]
                row.hints = [f"Start with the {topic.lower()} pattern."]
                row.tags = [topic.casefold()]
                row.skills = [topic]
                row.expected_answer_keywords = [topic.casefold()]
            row.active = True
            row.verified = True
    # Never expose legacy placeholder rows through the IDE. They can remain in
    # the table for historical references, but only complete curated rows are active.
    for row in db.query(CodingQuestion).all():
        if row.title not in {title for title, _, _, _ in CODING}:
            row.active = False
    for title, difficulty, category, topic in CODING:
        row = db.query(CodingQuestion).filter_by(title=title).first()
        if not row:
            continue
        row.difficulty, row.category, row.topic = difficulty, category, topic
        row.active, row.verified = True, True
        if not row.function_signature:
            slug = title.casefold().replace(" ", "_").replace("-", "_")
            row.description = f"Implement a deterministic solution for {title.lower()} and return the required result."
            row.input_format = "The input contains the values described in the problem statement."
            row.output_format = "Return the requested result in the specified format."
            row.constraints = "Handle empty input and ordinary interview-sized inputs correctly."
            row.examples = [{"input": "A valid example input", "output": "The expected result"}]
            row.explanation = f"Use the core {topic.lower()} technique and explain the invariant used by the solution."
            row.expected_complexity = "State the time complexity of the solution."
            row.expected_space_complexity = "State the auxiliary space complexity."
            row.starter_code = f"def {slug}(data):\n    # Return the solution for {title}.\n    pass\n"
            row.function_signature = f"{slug}(data)"
            row.test_cases = [{"input": "valid input", "expected": "expected output"}]
            row.hints, row.tags, row.skills = [f"Start with the {topic.lower()} pattern."], [topic.casefold()], [topic]
            row.expected_answer_keywords = [topic.casefold()]
    guidance = "Use a structured response, mention trade-offs, and include a concrete example or edge case."
    interview_bank = [
        ("Tell me about a project you are proud of.", "Behavioral", "Projects", None, "medium"),
        ("Describe a time you resolved a disagreement.", "Behavioral", "Teamwork", None, "medium"),
        ("How do you learn an unfamiliar technology?", "Behavioral", "Learning", None, "medium"),
        ("Describe a failure and what you changed afterward.", "Behavioral", "Reflection", None, "medium"),
        ("How do you prioritize competing deadlines?", "Behavioral", "Prioritization", None, "medium"),
        ("What makes code maintainable?", "Behavioral", "Engineering Practice", None, "medium"),
        ("Describe a time you received difficult feedback.", "Behavioral", "Communication", None, "medium"),
        ("How do you explain technical work to a non-technical audience?", "Behavioral", "Communication", None, "medium"),
        ("What role do you usually take on a team?", "Behavioral", "Teamwork", None, "medium"),
        ("What would you improve in your last project?", "Behavioral", "Reflection", None, "medium"),
        ("Why are you interested in this role?", "HR", "Career Motivation", None, "medium"),
        ("What are your strengths and what are you improving?", "HR", "Self Awareness", None, "medium"),
        ("Where would you like to grow in two years?", "HR", "Career Growth", None, "medium"),
        ("What does a good work environment mean to you?", "HR", "Work Style", None, "medium"),
        ("How would you handle a production bug just before release?", "Situational", "Incident Response", "Debugging", "medium"),
        ("A teammate is blocked before a deadline. What do you do?", "Situational", "Collaboration", None, "medium"),
        ("A requirement changes during implementation. How do you respond?", "Situational", "Change Management", None, "medium"),
        ("A user reports inconsistent results. How do you investigate?", "Situational", "Debugging", "Debugging", "medium"),
        ("A review comment conflicts with a project constraint. What do you do?", "Situational", "Decision Making", None, "medium"),
        ("Explain a complex technical idea in simple terms.", "Communication", "Clarity", None, "medium"),
        ("How do you structure a concise status update?", "Communication", "Written Communication", None, "medium"),
        ("How do you check that someone understood your explanation?", "Communication", "Active Listening", None, "medium"),
        ("Describe how you give constructive feedback.", "Communication", "Feedback", None, "medium"),
        ("How do you communicate uncertainty to a stakeholder?", "Communication", "Transparency", None, "medium"),
        ("Explain the difference between a list and a tuple in Python.", "Technical", "Python", "Python", "easy"),
        ("What problem does React state solve?", "Technical", "React", "React", "easy"),
        ("How does a FastAPI request become a response?", "Technical", "FastAPI", "FastAPI", "medium"),
        ("Explain an SQL JOIN with an example.", "Technical", "SQL", "SQL", "medium"),
        ("What is a database index and when can it hurt?", "Technical", "PostgreSQL", "PostgreSQL", "medium"),
        ("Explain the purpose of a Git branch.", "Technical", "Git", "Git", "easy"),
        ("What is the difference between a process and a thread?", "Technical", "Operating Systems", "Operating Systems", "medium"),
        ("Explain encapsulation and polymorphism.", "Technical", "OOP", "Object Oriented Programming", "easy"),
        ("How would you find a cycle in a graph?", "Technical", "Algorithms", "Data Structures and Algorithms", "medium"),
        ("What is Docker useful for during development?", "Technical", "Docker", "Docker", "easy"),
        ("What is dependency injection in FastAPI and why is it useful?", "Technical", "FastAPI", "FastAPI", "medium"),
        ("How would you validate request data in a FastAPI endpoint?", "Technical", "FastAPI", "FastAPI", "easy"),
        ("Explain Python decorators with a practical use case.", "Technical", "Python", "Python", "medium"),
        ("How do you handle exceptions cleanly in Python code?", "Technical", "Python", "Python", "easy"),
        ("What is the purpose of useEffect in React?", "Technical", "React", "React", "easy"),
        ("How does TypeScript help prevent bugs in a React application?", "Technical", "TypeScript", "TypeScript", "easy"),
        ("What is the difference between let, const, and var in JavaScript?", "Technical", "JavaScript", "JavaScript", "easy"),
        ("How do semantic HTML elements improve a web page?", "Technical", "HTML", "HTML", "easy"),
        ("How would you make a CSS layout responsive on mobile and desktop?", "Technical", "CSS", "CSS", "medium"),
        ("What is the difference between a REST API resource and an HTTP method?", "Technical", "REST APIs", "REST API", "medium"),
        ("How would you design simple pagination for a REST API?", "Technical", "REST APIs", "REST API", "medium"),
        ("What is an index in PostgreSQL and when should it be used?", "Technical", "PostgreSQL", "PostgreSQL", "medium"),
        ("How do transactions help keep database changes consistent?", "Technical", "SQL", "SQL", "medium"),
        ("What is the difference between a Docker image and a Docker container?", "Technical", "Docker", "Docker", "easy"),
        ("How would you inspect logs on a Linux server when an application fails?", "Technical", "Linux", "Linux", "easy"),
        ("What does a CI/CD pipeline do for a software team?", "Technical", "CI/CD", "GitHub Actions", "easy"),
        ("What is the difference between unit testing and integration testing?", "Technical", "Software Testing", "Software Testing", "easy"),
        ("How do you debug a backend API that returns the wrong response?", "Technical", "Debugging", "Debugging", "medium"),
        ("What is Big O notation and why does it matter in interviews?", "Technical", "Algorithms", "Data Structures and Algorithms", "easy"),
        ("How does a stack differ from a queue?", "Technical", "Data Structures", "Data Structures and Algorithms", "easy"),
        ("What should you consider when designing a simple URL shortener?", "System Design", "System Design", "System Design", "medium"),
        ("How would you split a small monolith into services safely?", "System Design", "Microservices", "Microservices", "hard"),
        ("What is AWS used for in a typical web application deployment?", "Cloud", "AWS", "AWS", "easy"),
        ("What problem does Kubernetes solve when running containers?", "Cloud", "Kubernetes", "Kubernetes", "medium"),
        ("How would you deploy a FastAPI and React project at a high level?", "Cloud", "Deployment", "Docker", "medium"),
        ("What are the main responsibilities of a Spring Boot controller?", "Technical", "Spring Boot", "Spring Boot", "medium"),
        ("How is Java different from JavaScript in typical backend and frontend work?", "Technical", "Java", "Java", "easy"),
    ]
    # The bank is intentionally static and curated. Keeping the records here
    # makes seeding deterministic and avoids runtime/LLM-generated questions.
    interview_bank.extend([
        ("What motivates you to work in software development?", "HR", "Motivation", None, "easy"),
        ("How would you introduce yourself in a professional interview?", "HR", "Introduction", None, "easy"),
        ("Why did you choose your current area of study?", "HR", "Background", None, "easy"),
        ("What type of role are you looking for next?", "HR", "Role Awareness", None, "easy"),
        ("What are your expectations from your first manager?", "HR", "Workplace Expectations", None, "easy"),
        ("How do you respond when you do not know an answer?", "HR", "Learning Attitude", None, "easy"),
        ("What kind of feedback helps you improve?", "HR", "Growth Mindset", None, "medium"),
        ("How do you keep yourself motivated during repetitive work?", "HR", "Motivation", None, "easy"),
        ("What would your teammates say is your strongest quality?", "HR", "Self Awareness", None, "easy"),
        ("How do you decide whether a company is a good fit for you?", "HR", "Company Motivation", None, "medium"),
        ("What does professionalism mean in a remote team?", "HR", "Workplace Expectations", None, "easy"),
        ("How do you plan your career development?", "HR", "Career Goals", None, "medium"),
        ("What interests you about this company's product or domain?", "HR", "Company Motivation", None, "medium"),
        ("How do you handle an unfamiliar work environment?", "HR", "Adaptability", None, "medium"),
        ("What does success look like in your first six months?", "HR", "Role Awareness", None, "medium"),
        ("How do you balance personal growth with delivery commitments?", "HR", "Career Goals", None, "medium"),
        ("Describe a time you took responsibility for a mistake.", "Behavioral", "Responsibility", None, "medium"),
        ("Tell me about a time you helped a teammate succeed.", "Behavioral", "Teamwork", None, "easy"),
        ("Describe a difficult problem and how you broke it down.", "Behavioral", "Problem Solving", None, "medium"),
        ("Tell me about a time you adapted to a major change.", "Behavioral", "Adaptability", None, "medium"),
        ("Describe an achievement and how you measured its impact.", "Behavioral", "Achievements", None, "medium"),
        ("Tell me about a time you led without formal authority.", "Behavioral", "Leadership", None, "medium"),
        ("Describe how you handled an unexpected delay.", "Behavioral", "Time Management", None, "easy"),
        ("Tell me about a time you had to make a trade-off.", "Behavioral", "Decision Making", None, "medium"),
        ("Describe a time you changed your approach after learning more.", "Behavioral", "Learning", None, "medium"),
        ("Tell me about a conflict you helped resolve.", "Behavioral", "Conflict Resolution", None, "medium"),
        ("Requirements are unclear but the deadline is close. What steps do you take?", "Situational", "Requirements", None, "medium"),
        ("Two stakeholders give you conflicting priorities. How do you respond?", "Situational", "Prioritization", None, "medium"),
        ("A teammate repeatedly misses commitments. How would you handle it?", "Situational", "Accountability", None, "medium"),
        ("You discover a security issue before release. What do you do?", "Situational", "Security", "Security", "medium"),
        ("A database query becomes slow after a data increase. How do you investigate?", "Situational", "Database Performance", "PostgreSQL", "medium"),
        ("A customer reports a problem you cannot reproduce. What is your process?", "Situational", "Incident Investigation", "Debugging", "medium"),
        ("You disagree with a manager's technical direction. How do you present your view?", "Situational", "Disagreement", None, "medium"),
        ("You must use a technology you have never seen before. How do you begin?", "Situational", "Unfamiliar Technology", None, "easy"),
        ("A last-minute release change could increase risk. What do you recommend?", "Situational", "Release Management", "CI/CD", "medium"),
        ("A production service is intermittently failing. What information do you collect first?", "Situational", "Incident Response", "Debugging", "medium"),
        ("A teammate asks you to approve code you have not reviewed. How do you respond?", "Situational", "Code Review", None, "easy"),
        ("A customer asks for a feature that conflicts with privacy requirements. What do you do?", "Situational", "Privacy", "Security", "medium"),
        ("You have more work than can fit into the sprint. How do you negotiate scope?", "Situational", "Planning", None, "medium"),
        ("A test is flaky and blocks deployment. How do you proceed?", "Situational", "Testing", "Software Testing", "medium"),
        ("Your team is split between two implementation options. How do you reach a decision?", "Situational", "Decision Making", None, "medium"),
        ("How would you explain an API to a non-technical stakeholder?", "Communication", "Technical Explanation", None, "easy"),
        ("How do you communicate a project delay without creating confusion?", "Communication", "Communicating Delays", None, "easy"),
        ("How would you present the results of a technical project?", "Communication", "Presentations", None, "medium"),
        ("What information do you include when asking for technical help?", "Communication", "Asking for Help", None, "easy"),
        ("How do you explain a bug and its customer impact?", "Communication", "Explaining Bugs", None, "easy"),
        ("How do you communicate a risk that may not happen?", "Communication", "Risk Communication", None, "medium"),
        ("How would you handle disagreement during a design discussion?", "Communication", "Disagreement", None, "medium"),
        ("How do you make a status update useful to both engineers and managers?", "Communication", "Status Updates", None, "medium"),
        ("How do you confirm that requirements were understood correctly?", "Communication", "Active Listening", None, "easy"),
        ("How would you document a decision for people who were not in the meeting?", "Communication", "Documentation", None, "easy"),
        ("What makes a technical presentation clear and persuasive?", "Communication", "Presentations", None, "medium"),
        ("How do you communicate an error you made to a customer?", "Communication", "Transparency", None, "medium"),
        ("How do you adjust your explanation for an experienced versus new audience?", "Communication", "Audience Awareness", None, "medium"),
        ("How do you summarize a complex incident after it is resolved?", "Communication", "Incident Reports", None, "medium"),
        ("How would you explain a trade-off when there is no perfect solution?", "Communication", "Trade-offs", None, "medium"),
        ("What is the purpose of a database transaction isolation level?", "Technical", "Databases", "PostgreSQL", "hard"),
        ("How does caching improve an API and what can go wrong?", "Technical", "Web Development", "REST API", "medium"),
        ("What is the difference between authentication and authorization?", "Technical", "Security", "Security", "easy"),
    ])
    # Existing company/cloud/system-design categories remain supported for
    # backwards compatibility; the requested five core categories are fully
    # represented by the curated bank above.
    interview_bank = [(q, category, topic, skill, difficulty) for q, category, topic, skill, difficulty in interview_bank]
    for question, category, topic, skill, difficulty in interview_bank:
        normalized = " ".join(question.casefold().split())
        canonical_category = "technical" if category.casefold() in {"cloud", "system design"} else category.casefold()
        row = next((candidate for candidate in db.query(InterviewQuestion).all() if " ".join(candidate.question.casefold().split()) == normalized), None)
        if row is None:
            db.add(InterviewQuestion(question=question, category=canonical_category, topic=topic, skill=skill, difficulty=difficulty, sample_answer_guidance=guidance, source=SOURCE, verified=True, active=True))
        else:
            row.category = canonical_category
            row.topic = topic
            row.skill = skill
            row.difficulty = difficulty
            row.sample_answer_guidance = row.sample_answer_guidance or guidance
            row.verified = True
            row.active = True
    resources = [("Python documentation", "Programming", "Python", "Documentation", "https://docs.python.org/3/"), ("Java documentation", "Programming", "Java", "Documentation", "https://docs.oracle.com/en/java/"), ("JavaScript guide", "Programming", "JavaScript", "Documentation", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"), ("TypeScript handbook", "Programming", "TypeScript", "Documentation", "https://www.typescriptlang.org/docs/handbook/intro.html"), ("React documentation", "Frontend", "React", "Documentation", "https://react.dev/learn"), ("HTML guide", "Frontend", "HTML", "Reference", "https://developer.mozilla.org/en-US/docs/Learn/HTML"), ("CSS guide", "Frontend", "CSS", "Reference", "https://developer.mozilla.org/en-US/docs/Learn/CSS"), ("FastAPI documentation", "Backend", "FastAPI", "Documentation", "https://fastapi.tiangolo.com/"), ("REST API basics", "Backend", "REST APIs", "Tutorial", "https://developer.mozilla.org/en-US/docs/Glossary/REST"), ("PostgreSQL documentation", "Database", "PostgreSQL", "Documentation", "https://www.postgresql.org/docs/"), ("SQL tutorial", "Database", "SQL", "Tutorial", "https://www.postgresql.org/docs/current/tutorial.html"), ("Git documentation", "Tools", "Git", "Documentation", "https://git-scm.com/doc"), ("Docker getting started", "Tools", "Docker", "Tutorial", "https://docs.docker.com/get-started/"), ("AWS getting started", "Cloud", "AWS", "Documentation", "https://docs.aws.amazon.com/"), ("Data structures reference", "Computer Science", "Data Structures", "Reference", "https://en.wikipedia.org/wiki/Data_structure"), ("Algorithms reference", "Computer Science", "Algorithms", "Reference", "https://en.wikipedia.org/wiki/Algorithm"), ("DBMS overview", "Computer Science", "DBMS", "Reference", "https://en.wikipedia.org/wiki/Database"), ("Operating systems overview", "Computer Science", "Operating Systems", "Reference", "https://en.wikipedia.org/wiki/Operating_system"), ("Object-oriented programming", "Computer Science", "OOP", "Reference", "https://en.wikipedia.org/wiki/Object-oriented_programming")]
    for title, category, skill, resource_type, url in resources:
        if not db.query(LearningResource).filter_by(title=title).first():
            db.add(LearningResource(title=title, description=f"Authoritative starting point for learning {skill}.", category=category, topic=skill, skill=skill, resource_type=resource_type, url=url, source=title, verified=True, active=True))
    db.commit()
    return {"coding_questions": len(CODING), "interview_questions": len(interview_bank), "learning_resources": len(resources)}
