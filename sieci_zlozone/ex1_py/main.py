from github import Github
import json

if __name__ == "__main__":
    name = "kobala58"
    token = "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"
    git = Github(name, token)

    repos = git.search_repositories(query="rust", language="rust")
    cnt = 0
    data = []
    for repo in repos:
        cnt += 1
        # contr = set([cmt.commit.author.name for cmt in repo.get_contributors()])
        if cnt == 1:
            continue
        users = [x.login for x in repo.get_contributors()]
        tmp = {
                "name": repo.full_name,
                "contributors": users,
                "number": len(users)
                }
        data.append(tmp)
        if len(data) == 1000:
            break
        print(f"{cnt}/1000 -> repo.full_name")
    with open("results.json", "w") as file:
        json.dump(data, file, indent = 4)
    # repos_ = {repo: len(commiters) for repo, commiters in repo.}
