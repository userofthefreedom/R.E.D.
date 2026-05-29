<script setup lang="ts">
import { Download, FileArchive, Play } from "@lucide/vue";
import { savedReports } from "../app/mockData";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
import ReportPreviewMock from "../components/report/ReportPreviewMock.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="실무 산출물 생성" title="보고서 미리보기" description="체크리스트, 필요서류, 사전협의 질문, 신청서 초안, 종합보고서를 검토합니다.">
      <template #actions><button class="button"><Download />PDF</button><button class="button primary"><FileArchive />DOCX</button></template>
    </PageHeader>
    <section class="result-layout">
      <div class="grid report-workbench">
        <div class="panel">
          <div class="section-title"><h2>생성 항목</h2><span class="badge">선택됨</span></div>
          <ul class="mini-list">
            <li v-for="report in savedReports" :key="report"><span>{{ report }}</span><span class="badge">v1.0</span></li>
          </ul>
        </div>

        <div class="panel">
          <h2>프로젝트 요약</h2>
          <p>신축 · 업무시설 · 대지 540.00㎡ · 연면적 1,200.00㎡ · 조건부 가능성 · 주 인허가 유형 건축허가</p>
          <div class="report-kpi-grid">
            <div><span>조건부 절차</span><strong>3건</strong></div>
            <div><span>근거 문서</span><strong>4개</strong></div>
            <div><span>누락정보</span><strong>3건</strong></div>
          </div>
          <button class="button primary"><Play />생성하기</button>
        </div>

        <div class="panel">
          <div class="section-title"><h2>산출물 구성 상태</h2><span class="badge warning">문서 생성 중</span></div>
          <ol class="progress-list compact-progress">
            <li><span>보고서 컨텍스트 구성</span><strong>완료</strong></li>
            <li><span>Rule / Evidence Trace 정리</span><strong>완료</strong></li>
            <li class="active"><span>사전협의 질문 문서화</span><strong>진행 중</strong></li>
            <li><span>DOCX/PDF 패키징</span><strong>대기</strong></li>
          </ol>
        </div>

        <div class="panel">
          <div class="section-title"><h2>보고서 포함 범위</h2><span class="badge">Trace 포함</span></div>
          <div class="readiness-grid three-up">
            <div><strong>룰셋</strong><span>rule-set-v0.1.0</span></div>
            <div><strong>법령 기준일</strong><span>2025-05-20</span></div>
            <div><strong>면책 문구</strong><span>사전진단 참고자료</span></div>
          </div>
          <div class="notice compact-note">
            <strong>활용 안내</strong>
            <span>내부 검토와 관할부서 사전협의에 바로 붙일 수 있는 요약형 산출물입니다.</span>
          </div>
        </div>
      </div>
      <ReportPreviewMock />
    </section>
  </AppShell>
</template>
