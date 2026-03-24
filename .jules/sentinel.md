## 2024-03-24 - Command Injection in Python build script
**Vulnerability:** Command injection vulnerability in `src/build.py`.
**Learning:** `os.system` with f-strings allows arbitrary shell command execution if the URL or filename variables contain shell metacharacters.
**Prevention:** Use `subprocess.run` with a list of arguments instead of a single string and `shell=False` (default) when executing external commands.
