import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import AccountSettingsPage from "../pages/AccountSettingsPage.vue";
import NotificationCenterPage from "../pages/NotificationCenterPage.vue";
import SupportPage from "../pages/SupportPage.vue";
import ServiceIntroPage from "../pages/ServiceIntroPage.vue";
import DataSourcesPage from "../pages/DataSourcesPage.vue";
import ProjectDashboardPage from "../pages/ProjectDashboardPage.vue";
import ProjectListPage from "../pages/ProjectListPage.vue";
import ProjectCreatePage from "../pages/ProjectCreatePage.vue";
import ProjectDetailPage from "../pages/ProjectDetailPage.vue";
import DiagnosisWizardPage from "../pages/DiagnosisWizardPage.vue";
import AlternativeScenarioPage from "../pages/AlternativeScenarioPage.vue";
import DiagnosisHistoryComparePage from "../pages/DiagnosisHistoryComparePage.vue";
import ReportPreviewPage from "../pages/ReportPreviewPage.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: HomePage },
    { path: "/login", component: LoginPage },
    { path: "/register", component: RegisterPage },
    { path: "/account", component: AccountSettingsPage },
    { path: "/notifications", component: NotificationCenterPage },
    { path: "/support", component: SupportPage },
    { path: "/service-intro", component: ServiceIntroPage },
    { path: "/data-sources", component: DataSourcesPage },
    { path: "/dashboard", component: ProjectDashboardPage },
    { path: "/projects", component: ProjectListPage },
    { path: "/projects/new", component: ProjectCreatePage },
    { path: "/projects/:projectId", component: ProjectDetailPage },
    { path: "/projects/:projectId/diagnosis", component: DiagnosisWizardPage },
    { path: "/projects/:projectId/diagnosis/alternatives", component: AlternativeScenarioPage },
    { path: "/projects/:projectId/history", component: DiagnosisHistoryComparePage },
    { path: "/reports/:reportId", component: ReportPreviewPage },
  ],
});

