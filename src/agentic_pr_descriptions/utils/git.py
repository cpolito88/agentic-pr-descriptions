import git

from agentic_pr_descriptions.logger import log


def create_patch(repo_path, feature_branch, base_branch=None):
    """
    Computes a patch (diff) from two branches and returns it as a sttring.

    Args:
        repo_path (str): The file system path to the git repository.
        feature_branch (str): The name of the branch with new changes.
        base_branch (str, optional): The name of the base branch to compare against.
                                     If not provided, it will be determined automatically.
                                     Defaults to None.
    Returns:
        str or None: A string containing the diff in the patch format if output_file is None,
                     otherwise None.

    Raises:
        git.exc.NoSuchPathError: If the repository path does not exist.
        git.exc.InvalidGitRepositoryError: If the path is not a valid git repository.
        ValueError: If the specified branches cannot be found.
        Exception: For any other unexpected errors.
    """
    try:
        repo = git.Repo(repo_path)
        log.info(f"Successfully opened repository: {repo_path}")

        if base_branch is None:
            try:
                remote_head = repo.remote().refs.HEAD
                base_branch = remote_head.ref.name.split("/")[-1]
            except (ValueError, IndexError):
                if "main" in repo.branches:
                    base_branch = "main"
                elif "master" in repo.branches:
                    base_branch = "master"
                else:
                    raise ValueError(
                        "Could not determine the default branch. Please specify a base_branch."
                    )

        if feature_branch not in repo.branches:
            raise ValueError(f"Error: Feature branch '{feature_branch}' not found.")
        if base_branch not in repo.branches:
            raise ValueError(f"Error: Base branch '{base_branch}' not found.")

        log.info(
            f"Comparing feature branch '{feature_branch}' against base '{base_branch}'"
        )

        patch_content = repo.git.diff(f"{base_branch}..{feature_branch}")

        log.info("Successfully generated patch content.")
        return patch_content

    except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError, ValueError):
        raise
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")
