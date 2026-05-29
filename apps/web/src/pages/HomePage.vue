<script setup lang="ts">
import { ArrowRight, ClipboardCheck, FileText, MapPinned, Scale } from "@lucide/vue";
import AppShell from "../components/layout/AppShell.vue";
import ParcelMapMock from "../components/map/ParcelMapMock.vue";
</script>

<template>
  <AppShell>
    <section class="page-header">
      <div>
        <p class="eyebrow">AI Building Permit Manager</p>
        <h1>주소와 건축계획만으로 인허가 사전진단</h1>
        <p>
          위치 기반 공공데이터, 룰엔진, 법령 근거 검색, 보고서 생성을 하나의 흐름으로
          연결한 실무형 검토 도구입니다.
        </p>
        <div class="topbar-actions">
          <RouterLink class="button primary" to="/projects/new"><ArrowRight />새 진단 시작</RouterLink>
          <RouterLink class="button" to="/dashboard">대시보드 보기</RouterLink>
        </div>
      </div>
      <div class="panel" style="min-width: min(460px, 100%)">
        <ParcelMapMock />
      </div>
    </section>

    <section class="grid three">
      <article class="card">
        <MapPinned />
        <h3>위치 기반 진단</h3>
        <p>주소, 지번, 좌표를 PNU와 필지 정보로 정규화합니다.</p>
      </article>
      <article class="card">
        <Scale />
        <h3>룰엔진 기반 판단</h3>
        <p>주 인허가 유형과 조건부 절차를 재현 가능한 규칙으로 분기합니다.</p>
      </article>
      <article class="card">
        <FileText />
        <h3>보고서 생성</h3>
        <p>근거와 판정 결과를 체크리스트, 질문, 종합보고서로 정리합니다.</p>
      </article>
    </section>

    <section class="panel" style="margin-top: 18px">
      <div class="section-title">
        <h2>이용 흐름</h2>
        <span class="badge">4단계</span>
      </div>
      <div class="flow-strip">
        <div class="flow-step"><ClipboardCheck /><strong>1. 주소 입력 및 PNU 확인</strong></div>
        <div class="flow-step"><ClipboardCheck /><strong>2. 건축계획 입력 및 조건 설정</strong></div>
        <div class="flow-step"><ClipboardCheck /><strong>3. 판정 및 근거 확인</strong></div>
        <div class="flow-step"><ClipboardCheck /><strong>4. 리포트 생성 및 저장</strong></div>
      </div>
    </section>
  </AppShell>
</template>
