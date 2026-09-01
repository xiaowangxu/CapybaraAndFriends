<script setup lang="ts">
import { computed, ref } from 'vue'
import {
  BENCHMARK_RECORDS,
  MODEL_IDS,
  MODEL_LABELS,
  SPLIT_IDS,
  SPLIT_LABELS,
  TASK_IDS,
  TASK_LABELS,
  type BenchmarkRecord,
  type MetricId,
  type ModelId,
  type SplitId,
  type TaskId,
} from '../data/atpm-benchmark-results'

interface MetricOption {
  value: MetricId
  label: string
  shortLabel: string
  better: 'higher' | 'lower'
}

const metricOptions: readonly MetricOption[] = [
  { value: 'exactMatch', label: 'Exact match', shortLabel: 'Exact match', better: 'higher' },
  { value: 'tokenAccuracy', label: 'Token accuracy', shortLabel: 'Token acc.', better: 'higher' },
  { value: 'crossEntropy', label: 'Cross-entropy', shortLabel: 'CE', better: 'lower' },
]

const selectedTask = ref<TaskId>('mixed_all')
const selectedSplit = ref<SplitId>('iid')
const selectedMetric = ref<MetricId>('exactMatch')

const recordIndex = new Map(
  BENCHMARK_RECORDS.map(record => [recordKey(record.model, record.task, record.split), record]),
)

const activeMetric = computed(() => (
  metricOptions.find(option => option.value === selectedMetric.value) ?? metricOptions[0]
))

const chartRecords = computed(() => MODEL_IDS
  .map(model => getRecord(model, selectedTask.value, selectedSplit.value))
  .sort((left, right) => {
    const delta = metricValue(left) - metricValue(right)
    return activeMetric.value.better === 'higher' ? -delta : delta
  }))

const chartMaximum = computed(() => {
  if (selectedMetric.value !== 'crossEntropy') return 1
  const maximum = Math.max(...chartRecords.value.map(metricValue))
  return maximum > 0 ? maximum : 1
})

function recordKey(model: ModelId, task: TaskId, split: SplitId) {
  return `${model}|${task}|${split}`
}

function getRecord(model: ModelId, task: TaskId, split: SplitId): BenchmarkRecord {
  const record = recordIndex.get(recordKey(model, task, split))
  if (!record) throw new Error(`Missing benchmark record: ${model}/${task}/${split}`)
  return record
}

function metricValue(record: BenchmarkRecord) {
  return record[selectedMetric.value]
}

function chartWidth(record: BenchmarkRecord) {
  const value = metricValue(record)
  if (value === 0) return '0%'
  return `${Math.max(1.5, (value / chartMaximum.value) * 100)}%`
}

function formatValue(value: number) {
  if (selectedMetric.value !== 'crossEntropy') return `${(value * 100).toFixed(1)}%`
  if (value === 0) return '0.000'
  if (value < 0.0001) return value.toExponential(2)
  return value.toFixed(3)
}

function bestValue(task: TaskId) {
  const values = MODEL_IDS.map(model => metricValue(getRecord(model, task, selectedSplit.value)))
  return activeMetric.value.better === 'higher' ? Math.max(...values) : Math.min(...values)
}

function isBest(task: TaskId, model: ModelId) {
  const value = metricValue(getRecord(model, task, selectedSplit.value))
  return Math.abs(value - bestValue(task)) < 1e-12
}
</script>

