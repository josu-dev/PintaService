<script setup>
  const props = defineProps({
    institution: {
      type: Object,
      default: () => {}
    }
  });

  defineEmits(['update:value']);
</script>

<template>
  <div class="institution-detail">
    <table>
      <tr>
        <td class="font-bold">Nombre:</td>
        <td>&nbsp;&nbsp;{{ institution.name }}</td>
      </tr>
      <tr>
        <td class="font-bold">Descripcion:</td>
        <td>&nbsp;&nbsp;{{ institution.information }}</td>
      </tr>
      <tr>
        <td class="font-bold">Direccion:</td>
        <td>&nbsp;&nbsp;{{ institution.address }}</td>
      </tr>
      <tr>
        <td class="font-bold">Palabras clave:</td>
        <td>&nbsp;&nbsp;{{ institution.keywords }}</td>
      </tr>
      <tr>
        <td class="font-bold">Web:</td>
        <td>&nbsp;&nbsp;{{ institution.web }}</td>
      </tr>
      <tr>
        <td class="font-bold">Email:</td>
        <td>&nbsp;&nbsp;{{ institution.email }}</td>
      </tr>
      <tr>
        <td class="font-bold">Horarios:</td>
        <td>&nbsp;&nbsp;{{ institution.days_and_opening_hours }}</td>
      </tr>
      <tr>
        <td class="font-bold">Habilitada:</td>
        <td>&nbsp;&nbsp;{{ institution.enabled ? '✅' : '❌' }}</td>
      </tr>
    </table>
  </div>
</template>
