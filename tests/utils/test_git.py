import os

import git
import pytest

from agentic_pr_descriptions.utils.git import create_patch


@pytest.fixture
def git_repo(tmp_path):
    repo = git.Repo.init(tmp_path)
    with open(os.path.join(tmp_path, "README.md"), "w") as f:
        f.write("This is the main branch.\n")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit on main")

    feature_branch = repo.create_head("feature")
    repo.head.set_reference(feature_branch)
    repo.head.reset(index=True, working_tree=True)
    with open(os.path.join(tmp_path, "README.md"), "a") as f:
        f.write("An update from the feature branch.\n")
    with open(os.path.join(tmp_path, "feature_file.txt"), "w") as f:
        f.write("A new file.\n")
    repo.index.add(["README.md", "feature_file.txt"])
    repo.index.commit("Add feature and update README")

    repo.create_head("no-diff-feature", "main")

    repo.heads.main.checkout()

    yield tmp_path


def test_create_patch_success(git_repo):
    patch = create_patch(git_repo, "feature", "main")

    assert not patch.startswith("Error:")

    assert "diff --git a/README.md b/README.md" in patch
    assert "--- a/README.md" in patch
    assert "+++ b/README.md" in patch
    assert "+An update from the feature branch." in patch

    assert "diff --git a/feature_file.txt b/feature_file.txt" in patch
    assert "new file mode" in patch
    assert "--- /dev/null" in patch
    assert "+++ b/feature_file.txt" in patch
    assert "+A new file." in patch


def test_create_patch_no_difference(git_repo):
    patch = create_patch(git_repo, "no-diff-feature", "main")
    assert patch == ""
    assert not patch.startswith("Error:")


def test_non_existent_repo_path():
    with pytest.raises(git.exc.NoSuchPathError):
        create_patch("/whatever", "feature", "main")


def test_invalid_git_repo_path(tmp_path):
    with pytest.raises(git.exc.InvalidGitRepositoryError):
        create_patch(tmp_path, "feature", "main")


def test_non_existent_feature_branch(git_repo):
    with pytest.raises(ValueError) as ex:
        create_patch(git_repo, "non-existent-branch", "main")
    assert "Feature branch 'non-existent-branch' not found" in ex.exconly()


def test_non_existent_base_branch(git_repo):
    with pytest.raises(ValueError) as ex:
        create_patch(git_repo, "feature", "non-existent-base")
    assert "Base branch 'non-existent-base' not found" in ex.exconly()


def test_master_fallback(git_repo):
    repo = git.Repo(git_repo)
    patch = create_patch(git_repo, "feature")
    assert "--- a/README.md" in patch
    assert "+++ b/README.md" in patch
    assert not patch.startswith("Error:")

    repo.branches["main"].rename("master")

    patch = create_patch(git_repo, "feature")
    assert "--- a/README.md" in patch
    assert "+++ b/README.md" in patch
    assert not patch.startswith("Error:")
