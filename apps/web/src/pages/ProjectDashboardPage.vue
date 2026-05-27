<script setup lang="ts">
import { Bell, FileText, FolderKanban, Hourglass, PlusCircle } from "@lucide/vue";
import { projectRows } from "../app/mockData";
import PageHeader from "../components/common/PageHeader.vue";
import StatCard from "../components/common/StatCard.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="프로젝트 / 대시보드" title="검토 중인 사전진단을 한눈에 확인" description="프로젝트 상태, 저장 보고서, 최근 알림, 이어하기 액션을 mock 데이터로 구성했습니다.">
      <template #actions>
        <RouterLink class="button primary" to="/projects/new"><PlusCircle />새 진단 시작</RouterLink>
      </template>
    </PageHeader>
    <section class="grid four">
      <StatCard label="전체 프로젝트" value="42" hint="전월 대비 +6" :icon="FolderKanban" />
      <StatCard label="진행 중 진단" value="18" hint="룰엔진 대기 4건" :icon="Hourglass" />
      <StatCard label="저장된 보고서" value="24" hint="최근 7일 +5" :icon="FileText" />
      <StatCard label="최근 알림" value="3" hint="확인 필요" :icon="Bell" />
    </section>
    <section class="grid two" style="margin-top: 18px">
      <div class="panel">
        <div class="section-title"><h2>프로젝트 목록</h2><RouterLink class="button" to="/projects">전체 보기</RouterLink></div>
        <table class="table">
          <thead><tr><th>프로젝트명</th><th>대상지</th><th>상태</th><th>최근 수정</th></tr></thead>
          <tbody>
            <tr v-for="project in projectRows" :key="project.pnu">
              <td><RouterLink to="/projects/demo">{{ project.name }}</RouterLink></td>
              <td>{{ project.address }}<br /><span class="subtle">PNU {{ project.pnu }}</span></td>
              <td><span class="badge">{{ project.status }}</span></td>
              <td>{{ project.updatedAt }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="grid">
        <section class="panel">
          <div class="section-title"><h2>최근 진단</h2><span class="badge warning">이어하기</span></div>
          <ul class="mini-list">
            <li v-for="project in projectRows.slice(0, 3)" :key="project.name">
              <span><strong>{{ project.name }}</strong><br /><span class="subtle">{{ project.updatedAt }}</span></span>
              <RouterLink class="button" to="/projects/demo/diagnosis">보기</RouterLink>
            </li>
          </ul>
        </section>
        <section class="panel">
          <div class="section-title"><h2>저장된 보고서</h2><span class="badge neutral">24건</span></div>
          <ul class="mini-list">
            <li><span>강남 역삼동 근린시설 계획<br /><span class="subtle">보고서 v1 · 2025-05-19</span></span><RouterLink class="button" to="/reports/demo">다운로드</RouterLink></li>
            <li><span>부산 해운대 업무시설 신축<br /><span class="subtle">보고서 v1 · 2025-05-18</span></span><RouterLink class="button" to="/reports/demo">다운로드</RouterLink></li>
          </ul>
        </section>
      </div>
    </section>
  </AppShell>
</template>
