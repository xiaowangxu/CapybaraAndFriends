<template>
    <div class="max-w-full relative">
        <div ref="bg-dom" class="max-w-fit contain-paint transition-transform overflow-hidden" v-bind="$attrs"
            :class="{ active: state }">
            <div ref="cot-dom" class="w-1/1 h-full isolate flex select-none">
                <slot name="static" :show="() => state = true" :hide="() => state = false"
                    :toggle="() => state = !state" />
                <div ref="summary-dom"
                    class="fade min-h-9 h-full text-sm top-0 left-0 flex gap-1.5 py-0"
                    :class="[state ? 'active' : undefined]">
                    <slot name="compact" :show="() => state = true" :hide="() => state = false"
                        :toggle="() => state = !state" />
                </div>
                <div ref="activity-dom"
                    class="relative fade top-0 left-0 self-start text-md overflow-hidden"
                    :class="[!state ? 'active' : undefined]">
                    <slot name="default" :show="() => state = true" :hide="() => state = false"
                        :toggle="() => state = !state" />
                </div>
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
import { useTemplateRef, watch, ref, onMounted, toRef, readonly } from 'vue';

defineOptions({
    inheritAttrs: false,
});

const props = withDefaults(
    defineProps<{
        initialExpanded?: boolean
    }>(),
    {
        initialExpanded: false
    }
);

const bg_dom = useTemplateRef('bg-dom');
const cot_dom = useTemplateRef('cot-dom');
const summary_dom = useTemplateRef('summary-dom');
const activity_dom = useTemplateRef('activity-dom');

const state = ref(props.initialExpanded);
if (props.initialExpanded) {
    onMounted(() => {
        switch_state(props.initialExpanded, true);
    });
}
watch(state, (s) => switch_state(s), { flush: 'post' });

let last_animation: Animation | undefined;
async function switch_state(state: boolean, immediate: boolean = false) {
    if (cot_dom.value === null || summary_dom.value === null || activity_dom.value === null) return;
    if (bg_dom.value === null) return;

    const { width, height } = bg_dom.value.getBoundingClientRect();

    last_animation?.cancel();
    last_animation = undefined;

    const bg = bg_dom.value;
    const cot = cot_dom.value;
    const summary = summary_dom.value;
    const activity = activity_dom.value;

    cot.style.maxWidth = 'fit-content';
    bg.style.width = 'unset';
    bg.style.maxWidth = 'unset';
    summary.style.width = 'unset';
    activity.style.width = 'unset';

    let summary_width: number, summary_height: number;
    let activity_width: number, activity_height: number;

    let self_summary_width: number, self_summary_height: number;
    let self_activity_width: number, self_activity_height: number;

    let summary_x: number, summary_y: number;
    let activity_x: number, activity_y: number;

    {
        activity.style.position = 'unset';
        summary.style.position = 'absolute';
        const { width: width_self, height: height_self } = activity.getBoundingClientRect();
        self_activity_width = width_self;
        self_activity_height = height_self;
        const { width, height } = cot.getBoundingClientRect();
        activity_x = activity.offsetLeft;
        activity_y = activity.offsetTop;
        activity_width = width;
        activity_height = height;
    }
    {
        activity.style.position = 'absolute';
        summary.style.position = 'unset';
        const { width: width_self, height: height_self } = summary.getBoundingClientRect();
        self_summary_width = width_self;
        self_summary_height = height_self;
        const { width, height } = cot.getBoundingClientRect();
        summary_x = summary.offsetLeft;
        summary_y = summary.offsetTop;
        summary_width = width;
        summary_height = height;
    }

    if (!state) {
        activity.style.position = 'absolute';
        activity.style.left = `${activity_x}px`;
        activity.style.top = `${activity_y}px`;
        summary.style.position = 'unset';
        summary.style.left = 'unset';
        summary.style.top = 'unset';
    }
    else {
        activity.style.position = 'unset';
        activity.style.left = 'unset';
        activity.style.top = 'unset';
        summary.style.position = 'absolute';
        summary.style.left = `${summary_x}px`;
        summary.style.top = `${summary_y}px`;
    }

    bg.style.maxWidth = 'unset';
    cot.style.maxWidth = '100%';
    bg.style.minHeight = 'unset';
    // summary.style.width = `${self_summary_width}px`;
    // activity.style.width = `${self_activity_width}px`;

    const new_width = state ? activity_width : summary_width;
    const new_height = state ? activity_height : summary_height;
    let animation;
    if (!immediate) {
        animation = bg.animate([
            { width: `${width}px`, height: `${height}px`, transform: 'scale(1)', easing: 'ease-out' },
            { width: `${width}px`, height: `${height}px`, transform: `scale(${Math.min((width + 8) / width, (height + 8) / height)})`, offset: 0.15, easing: 'cubic-bezier(0.4, 0, 0.2, 1)' },
            { width: `${new_width}px`, height: `${new_height}px`, transform: `scale(${Math.min((new_width + 2) / new_width, (new_height + 2) / new_height)})`, offset: 0.85, easing: 'ease-out' },
            { width: `${new_width}px`, height: `${new_height}px`, transform: 'scale(1)' },
        ], {
            duration: 450,
        });
        last_animation = animation;
    }
    try {
        await animation?.finished;
        bg.style.maxWidth = 'fit-content';
        cot.style.maxWidth = 'fit-content';
        summary.style.width = 'unset';
        summary.style.minWidth = 'unset';
        activity.style.width = 'unset';
        activity.style.minWidth = 'unset';
        animation?.cancel();
        if (last_animation === animation) {
            last_animation = undefined;
        }
    }
    catch (err) { }
}

defineExpose({
    expanded: readonly(state),
    show: () => state.value = true,
    hide: () => state.value = false,
});

</script>

<style scoped>
@reference '../../style/style.css';

.fade {
    @apply opacity-100 filter-[blur(0px)] transition-[opacity,filter] duration-350 delay-50;
}

.fade.active {
    @apply opacity-0 filter-[blur(10px)] pointer-events-none delay-0;
}
</style>