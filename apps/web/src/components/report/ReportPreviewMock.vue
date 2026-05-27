<script setup lang="ts">
import { Download, Maximize, Search, ZoomIn } from "@lucide/vue";
</script>

<template>
  <section class="panel report-preview">
    <div class="preview-toolbar">
      <div class="topbar-actions">
        <button class="button ghost" title="페이지">1 / 15</button>
        <button class="button ghost" title="확대"><ZoomIn />100%</button>
      </div>
      <div class="topbar-actions">
        <button class="button ghost" title="검색"><Search /></button>
        <button class="button ghost" title="다운로드"><Download /></button>
        <button class="button ghost" title="전체화면"><Maximize /></button>
      </div>
    </div>
    <div class="document-page">
      <h2>건축 인허가 사전진단 종합보고서</h2>
      <p>대상지: 서울특별시 OO구 OO동 123-45</p>
      <div class="document-line" />
      <div class="document-line short" />
      <div class="document-line" />
      <div class="grid two" style="margin-top: 22px">
        <div class="card">
          <strong>종합 판정</strong>
          <p>조건부 가능성</p>
        </div>
        <div class="card">
          <strong>리스크</strong>
          <p>중간</p>
        </div>
      </div>
      <div class="document-line" />
      <div class="document-line" />
      <div class="document-line short" />
    </div>
  </section>
</template>
