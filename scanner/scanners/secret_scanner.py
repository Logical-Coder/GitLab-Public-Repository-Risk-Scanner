import re


class SecretScanner:

    PATTERNS = [
        r"password\s*=",
        r"passwd\s*=",
        r"api[_-]?key\s*=",
        r"secret\s*=",
        r"token\s*=",
        r"AKIA[0-9A-Z]{16}",
        r"glpat-[A-Za-z0-9_-]+"
    ]

    def scan(self, content):

        findings = []

        for pattern in self.PATTERNS:

            if re.search(
                pattern,
                content,
                re.IGNORECASE
            ):

                findings.append(
                    {
                        "issue":
                        "Potential Secret Found",

                        "severity":
                        "HIGH",

                        "pattern":
                        pattern
                    }
                )

        return findings