
import re
from itertools import product


# --------------------------------
# Evaluate propositional expression
# --------------------------------

def evaluate(expression, model):

    tokens = re.findall(
        r'\(|\)|[A-Za-z_][A-Za-z0-9_]*',
        expression.strip()
    )

    position = [0]

    def parse_primary():

        if position[0] >= len(tokens):
            raise ValueError("Incomplete expression")

        token = tokens[position[0]]

        if token == "NOT":
            position[0] += 1
            return not parse_primary()

        elif token == "(":
            position[0] += 1
            result = parse_implies()

            if position[0] >= len(tokens) or tokens[position[0]] != ")":
                raise ValueError("Missing closing parenthesis")

            position[0] += 1
            return result

        else:
            position[0] += 1

            if token not in model:
                raise ValueError("Unknown symbol: " + token)

            return model[token]

    def parse_and():

        result = parse_primary()

        while position[0] < len(tokens) and tokens[position[0]] == "AND":
            position[0] += 1
            right = parse_primary()
            result = result and right

        return result

    def parse_or():

        result = parse_and()

        while position[0] < len(tokens) and tokens[position[0]] == "OR":
            position[0] += 1
            right = parse_and()
            result = result or right

        return result

    def parse_implies():

        result = parse_or()

        if position[0] < len(tokens) and tokens[position[0]] == "IMPLIES":
            position[0] += 1
            right = parse_implies()
            result = (not result) or right

        return result

    result = parse_implies()

    if position[0] != len(tokens):
        raise ValueError("Invalid expression: " + expression)

    return result


# --------------------------------
# Truth Table Enumeration
# --------------------------------

def tt_entails(KB):

    queries = [
        ("(ii) KB entails R", "R"),
        ("(iii) KB entails R -> P", "R IMPLIES P"),
        ("(iv) KB entails Q -> R", "Q IMPLIES R")
    ]

    # Find all symbols
    symbols = set()

    for sentence in KB + [q[1] for q in queries]:

        words = re.findall(
            r'[A-Za-z_][A-Za-z0-9_]*',
            sentence
        )

        for word in words:
            if word not in ["AND", "OR", "NOT", "IMPLIES"]:
                symbols.add(word)

    symbols = sorted(symbols)

    # Print truth table
    print("\nTRUTH TABLE")
    print("=" * 110)

    sw = 8
    kw = 10
    bw = 8
    qw = 10

    for s in symbols:
        print(f"{s:^{sw}}", end="")

    for i in range(len(KB)):
        print(f"{'KB' + str(i+1):^{kw}}", end="")

    print(f"{'KB':^{bw}}", end="")

    for i in range(len(queries)):
        print(f"{'Query' + str(i+1):^{qw}}", end="")

    print()
    print("-" * 110)

    models = []

    # Generate all possible truth assignments
    for values in product([True, False], repeat=len(symbols)):

        model = dict(zip(symbols, values))

        # Evaluate KB
        results = [
            evaluate(sentence, model)
            for sentence in KB
        ]

        kb_true = all(results)

        # Evaluate queries
        query_results = [
            evaluate(query[1], model)
            for query in queries
        ]

        # Display T/F
        for s in symbols:
            print(f"{'T' if model[s] else 'F':^{sw}}", end="")

        for result in results:
            print(f"{'T' if result else 'F':^{kw}}", end="")

        print(f"{'T' if kb_true else 'F':^{bw}}", end="")

        for result in query_results:
            print(f"{'T' if result else 'F':^{qw}}", end="")

        print()

        if kb_true:
            models.append(model)

    print("-" * 110)

    # Display models
    print("\nMODELS WHERE KB IS TRUE:")

    if models:
        for model in models:
            print(model)
    else:
        print("No models found.")

    # Check entailment
    print("\nENTAILMENT RESULTS:")

    for label, query in queries:

        entails = all(
            evaluate(query, model)
            for model in models
        )

        print(label, ":", entails)


# --------------------------------
# Main Program
# --------------------------------

print("TRUTH TABLE ENUMERATION ALGORITHM")
print("----------------------------------")

n = int(input("\nEnter number of sentences in KB: "))

KB = []

print("\nEnter KB sentences:")
print("Use AND, OR, NOT, IMPLIES and parentheses.")

for i in range(n):

    sentence = input("Sentence " + str(i + 1) + ": ").strip()

    KB.append(sentence)


tt_entails(KB)

print("usn - 1WA24CS091")
print("Name - Charitha Reddy")