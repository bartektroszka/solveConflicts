import { Gitgraph } from '@gitgraph/react';
import { GitCommit, Props } from './types';

export const GitTree = ({ commits }: Props) => {
  return (
    <Gitgraph>
      {(gitgraph) => {
        /* const master = gitgraph.branch({
          name: 'master',
          style: {
            color: 'green',
            label: {
              bgColor: '#ffce52',
              color: 'black',
              strokeColor: '#ce9b00',
            },
          },
        });
        const father: GitCommit = commits.filter(
          (commit) => commit.parents.length === 0
        )[0]; */
        let convertingCommits: any = {};
        commits.forEach((commit) => (convertingCommits[commit.hash] = {}));
        const prepareFutureBranches = (tempFather: GitCommit) => {
          const children = commits.filter((commit) =>
            commit.parents.includes(tempFather.hash)
          );
          for (const child of children) {
            let parent = convertingCommits[tempFather.hash];
            parent[child.hash] = gitgraph.branch(child.hash);
          }
        };
        const buildCommit = (commit: GitCommit) => {
          if (commit.parents.length === 1) {
            let branch = convertingCommits[commit.parents[0]][commit.hash];
            branch.commit(commit.hash);
          } else if (commit.parents.length === 2) {
            let mainBranch = convertingCommits[commit.parents[0]][commit.hash];
            let secondBranch =
              convertingCommits[commit.parents[1]][commit.hash];
            mainBranch.merge(secondBranch);
          } else if (commit.parents.length === 0) {
            gitgraph.branch('master').commit();
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
