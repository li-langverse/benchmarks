/** GitHub tree URL for a benchmark path under li-langverse org repos. */
export function githubTreeUrl(repo: string, repoPath: string): string {
  const clean = repoPath.replace(/^\/+/, "").replace(/\/+$/, "");
  if (!clean || clean === "unknown") {
    return `https://github.com/li-langverse/${repo}`;
  }
  return `https://github.com/li-langverse/${repo}/tree/main/${clean}`;
}
