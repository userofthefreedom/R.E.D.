<script setup lang="ts">
import {
  Bell,
  BookOpen,
  ClipboardCheck,
  Database,
  FileText,
  FolderKanban,
  HelpCircle,
  Home,
  LayoutDashboard,
  LogIn,
  PlusCircle,
  Settings,
} from "@lucide/vue";
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <RouterLink class="brand" to="/">
        <span class="brand-mark">AI</span>
        <span>
          <strong>건축 인허가 매니저</strong>
          <span>사전진단 워크스페이스</span>
        </span>
      </RouterLink>

      <nav class="nav-group" aria-label="주요 메뉴">
        <p class="nav-label">글로벌</p>
        <RouterLink class="nav-link" to="/"><Home />홈</RouterLink>
        <RouterLink class="nav-link" to="/login"><LogIn />로그인</RouterLink>
        <RouterLink class="nav-link" to="/service-intro"><BookOpen />서비스 소개</RouterLink>
        <RouterLink class="nav-link" to="/data-sources"><Database />데이터 출처</RouterLink>
      </nav>

      <nav class="nav-group" aria-label="프로젝트 메뉴">
        <p class="nav-label">프로젝트</p>
        <RouterLink class="nav-link" to="/dashboard"><LayoutDashboard />대시보드</RouterLink>
        <RouterLink class="nav-link" to="/projects"><FolderKanban />내 프로젝트</RouterLink>
        <RouterLink class="nav-link" to="/projects/new"><PlusCircle />새 진단</RouterLink>
        <RouterLink class="nav-link" to="/reports/demo"><FileText />보고서</RouterLink>
      </nav>

      <nav class="nav-group" aria-label="지원 메뉴">
        <p class="nav-label">지원</p>
        <RouterLink class="nav-link" to="/notifications"><Bell />알림</RouterLink>
        <RouterLink class="nav-link" to="/account"><Settings />계정 설정</RouterLink>
        <RouterLink class="nav-link" to="/support"><HelpCircle />고객지원</RouterLink>
      </nav>
    </aside>

    <section class="shell-main">
      <header class="topbar">
        <div class="topbar-title">
          <ClipboardCheck />
          <span>Mockup preview · 백엔드 연결 전 화면 검토용</span>
        </div>
        <div class="topbar-actions">
          <RouterLink class="button ghost" to="/notifications"><Bell />알림</RouterLink>
          <RouterLink class="button primary" to="/projects/new"><PlusCircle />새 진단 시작</RouterLink>
        </div>
      </header>
      <main class="content">
        <slot />
      </main>
    </section>
  </div>
</template>
