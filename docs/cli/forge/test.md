# FORGE TEST

## Tier: Basic
- Runs 'pytest' on the test file located in the asset's package.
- Verifies success, edge cases, and failure modes.
- Prevents deployment of broken or malicious code.
Usage: ./cli forge test <id>

## Tier: More
- Runs 'pytest' on the test file located in the asset's package.
- Verifies success, edge cases, and failure modes.
- Prevents deployment of broken or malicious code.
Usage: ./cli forge test <id>

TECHNICAL DEEP-DIVE:
The 'test' command implements 'Automated Quality Gating'.
1. Discovery: Locates the 'test_<name>.py' file in the tool's subdirectory.
2. Execution: Runs 'subprocess.run(["pytest", test_path])'.
3. Reporting: Captures stdout/stderr and returns a boolean success status.
4. Security: Part of the 'Verification' gate that protects the Termux environment.
Every forged asset is born with a corresponding test suite to ensure long-term reliability.

## Tier: Full
- Runs 'pytest' on the test file located in the asset's package.
- Verifies success, edge cases, and failure modes.
- Prevents deployment of broken or malicious code.
Usage: ./cli forge test <id>

TECHNICAL DEEP-DIVE:
The 'test' command implements 'Automated Quality Gating'.
1. Discovery: Locates the 'test_<name>.py' file in the tool's subdirectory.
2. Execution: Runs 'subprocess.run(["pytest", test_path])'.
3. Reporting: Captures stdout/stderr and returns a boolean success status.
4. Security: Part of the 'Verification' gate that protects the Termux environment.
Every forged asset is born with a corresponding test suite to ensure long-term reliability.

[EXPANSION PENDING]
