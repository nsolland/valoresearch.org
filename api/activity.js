export const config = { runtime: 'edge' };

const TEAM = [
  { name: 'Njål',  initials: 'NS', color: '#1e40af', repo: 'nsolland/Index' },
  // { name: 'Svein', initials: 'ST', color: '#065f46', repo: 'svein-torgersen/Index' },
  // { name: 'Frank', initials: 'FK', color: '#7c2d12', repo: 'frank-xxx/Index' },
];

async function ghFetch(path, token) {
  const r = await fetch(`https://api.github.com/${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
  });
  if (!r.ok) return null;
  return r.json();
}

export default async function handler(req) {
  const token = process.env.GITHUB_TOKEN;
  if (!token) return new Response(JSON.stringify({ error: 'No token' }), { status: 500 });

  const results = await Promise.all(
    TEAM.map(async (member) => {
      const [commits, contents] = await Promise.all([
        ghFetch(`repos/${member.repo}/commits?per_page=8`, token),
        ghFetch(`repos/${member.repo}/contents`, token),
      ]);

      const recentCommits = (commits || []).map((c) => ({
        sha: c.sha.slice(0, 7),
        message: c.commit.message.split('\n')[0],
        date: c.commit.author.date.slice(0, 10),
        author: c.commit.author.name,
      }));

      // Count files per folder
      const folderCounts = {};
      if (Array.isArray(contents)) {
        for (const item of contents) {
          if (item.type === 'dir') folderCounts[item.name] = item.name;
        }
      }

      return { ...member, commits: recentCommits, folders: Object.keys(folderCounts) };
    })
  );

  return new Response(JSON.stringify(results), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 's-maxage=120, stale-while-revalidate=60',
    },
  });
}
