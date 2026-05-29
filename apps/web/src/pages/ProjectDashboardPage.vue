<script setup lang="ts">
import { Bell, FileText, FolderKanban, Hourglass, PlusCircle } from "@lucide/vue";
import { projectRows, recentNotifications, savedReports } from "../app/mockData";
import PageHeader from "../components/common/PageHeader.vue";
import StatCard from "../components/common/StatCard.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader
      eyebrow="프로젝트 / 대시보드"
      title="검토 중인 사전진단을 한눈에 확인"
      description="진행 중인 진단, 저장된 보고서, 최근 알림과 다음 액션을 한 화면에서 확인합니다."
    >
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
      <div class="panel dashboard-project-panel">
        <div class="section-title">
          <div>
            <h2>프로젝트 목록</h2>
            <p class="subtle">상태별로 다음 액션이 바로 이어지도록 구성했습니다.</p>
          </div>
          <RouterLink class="button" to="/projects">전체 보기</RouterLink>
        </div>
        <table class="table">
          <thead><tr><th>프로젝트명</th><th>대상지</th><th>상태</th><th>리스크</th><th>액션</th></tr></thead>
          <tbody>
            <tr v-for="project in projectRows" :key="project.id">
              <td><RouterLink to="/projects/demo">{{ project.name }}</RouterLink><br /><span class="subtle">{{ project.updatedAt }}</span></td>
              <td>{{ project.address }}<br /><span class="subtle">PNU {{ project.pnu }}</span></td>
              <td><span class="badge" :class="{ warning: project.status.includes('필요') }">{{ project.status }}</span></td>
              <td>{{ project.risk }}</td>
              <td><RouterLink class="button" to="/projects/demo/diagnosis">{{ project.action }}</RouterLink></td>
            </tr>
          </tbody>
        </table>

        <div class="dashboard-bottom-grid">
          <section class="compact-surface">
            <div class="section-title compact">
              <h3>오늘 우선 확인</h3>
              <span class="badge warning">3건</span>
            </div>
            <ul class="mini-list dense-list">
              <li><span>강남 역삼동 계획 주차 기준 보완</span><span class="badge warning">중간</span></li>
              <li><span>부산 해운대 법령 근거 갱신 확인</span><span class="badge">RAG</span></li>
              <li><span>인천 송도 추가정보 요청 문구 정리</span><span class="badge neutral">검토</span></li>
            </ul>
          </section>

          <section class="compact-surface">
            <div class="section-title compact">
              <h3>진단 처리 큐</h3>
              <span class="badge">룰엔진 대기 4건</span>
            </div>
            <div class="queue-grid">
              <div><strong>7</strong><span>공공데이터 조회</span></div>
              <div><strong>4</strong><span>룰엔진 대기</span></div>
              <div><strong>5</strong><span>보고서 생성</span></div>
            </div>
          </section>
        </div>
      </div>

      <div class="grid">
        <section class="panel">
          <div class="section-title"><h2>최근 진단</h2><span class="badge warning">이어하기</span></div>
          <ul class="mini-list">
            <li v-for="project in projectRows.slice(0, 3)" :key="project.name">
              <span><strong>{{ project.name }}</strong><br /><span class="subtle">{{ project.status }} · {{ project.updatedAt }}</span></span>
              <RouterLink class="button" to="/projects/demo/diagnosis">보기</RouterLink>
            </li>
          </ul>
        </section>

        <section class="panel">
          <div class="section-title"><h2>저장된 보고서</h2><span class="badge neutral">{{ savedReports.length }}종</span></div>
          <ul class="mini-list">
            <li v-for="report in savedReports.slice(0, 4)" :key="report">
              <span>{{ report }}<br /><span class="subtle">강남 역삼동 근린시설 계획</span></span>
              <RouterLink class="button" to="/reports/demo">열기</RouterLink>
            </li>
          </ul>
        </section>

        <section class="panel">
          <div class="section-title"><h2>최근 알림</h2><RouterLink class="button" to="/notifications">전체</RouterLink></div>
          <ul class="mini-list">
            <li v-for="item in recentNotifications" :key="item">
              <span>{{ item }}</span>
              <span class="badge warning">확인</span>
            </li>
          </ul>
        </section>
      </div>
    </section>
  </AppShell>
</template>
