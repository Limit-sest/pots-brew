import { defineStore } from 'pinia'
import type { Item } from '@/types'

export const useDiscovered = defineStore('discovered', {
  state: () => ({
    discovered: [] as Item[],
  }),
})
