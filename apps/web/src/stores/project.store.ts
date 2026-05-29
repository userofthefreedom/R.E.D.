import { defineStore } from "pinia";

export const useProjectStore = defineStore("project", {
  state: () => ({
    currentProjectId: null as string | null,
    currentParcelId: null as string | null,
    currentRegulationOverlayId: null as string | null,
    currentActionId: null as string | null,
    currentDiagnosisRunId: null as string | null,
  }),
});
