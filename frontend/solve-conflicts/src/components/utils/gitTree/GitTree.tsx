import { Gitgraph } from "@gitgraph/react";
import { GitCommit, Props } from "./types";

export const GitTree = ({ commits }: Props) => {
	return (
		<Gitgraph>
			{gitgraph => {
				const futureBranches: any = {};
				const nativeBranch: any = {};
				let masterName = "master";
				commits.forEach(commit => (futureBranches[commit.hash] = {}));

				const prepareFutureBranches = (tempFather: GitCommit) => {
					const children = commits.filter(commit => commit.parents.includes(tempFather.hash));
					let parent = futureBranches[tempFather.hash];

					for (var i = 0; i < children.length; i++) {
						if (tempFather.branch === children[i].branch) {
							continue;
						}

						parent[children[i].hash] = gitgraph.branch({
							name: children[i].branch,
							style: {
								label: {
									bgColor: "#d3d3d3",
								},
							},
						});
					}
				};
				const buildCommit = (commit: GitCommit) => {
					if (commit.parents.length === 0) {
						masterName = commit.branch;

						nativeBranch[commit.hash] = gitgraph.branch({
							name: masterName,
							style: {
								color: "#639b49",
								label: {
									bgColor: "#d3d3d3",
									color: "#639b49",
								},
							},
						});

						nativeBranch[commit.hash].commit({
							hash: commit.hash,
							subject: commit.message,
							body: "",
							dotText: "",
							style: {
								dot: { color: "#639b49" },
								message: { color: "#84b96c", displayAuthor: false },
							},
						});
					} else if (commit.parents.length === 1) {
						let branch;

						if (commit.hash in futureBranches[commit.parents[0]])
							branch = futureBranches[commit.parents[0]][commit.hash];
						else branch = nativeBranch[commit.parents[0]];

						branch.commit(
							branch.name === masterName
								? {
										hash: commit.hash,
										subject: commit.message,
										body: "",
										dotText: "",
										style: {
											dot: { color: "#639b49" },
											message: { color: "#84b96c", displayAuthor: false },
										},
								  }
								: {
										hash: commit.hash,
										subject: commit.message,
										body: "",
										dotText: "",
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
								mainBranch.name === masterName
									? {
											hash: commit.hash,
											style: {
												subject: commit.message,
												body: "",
												dotText: "",
												dot: { color: "#639b49" },
												message: { color: "#639b49", displayAuthor: false },
											},
									  }
									: {
											hash: commit.hash,
											style: {
												subject: commit.message,
												body: "",
												dotText: "",
												dot: { color: "#639b49" },
												message: { displayAuthor: false },
											},
									  },
						});
						nativeBranch[commit.hash] = mainBranch;
					}
				};

				for (let i = 0; i < commits.length; i += 1) {
					let commit = commits[i];
					buildCommit(commit);
					prepareFutureBranches(commit);
					// if (i == 0) break;
				}
			}}
		</Gitgraph>
	);
};
