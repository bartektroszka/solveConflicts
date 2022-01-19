import { Gitgraph } from '@gitgraph/react';
import { GitCommit, Props } from './types';

export const GitTree = ({ commits }: Props) => {
  return (
    <Gitgraph>
      {(gitgraph) => {
        const futureBranches: any = {};
        const nativeBranch: any = {};

        commits.forEach((commit) => (futureBranches[commit.hash] = {}));
        const prepareFutureBranches = (tempFather: GitCommit) => {
          const children = commits.filter((commit) =>
            commit.parents.includes(tempFather.hash)
          );
          let parent = futureBranches[tempFather.hash];

          // looping from one, since the first children will be from native
          for (var i = 1; i < children.length; i++) {
            console.log(children);
            parent[children[i].hash] = gitgraph.branch({
              name: children[i].branches[0],
              style: {
                label: {
                  bgColor: '#d3d3d3',
                },
              },
            });
          }
        };
        const buildCommit = (commit: GitCommit) => {
          if (commit.parents.length === 0) {
            nativeBranch[commit.hash] = gitgraph.branch({
              name: 'master',
              style: {
                color: '#639b49',
                label: {
                  bgColor: '#d3d3d3',
                  color: '#639b49',
                },
              },
            });
            nativeBranch[commit.hash].commit(
              nativeBranch[commit.hash].name === 'master'
                ? {
                    subject: commit.message,
                    body: '',
                    dotText: '',
                    style: {
                      dot: { color: '#639b49' },
                      message: { color: '#84b96c', displayAuthor: false },
                    },
                  }
                : {
                    subject: '',
                    body: '',
                    style: { message: { displayAuthor: false } },
                  }
            );
          } else if (commit.parents.length === 1) {
            let branch;
            if (commit.hash in futureBranches[commit.parents[0]])
              branch = futureBranches[commit.parents[0]][commit.hash];
            else branch = nativeBranch[commit.parents[0]];
            branch.commit(
              branch.name === 'master'
                ? {
                    subject: commit.message,
                    body: '',
                    dotText: '',
                    style: {
                      dot: { color: '#639b49' },
                      message: { color: '#84b96c', displayAuthor: false },
                    },
                  }
                : {
                    subject: commit.message,
                    body: '',
                    dotText: '',
                    style: {
                      message: { displayAuthor: false },
                    },
                  }
            );
            nativeBranch[commit.hash] = branch;
          } else if (commit.parents.length === 2) {
            let mainBranch = nativeBranch[commit.parents[0]];
            let secondBranch = nativeBranch[commit.parents[1]];

            // mainBranch.commit();
            // secondBranch.commit();

            mainBranch.merge({
              branch: secondBranch,
              commitOptions:
                mainBranch.name === 'master'
                  ? {
                      style: {
                        subject: commit.message,
                        body: '',
                        dotText: '',
                        dot: { color: '#639b49' },
                        message: { color: '#639b49', displayAuthor: false },
                      },
                    }
                  : {
                      style: {
                        subject: commit.message,
                        body: '',
                        dotText: '',
                        message: { displayAuthor: false },
                      },
                    },
            });
            nativeBranch[commit.hash] = mainBranch;
          }
        };
        commits.forEach((commit) => {
          buildCommit(commit);
          prepareFutureBranches(commit);
        });
      }}
    </Gitgraph>
  );
};
