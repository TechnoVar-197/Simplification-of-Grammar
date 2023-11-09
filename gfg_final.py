def get_productions():
    productions = []
    while True:
        production = input("Enter a production (e.g., A -> alpha), or 'q' to quit: ")
        if production == 'q':
            break
        productions.append(production)
    return productions

def find_nullable_variables(cfg):
    nullable = set()

    # Initialize nullable variables with epsilon
    nullable.update([key for key, value in cfg.items() if "ε" in value])

    # Iterate until no new nullable variables are found
    while True:
        previous_nullable_count = len(nullable)

        for key, value in cfg.items():
            for production in value:
                if all(symbol in nullable or symbol == "ε" for symbol in production):
                    nullable.add(key)

        if len(nullable) == previous_nullable_count:
            break

    return nullable

def remove_nullable_productions(cfg, nullable):
    new_cfg = {}

    for key, value in cfg.items():
        new_productions = []

        for production in value:
            if production == "ε":
                continue  # Skip epsilon productions

            nullable_combinations = [""]
            for symbol in production:
                if symbol in nullable:
                    new_combinations = [x + symbol for x in nullable_combinations]
                    nullable_combinations.extend(new_combinations)
                else:
                    nullable_combinations = [x + symbol for x in nullable_combinations]

            new_productions.extend(nullable_combinations)

        new_cfg[key] = list(set(new_productions))

    return new_cfg

def remove_unit_productions(cfg):
    new_cfg = cfg.copy()

    for key, value in cfg.items():
        new_productions = []

        for production in value:
            if len(production) == 1 and production.isupper() and production != key:
                if production in cfg:
                    new_productions.extend(cfg[production])
            else:
                new_productions.append(production)

        new_cfg[key] = new_productions

    return new_cfg

def eliminate_useless_symbols(cfg, start_symbol):
    reachable = set()
    productive = set()

    # Find reachable symbols
    def find_reachable_symbols(symbol):
        if symbol not in reachable:
            reachable.add(symbol)
            if symbol in cfg:
                for production in cfg[symbol]:
                    for char in production:
                        if char.isupper():
                            find_reachable_symbols(char)

    find_reachable_symbols(start_symbol)

    # Find productive symbols
    for symbol in reachable:
        if is_non_terminal(symbol) and symbol in cfg:  # Check if the symbol is in the CFG
            for production in cfg[symbol]:
                if all(char in reachable or not is_non_terminal(char) for char in production):
                    productive.add(symbol)

    new_cfg = {}
    for symbol, productions in cfg.items():
        if symbol in reachable and (is_non_terminal(symbol) or symbol in productive):
            new_cfg[symbol] = [production for production in productions if
                               all(char in reachable or not is_non_terminal(char) for char in production)]

    return new_cfg

def is_non_terminal(symbol):
    return symbol.isupper()

def convert_to_cfg(productions):
    cfg = {}
    for production in productions:
        left, right = production.split('->')
        left = left.strip()
        right = right.strip()

        if left in cfg:
            cfg[left].append(right)
        else:
            cfg[left] = [right]

    return cfg

def main():
    print("Convert a Context-Free Language to a Context-Free Grammar")
    print("Enter productions in the form A -> alpha")
    productions = get_productions()
    
    start_symbol = productions[0].split('->')[0].strip()  # Assume the first production is the start symbol
    cfg = convert_to_cfg(productions)

    nullable = find_nullable_variables(cfg)
    cfg = remove_nullable_productions(cfg, nullable)
    cfg = remove_unit_productions(cfg)
    cfg = eliminate_useless_symbols(cfg, start_symbol)

    print("\nContext-Free Grammar (without null productions, unit productions, and useless symbols):")
    for left, right in cfg.items():
        for production in right:
            if production:
                print(f"{left} -> {production}")

if __name__ == "__main__":
    main()
