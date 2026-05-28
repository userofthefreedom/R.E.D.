<script setup lang="ts">
import { computed, ref } from "vue";
import { ExternalLink } from "@lucide/vue";
import { diagnosisMeta, evidenceItems, evidenceTraces, ruleTraces } from "../../app/mockData";

const tabs = ["법령/조례 근거", "Evidence Trace", "Rule Trace"];
const activeTab = ref(tabs[0]);
const activeIndex = computed(() => tabs.indexOf(activeTab.value));
</script>

<template>
  <section class="panel evidence-panel">
    <div class="section-title">
      <div>
        <h2>판단 근거</h2>
        <p class="subtle">룰엔진 판단과 RAG 근거를 함께 확인하세요.</p>
      </div>
      <span class="badge neutral">{{ diagnosisMeta.ragIndexVersion }}</span>
    </div>

    <div class="segmented-tabs" role="tablist">
      <button
        v-for="tab in tabs"
        :key="tab"
        class="segment"
        :class="{ active: activeTab === tab }"
        type="button"
        @click="activeTab = tab"
      >
        {{ tab }}
      </button>
    </div>

    <div v-if="activeIndex === 0" class="grid">
      <article v-for="item in evidenceItems" :key="item.title" class="trace-card">
        <div>
          <strong>{{ item.title }}</strong>
          <p>{{ item.detail }}</p>
        </div>
        <div class="trace-meta">
          <span>{{ item.source }}</span>
          <span>{{ item.date }}</span>
        </div>
      </article>
      <button class="button"><ExternalLink />원문 근거 열람</button>
    </div>

    <div v-else-if="activeIndex === 1" class="grid">
      <article v-for="trace in evidenceTraces" :key="trace.chunkId" class="trace-card">
        <div class="section-title compact">
          <strong>{{ trace.procedure }}</strong>
          <span class="badge">{{ Math.round(trace.confidence * 100) }}%</span>
        </div>
        <p>{{ trace.reason }}</p>
        <div class="trace-meta">
          <span>{{ trace.source }}</span>
          <span>{{ trace.chunkId }}</span>
        </div>
      </article>
    </div>

    <div v-else class="grid">
      <article v-for="trace in ruleTraces" :key="trace.ruleId" class="trace-card">
        <div class="section-title compact">
          <strong>{{ trace.ruleId }}</strong>
          <span class="badge warning">{{ trace.result }}</span>
        </div>
        <h3>{{ trace.ruleName }}</h3>
        <p>{{ trace.reason }}</p>
        <div class="chip-row">
          <span v-for="field in trace.inputFields" :key="field" class="chip">{{ field }}</span>
        </div>
      </article>
    </div>
  </section>
</template>
