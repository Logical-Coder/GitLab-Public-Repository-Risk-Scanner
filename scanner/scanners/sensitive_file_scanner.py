class SensitiveFileScanner:

    SENSITIVE_FILES = [
        ".env",
        ".env.local",
        ".env.production",
        "id_rsa",
        ".pem",
        "secrets.yml",
        "config.json"
    ]

    def scan(self, files):

        findings = []

        for file in files:

            if file["name"] in self.SENSITIVE_FILES:

                findings.append(
                    {
                        "issue": "Sensitive File Found",
                        "severity": "HIGH",
                        "file": file["path"]
                    }
                )

        return findings