<template>
    <div>
        <header class="flex items-center justify-between h-16 border-b">
            <div class="mr-3">
                <span class="mx-4 font-bold text-3xl">COOK</span>
                <span>Admin</span>
            </div>
            <Menu class="mr-48" />
        </header>
    </div>
</template>

<script setup>
import Menu from '~/components/admin/Menu.vue';
</script>