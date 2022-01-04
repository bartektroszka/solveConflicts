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
        const names: any = {};
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
            parent[children[i].hash] = gitgraph.branch(children[i].hash);
          }
        };
        const buildCommit = (commit: GitCommit) => {
          if (commit.parents.length === 0) {
            nativeBranch[commit.hash] = gitgraph.branch('master')
            nativeBranch[commit.hash].commit();
          } 
          else if (commit.parents.length === 1) {
            let branch;
            if (commit.hash in futureBranches[commit.parents[0]])
              branch = futureBranches[commit.parents[0]][commit.hash];
            else
              branch = nativeBranch[commit.parents[0]];
            branch.commit(commit.hash);
            nativeBranch[commit.hash] = branch
          } 
          else if (commit.parents.length === 2) {
            let mainBranch = nativeBranch[commit.parents[0]]; 
            let secondBranch = nativeBranch[commit.parents[1]];
            
            // mainBranch.commit();
            // secondBranch.commit();
            mainBranch.merge(secondBranch);
            nativeBranch[commit.hash] = mainBranch
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
