import { Gitgraph } from '@gitgraph/react';
import { ConvertingCommit, GitCommit, Props } from './types';

export const GitTree = ({ commits }: Props) => {
  const convertCommits = () => {
    let convertedCommits = [];
    console.log(commits);
    const father: GitCommit = commits.filter(
      (commit) => commit.parents.length === 0
    )[0];
    console.log('father', father);
    convertedCommits.push({ hash: father.hash, merge: false });
    const convertCommitsOnce = (tempFather: ConvertingCommit) => {
      const loopCommits = commits.filter((commit) =>
        commit.parents.includes(tempFather.hash)
      );
      loopCommits.forEach((commit) => {
        let convertedCommit = {
          hash: commit.hash,
          merge: !(commit.parents.length === 1),
          branch: tempFather.branch,
        };
        convertedCommits.push(convertedCommit);
        convertCommitsOnce(convertedCommit);
      });
    };
    let tempFather = { hash: father.hash, merge: false, branch: 'master' };
    convertCommitsOnce(tempFather);
    return convertedCommits;
  };
  if (commits.length > 0) console.log(convertCommits());
  return (
    <Gitgraph>
      {(gitgraph) => {
        const master = gitgraph.branch({
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
        commits.map((commit) => {
          console.log(commit);
          return master.commit({
            author: '',
            subject: '',
            body: '',
            hash: commit.hash,
            style: { message: { color: 'green' }, dot: { color: 'green' } },
          });
        });
      }}
    </Gitgraph>
  );
};
