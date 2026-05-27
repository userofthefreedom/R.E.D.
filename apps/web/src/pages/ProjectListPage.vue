<script setup lang="ts">
import { Search } from "@lucide/vue";
import { projectRows } from "../app/mockData";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="프로젝트 / 내 프로젝트" title="내 프로젝트 목록" description="프로젝트명, 주소, PNU, 상태값으로 진단 건을 빠르게 찾고 이어갈 수 있습니다." />
    <section class="panel">
      <div class="section-title">
        <div class="field" style="width: min(420px, 100%)">
          <label>프로젝트명 / 주소 / PNU 검색</label>
          <div style="display: flex; gap: 8px"><input class="input" value="강남 역삼" /><button class="button"><Search />검색</button></div>
        </div>
        <div class="topbar-actions"><select class="select" style="width: 150px"><option>상태 전체</option></select><select class="select" style="width: 150px"><option>전체 기간</option></select></div>
      </div>
      <table class="table">
        <thead><tr><th>프로젝트명</th><th>대상지</th><th>리스크</th><th>상태</th><th>최근 수정</th><th>액션</th></tr></thead>
        <tbody>
          <tr v-for="project in projectRows" :key="project.pnu">
            <td>{{ project.name }}</td>
            <td>{{ project.address }}<br /><span class="subtle">PNU {{ project.pnu }}</span></td>
            <td><span class="badge" :class="{ warning: project.risk === '중간', danger: project.risk === '높음' }">{{ project.risk }}</span></td>
            <td>{{ project.status }}</td>
            <td>{{ project.updatedAt }}</td>
            <td><RouterLink class="button" to="/projects/demo">상세</RouterLink></td>
          </tr>
        </tbody>
      </table>
    </section>
  </AppShell>
</template>
