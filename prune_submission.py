
import csv
import json

csv.field_size_limit(10_000_000)

PUZZLES_FILE = "puzzles.csv"
SAMPLE_FILE = "sample_submission.csv"
OUTPUT_FILE = "pruned_submission.csv"


def calculate(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0 or a % b != 0:
            raise ValueError("Invalid division")
        return a // b
    raise ValueError("Unknown operation: " + str(op))


def build_pruned_program(puzzle, program):
    starting = json.loads(puzzle["starting_values"])
    targets = set(json.loads(puzzle["targets"]))
    limit = int(puzzle["value_limit"])
    register_count = int(puzzle["registers"])

    # Each node represents one value stored in a register.
    nodes = []
    current = [None] * register_count

    for i, value in enumerate(starting):
        if value <= 0 or value > limit:
            raise ValueError("Invalid starting value")

        nodes.append({
            "value": value,
            "parents": [],
            "step": None
        })
        current[i] = len(nodes) - 1

    needed_targets = set(targets)
    required_nodes = set()

    # Targets already present in starting registers.
    for i, value in enumerate(starting):
        if value in needed_targets:
            required_nodes.add(current[i])
            needed_targets.remove(value)

    instruction_nodes = []

    # Execute the original program and record dependencies.
    for step, instruction in enumerate(program):
        op, src1, src2, dest = instruction

        if not (0 <= src1 < register_count and
                0 <= src2 < register_count and
                0 <= dest < register_count):
            raise ValueError("Register index out of range")

        parent1 = current[src1]
        parent2 = current[src2]

        if parent1 is None or parent2 is None:
            raise ValueError("Reading an uninitialized register")

        a = nodes[parent1]["value"]
        b = nodes[parent2]["value"]
        result = calculate(op, a, b)

        if result <= 0 or result > limit:
            raise ValueError("Value outside allowed limits")

        node_id = len(nodes)
        nodes.append({
            "value": result,
            "parents": [parent1, parent2],
            "step": step
        })

        # Destination is overwritten after both sources are read.
        current[dest] = node_id
        instruction_nodes.append(node_id)

        if result in needed_targets:
            required_nodes.add(node_id)
            needed_targets.remove(result)

    if needed_targets:
        raise ValueError(
            "Original program misses targets: " +
            str(len(needed_targets))
        )

    # Trace backwards from every target to its dependencies.
    stack = list(required_nodes)

    while stack:
        node_id = stack.pop()

        for parent in nodes[node_id]["parents"]:
            if parent not in required_nodes:
                required_nodes.add(parent)
                stack.append(parent)

    # Keep only instructions required by target calculations.
    pruned = []

    for node_id in instruction_nodes:
        if node_id in required_nodes:
            step = nodes[node_id]["step"]
            pruned.append(program[step])

    return pruned


def validate_program(puzzle, program):
    starting = json.loads(puzzle["starting_values"])
    targets = set(json.loads(puzzle["targets"]))
    limit = int(puzzle["value_limit"])
    register_count = int(puzzle["registers"])

    if len(program) > 4096:
        return False

    if any(v <= 0 or v > limit for v in starting):
        return False

    registers = [None] * register_count

    for i, value in enumerate(starting):
        registers[i] = value

    found = set(starting) & targets

    try:
        for op, src1, src2, dest in program:
            if not all(
                isinstance(x, int)
                for x in (src1, src2, dest)
            ):
                return False

            if not (
                0 <= src1 < register_count
                and 0 <= src2 < register_count
                and 0 <= dest < register_count
            ):
                return False

            a = registers[src1]
            b = registers[src2]

            if a is None or b is None:
                return False

            result = calculate(op, a, b)

            if result <= 0 or result > limit:
                return False

            registers[dest] = result

            if result in targets:
                found.add(result)

    except (ValueError, ZeroDivisionError):
        return False

    return found == targets


def main():
    with open(PUZZLES_FILE, encoding="utf-8-sig") as f:
        puzzles = {
            row["id"]: row
            for row in csv.DictReader(f)
        }

    with open(SAMPLE_FILE, encoding="utf-8-sig") as f:
        baseline = {
            row["id"]: json.loads(row["program"])
            for row in csv.DictReader(f)
        }

    if set(puzzles) != set(baseline):
        raise ValueError("Puzzle IDs do not match submission IDs")

    output = []
    original_total = 0
    optimized_total = 0
    improved = 0

    for puzzle_id, puzzle in puzzles.items():
        original = baseline[puzzle_id]

        if not validate_program(puzzle, original):
            raise ValueError(
                "Invalid original program: " + puzzle_id
            )

        optimized = build_pruned_program(puzzle, original)

        if not validate_program(puzzle, optimized):
            raise ValueError(
                "Pruned program failed validation: " + puzzle_id
            )

        original_total += len(original)
        optimized_total += len(optimized)

        if len(optimized) < len(original):
            improved += 1

        output.append({
            "id": puzzle_id,
            "program": json.dumps(
                optimized,
                separators=(",", ":")
            )
        })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "program"])
        writer.writeheader()
        writer.writerows(output)

    print("\nOPTIMIZATION RESULTS")
    print("----------------------------")
    print("Puzzles:", len(output))
    print("Original instructions:", original_total)
    print("Optimized instructions:", optimized_total)
    print("Instructions saved:", original_total - optimized_total)
    print("Improved puzzles:", improved)
    print("Output:", OUTPUT_FILE)
    print("VALIDATION: ALL PROGRAMS PASSED")


if __name__ == "__main__":
    main()
