export interface GitCommit {
  branch: string;
  children: string[];
  hash: string;
  parents: string[];
  message: string;
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
