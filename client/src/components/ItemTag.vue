<script setup lang="ts">
import { defineProps, inject, type Ref } from 'vue'
import type { Item } from '@/types'
import { HoverCard, HoverCardContent, HoverCardTrigger } from '@/components/ui/hover-card'
import { Badge } from '@/components/ui/badge'

const divRef = inject<Ref<HTMLDivElement | null>>('divRef')

const props = defineProps<{
  item: Item
}>()
</script>

<template>
  <HoverCard :open-delay="0" :close-delay="0">
    <HoverCardTrigger>
      <Badge variant="outline" class="m-1">{{ `${item.emoji} ${item.name}` }}</Badge>
    </HoverCardTrigger>
    <HoverCardContent class="w-80 m-4" :reference="divRef" align="start">
      <div class="flex flex-col gap-3">
        <p class="text-foreground">{{ `${item.emoji} ${item.name}` }}</p>
        <p class="italic text-sm text-muted-foreground">{{ item.description }}</p>
      </div>
    </HoverCardContent>
  </HoverCard>
</template>
