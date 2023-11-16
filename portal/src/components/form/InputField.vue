<script setup>
  const props = defineProps({
    value: {
      type: String,
      default: ''
    },
    name: String,
    label: String,
    type: {
      type: String,
      default: 'text'
    },
    required: {
      type: Boolean,
      default: false
    },
    autocomplete: {
      type: String,
      default: 'off'
    }
  });

  defineEmits(['update:value']);
</script>

<template>
  <div class="form-control w-full max-w-xs">
    <label class="label" :for="props.name">
      <span class="label-text text-sm md:text-base"
        >{{ props.label }}<span v-if="props.required" class="text-red-500 font-bold">&nbsp;*</span>
      </span>
    </label>
    <input
      :type="props.type"
      :name="props.name"
      :id="props.name"
      :value="value"
      :required="props.required"
      :autocomplete="props.autocomplete"
      @input="
        // @ts-expect-error - target.value is valid
        $emit('update:value', $event.target?.value)
      "
      class="input input-bordered w-full max-w-xs input-sm md:input-md"
    />
  </div>
</template>
