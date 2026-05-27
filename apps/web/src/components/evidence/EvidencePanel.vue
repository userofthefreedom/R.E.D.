<script setup lang="ts">
import { ExternalLink } from "@lucide/vue";
import { evidenceItems } from "../../app/mockData";
</script>

<template>
  <section class="panel">
    <div class="section-title">
      <h2>근거 자료</h2>
      <span class="badge neutral">Evidence Trace</span>
    </div>
    <div class="grid">
      <div class="notice">
        <strong>법령/조례 근거</strong>
        <ul>
          <li v-for="item in evidenceItems" :key="item">{{ item }}</li>
        </ul>
      </div>
      <div class="grid two">
        <div class="card">
          <h3>Rule Trace</h3>
          <p>MAIN-NEW-001, DEV-ACT-001, PARKING-LOCAL-002 실행</p>
        </div>
        <div class="card">
          <h3>원문 링크</h3>
          <p>조문, 페이지, 수집일 기준으로 원문 확인이 가능합니다.</p>
          <button class="button"><ExternalLink />원문 보기</button>
        </div>
      </div>
    </div>
  </section>
</template>
