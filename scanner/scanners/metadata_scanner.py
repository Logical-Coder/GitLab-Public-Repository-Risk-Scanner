class MetadataScanner:

    def scan(self, files):

        findings = []

        file_names = {
            file["name"]
            for file in files
        }

        if "README.md" not in file_names:

            findings.append(
                {
                    "issue": "Missing README",
                    "severity": "LOW"
                }
            )

        if "LICENSE" not in file_names:

            findings.append(
                {
                    "issue": "Missing LICENSE",
                    "severity": "LOW"
                }
            )

        return findings