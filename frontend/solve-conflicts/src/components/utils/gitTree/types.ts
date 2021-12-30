export interface GitCommit {
  branches: string[];
  children: string[];
  hash: string;
  parents: string[];
}

export interface Props {
  commits: GitCommit[];
}

export interface ConvertingCommit {
  merge: boolean;
  hash: string;
  branch: string;
  futureBranches: string[];
}
