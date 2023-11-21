<template>
    <div class="service-detail">
        <table>
            <tr>
                <td class="font-bold">Nombre:</td>
                <td>&nbsp;&nbsp;{{ service.name }}</td>
            </tr>
            <tr>
                <td class="font-bold">Descripcion:</td>
                <td>&nbsp;&nbsp;{{ service.description }}</td>
            </tr>
            <tr>
                <td class="font-bold">Palabras Clave:</td>
                <td>&nbsp;&nbsp;{{ service.keywords }}</td>
            </tr>
            <tr>
                <td class="font-bold">Habilitado:</td>
                <td>&nbsp;&nbsp;{{ service.enabled ? '✅' : '❌' }}</td>
            </tr>
        </table>
    </div>
</template>

<script setup>
const props = defineProps({
    service: {
        type: Object,
        default: () => { }
    },

});

defineEmits(['update:value']);
</script>

