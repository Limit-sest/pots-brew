<script setup lang="ts">
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
} from '@/components/ui/sidebar'
import ItemTag from './ItemTag.vue'
import { useDiscovered } from '@/stores/discovered'
const discovered = useDiscovered()
</script>

<template>
  <Sidebar>
    <SidebarHeader />
    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel>Discovered Ingredients</SidebarGroupLabel>
        <SidebarGroupContent class="flex flex-wrap"
          ><ItemTag v-for="item in discovered.discovered" :key="item.id" :item="item"
        /></SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>
    <SidebarFooter />
  </Sidebar>
</template>
