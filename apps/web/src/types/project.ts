export interface Project {
  id: string;
  name: string;
}

export interface ApiProject {
  id: string;
  owner_id: string | null;
  name: string;
  status: string;
  risk_level: string | null;
  address: string | null;
  pnu: string | null;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProjectRow {
  id: string;
  name: string;
  address: string;
  pnu: string;
  status: string;
  updatedAt: string;
  risk: string;
  action: string;
}
