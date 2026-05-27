import { defineStore } from "pinia";

export const useWizardStore = defineStore("wizard", {
  state: () => ({
    currentStep: 1,
    totalSteps: 4,
  }),
});

