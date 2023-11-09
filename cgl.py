from collections import defaultdict

def cfl_to_cfg(cfl):
    # Define a dictionary to store CFG rules
    cfg_rules = defaultdict(list)

    # Process CFL rules and convert them to CFG rules
    for rule in cfl:
        non_terminal, productions = rule.split(' -> ')
        production_list = productions.split(' | ')
        for production in production_list:
            # Add the production to the corresponding non-terminal
            cfg_rules[non_terminal].append(production)

    # Create a list to store the CFG rules in the required format
    cfg_rules_list = []

    for non_terminal, productions in cfg_rules.items():
        for production in productions:
            cfg_rules_list.append(f"{non_terminal} -> {production}")

    return cfg_rules_list

# Custom CFL rules
custom_cfl_rules = [
    "S -> aSb | ε",
    "A -> aA | bA | ε",
    "B -> AaB | ε"
]

# Convert the custom CFL to CFG
custom_cfg_rules = cfl_to_cfg(custom_cfl_rules)

# Print the resulting CFG rules
for rule in custom_cfg_rules:
    print(rule)
