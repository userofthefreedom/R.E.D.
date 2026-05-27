import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import ProjectListPage from "../pages/ProjectListPage.vue";
import ProjectCreatePage from "../pages/ProjectCreatePage.vue";
import DiagnosisWizardPage from "../pages/DiagnosisWizardPage.vue";
import ReportPreviewPage from "../pages/ReportPreviewPage.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: HomePage },
    { path: "/projects", component: ProjectListPage },
    { path: "/projects/new", component: ProjectCreatePage },
    { path: "/projects/:projectId/diagnosis", component: DiagnosisWizardPage },
    { path: "/reports/:reportId", component: ReportPreviewPage },
  ],
});

