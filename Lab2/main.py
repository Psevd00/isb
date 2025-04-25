from nist import frequency_test, load_constants, longest_run_test, runs_test

constants = load_constants()


def test_sequence(file_path):
    with open(file_path, 'r') as f:
        sequence = f.read().strip()

    freq_p = frequency_test(sequence)
    runs_p = runs_test(sequence)
    long_run_p = longest_run_test(sequence)

    def is_random(p_value):
        return "Случайное" if p_value >= 0.01 else "Неслучайное"

    return {
        'frequency': (freq_p, is_random(freq_p)),
        'runs': (runs_p, is_random(runs_p)),
        'longest_run': (long_run_p, is_random(long_run_p))
    }


cpp_results = test_sequence(constants['SEQUENCE_CPP_PATH'])
java_results = test_sequence(constants['SEQUENCE_JAVA_PATH'])

with open(constants['RESULTS_PATH'], 'w') as f:
    f.write("=== C++ Results ===\n")
    f.write(f"Frequency Test: P-value = {cpp_results['frequency'][0]:.4f} - {cpp_results['frequency'][1]}\n")
    f.write(f"Runs Test: P-value = {cpp_results['runs'][0]:.4f} - {cpp_results['runs'][1]}\n")
    f.write(f"Longest Run Test: P-value = {cpp_results['longest_run'][0]:.4f} - {cpp_results['longest_run'][1]}\n\n")

    f.write("=== Java Results ===\n")
    f.write(f"Frequency Test: P-value = {java_results['frequency'][0]:.4f} - {java_results['frequency'][1]}\n")
    f.write(f"Runs Test: P-value = {java_results['runs'][0]:.4f} - {java_results['runs'][1]}\n")
    f.write(f"Longest Run Test: P-value = {java_results['longest_run'][0]:.4f} - {java_results['longest_run'][1]}\n")
