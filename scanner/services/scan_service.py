from gitlab.services.gitlab_service import (
    GitLabService
)

from scanner.scanners.sensitive_file_scanner import (
    SensitiveFileScanner
)

from scanner.scanners.metadata_scanner import (
    MetadataScanner
)

from scanner.scanners.secret_scanner import (
    SecretScanner
)


class ScanService:

    def execute_scan(
        self,
        target_type,
        target_name
    ):

        gitlab_service = GitLabService()

        projects = gitlab_service.get_projects(
            target_type,
            target_name
        )

        sensitive_scanner = SensitiveFileScanner()

        metadata_scanner = MetadataScanner()

        secret_scanner = SecretScanner()

        results = []

        for project in projects:

            print(
                f"Scanning repository: "
                f"{project['name']}"
            )

            try:
                files = gitlab_service.get_repository_tree(
                    project["id"]
                )
            except Exception as error:

                print(
                    f"Failed to get repository tree "
                    f"for {project['name']}: {error}"
                )

                continue

            findings = []

            # Sensitive file scan
            findings.extend(
                sensitive_scanner.scan(files)
            )

            # Metadata scan
            findings.extend(
                metadata_scanner.scan(files)
            )

            # Secret scan
            for file in files:

                if file.get("type") != "blob":
                    continue

                try:

                    content = (
                        gitlab_service.get_file_content(
                            project["id"],
                            file["path"]
                        )
                    )

                    findings.extend(
                        secret_scanner.scan(
                            content
                        )
                    )

                except Exception as error:

                    print(
                        f"Failed to scan file "
                        f"{file['path']}: "
                        f"{error}"
                    )

            results.append(
                {
                    "repository_name":
                    project["name"],

                    "repository_url":
                    project["web_url"],

                    "findings":
                    findings
                }
            )

        return {
            "scan_target":
            target_name,

            "repositories_scanned":
            len(results),

            "total_findings":
            sum(
                len(
                    repository["findings"]
                )
                for repository in results
            ),

            "repositories":
            results
        }