<template>
  <section class="benchmark" aria-label="ATPM 合成任务基准结果">
    <div class="benchmark__controls">
      <label class="benchmark__task-select">
        <select v-model="selectedTask">
          <option v-for="task in TASK_IDS" :key="task" :value="task">
            {{ TASK_LABELS[task] }}
          </option>
        </select>
      </label>

      <fieldset class="benchmark__control-group">
        <div class="benchmark__segments">
          <button v-for="split in SPLIT_IDS" :key="split" type="button"
            :class="{ 'is-active': selectedSplit === split }" :aria-pressed="selectedSplit === split"
            @click="selectedSplit = split">
            {{ SPLIT_LABELS[split] }}
          </button>
        </div>
      </fieldset>

      <fieldset class="benchmark__control-group benchmark__control-group--metric">
        <div class="benchmark__segments">
          <button v-for="metric in metricOptions" :key="metric.value" type="button"
            :class="{ 'is-active': selectedMetric === metric.value }" :aria-pressed="selectedMetric === metric.value"
            @click="selectedMetric = metric.value">
            {{ metric.shortLabel }}
          </button>
        </div>
      </fieldset>
    </div>

    <!-- <div class="benchmark__chart-heading">
      <div>
        <strong>{{ TASK_LABELS[selectedTask] }}</strong>
        <span>{{ SPLIT_LABELS[selectedSplit] }} · {{ activeMetric.label }}</span>
      </div>
      <span>{{ activeMetric.better === 'higher' ? '越高越好' : '越低越好' }}</span>
    </div> -->

    <div class="benchmark__chart" role="img"
      :aria-label="`${TASK_LABELS[selectedTask]} 的 ${SPLIT_LABELS[selectedSplit]} ${activeMetric.label} 模型比较`">
      <div v-for="record in chartRecords" :key="record.model" class="benchmark__bar-row"
        :class="{ 'is-atpm': record.model === 'atpm_v2' }">
        <span class="benchmark__model-name">{{ MODEL_LABELS[record.model] }}</span>
        <span class="benchmark__track" aria-hidden="true">
          <span class="benchmark__fill" :style="{ width: chartWidth(record) }"></span>
        </span>
        <span class="benchmark__bar-value">{{ formatValue(metricValue(record)) }}</span>
      </div>
    </div>

    <div class="benchmark__table-wrap" tabindex="0" aria-label="全部合成任务结果，可横向滚动">
      <table class="benchmark__table">
        <!-- <caption>
          全部任务 · {{ SPLIT_LABELS[selectedSplit] }} · {{ activeMetric.label }}
        </caption> -->
        <thead>
          <tr>
            <th scope="col">任务</th>
            <th v-for="model in MODEL_IDS" :key="model" scope="col">
              {{ MODEL_LABELS[model] }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in TASK_IDS" :key="task" :class="{ 'is-selected': selectedTask === task }"
            @click="selectedTask = task">
            <td scope="row" style="text-align: left;">
              <button type="button" @click="selectedTask = task">
                {{ TASK_LABELS[task] }}
              </button>
            </td>
            <td v-for="model in MODEL_IDS" :key="model" :class="{
              'is-best': isBest(task, model),
              'is-atpm': model === 'atpm_v2',
            }">
              {{ formatValue(metricValue(getRecord(model, task, selectedSplit))) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- <p class="benchmark__note">
      Exact match 与 token accuracy 来自 autoregressive evaluation；CE 来自 teacher-forced evaluation。
      加粗值表示该任务和当前 split 下的最优结果，允许并列。
    </p> -->
  </section>
</template>

<style scoped>
.benchmark {
  padding-block: 2rem;
}

.benchmark__controls {
  display: grid;
  grid-template-columns: minmax(11rem, 1.15fr) 1fr 1.45fr;
  gap: 1rem;
  align-items: end;
}

.benchmark__controls > * {
  height: 100%;
}

.benchmark__task-select,
.benchmark__control-group {
  display: grid;
  gap: .45rem;
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
}

.benchmark__task-select>span,
.benchmark__control-group legend {
  padding: 0;
  color: var(--cf-muted);
  font-size: .75rem;
}

.benchmark__task-select select {
  width: 100%;
  min-height: 2.35rem;
  border: 1px solid var(--cf-border-strong);
  border-radius: .5rem;
  background: var(--cf-surface);
  padding: .4rem .65rem;
  color: var(--cf-text);
}

.benchmark__segments {
  display: flex;
  min-width: 0;
  border: 1px solid var(--cf-border-strong);
  border-radius: .5rem;
  overflow: hidden;
}

.benchmark__segments button {
  flex: 1 1 auto;
  min-height: 2.35rem;
  border: 0;
  border-left: 1px solid var(--cf-border);
  background: var(--cf-surface);
  padding: .4rem .65rem;
  cursor: pointer;
  white-space: nowrap;
}

.benchmark__segments button:first-child {
  border-left: 0;
}

.benchmark__segments button.is-active {
  background: var(--cf-text);
  color: var(--cf-surface);
}

.benchmark__chart-heading {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 2rem;
}

.benchmark__chart-heading div {
  display: flex;
  gap: 1rem;
  align-items: baseline;
}

.benchmark__chart-heading span {
  color: var(--cf-muted);
}

.benchmark__chart {
  display: grid;
  gap: .62rem;
  margin-top: 2rem;
  font-size: 0.92rem;
}

.benchmark__bar-row {
  display: grid;
  grid-template-columns: 7.5rem minmax(6rem, 1fr) 4.4rem;
  gap: .8rem;
  align-items: center;
  font-variant-numeric: tabular-nums;
}

.benchmark__model-name,
.benchmark__bar-value {
}

.benchmark__bar-value {
  text-align: right;
}

.benchmark__track {
  display: block;
  height: .75rem;
  background: var(--cf-soft);
  overflow: hidden;
}

.benchmark__fill {
  display: block;
  height: 100%;
  background: #a8adb4;
  transition: width .2s ease;
}

.benchmark__bar-row.is-atpm .benchmark__model-name,
.benchmark__bar-row.is-atpm .benchmark__bar-value {
  color: var(--cf-accent);
}

.benchmark__bar-row.is-atpm .benchmark__fill {
  background: var(--cf-accent);
}

.benchmark__table-wrap {
  width: 100%;
  margin-top: 2rem;
  overflow-x: auto;
  overscroll-behavior-inline: contain;
}

.benchmark__table {
  display: table;
  width: 100%;
  min-width: 42rem;
  margin: 0;
  border-collapse: collapse;
  table-layout: auto;
  /* font-size: .75rem; */
  line-height: 1.35;
  font-variant-numeric: tabular-nums;
}

.benchmark__table thead {
  display: table-header-group;
  width: auto;
  min-width: 0;
}

.benchmark__table tbody {
  display: table-row-group;
  width: auto;
  min-width: 0;
}

.benchmark__table caption {
  padding-bottom: .65rem;
  color: var(--cf-muted);
  text-align: left;
  font-size: .75rem;
}

.benchmark__table th,
.benchmark__table td {
  width: auto;
  min-width: 7.25rem;
  border: 0;
  border-bottom: 1px solid var(--cf-border);
  padding: .62rem .7rem;
  text-align: right;
  white-space: nowrap;
}

.benchmark__table thead th {
  border-bottom: 1px solid #6b6763;
}

.benchmark__table th:first-child {
  position: sticky;
  left: 0;
  z-index: 1;
  width: 12rem;
  min-width: 12rem;
  text-align: left;
}

.benchmark__table thead th:first-child {
  z-index: 2;
}

.benchmark__table tbody tr {
  cursor: pointer;
}

.benchmark__table tbody tr:hover th,
.benchmark__table tbody tr:hover td,
.benchmark__table tbody tr.is-selected th,
.benchmark__table tbody tr.is-selected td {
  background: var(--cf-surface);
}

.benchmark__table th button {
  width: 100%;
  border: 0;
  background: transparent;
  padding: 0;
  color: inherit;
  cursor: pointer;
  text-align: left;
}

.benchmark__table td.is-atpm {
  color: var(--cf-accent);
}

.benchmark__table td.is-best {
  font-weight: 700;
}

.benchmark__note {
  margin: .85rem 0 0;
  color: var(--cf-muted);
  font-size: .75rem;
  line-height: 1.6;
}

@media (max-width: 760px) {
  .benchmark__controls {
    grid-template-columns: 1fr;
  }

  .benchmark__bar-row {
    grid-template-columns: 6.5rem minmax(4rem, 1fr) 3.8rem;
    gap: .55rem;
  }

  .benchmark__chart-heading div {
    display: grid;
    gap: .15rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .benchmark__fill {
    transition: none;
  }
}
</style>
