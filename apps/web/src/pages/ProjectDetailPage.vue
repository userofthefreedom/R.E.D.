<script setup lang="ts">
import { Download, History, PenLine } from "@lucide/vue";
import { savedReports } from "../app/mockData";
import EvidencePanel from "../components/evidence/EvidencePanel.vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="프로젝트 / 상세" title="강남 역삼동 근린시설 계획" description="프로젝트 기본 정보, 진단 요약, 저장 보고서, 근거 스냅샷, Action 이력을 확인합니다.">
      <template #actions>
        <RouterLink class="button" to="/projects/demo/history"><History />이력 비교</RouterLink>
        <RouterLink class="button primary" to="/projects/demo/diagnosis"><PenLine />진단 수정</RouterLink>
      </template>
    </PageHeader>
    <section class="grid four">
      <div class="card"><span class="subtle">종합 판정</span><h2>적합</h2><span class="badge warning">조건부</span></div>
      <div class="card"><span class="subtle">주 인허가 유형</span><h2>건축허가</h2></div>
      <div class="card"><span class="subtle">조건부/보완</span><h2>3건</h2></div>
      <div class="card"><span class="subtle">근거 법령 수</span><h2>18개</h2></div>
    </section>
    <section class="grid two" style="margin-top: 18px">
      <div class="panel">
        <h2>프로젝트 정보</h2>
        <table class="table"><tbody>
          <tr><th>위치</th><td>서울특별시 OO구 OO동</td></tr>
          <tr><th>용도</th><td>제2종 근린생활시설</td></tr>
          <tr><th>규모</th><td>지상 5층 / 연면적 1,234.56㎡</td></tr>
          <tr><th>생성일</th><td>2025-05-18 14:22</td></tr>
        </tbody></table>
      </div>
      <div class="panel">
        <div class="section-title"><h2>저장된 보고서</h2><button class="button"><Download />모두 다운로드</button></div>
        <ul class="mini-list"><li v-for="report in savedReports" :key="report"><span>{{ report }}</span><button class="button"><Download />다운로드</button></li></ul>
      </div>
    </section>
    <section style="margin-top: 18px"><EvidencePanel /></section>
  </AppShell>
</template>
