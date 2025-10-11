<script setup lang="ts">
import AppSidebar from '@/components/AppSidebar.vue'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import BrewView from './components/BrewView.vue'
import { useDiscovered } from '@/stores/discovered'
import { onMounted, ref, provide } from 'vue'
const discovered = useDiscovered()
const divRef = ref<HTMLDivElement | null>(null)

provide('divRef', divRef)

onMounted(() => {
  discovered.getInitial()
})

defineExpose({
  divRef,
})
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <main>
      <SidebarTrigger class="block md:hidden" />
      <div ref="divRef"></div>
      <BrewView />
    </main>
  </SidebarProvider>
</template>
