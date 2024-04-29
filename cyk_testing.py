import subprocess

for i in range(1, 5):
    question_rules_file = f"Question {i} Rules.txt"
    test_file = f"Q{i}Test.txt"

    # Run cyk.py for the current files
    print("Running CYK for Question", i, "Strings...")
    subprocess.run(["python", "cyk.py", "-c", question_rules_file, "-t", test_file])
