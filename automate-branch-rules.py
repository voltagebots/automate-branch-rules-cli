"""Importing necessary libraries."""
from github import Github
from github import GithubException
import sys, getopt
from stdiomask import getpass
from config import branches
from config import branch_rules
from config import signed_commit
from config import add_codeowners_file
import codeowners


"""Declare Variables"""
org_name = ''
repo_name = ''
pat = ''
exec_type = ''

def add_default(pat):
    """Add all function."""
    print("")
    for repo in git.get_organization(org_name).get_repos():
        for branch_name in branches:
            try:
                default_branch = repo.default_branch
                repo.get_branch(default_branch)
            except GithubException:
                print("Error:", repo.name, ",",
                      default_branch, "-->", sys.exc_info()[1])
            else:
                default_branch = repo.default_branch
                branch = repo.get_branch(default_branch)
                if(add_codeowners_file):
                    codeowners.add(org_name, pat, repo.name, default_branch)
                branch.edit_protection(**branch_rules)
                if(signed_commit):
                    branch.add_required_signatures()
                else:
                    branch.remove_required_signatures()
                print("Edited the branch protection rules for: "
                      + repo.name + "," + default_branch)

def add_all(pat):
    """Add all function."""
    print("")
    for repo in git.get_organization(org_name).get_repos():
        for branch_name in branches:
            try:
                repo.get_branch(branch_name)
            except GithubException:
                print("Error:", repo.name, ",",
                      branch_name, "-->", sys.exc_info()[1])
            else:
                branch = repo.get_branch(branch_name)
                if(add_codeowners_file):
                    codeowners.add(org_name, pat, repo.name, branch_name)
                branch.edit_protection(**branch_rules)
                if(signed_commit):
                    branch.add_required_signatures()
                else:
                    branch.remove_required_signatures()
                print("Edited the branch protection rules for: "
                      + repo.name + "," + branch_name)


def add_one(pat):
    """Add one function."""
    repo = git.get_repo(org_name+"/"+repo_name)
    for branch_name in branches:
        try:
            repo.get_branch(branch_name)
        except GithubException:
            print("Error:", repo.name, ",", branch_name, "-->",
                  sys.exc_info()[1])
        else:
            branch = repo.get_branch(branch_name)
            if(add_codeowners_file):
                codeowners.add(org_name, pat, repo_name, branch_name)
            branch.edit_protection(**branch_rules)
            if(signed_commit):
                branch.add_required_signatures()
            else:
                branch.remove_required_signatures()
            print("Edited the branch protection rules for: "
                  + repo.name + "," + branch_name)


def remove_one():
    """Remove One Function."""
    repo = git.get_repo(org_name+"/"+repo_name)
    for branch_name in branches:
        try:
            repo.get_branch(branch_name)
        except GithubException:
            print("Error:", repo.name, ",",
                  branch_name, "-->", sys.exc_info()[1])
        else:
            branch = repo.get_branch(branch_name)
            if (branch.protected):
                branch.remove_protection()
                print("Removed branch protection rules for: "
                      + repo.name + "," + branch_name)
            else:
                print("No branch protection rules for: "
                      + repo.name + "," + branch.name)


def remove_all():
    """Remove all function."""
    print("")
    for repo in git.get_organization(org_name).get_repos():
        for branch_name in branches:
            try:
                repo.get_branch(branch_name)
            except GithubException:
                print("Error:", repo.name, ",",
                      branch_name, "-->", sys.exc_info()[1])
            else:
                branch = repo.get_branch(branch_name)
                if (branch.protected):
                    branch.remove_protection()
                    print("Removed branch protection rules for: "
                          + repo.name + "," + branch_name)
                else:
                    print("No branch protection rules for: "
                          + repo.name + "," + branch.name)


def main(argv):
   global org_name
   global repo_name
   global pat
   global exec_type
   global git
   header = open("header.txt", "r")
   print(header.read())

   try:
      opts, args = getopt.getopt(argv,"ho:r:p:e:",["organization=","repository=","pat=","execType="])
   except getopt.GetoptError:
      print('automate-branch-rules -o <Github Org Name> -r <Github Repo Name> -p <Personal Access Token> -e <exec style>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('automate-branch-rules -o <Github Org Name> -r <Github Repo Name> -p <Personal Access Token> -e <exec style>')
         sys.exit()
      elif opt in ("-o", "--organization"):
         org_name = arg
      elif opt in ("-r", "--repository"):
         repo_name = arg
      elif opt in ("-p", "--pat"):
         pat = (arg)
         git = Github(arg)
      elif opt in ("-e", "--execType"):
         exec_type = arg
         if (exec_type == 'O'):
           add_one(pat)
         elif (exec_type == 'D'):
           add_default(pat)
         elif (exec_type == 'A'):
           add_all(pat)
         elif (exec_type == 'S'):
           remove_one()
         elif (exec_type == 'R'):
           remove_all()
         else:
           print("Invalid input. Re-run")

if __name__ == "__main__":
   main(sys.argv[1:])