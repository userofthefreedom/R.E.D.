import { projectRows } from "../app/mockData";
import type { ApiProject, ProjectRow } from "../types/project";

export function rowsFromApiProjects(projects: ApiProject[]): ProjectRow[] {
  if (!projects.length) {
    return projectRows;
  }

  return projects.map((project, index) => ({
    ...projectRows[index % projectRows.length],
    id: project.id,
    pnu: project.pnu ?? projectRows[index % projectRows.length].pnu,
  }));
}
