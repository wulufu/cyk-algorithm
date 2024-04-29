import subprocess

for i in range(1, 5):
    question_rules_file = f"Question {i} Rules.txt"
    test_file = f"Q{i}Test.txt"

    # Run cyk.py for the current files
    subprocess.run(["python", "cyk.py", " -f ", question_rules_file, test_file])