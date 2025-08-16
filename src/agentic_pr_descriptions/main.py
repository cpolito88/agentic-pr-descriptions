import argparse
import sys

from agentic_pr_descriptions.crew import PRDescriptionCrew
from agentic_pr_descriptions.logger import log
from agentic_pr_descriptions.utils.git import create_patch


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a PR description based on the diff between two Git branches.",
        epilog="Example: python your_script_name.py ./my-repo my-feature --base-branch main",
    )

    parser.add_argument(
        "--repo_path",
        type=str,
        help="The file system path to the local Git repository.",
    )
    parser.add_argument(
        "--feature_branch",
        type=str,
        help="The name of the feature branch (the 'new' code).",
    )
    parser.add_argument(
        "--base_branch",
        type=str,
        default="main",
        help="The name of the base branch to compare against. Defaults to 'main'.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    patch_content = create_patch(args.repo_path, args.feature_branch, args.base_branch)

    if not patch_content:
        log.warning("The two branches are identical. No patch generated. Exiting.")
        sys.exit(0)

    log.info("Initializing PRDescriptionCrew to generate description...")
    crew = PRDescriptionCrew().crew()
    response = crew.kickoff(inputs={"diff_content": patch_content})
    log.info("Successfully received response from the crew.")

    print("\n--- Generated PR Description ---")
    print(response)
    print("---------------------------------")


if __name__ == "__main__":
    main()
