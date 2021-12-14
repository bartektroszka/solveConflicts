import { Gitgraph } from '@gitgraph/react';

export const GitTree = () => {
  return (
    <Gitgraph>
      {(gitgraph) => {
        // Simulate git commands with Gitgraph API.
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
        master.commit({
          author: '',
          subject: 'first commit',
          style: { message: { color: 'green' }, dot: { color: 'green' } },
        });
        master.commit({
          author: '',
          subject: 'second commit',
          style: { message: { color: 'green' }, dot: { color: 'green' } },
        });
      }}
    </Gitgraph>
  );
};
