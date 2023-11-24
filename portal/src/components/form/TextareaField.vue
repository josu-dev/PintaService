<script setup>
  import { onMounted, onUnmounted, ref } from 'vue';

  const props = defineProps({
    value: {
      type: String,
      default: ''
    },
    name: String,
    label: String,
    required: {
      type: Boolean,
      default: false
    },
    rows: {
      type: Number,
      default: 4
    },
    classTextarea: {
      type: String,
      default: ''
    }
  });

  const emit = defineEmits(['update:value', 'ref:input']);

  const inputRef = ref(null);

  onMounted(() => {
    emit('ref:input', inputRef.value);
  });
  onUnmounted(() => {
    emit('ref:input', null);
  });
</script>

<template>
  <div class="form-control w-full">
    <label class="label" :for="props.name">
      <span class="label-text text-sm md:text-base"
        >{{ props.label }}<span v-if="props.required" class="text-red-500 font-bold">&nbsp;*</span>
      </span>
    </label>
    <textarea
      :name="props.name"
      :id="props.name"
      :value="value"
      :required="props.required"
      spellcheck="false"
      :rows="props.rows"
      @input="
        // @ts-expect-error - target.value is valid
        $emit('update:value', $event.target?.value)
      "
      ref="inputRef"
      :class="
        'textarea textarea-bordered w-full textarea-sm md:textarea-md resize-none !leading-normal ' +
        props.classTextarea
      "
    />
  </div>
</template>
